from airflow.sdk import dag, task
from airflow.decorators import task_group
from datetime import datetime
from pendulum import duration
import logging

task_logger = logging.getLogger("airflow.task")

@dag(
    start_date=datetime(2025, 1, 1),
    schedule="0 0 * * 1",
    default_args={
        "retries": 2,
        "retry_delay": duration(minutes=3)
    }
)
def economics_news_etl():

    @task
    def extract_past_week_data(**context):
        from airflow.providers.mongo.hooks.mongo import MongoHook
        from include.pipeline.extract import get_current_week_start

        # Get current week start date
        today = context["ts"]
        current_week_start = get_current_week_start(today)
        current_week_start = "27-07-2025"
        task_logger.info(f"Filtering articles from week starting: {current_week_start}")

        # MongoDB aggregation query with week filter
        query = [
            {
                "$match": {
                    "extracted_date": current_week_start
                }
            },
            # Project and clean array fields
            {
                "$project": {
                    "_id": 0,  # Exclude _id
                    "url": 1,
                    "extracted_date": 1,
                    # Convert array fields to single values
                    "title": {
                        "$cond": {
                            "if": {"$isArray": "$title"},
                            "then": {"$arrayElemAt": ["$title", 0]},
                            "else": "$title"
                        }
                    },
                    "date": {
                        "$cond": {
                            "if": {"$isArray": "$date"},
                            "then": {"$arrayElemAt": ["$date", 0]},
                            "else": "$date"
                        }
                    },
                    "lead": {
                        "$cond": {
                            "if": {"$isArray": "$lead"},
                            "then": {"$arrayElemAt": ["$lead", 0]},
                            "else": "$lead"
                        }
                    },
                    "author": {
                        "$cond": {
                            "if": {"$isArray": "$author"},
                            "then": {"$arrayElemAt": ["$author", 0]},
                            "else": "$author"
                        }
                    }
                }
            },
            {
                "$limit": 2
            }
        ]

        mongodb_conn = MongoHook(
            mongo_conn_id="mongo_id"
        )

        collection = mongodb_conn.get_collection("articles", mongo_db="newsdb")
        # Exclude _id from projection to avoid serialization issues
        cursor = collection.aggregate(query)
        articles = list(cursor)
        task_logger.info(articles)
        task_logger.info(f"Extracted {len(articles)} articles")

        return articles

    @task_group
    def transform(articles):
        @task
        def remove_duplicates(articles):
            import pandas as pd

            df_articles = pd.DataFrame(articles)
            # Drop duplicates and dropna
            df_deduplicated_data = df_articles.drop_duplicates().dropna()

            return df_deduplicated_data.to_dict(orient="records")

        @task
        def clean_each_article(article):
            from include.pipeline.transform import transform
            import pandas as pd

            df_article = pd.DataFrame([article])
            df_transformed_article = transform(df_article)
            task_logger.info(df_transformed_article)
            return df_transformed_article.to_dict(orient="records")

        _removed_duplicates = remove_duplicates(articles)
        _clean_each_article = clean_each_article.expand(article=_removed_duplicates)

        return _clean_each_article

    @task
    def load(article):
        task_logger.info("article")

    _extracted_past_week_data = extract_past_week_data()
    _transformed_data = transform(_extracted_past_week_data)
    load.expand(article=_transformed_data)

economics_news_etl()

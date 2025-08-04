DROP TABLE IF EXISTS public."Articles";

CREATE TABLE IF NOT EXISTS public."Articles"
(
    id serial PRIMARY KEY NOT NULL,
    title text NOT NULL,
    published_at date NOT NULL,
    lead text NOT NULL,
    author text NOT NULL,
    url text NOT NULL,
    source text NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Articles"
    OWNER to postgres;

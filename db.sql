CREATE DATABASE pgws

CREATE TABLE todo
(
    id serial PRIMARY KEY NOT NULL,
    description character varying(255),
    done boolean NOT NULL
)

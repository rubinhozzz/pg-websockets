CREATE DATABASE pgws

CREATE TABLE todo
(
    id serial PRIMARY KEY NOT NULL,
    description character varying(255),
    done boolean NOT NULL
)

CREATE OR REPLACE FUNCTION notify_alert_insert() RETURNS trigger AS $$
DECLARE
BEGIN
    PERFORM pg_notify('todo_updates', row_to_json(NEW)::TEXT);
    RETURN new;
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS trig_alert_insert ON todo;

CREATE TRIGGER trig_alert_insert AFTER INSERT ON todo
FOR EACH ROW EXECUTE PROCEDURE notify_alert_insert();

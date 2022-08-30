-- DROP SCHEMA auth;

CREATE SCHEMA auth AUTHORIZATION app;
-- auth.users definition

-- Drop table

-- DROP TABLE auth.users;

CREATE TABLE auth.users (
	id uuid NOT NULL,
	email text NOT NULL,
	"password" text NOT NULL,
	created_at timestamptz NULL,
	updated_at timestamptz NULL
);

-- DROP TABLE auth.history;

CREATE TABLE auth.history (
	id uuid NOT NULL,
	user_id uuid NOT NULL,
	description text NOT NULL,
	created_at timestamptz NULL,
	updated_at timestamptz NULL
);
-- Permissions

ALTER TABLE auth.users OWNER TO app;
GRANT ALL ON TABLE auth.users TO app;
ALTER TABLE auth.history OWNER TO app;
GRANT ALL ON TABLE auth.history TO app;



-- Permissions

GRANT ALL ON SCHEMA auth TO app;

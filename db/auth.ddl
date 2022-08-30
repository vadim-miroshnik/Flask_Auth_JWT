CREATE SCHEMA IF NOT EXISTs auth AUTHORIZATION admin;

CREATE TABLE auth.users (
	id uuid NOT NULL,
	email text NOT NULL,
	"password" text NOT NULL,
	created_at timestamptz NULL,
	updated_at timestamptz NULL
);

CREATE TABLE auth.roles (
    name varchar(64) primary key
);

CREATE TABLE auth.roles_rights (
	id uuid primary key,
    role varchar(64) not null,
    object_address varchar(128),
    read boolean default false,
    edit boolean default false,
    add boolean default false,
    remove boolean default false,
	created_at timestamptz NULL,
	updated_at timestamptz NULL
);

CREATE TABLE auth.users_roles (
	id uuid primary key,
    user_id uuid not null,
    role varchar(64) not null,
	created_at timestamptz NULL,
	updated_at timestamptz NULL
);

ALTER TABLE auth.users OWNER TO admin;
GRANT ALL ON TABLE auth.users TO admin;

GRANT ALL ON SCHEMA auth TO admin;

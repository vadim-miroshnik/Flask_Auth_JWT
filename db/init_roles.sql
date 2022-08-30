insert into auth.roles (name)
values ('superuser'),
       ('admin'),
       ('regular'),
       ('subscriber'),
       ('guest')
on conflict do nothing
;

insert into auth.users_roles (id, user_id, role, created_at, updated_at)
values ('926c5480-6077-46ca-b286-411797951690', NULL, 'guest', now(), now())
on conflict do nothing
;
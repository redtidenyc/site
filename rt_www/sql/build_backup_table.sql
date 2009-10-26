CREATE TABLE "uid_swimmer_map" (
    "swimmer_id" integer NOT NULL,
    "user_id" integer NOT NULL
);
insert into uid_swimmer_map select a.id as swimmer_id, a.user_id as user_id from swimmers_swimmer as a, registration_registration as b where a.id = b.swimmer_id and b.plan_id = 14;

/*
    This handles the migration of the Swimmer Object from a ForeignKey to a OneToOneField
*/

BEGIN;

/* Backup the existing tables */

ALTER TABLE "mailinglist_forward" RENAME TO "mailinglist_forward_bk";
ALTER TABLE "mailinglist_mailinglist_swimmers" RENAME TO "mailinglist_mailinglist_swimmers_bk";
ALTER TABLE "mailinglist_rtmessage" RENAME TO "mailinglist_rtmessage_bk";
ALTER TABLE "registration_payment" RENAME TO "registration_payment_bk";
ALTER TABLE "registration_registration" RENAME TO "registration_registration_bk";
ALTER TABLE "swimmers_coach" RENAME TO "swimmers_coach_bk";
ALTER TABLE "swimmers_boardmember" RENAME TO "swimmers_boardmember_bk";
ALTER TABLE "swimmers_swimmer" RENAME TO "swimmers_swimmer_bk";

CREATE TABLE "mailinglist_forward" (
    "id" integer NOT NULL PRIMARY KEY,
    "swimmer_id" integer NOT NULL REFERENCES "swimmers_swimmer" ("user_id"),
    "forward" varchar(75) NOT NULL UNIQUE
);

CREATE TABLE "mailinglist_rtmessage" (
    "id" integer NOT NULL PRIMARY KEY,
    "fromswimmer_id" integer NOT NULL REFERENCES "swimmers_swimmer" ("user_id"),
    "tolist_id" integer NOT NULL REFERENCES "mailinglist_mailinglist" ("id"),
    "message" text NOT NULL,
    "subject" text NULL,
    "datesent" date NOT NULL
);

CREATE TABLE "mailinglist_mailinglist_swimmers" (
    "id" integer NOT NULL PRIMARY KEY,
    "mailinglist_id" integer NOT NULL REFERENCES "mailinglist_mailinglist" ("id"),
    "swimmer_id" integer NOT NULL REFERENCES "swimmers_swimmer" ("user_id"),
    UNIQUE ("mailinglist_id", "swimmer_id")
);

CREATE TABLE "registration_payment" (
    "id" integer NOT NULL PRIMARY KEY,
    "paypal_trans_id" varchar(25) NOT NULL,
    "swimmer_id" integer NOT NULL REFERENCES "swimmers_swimmer" ("user_id"),
    "paid_date" date NOT NULL,
    "amount_paid" numeric(6, 2) NOT NULL,
    "plan_id" integer NOT NULL REFERENCES "registration_plan" ("id"),
    "registration_id" integer NOT NULL REFERENCES "registration_registration" ("id")
);

CREATE TABLE "registration_registration" (
    "id" integer NOT NULL PRIMARY KEY,
    "swimmer_id" integer NOT NULL REFERENCES "swimmers_swimmer" ("user_id"),
    "registration_date" date NOT NULL,
    "registration_status" integer NULL,
    "plan_id" integer NOT NULL REFERENCES "registration_plan" ("id"),
    "comment" text NULL
);

CREATE TABLE "swimmers_coach" (
    "swimmer_id" integer NOT NULL PRIMARY KEY REFERENCES "auth_user" ("id"),
    "title" varchar(1) NOT NULL,
    "bio" text NOT NULL,
    "is_active" bool NOT NULL
);

CREATE TABLE "swimmers_boardmember" (
    "swimmer_id" integer NOT NULL PRIMARY KEY REFERENCES "auth_user" ("id"),
    "position_id" integer NOT NULL REFERENCES "swimmers_boardposition" ("id")
);

CREATE TABLE "swimmers_swimmer" (
    "user_id" integer NOT NULL PRIMARY KEY REFERENCES "auth_user" ("id"),
    "street" varchar(32) NOT NULL,
    "street2" varchar(32) NOT NULL,
    "city" varchar(32) NOT NULL,
    "state_id" integer NOT NULL REFERENCES "swimmers_state" ("id"),
    "zipcode" varchar(16) NOT NULL,
    "usms_code" varchar(10) NOT NULL,
    "date_of_birth" date NOT NULL,
    "day_phone" varchar(15) NULL,
    "evening_phone" varchar(15) NULL,
    "gender" varchar(1) NOT NULL
);

/* Boy this is a pain */

INSERT INTO mailinglist_forward 
    SELECT a.id as id, b.user_id as swimmer_id, a.forward as forward 
        FROM mailinglist_forward_bk as a, swimmers_swimmer_bk as b 
        WHERE a.swimmer_id = b.id;

INSERT INTO mailinglist_rtmessage 
    SELECT a.id as id, b.user_id as fromswimmer_id, a.tolist_id as tolist_id,
        a.message as message, a.subject as subject, a.datesent as datesent
        FROM mailinglist_rtmessage_bk as a, swimmers_swimmer_bk as b
        WHERE a.fromswimmer_id = b.id;

INSERT INTO mailinglist_mailinglist_swimmers
    SELECT a.id as id, a.mailinglist_id as mailinglist_id, b.user_id as swimmer_id
        FROM mailinglist_mailinglist_swimmers_bk as a, swimmers_swimmer_bk as b
        WHERE a.swimmer_id = b.id;  

INSERT INTO registration_payment
    SELECT a.id as id, a.paypal_trans_id as paypal_trans_id, b.user_id as swimmer_id,
        a.paid_date as paid_date, a.amount_paid as amount_paid, a.plan_id as plan_id,
        a.registration_id as registration_id
        FROM registration_payment_bk as a, swimmers_swimmer_bk as b
        WHERE a.swimmer_id = b.id;

INSERT INTO registration_registration
    SELECT a.id as id, b.user_id as swimmer_id, a.registration_date as registration_date,
        a.registration_status as registration_status, a.plan_id as plan_id, a.comment as comment
        FROM registration_registration_bk as a, swimmers_swimmer_bk as b
        WHERE a.swimmer_id = b.id;

INSERT INTO swimmers_coach
    SELECT b.user_id as swimmer_id, a.title as title, a.bio as bio, a.is_active as is_active
        FROM swimmers_coach_bk as a, swimmers_swimmer_bk as b
        WHERE a.swimmer_id = b.id;

INSERT INTO swimmers_boardmember
    SELECT b.user_id as swimmer_id, a.position_id as position_id
        FROM swimmers_boardmember_bk as a, swimmers_swimmer_bk as b
        WHERE a.swimmer_id = b.id;

INSERT INTO swimmers_swimmer
    SELECT user_id, street, street2, city, state_id, zipcode, usms_code, date_of_birth, day_phone, evening_phone, gender
    FROM swimmers_swimmer_bk; 

/* Now we can dump all the backup tables */

DROP TABLE mailinglist_forward_bk;
DROP TABLE mailinglist_rtmessage_bk;
DROP TABLE mailinglist_mailinglist_swimmers_bk;
DROP TABLE registration_payment_bk;
DROP TABLE registration_registration_bk;
DROP TABLE swimmers_coach_bk;
DROP TABLE swimmers_boardmember_bk;
DROP TABLE swimmers_swimmer_bk; 

COMMIT;

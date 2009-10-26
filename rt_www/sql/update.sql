BEGIN;
ALTER TABLE "index_meet" RENAME TO "index_meet_bk";
CREATE TABLE "index_meet" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "date_start" date NOT NULL,
    "date_end" date NULL,
    "date_close" date NULL,
    "entry_link" varchar(200) NOT NULL,
    "results_link" varchar(200) NULL,
    "meet_pool" varchar(100) NOT NULL,
    "city" varchar(100) NOT NULL,
    "state_id" integer NULL REFERENCES "swimmers_state" ("id"),
    "country" varchar(200) NOT NULL
);
INSERT INTO index_meet SELECT id, name, date_start, date_end, NULL as date_close, entry_link, results_link, meet_pool, city, state_id, 'United States' as country from index_meet_bk;
DROP TABLE index_meet_bk;
COMMIT;

ALTER TABLE "index_announcement" RENAME TO "index_announcement_bk";
CREATE TABLE "index_announcement" (
    "id" integer NOT NULL PRIMARY KEY,
    "fptext" text NOT NULL,
    "title" varchar(200) NOT NULL,
    "pub_date" date NOT NULL,
    "expiration_date" date NOT NULL
);
INSERT INTO index_announcement SELECT id, fptext, title, pub_date, expiration_date FROM index_announcement_bk;
DROP TABLE index_announcement_bk;   

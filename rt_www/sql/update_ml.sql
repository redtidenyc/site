ALTER TABLE "mailinglist_mailinglist" RENAME TO "mailinglist_mailinglist_bk";

CREATE TABLE "mailinglist_mailinglist" (
    "id" integer NOT NULL PRIMARY KEY,
    "listaddress" varchar(75) NOT NULL UNIQUE,
    "description" text NULL,
    "ismandatory" bool NOT NULL,
    "board_postable_only" bool NOT NULL,
    "admin_sendable_only" bool NOT NULL
);

INSERT INTO mailinglist_mailinglist SELECT id, listaddress, description, ismandatory, 0 as board_postable_only, admin_sendable_only from mailinglist_mailinglist_bk;
DROP TABLE mailinglist_mailinglist_bk;

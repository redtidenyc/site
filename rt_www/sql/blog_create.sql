CREATE TABLE "index_blog" (
    "id" integer NOT NULL PRIMARY KEY,
    "title" varchar(256) NOT NULL,
    "text" text NOT NULL,
    "pub_date" datetime NOT NULL,
    "author_id" integer NOT NULL REFERENCES "swimmers_swimmer" ("user_id")
);
CREATE INDEX index_blog_author_id ON "index_blog" ("author_id");

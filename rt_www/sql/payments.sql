BEGIN;
CREATE TABLE "payments_variable" (
    "id" integer NOT NULL PRIMARY KEY,
    "variable" varchar(256) NOT NULL,
    "value" varchar(256) NULL
);
CREATE TABLE "payments_account" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(256) NOT NULL,
    "account_slug" varchar(50) NOT NULL,
    "vendor_id" integer NOT NULL,
    "vendor_token" varchar(512) NOT NULL
);
CREATE TABLE "payments_paymentprocessor" (
    "id" integer NOT NULL PRIMARY KEY,
    "vendor_name" varchar(256) NOT NULL,
    "vendor_slug" varchar(50) NOT NULL,
    "http_method" integer NOT NULL,
    "url" varchar(200) NOT NULL,
    "validate_url" varchar(200) NULL,
    "processor" integer NOT NULL
);
CREATE TABLE "payments_account_fixed_vars" (
    "id" integer NOT NULL PRIMARY KEY,
    "account_id" integer NOT NULL REFERENCES "payments_account" ("id"),
    "variable_id" integer NOT NULL REFERENCES "payments_variable" ("id"),
    UNIQUE ("account_id", "variable_id")
);
CREATE INDEX payments_account_account_slug ON "payments_account" ("account_slug");
CREATE INDEX payments_account_vendor_id ON "payments_account" ("vendor_id");
CREATE INDEX payments_paymentprocessor_vendor_slug ON "payments_paymentprocessor" ("vendor_slug");
COMMIT;

from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(256) NOT NULL UNIQUE,
    "password" VARCHAR(64) NOT NULL
);
CREATE TABLE IF NOT EXISTS "webhook" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "address" VARCHAR(256) NOT NULL,
    "event" VARCHAR(256) NOT NULL,
    "url" VARCHAR(2048) NOT NULL,
    "label" VARCHAR(64) NOT NULL,
    "active" BOOL NOT NULL  DEFAULT True,
    "abi" JSONB NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "history" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "log" JSONB NOT NULL,
    "transaction_hash" VARCHAR(256) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "sent" BOOL NOT NULL  DEFAULT False,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "webhook_id" INT NOT NULL REFERENCES "webhook" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """

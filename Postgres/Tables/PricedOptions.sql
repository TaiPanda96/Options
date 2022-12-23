CREATE TABLE IF NOT EXISTS "priced_options" (
    "type" VARCHAR NOT NULL,
    "symbol" VARCHAR,
    "contractSymbol" VARCHAR NOT NULL,
    "lastPrice" NUMERIC,
    "modelPrice" NUMERIC,
    "priceDifference" NUMERIC,
    "expiration" TIMESTAMP WITH TIME ZONE NOT NULL,
    "impliedVolatility" NUMERIC,
    PRIMARY KEY ("contractSymbol", "expiration", "type")
);
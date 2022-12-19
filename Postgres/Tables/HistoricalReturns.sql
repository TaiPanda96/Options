CREATE TABLE IF NOT EXISTS "historical_returns" (
    "symbol" VARCHAR NOT NULL,
    "avgLogReturns" NUMERIC,
    "standardDeviation" NUMERIC,
    "timestamp" TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY ("symbol", "timestamp")
);
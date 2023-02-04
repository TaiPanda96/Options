CREATE TABLE IF NOT EXISTS "risk_free_rate" (
    "riskFreeRate" NUMERIC,
    "timestamp" TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY ("symbol", "timestamp")
);
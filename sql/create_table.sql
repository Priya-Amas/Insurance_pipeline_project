CREATE OR REPLACE TABLE insurance_policies (
    policy_id        NUMBER,
    customer_name    STRING,
    premium_amount   FLOAT,
    status           STRING,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

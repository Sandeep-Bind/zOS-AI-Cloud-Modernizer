-- =========================================================================
-- DB2 to Cloud PostgreSQL Schema Mapping for Change Data Capture (CDC)
-- =========================================================================

CREATE TABLE cloud_core_accounts (
    account_id       VARCHAR(12) NOT NULL PRIMARY KEY,
    customer_name    VARCHAR(50) NOT NULL,
    account_type     VARCHAR(3) NOT NULL,
    balance          NUMERIC(13, 2) NOT NULL,
    interest_accrued NUMERIC(11, 4) DEFAULT 0.0000,
    status           VARCHAR(1) NOT NULL,
    last_updated     TIMESTAMP WITHOUT TIME ZONE NOT NULL
);

CREATE INDEX idx_cloud_acc_status ON cloud_core_accounts(status);

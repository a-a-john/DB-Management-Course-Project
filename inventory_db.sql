-- SQL Code here
CREATE TABLE EMPLOYEE (
    employee_id BIGINT              NOT NULL,
    emp_name    VARCHAR(100)        NOT NULL,
    email       VARCHAR(320)        NOT NULL,
    job_type    VARCHAR(20)         NOT NULL,
    branch_no   BIGINT              NOT NULL,

    PRIMARY KEY (employee_id)
);

CREATE TABLE SUPERMARKET_COMPANY (
    company_name    VARCHAR(100)    NOT NULL,
    
    PRIMARY KEY (company_name)
);

CREATE TABLE BRANCH (
    branch_no       BIGINT          NOT NULL,
    branch_location VARCHAR(MAX)    NOT NULL,
    company_name    VARCHAR(100)    NOT NULL,

    FOREIGN KEY (company_name) REFERENCES SUPERMARKET_COMPANY(company_name)
    PRIMARY KEY (branch_code)
);

CREATE TABLE SUPPLIER (
    supplier_name   VARCHAR(100)    NOT NULL,

    PRIMARY KEY (supplier_name)
);

CREATE TABLE ORDER_ (
    order_no        INT AUTO_INCREMENT  NOT NULL,
    amount_paid     DECIMAL(10,2)       NOT NULL,
    status          VARCHAR(10)         NOT NULL, -- placed, in_transit, arrived, error

    PRIMARY KEY (order_no));

CREATE TABLE ITEMS (
    item_code   SMALLINT            NOT NULL,
    price       DECIMAL(10,2)       NOT NULL,
    quantity    SMALLINT            NOT NULL,
    item_name   VARCHAR(100)        NOT NULL,
    GMFlag      SMALLINT            NOT NULL,
    FFlag       SMALLINT            NOT NULL,
    HFlag       SMALLINT            NOT NULL,
    TFlag       SMALLINT            NOT NULL,
    HBFlag      SMALLINT            NOT NULL,

    PRIMARY KEY (item_code));
    
CREATE TABLE PURCHASE (
    purchase_no         SMALLINT            NOT NULL,
    amount_recieved     DECIMAL(10,2)       NOT NULL,

    PRIMARY KEY (purchase_no));
    

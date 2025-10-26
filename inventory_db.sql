/*DROP DATABASE IF EXISTS inventory_db;*/

CREATE DATABASE IF NOT EXISTS inventory_db;
USE inventory_db;

CREATE TABLE SUPERMARKET_COMPANY (
    company_name    VARCHAR(100)    NOT NULL,
    
    PRIMARY KEY (company_name)
);

CREATE TABLE BRANCH (
    branch_no       BIGINT          NOT NULL,
    branch_location VARCHAR(255)    NOT NULL,
    company_name    VARCHAR(100)    NOT NULL,

    FOREIGN KEY (company_name) REFERENCES SUPERMARKET_COMPANY(company_name),

    PRIMARY KEY (branch_no)
);

CREATE TABLE EMPLOYEE (
    employee_id BIGINT              NOT NULL,
    emp_name    VARCHAR(100)        NOT NULL,
    email       VARCHAR(320)        NOT NULL UNIQUE,
    job_type    VARCHAR(20)         NOT NULL,
    branch_no   BIGINT              NOT NULL,

    FOREIGN KEY (branch_no) REFERENCES BRANCH(branch_no),

    PRIMARY KEY (employee_id)
);

CREATE TABLE SUPPLIER (
    supplier_name   VARCHAR(100)    NOT NULL,

    PRIMARY KEY (supplier_name)
);

CREATE TABLE SUPPLY_ORDER (
    order_no        INT AUTO_INCREMENT  NOT NULL,
    amount_paid     DECIMAL(10,2)       NOT NULL,
    status          VARCHAR(10)         NOT NULL, -- placed, in_transit, arrived, error

    PRIMARY KEY (order_no)
);

CREATE TABLE ITEMS (
    item_code   SMALLINT            NOT NULL,
    price       DECIMAL(10,2)       NOT NULL,
    quantity    SMALLINT            NOT NULL,
    item_name   VARCHAR(100)        NOT NULL,
    GMFlag      TINYINT(1)          NOT NULL DEFAULT 0,
    FFlag       TINYINT(1)          NOT NULL DEFAULT 0,
    HFlag       TINYINT(1)          NOT NULL DEFAULT 0,
    TFlag       TINYINT(1)          NOT NULL DEFAULT 0,
    HBFlag      TINYINT(1)          NOT NULL DEFAULT 0,

    PRIMARY KEY (item_code)
);

CREATE TABLE PURCHASE (
    purchase_no         SMALLINT            NOT NULL,
    amount_received     DECIMAL(10,2)       NOT NULL,

    PRIMARY KEY (purchase_no)
);

CREATE TABLE ORDER_PLACEMENT (
    branch_no       BIGINT          NOT NULL,
    supplier_name   VARCHAR(100)    NOT NULL,
    order_no        INT             NOT NULL,

    FOREIGN KEY (branch_no) REFERENCES BRANCH(branch_no),
    FOREIGN KEY (supplier_name) REFERENCES SUPPLIER(supplier_name),
    FOREIGN KEY (order_no) REFERENCES SUPPLY_ORDER(order_no),

    PRIMARY KEY (branch_no, supplier_name, order_no)
);
    
CREATE TABLE ORDER_CONTAINS (
    order_no    INT         NOT NULL,
    item_code   SMALLINT    NOT NULL,
    quantity    SMALLINT    NOT NULL,

    FOREIGN KEY (order_no) REFERENCES SUPPLY_ORDER(order_no),
    FOREIGN KEY (item_code) REFERENCES ITEMS(item_code),

    PRIMARY KEY (order_no, item_code)
);
    
CREATE TABLE OFFERS (
    branch_no       BIGINT      NOT NULL,
    item_code       SMALLINT    NOT NULL,
    local_quantity  SMALLINT    NOT NULL,

    FOREIGN KEY (branch_no) REFERENCES BRANCH(branch_no),
    FOREIGN KEY (item_code) REFERENCES ITEMS(item_code),

    PRIMARY KEY (branch_no, item_code)
);

CREATE TABLE BELONGS_TO (
    purchase_no SMALLINT    NOT NULL,
    item_code   SMALLINT    NOT NULL,

    FOREIGN KEY (purchase_no) REFERENCES PURCHASE(purchase_no),
    FOREIGN KEY (item_code) REFERENCES ITEMS(item_code),

    PRIMARY KEY (purchase_no, item_code)
);
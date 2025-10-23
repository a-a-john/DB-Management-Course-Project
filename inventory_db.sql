-- SQL Code here
CREATE TABLE EMPLOYEE (
    PRIMARY KEY (employee_id),

    emp_name    VARCHAR(100)        NOT NULL,
    email       VARCHAR(320)        NOT NULL,
    job_type    VARCHAR(20)         NOT NULL,
    branch_code INT                 NOT NULL,
);

CREATE TABLE BRANCH (
    PRIMARY KEY (branch_code),

    branch_location VARCHAR(MAX)    NOT NULL,
    company_name    VARCHAR(100)    NOT NULL,
);

CREATE TABLE SUPERMARKET_COMPANY (
    PRIMARY KEY (company_name)
);

CREATE TABLE SUPPLIER (
    PRIMARY KEY (supplier_name)
);
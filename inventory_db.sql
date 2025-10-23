-- SQL Code here
CREATE TABLE EMPLOYEE (
    employee_id BIGINT              NOT NULL,
    emp_name    VARCHAR(100)        NOT NULL,
    email       VARCHAR(320)        NOT NULL,
    job_type    VARCHAR(20)         NOT NULL,
    branch_code INT                 NOT NULL,

    PRIMARY KEY (employee_id)
);

CREATE TABLE SUPERMARKET_COMPANY (
    company_name    VARCHAR(100)    NOT NULL,
    
    PRIMARY KEY (company_name)
);

CREATE TABLE BRANCH (
    branch_code     BIGINT          NOT NULL,
    branch_location VARCHAR(MAX)    NOT NULL,
    company_name    VARCHAR(100)    NOT NULL,

    FOREIGN KEY (company_name) REFERENCES SUPERMARKET_COMPANY(company_name)
    PRIMARY KEY (branch_code)
);

CREATE TABLE SUPPLIER (
    supplier_name   VARCHAR(100)    NOT NULL,

    PRIMARY KEY (supplier_name)
);
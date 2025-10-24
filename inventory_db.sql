-- SQL Code here

CREATE DATABASE inventory_db;

USE inventory_db;

CREATE TABLE ORDER_PLACEMENT (
	branch_no       SMALLINT            NOT NULL,
    supplier_name   VARCHAR(25)         NOT NULL,
    order_no        INT AUTO_INCREMENT  NOT NULL,

    FOREIGN KEY (branch_no) REFERENCES BRANCH(branch_no),
    FOREIGN KEY (supplier_name) REFERENCES SUPPLIER(supplier_no),
    FOREIGN KEY (order_no) REFERENCES ORDER_(order_no)
    PRIMARY KEY (BranchNo,SupplierName,OrderNo));
    
CREATE TABLE ORDER_CONTAINS (
	order_no    INT AUTO_INCREMENT  NOT NULL,
    item_code   SMALLINT            NOT NULL,
    quantity    SMALLINT            NOT NULL,

    FOREIGN KEY (order_no) REFERENCES ORDER_(order_no),
    FOREIGN KEY (item_code) REFERENCES ITEM(item_code),
    PRIMARY KEY (order_no, item_code));
    
CREATE TABLE OFFERS (
	branch_no    SMALLINT    NOT NULL,
    item_code    SMALLINT    NOT NULL,

    FOREIGN KEY (branch_no) REFERENCES BRANCH(branch_code),
    FOREIGN KEY (item_code) REFERENCES ITEM(item_code),
    PRIMARY KEY (branch_no, item_code));
    
CREATE TABLE BELONGS_TO (
	purchase_no SMALLINT    NOT NULL,
    item_code   SMALLINT    NOT NULL,

    FOREIGN KEY (purchase_no) REFERENCES PURCHASE(purchase_no),
    FOREIGN KEY (item_code) REFERENCES ITEM(item_code),
    PRIMARY KEY (purchase_no, item_code));
	
    
    
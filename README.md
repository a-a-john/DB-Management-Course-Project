# **Inventory Management System**
Course: CPSC 471 — Database Management Systems

Instructor: Dr. Leanne Wu

Project Status: Ongoing Group Project


## **Overview**
This project is an inventory management system designed for supermarket companies that operate one or more branches. The system supports efficient tracking of stock levels, organization of items by overlapping categories (such as Home Goods, Food, and Toiletries), and streamlined re-ordering when supplies run low.

System users are supermarket employees, categorized as:

Branch Managers: Can manage branch and global inventory, and place orders with suppliers when stock is low.

Cashiers: Can bill customers, with the system automatically updating inventory quantities.

This project was designed and built from the ground up to practice foundational database concepts. The development process began with an Entity-Relationship (ER) diagram and a Relational Schema, which guided the database implementation.


## **Features Implemented**
User Login System: Authenticates employees as Branch Managers or Cashiers.

Inventory Adjustment: Automatic incrementing and decrementing of stock both globally and per branch.

Ordering: Branch Managers can order more stock with automatic inventory updates.

Billing: Cashiers can process customer purchases with automatic inventory updates.


## **Features In Progress**
Low Stock Alerts: Notifications when inventory levels fall below a defined threshold.

Inventory Display: Detailed views of stock levels per branch and globally.

Supplier Ordering Interface: A streamlined workflow for Branch Managers to order new stock.


## Technologies Used

- Database: SQL (Relational Database)
  
- Backend: Python, Flask, SQLAlchemy
  
- Frontend: HTML, CSS

- Tools / Frameworks: Flask, SQLAlchemy
  

## **Purpose**
This project serves as practical experience applying database design principles learned in CPSC 471. By modeling, implementing, and querying a real system, our group gains hands-on familiarity with relational databases, creating usable applications, constraints, and multi-user workflows.

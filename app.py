import os

import mysql.connector
from flask import Flask, render_template, request
from dotenv import load_dotenv

from dummy_items import get_random_item 

load_dotenv()  # Loads .env variables

HOST = os.getenv("HOST")
USER = os.getenv("USER") 
PASSWORD = os.getenv("PASSWORD") 
DATABASE = os.getenv("DATABASE")

curr_cashier_logs = []
curr_order_logs = []

def get_db_connection():
    
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )

app = Flask(__name__, static_folder='styles')

@app.route("/")
def index():
    return render_template("index.html", page="index", title="Home")

@app.route("/cashier", methods=["GET", "POST"])
def cashier():
    if request.method == "POST":
        item_code = request.form.get("item_code")
        quantity = int(request.form.get("quantity"))

        db = get_db_connection()
        cursor = db.cursor()

        try:
            # check if the item is there
            cursor.execute("SELECT quantity FROM ITEMS WHERE item_code = %s", (item_code,))
            result = cursor.fetchone()

            if result:
                current_qty = result[0]
                if current_qty >= quantity:
                    new_qty = current_qty - quantity
                    cursor.execute("UPDATE ITEMS SET quantity = %s WHERE item_code = %s", (new_qty, item_code))
                    db.commit()
                    print("Purchase recorded successfully!")
                else:
                    print("Error: Insufficent stock.")
            else:
                print("Error: Item not found.")

            curr_cashier_logs.append({
                "item_code": item_code,
                "quantity": quantity
            })

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            db.rollback()

        finally:
            cursor.close()
            db.close()

    return render_template("cashier.html", page="cashier", title="Cashier", submitted=curr_cashier_logs)


@app.route("/manager", methods=["GET", "POST"])
def manager():
    if request.method == "POST":
        item_code = request.form.get("item_code")
        quantity = request.form.get("quantity")

        db = get_db_connection()
        cursor = db.cursor()

        try:
            # insert new supply order
            cursor.execute(
                "INSERT INTO SUPPLY_ORDER (amount_paid, status) VALUES (%s, %s)",
                (0.00, "placed")
            )
            order_no = cursor.lastrowid  # ID of new order

            # insert and quantity into ORDER_CONTAINS
            cursor.execute(
                "INSERT INTO ORDER_CONTAINS (order_no, item_code, quantity) VALUES (%s, %s, %s)",
                (order_no, item_code, quantity)
            )

            db.commit()

            curr_order_logs.append({
                "item_code": item_code,
                "quantity": quantity
            })

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            db.rollback()

        finally:
            cursor.close()
            db.close()

    return render_template("manager.html", page="manager", title="Manager", submitted=curr_order_logs)


@app.route("/inventory")
def inventory():
    return render_template("inventory.html", page="inventory", title="Inventory")

def add_dummy_items(count: int):
    db = get_db_connection()
    cursor = db.cursor()
    
    table_name = "ITEMS"
    column_name = "item_code"
    
    
    for i in range(1, count+1):
        random_item = get_random_item()
        search_value = random_item["item_code"]
        search_query = f"SELECT 1 FROM {table_name} WHERE {column_name} = %s LIMIT 1"
        
        cursor.execute(search_query, (search_value,))
        
        item_exists = cursor.fetchone() is not None
        
        if item_exists:
            update_query = f"UPDATE {table_name} SET quantity = quantity + 1 WHERE {column_name} = %s"
            cursor.execute(update_query, (search_value,))            

        else:
            insert_query = f"INSERT INTO {table_name} (item_name, item_code, quantity, {random_item['flag']}, price) VALUES (%s, %s, %s, %s, %s)"
            values = (
                        random_item["item_name"],   # item_name
                        random_item["item_code"],   # item_code
                        1,                          # quantity starts at 1
                        1,                          # that flag column gets 1
                        5.00,
                    )
            
            
            cursor.execute(insert_query, values)
    
    print(f"{count} DUMMY ITEMS INSERTED INTO ITEMS TABLE")
    cursor.close()    
    db.commit()
        
        

if __name__ == "__main__":
    add_dummy_items(1000)
    app.run(debug=True)
    
    db = get_db_connection()
    cursor = db.cursor()
    
    cursor.execute("DELETE FROM SUPPLY_ORDER;")
    cursor.execute("DELETE FROM ORDER_CONTAINS;")
    cursor.execute("DELETE FROM ITEMS;")
    cursor.close()
    db.commit()
    
    db.close()
from flask import Flask, render_template, request
import mysql.connector
from dotenv import load_dotenv
import os

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
        item_code = request.form.get("item_code") # you can use this for your SQL connection
        quantity = request.form.get("quantity") # Same as this
        
        # We can check if an item exists here later
        
        curr_cashier_logs.append({
            "item_code": item_code,
            "quantity": quantity
        })
        
    return render_template("cashier.html", page="cashier", title="Cashier", submitted=curr_cashier_logs)

@app.route("/manager", methods=["GET", "POST"])
def manager():
    if request.method == "POST":
        item_code = request.form.get("item_code") # you can use this for your SQL connection
        quantity = request.form.get("quantity") # Same as this
        
        # We can check if an item exists here later
        
        curr_order_logs.append({
            "item_code": item_code,
            "quantity": quantity
        })
        
    return render_template("manager.html", page="manager", title="Manager", submitted=curr_order_logs)

@app.route("/inventory")
def inventory():
    return render_template("inventory.html", page="inventory", title="Inventory")

if __name__ == "__main__":
    app.run(debug=True)
import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from dummy_items import get_random_item

# Load .env variables
load_dotenv()
HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

app = Flask(__name__, static_folder='styles')

# SQLAlchemy Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Definition of database tables
class SupermarketCompany(db.Model):
    __tablename__ = "SUPERMARKET_COMPANY"

    company_name = db.Column(db.String(100), primary_key=True)

    branches = db.relationship("Branch", back_populates="company")

class Branch(db.Model):
    __tablename__ = "BRANCH"

    branch_no = db.Column(db.BigInteger, primary_key=True)
    branch_location = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(100), db.ForeignKey("SUPERMARKET_COMPANY.company_name"), nullable=False)

    company = db.relationship("SupermarketCompany", back_populates="branches")
    # employees = db.relationship("Employee", back_populates="branch")
    order_placements = db.relationship("OrderPlacement", back_populates="branch")
    offers = db.relationship("Offers", back_populates="branch")

class Employee(db.Model):
    __tablename__ = "EMPLOYEE"

    employee_id = db.Column(db.BigInteger, primary_key=True)
    emp_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    job_type = db.Column(db.String(20), nullable=False)
    # removed db.ForeignKey("BRANCH.branch_no"): change back when we implemented branches
    branch_no = db.Column(db.BigInteger, nullable=False)

    # branch = db.relationship("Branch", back_populates="employees")

class Supplier(db.Model):
    __tablename__ = "SUPPLIER"

    supplier_name = db.Column(db.String(100), primary_key=True)

    order_placements = db.relationship("OrderPlacement", back_populates="supplier")

class SupplyOrder(db.Model):
    __tablename__ = "SUPPLY_ORDER"

    order_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount_paid = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(10), nullable=False)  # placed, in_transit, arrived, error

    order_contains = db.relationship("OrderContains", back_populates="supply_order")
    order_placements = db.relationship("OrderPlacement", back_populates="supply_order")

class Item(db.Model):
    __tablename__ = "ITEMS"

    item_code = db.Column(db.SmallInteger, primary_key=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.SmallInteger, nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    GMFlag = db.Column(db.Boolean, default=False, nullable=False)
    FFlag = db.Column(db.Boolean, default=False, nullable=False)
    HFlag = db.Column(db.Boolean, default=False, nullable=False)
    TFlag = db.Column(db.Boolean, default=False, nullable=False)
    HBFlag = db.Column(db.Boolean, default=False, nullable=False)

    order_contains = db.relationship("OrderContains", back_populates="item")
    offers = db.relationship("Offers", back_populates="item")
    belongs_to = db.relationship("BelongsTo", back_populates="item")

class Purchase(db.Model):
    __tablename__ = "PURCHASE"

    purchase_no = db.Column(db.SmallInteger, primary_key=True)
    amount_received = db.Column(db.Numeric(10, 2), nullable=False)

    belongs_to = db.relationship("BelongsTo", back_populates="purchase")

class OrderPlacement(db.Model):
    __tablename__ = "ORDER_PLACEMENT"

    branch_no = db.Column(db.BigInteger, db.ForeignKey("BRANCH.branch_no"), primary_key=True)
    supplier_name = db.Column(db.String(100), db.ForeignKey("SUPPLIER.supplier_name"), primary_key=True)
    order_no = db.Column(db.Integer, db.ForeignKey("SUPPLY_ORDER.order_no"), primary_key=True)

    branch = db.relationship("Branch", back_populates="order_placements")
    supplier = db.relationship("Supplier", back_populates="order_placements")
    supply_order = db.relationship("SupplyOrder", back_populates="order_placements")

class OrderContains(db.Model):
    __tablename__ = "ORDER_CONTAINS"

    order_no = db.Column(db.Integer, db.ForeignKey("SUPPLY_ORDER.order_no"), primary_key=True)
    item_code = db.Column(db.SmallInteger, db.ForeignKey("ITEMS.item_code"), primary_key=True)
    quantity = db.Column(db.SmallInteger, nullable=False)

    supply_order = db.relationship("SupplyOrder", back_populates="order_contains")
    item = db.relationship("Item", back_populates="order_contains")

class Offers(db.Model):
    __tablename__ = "OFFERS"

    branch_no = db.Column(db.BigInteger, db.ForeignKey("BRANCH.branch_no"), primary_key=True)
    item_code = db.Column(db.SmallInteger, db.ForeignKey("ITEMS.item_code"), primary_key=True)
    local_quantity = db.Column(db.SmallInteger, nullable=False)

    branch = db.relationship("Branch", back_populates="offers")
    item = db.relationship("Item", back_populates="offers")

class BelongsTo(db.Model):
    __tablename__ = "BELONGS_TO"

    purchase_no = db.Column(db.SmallInteger, db.ForeignKey("PURCHASE.purchase_no"), primary_key=True)
    item_code = db.Column(db.SmallInteger, db.ForeignKey("ITEMS.item_code"), primary_key=True)

    purchase = db.relationship("Purchase", back_populates="belongs_to")
    item = db.relationship("Item", back_populates="belongs_to")


curr_cashier_logs = []
curr_order_logs = []

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Save data temporarily (for now)
        entered_login_data = {
            "email": email,
            "password": password
        }

        print("Received login data:", entered_login_data)

        # In the future: authenticate user here
        return render_template("home.html", page="home", title="Home", login_data=entered_login_data)

    return render_template("login.html", title="Login")


@app.route("/home")
def home():
    return render_template("home.html", page="home", title="Home")


@app.route("/cashier", methods=["GET", "POST"])
def cashier():
    if request.method == "POST":
        item_code = request.form.get("item_code")
        quantity = int(request.form.get("quantity"))

        try:
            item = Item.query.filter_by(item_code=item_code).first()
            if item:
                if item.quantity >= quantity:
                    item.quantity -= quantity
                    db.session.commit()
                    print("Purchase recorded successfully!")
                else:
                    print("Error: Insufficient stock.")
            else:
                print("Error: Item not found.")

            curr_cashier_logs.append({
                "item_code": item_code,
                "quantity": quantity
            })

        except Exception as e:
            db.session.rollback()
            print(f"Database Error: {e}")

    return render_template("cashier.html", page="cashier", title="Cashier", submitted=curr_cashier_logs)


@app.route("/manager", methods=["GET", "POST"])
def manager():
    if request.method == "POST":
        item_code = request.form.get("item_code")
        quantity = int(request.form.get("quantity"))

        try:
            # create new supply order
            new_order = SupplyOrder(amount_paid=0.00, status="placed")
            db.session.add(new_order)
            db.session.flush()  # to get order_no before commit

            # add to ORDER_CONTAINS
            new_contain = OrderContains(order_no=new_order.order_no, item_code=item_code, quantity=quantity)
            db.session.add(new_contain)

            # update item quantity
            item = Item.query.filter_by(item_code=item_code).first()
            if item:
                item.quantity += quantity
            db.session.commit()

            curr_order_logs.append({
                "item_code": item_code,
                "quantity": quantity
            })

        except Exception as e:
            db.session.rollback()
            print(f"Database Error: {e}")

    return render_template("manager.html", page="manager", title="Manager", submitted=curr_order_logs)


@app.route("/inventory")
def inventory():
    items = Item.query.all()
    return render_template("inventory.html", page="inventory", title="Inventory", items=items)


# dummy generator
def add_dummy_items(count: int):
    for i in range(count):
        random_item = get_random_item()
        item = Item.query.filter_by(item_code=random_item["item_code"]).first()

        if item:
            item.quantity += 1
        else:
            new_item = Item(
                item_name=random_item["item_name"],
                item_code=random_item["item_code"],
                quantity=1,
                price=5.00
            )

            flag_name = random_item["flag"]
            if hasattr(new_item, flag_name):
                setattr(new_item, flag_name, True)

            db.session.add(new_item)
    db.session.commit()
    print(f"{count} DUMMY ITEMS INSERTED INTO ITEMS TABLE")


def create_initial_employees():
    # Mitarbeiter-Definitionen
    employees_data = [
        {
            "employee_id": 1,
            "emp_name": "Adhira John",
            "email": "adhira.john@inventory.com",
            "job_type": "Manager",
            "branch_no": 1
        },
        {
            "employee_id": 2,
            "emp_name": "Taha Gummy",
            "email": "taha.gummy@inventory.com",
            "job_type": "Manager",
            "branch_no": 2
        },
        {
            "employee_id": 3,
            "emp_name": "Leonie Mertens",
            "email": "leonie.mertens@inventory.com",
            "job_type": "Cashier",
            "branch_no": 2
        }
    ]

    for emp_data in employees_data:
        # Prüfen, ob Mitarbeiter bereits existiert
        existing = Employee.query.filter_by(employee_id=emp_data["employee_id"]).first()
        
        if not existing:
            new_employee = Employee(**emp_data)
            db.session.add(new_employee)
    
    db.session.commit()
    print("Initial employees ensured in database.")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ensures tables exist
        add_dummy_items(1000)
        create_initial_employees()

    app.run(debug=True)

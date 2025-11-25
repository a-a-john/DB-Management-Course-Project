import json
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from dummy_items import get_random_item

# Load .env variables
load_dotenv()
HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

with open("users.json", "r") as f:
    USER_CREDENTIALS = json.load(f)["users"]

app = Flask(__name__, static_folder='styles')

app.secret_key = os.getenv("SECRET_KEY")

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
    employees = db.relationship("Employee", back_populates="branch")  # <- FIXED
    order_placements = db.relationship("OrderPlacement", back_populates="branch")
    offers = db.relationship("Offers", back_populates="branch")
    branch_items = db.relationship("BranchItems", back_populates="branch")


class Employee(db.Model):
    __tablename__ = "EMPLOYEE"

    employee_id = db.Column(db.BigInteger, primary_key=True)
    emp_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    job_type = db.Column(db.String(20), nullable=False)
    branch_no = db.Column(db.BigInteger, db.ForeignKey("BRANCH.branch_no"), nullable=False)  # <- Add FK

    branch = db.relationship("Branch", back_populates="employees")

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
    branch_items = db.relationship("BranchItems", back_populates="item")

class BranchItems(db.Model):
    __tablename__ = "BRANCH_ITEMS"

    branch_no = db.Column(db.BigInteger, db.ForeignKey("BRANCH.branch_no"), primary_key=True)
    item_code = db.Column(db.SmallInteger, db.ForeignKey("ITEMS.item_code"), primary_key=True)
    local_quantity = db.Column(db.Integer, default=0, nullable=False)

    branch = db.relationship("Branch", back_populates="branch_items")
    item = db.relationship("Item", back_populates="branch_items")

class Purchase(db.Model):
    __tablename__ = "PURCHASE"

    purchase_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    purchase_no = db.Column(db.Integer, db.ForeignKey("PURCHASE.purchase_no"), primary_key=True)
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
        # Check credentials
        valid_user = next(
            (user for user in USER_CREDENTIALS if user["email"] == email and user["password"] == password),
            None
        )

        if valid_user:
            print("Login successful:", email)
            employee_record = Employee.query.filter_by(email=email).first()
            if employee_record:
                branch_no = employee_record.branch_no
                job_type = employee_record.job_type
                session["branch_id"] = employee_record.branch_no
                session["job_type"] = employee_record.job_type
                # session["employee_email"] = employee_record.email
                # session["employee_name"] = employee_record.emp_name
                print("Stored branch ID:", branch_no)
                print("Stored job type:", job_type)

                if job_type.lower() == "cashier":
                    return redirect(url_for("cashier"))

                if job_type.lower() == "manager":
                    return redirect(url_for("manager"))

            return redirect(url_for("login"))

        else:
            print("Login failed.")
            return render_template("login.html", title="Login", error="Invalid email or password.")

    return render_template("login.html", title="Login")


@app.route("/home")
def home():
    return render_template("home.html", page="home", title="Home")


@app.route("/cashier", methods=["GET", "POST"])
def cashier():
    if request.method == "POST":
        try:
            item_code = int(request.form.get("item_code"))
            quantity = int(request.form.get("quantity"))
            branch_id = session.get("branch_id")

            # fetch item by item code
            item = Item.query.filter_by(item_code=item_code).first()
            if not item:
                return render_template("cashier.html", page="cashier", title="Cashier",
                                       submitted=curr_cashier_logs,
                                       error=f"Item {item_code} does not exist.")

            # fetch the same item as a branch item
            branch_item = BranchItems.query.filter_by(
                branch_no=branch_id,
                item_code=item_code
            ).first()

            if not branch_item:
                return render_template("cashier.html", page="cashier", title="Cashier",
                                       submitted=curr_cashier_logs,
                                       error=f"Item {item_code} not stocked in branch {branch_id}")

            # check stock - if there is not enough to sell, return error
            if branch_item.local_quantity < quantity:
                return render_template("cashier.html", page="cashier", title="Cashier",
                                       submitted=curr_cashier_logs,
                                       error="Insufficient stock in branch.")

            # decrease global and local quantities
            item.quantity -= quantity
            branch_item.local_quantity -= quantity
            print(f"Updated Item {item_code}: global={item.quantity}, branch={branch_item.local_quantity}")

            # create purchase and belongs to records
            new_purchase = Purchase(amount_received=0.00)
            db.session.add(new_purchase)
            db.session.flush() # now new_purchase.purchase_no exists - again, not sure exactly how this works
            belongs = BelongsTo(purchase_no=new_purchase.purchase_no, item_code=item_code)
            db.session.add(belongs)

            db.session.commit()

            # log to screen
            curr_cashier_logs.append({
                "item_code": item_code,
                "quantity": quantity,
                "branch_no": branch_id,
                "purchase_no": new_purchase.purchase_no
            })

        except Exception as e:
            db.session.rollback()
            print(f"Database Error: {e}")

    return render_template("cashier.html", page="cashier", title="Cashier", submitted=curr_cashier_logs)

@app.route("/manager", methods=["GET", "POST"])
def manager():
    if request.method == "POST":
        try:
            item_code = int(request.form.get("item_code"))
            quantity = int(request.form.get("quantity"))
            # get the appropriate branch from the session (which was saved upon login)
            branch_id = session.get("branch_id")

            # fetch item by item code
            item = Item.query.filter_by(item_code=item_code).first()
            if not item:
                print(f"Error: Item {item_code} not found")
                return render_template("manager.html", page="manager", title="Manager", submitted=curr_order_logs, error=f"Item {item_code} does not exist.")

            # fetch the same item as a branch item
            branch_item = BranchItems.query.filter_by(branch_no=branch_id, item_code=item_code).first()

            # increase quantities by the quantity requested in order
            item.quantity += quantity
            branch_item.local_quantity += quantity
            print(f"Updated Item {item_code}: global={item.quantity}, branch {branch_id}={branch_item.local_quantity}")

            # create supply order
            new_order = SupplyOrder(amount_paid = 0.00, status = "placed")
            db.session.add(new_order)
            db.session.flush()  # get order_no - again, not sure exactly how this works
            new_contain = OrderContains(order_no = new_order.order_no, item_code = item_code, quantity = quantity)
            db.session.add(new_contain)

            db.session.commit()

            # log to screen
            curr_order_logs.append({
                "item_code": item_code,
                "quantity": quantity,
                "branch_no": branch_id
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
import random

def add_dummy_items(count: int):
    branches = Branch.query.all()  # get all branches

    for _ in range(count):
        random_item = get_random_item()
        item_code = random_item["item_code"]

        # check if item exists
        item = Item.query.filter_by(item_code=item_code).first()

        if item:
            # item exists, so increase global quantity
            item.quantity += 1

            # pick a random branch
            branch = random.choice(branches)
            branch_item = BranchItems.query.filter_by(branch_no=branch.branch_no, item_code=item.item_code).first()

            # if the item is already in that branch, increase their local quantity of that item
            if branch_item:
                branch_item.local_quantity += 1
            else:
                # if item does not exist in that branch add it as a branch item
                branch_item = BranchItems(
                    branch_no=branch.branch_no,
                    item_code=item.item_code,
                    local_quantity=1
                )
                db.session.add(branch_item)

        else:
            # if the item is totally new, create new item
            new_item = Item(
                item_name=random_item["item_name"], item_code=item_code, quantity=1, price=5.00)

            # set flag if exists
            flag_name = random_item.get("flag")
            if flag_name and hasattr(new_item, flag_name):
                setattr(new_item, flag_name, True)

            db.session.add(new_item)
            db.session.flush()  # ensures item_code is available for FK - not super sure how this works...

            # assign the new item to a random branch
            branch = random.choice(branches)
            branch_item = BranchItems(branch_no=branch.branch_no, item_code=new_item.item_code, local_quantity=1)
            db.session.add(branch_item)

    db.session.commit()
    print(f"{count} DUMMY ITEMS inserted, with quantities updated per branch and globally")

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
        db.drop_all()
        db.create_all()

        company = SupermarketCompany(company_name="MySupermarket")
        db.session.add(company)

        branch1 = Branch(branch_no=1, branch_location="Location 1", company_name=company.company_name)
        branch2 = Branch(branch_no=2, branch_location="Location 2", company_name=company.company_name)
        db.session.add_all([branch1, branch2])
        db.session.commit()

        add_dummy_items(1000)
        create_initial_employees()

    app.run(debug=True)


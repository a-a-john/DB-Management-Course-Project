import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env variables

HOST, USER, PASSWORD, DATABASE = os.getenv("HOST"), os.getenv("USER"), os.getenv("PASSWORD"), os.getenv("DATABASE")

# mydb = mysql.connector.connect(
#       host="localhost",
#       user="yourusername",
#       password="yourpassword",
#       database="yourdatabase"
# )

print(HOST)
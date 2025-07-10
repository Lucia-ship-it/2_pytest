import importlib
from dotenv import load_dotenv
import os

load_dotenv()
library = os.getenv("LIBRARY")
if library == "luciakobzova":
    db = importlib.import_module("src.db_mysql")
else:
    db = importlib.import_module("src.db_pymysql")

if __name__ == "__main__":
    passwd = os.getenv("DB_PASSW")
    # db.initialize_database("localhost", "root", passwd, "mydb")
    conn = db.connect_to_db("mysql80.r4.websupport.sk", "luciakobzova", passwd, "luciakobzova", 3314)
    db.add_user(conn, "John", 28)
    print(db.get_users(conn))
    db.close_connection(conn)
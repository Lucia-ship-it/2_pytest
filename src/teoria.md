1. instalacia venv a pip
2. instalacia pytest
pip3 install -U pytest

ked testujeme, musim eredpokladat, ze je to spatne. preto by sme nemali verit, ze connection je dobre napisane v hlavnom skripte. preto si ju napiseme sami.

musime import.pytest. lebo sme dali @ a volame ho tam

logika fixture
- pytest fixture
aby sa pri testovani nestala chyba ked chcem zmazat data

yield na zaciatku / specialny typ return
zacne, skoci do funkce, potom sa vrati na koniec. ked v pyteste s fixtures tak to pekne funguje.

vytvorim conn, dam yield, con.close
from src.db_mysql import add_user
import mysql.connector
import pytest
# pozitivní: jestli můžeme přidat uživatele
# Jane Doe, 25

@pytest.fixture
def create_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111"
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS test_db")
    conn.database = "test_db"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT NOT NULL CHECK (age >= 0),
            email VARCHAR(255) DEFAULT NULL
        )
    """)
    conn.commit()
    yield 'test_db'
    cursor.execute('DROP DATABASE test_db')
    cursor.close()
    conn.close()


@pytest.fixture(scope="sesion")
def conn(create_database):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",
        database=create_database
    )
    print("Vytvářím connection")
    yield conn
    print("uazvírám connection")
    conn.close()

@pytest.mark.parametrize(
        "name,age,email",
        [("Jane Doe", 25, None),
         ("Teo Smith", 75, "teo@email.cz")]
)
def test_add_user(conn, name, age, email):
    add_user(conn, name, age, email)
    print(f"Používám connction:{(name, age, email)}")
    # jak zkontrolujeme, že ta fufnkce udělala, co měla?
    cursor = conn.cursor()
    cursor.execute("select name,age,email from users where name=%s", (name,))
    user = cursor.fetchall()[0]

    # zkontrolat, že jméno je "Jane Doe"
    assert user[0] == name
    # zkontrolovat, že věk je 25
    assert user[1] == age
    # zkontrolovat, že email je None
    assert user[2] == email

takto by sa vytvorila databaya, urobil test, vymazala databaza. a na dalsi riadok by sa znova musela vytvorti databaza znova a znova. ale ked pouzijem Scope, za BEH sa pusti zalozenie db len raz. 
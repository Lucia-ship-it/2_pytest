from src.db_pymysql import add_user
import pymysql
import pytest
# pozitivní: jestli můžeme přidat uživatele
# Jane Doe, 25

@pytest.fixture
def conn():
    conn = pymysql.connect(
        host="mysql80.r4.websupport.sk",
        user="luciakobzova",
        port=3314,
        password=".,;c6a[M;l:O*9&W[{w,",
        database="luciakobzova"
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

# def test_add_user_2():
#     con = conn("localhost", "root", "1111", "mydb")
#     add_user(con, "Teo Smith", 75, "teo@email.cz")  # věk jako int
#     cursor = con.cursor()
#     cursor.execute("SELECT name, age, email FROM users WHERE name='Teo Smith'")
#     user = cursor.fetchone()


#     assert user is not None, "Uživatel nebyl nalezen v databázi"
#     assert user[0] == "Teo Smith"
#     assert user[1] == 75
#     assert user[2] == "teo@email.cz"
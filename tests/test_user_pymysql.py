from scr.db_pymysql import add_user
import pymysql
# pozitivni test jestli muzeme pridat uzivatele
# Jana Doe, 25

def conn(host, user, passw, db):
    return pymysql.connect(
        host=host,
        user=user,
        password=passw,
        database=db
    )

def test_add_user():
    con = conn("localhost", "root", "1111", "mydb")
    add_user(con, "Jane Doe", 25)
    # jak zkontrolujeme, že ta fufnkce udělala, co měla?
    cursor = con.cursor()
    cursor.execute("select name,age,email from users where name='Jane Doe'")
    user = cursor.fetchall()[0]

    # zkontrolat, že jméno je "Jane Doe"
    assert user[0] == 'Jane Doe'
    # zkontrolovat, že věk je 25
    assert user[1] == 25
    # zkontrolovat, že email je None
    assert user[2] == None
    
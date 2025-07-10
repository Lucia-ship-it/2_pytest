from src.db_pymysql import add_user
import pymysql
import pytest
# pozitivni test jestli muzeme pridat uzivatele
# Jana Doe, 25

def conn(host, user, passw, db, port):
    return pymysql.connect(
        host=host,
        user=user,
        password=passw,
        database=db,
        port=port
    )

def test_add_user():
    con = conn("mysql80.r4.websupport.sk", "luciakobzova", ".,;c6a[M;l:O*9&W[{w,", "luciakobzova", 3314)
    add_user(con, "Jane Doe", 25)
    # jak zkontrolujeme, že ta fufnkce udělala, co měla?
    cursor = con.cursor()
    cursor.execute("select name,age,email from users where name='Jane Doe'")
    user = cursor.fetchall()[0]

    # zkontrolat, že jméno je "Jane Doe"
    assert user[0] == 'Jane Doe', "test 1"
    # zkontrolovat, že věk je 25
    assert user[1] == 25, "test 2"
    # zkontrolovat, že email je None
    assert user[2] == None,"test 3"

#ÚKOL:
#vyzkoušíte funkci add_user
def test_add_user_2():
    con = conn("mysql80.r4.websupport.sk", "luciakobzova", ".,;c6a[M;l:O*9&W[{w,", "luciakobzova", 3314)
    add_user(con, "Teo Smith", 75, "teo@email.cz")
    # jak zkontrolujeme, že ta fufnkce udělala, co měla?
    cursor = con.cursor()
    cursor.execute("select name,age,email from users where name='Teo Smith'")
    user = cursor.fetchall()[0]

    # zkontrolat, že jméno je "Jane Doe"
    assert user[0] == "Teo Smith"
    # zkontrolovat, že věk je 25
    assert user[1] == 75, "test 2"
    # zkontrolovat, že email je None
    assert user[2] == "teo@email.cz"

#//////////////////////////////////////////


@pytest.mark.parametrize(
        "name,age,email",
        [("Jane Doe", 25, None),
         ("Teo Smith", 75, "teo@email.cz")]
    )

def test_add_useris(name, age, email):
    con = conn("mysql80.r4.websupport.sk", "luciakobzova", ".,;c6a[M;l:O*9&W[{w,", "luciakobzova", 3314)
    add_user(con, name, age, email)
    # jak zkontrolujeme, že ta fufnkce udělala, co měla?
    cursor = con.cursor()
    cursor.execute("select name,age,email from users where name=%s", (name,))
    user = cursor.fetchall()[0]

    # zkontrolat, že jméno je "Jane Doe"
    assert user[0] == name
    # zkontrolovat, že věk je 25
    assert user[1] == age
    # zkontrolovat, že email je None
    assert user[2] == email
    
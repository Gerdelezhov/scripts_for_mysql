import pymysql
from cfg import host, user, password, db_name


# подключене к базе данных
def establish_connection():
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        return connection

    except Exception as ex:
        print("connection closed")
        print(ex)


# добавлениу пользователя в базы данных (user_info and notes)
def add_user(user_id, permission, user_name):
    connection = establish_connection()

    sql = "INSERT INTO user_info VALUES (%s, %s, %s)"
    sql2 = "INSERT INTO notes (ID) VALUES (%s)"

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id, permission, user_name))
            cursor.execute(sql2, (user_id))
            cursor.close()

    except Exception as ex:
        print("error by 'INSERT...'")
        print(ex)

    connection.commit()
    connection.close()


# поиск пользователя в базе данных
def find_user(user_id):
    connection = establish_connection()

    sql = "SELECT * FROM user_info WHERE ID=%s"

    with connection.cursor() as cursor:
        cursor.execute(sql, (user_id))
        data = cursor.fetchall()
        cursor.close()

    connection.close()

    if (data == ()):
        return 0
    elif (data[0][0] == user_id):
        return data


# смена уровня доступа
def change_permission(user_id, permission):
    connection = establish_connection()

    sql = "UPDATE user_info SET Permission =%s WHERE ID=%s"

    with connection.cursor() as cursor:
        cursor.execute(sql, (permission, user_id))
        cursor.close()

    connection.commit()
    connection.close()


# вывод базы данных
def database():
    connection = establish_connection()

    sql = "SELECT * FROM user_info"

    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
    connection.close()

    return data

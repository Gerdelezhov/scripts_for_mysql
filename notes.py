import pymysql
from cfg import host, user, password, db_name

max_number_of_notes = 10


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


# возвращает количество заметок
def number_of_notes(user_id):
    connection = establish_connection()

    sql = "SELECT * FROM notes WHERE ID=%s"

    with connection.cursor() as cursor:
        cursor.execute(sql, (user_id))
        data = cursor.fetchall()
        cursor.close()
    connection.close()

    count = 0
    for i in range(len(data[0])):
        if (data[0][i] != None):
            count += 1

    return count - 1


# проверят остались ли ячейки для записи заметок, если нет, добавляет 5 столбиков
def check_max_number_of_notes(note_number):
    if (note_number > max_number_of_notes):
        connection = establish_connection()
        sql = "ALTER TABLE notes ADD N%s TEXT;"
        try:
            with connection.cursor() as cursor:
                for i in range(5):
                    cursor.execute(sql, (note_number + i))
                cursor.close()

        except Exception as ex:
            print("error by 'Write note...'")
            print(ex)


# добавление заметки
def add_note(user_id, text):
    note_number = number_of_notes(user_id) + 1

    check_max_number_of_notes(note_number)

    connection = establish_connection()

    sql = "UPDATE notes SET N%s = %s WHERE ID = %s"

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, (note_number, text, user_id))
            cursor.close()
    except Exception as ex:
        print("error by 'Write note...'")
        print(ex)

    connection.commit()
    connection.close()


# получение заметки из базы данных
def read_note(user_id, note_number):
    amount = number_of_notes(user_id)

    if ((note_number > amount) or (note_number < 1)):
        return -1

    connection = establish_connection()

    sql = "SELECT N%s FROM notes WHERE ID=%s"

    with connection.cursor() as cursor:
        cursor.execute(sql, (note_number, user_id))
        note = cursor.fetchall()
        cursor.close()
    connection.close()

    return note[0][0]


# удаление заметки из базы данных
def delete_note(user_id, note_number):
    amount = number_of_notes(user_id)

    if ((note_number > amount) or (note_number < 1)):
        return -1

    connection = establish_connection()

    sql = "UPDATE notes SET N%s = %s WHERE ID = %s"
    get_sql = "SELECT * FROM notes WHERE ID=%s"

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, (note_number, None, user_id))
            cursor.execute(get_sql, (user_id))
            note = cursor.fetchall()

            for i in range(1, len(note[0])):
                if (i > note_number and i < amount + 2):
                    print(i, note[0][i])
                    cursor.execute(sql, (i - 1, note[0][i], user_id))

            cursor.close()
    except Exception as ex:
        print("error by 'Delete note...'")
        print(ex)

    connection.commit()
    connection.close()

import pymysql
from cfg import host, user, password, db_name


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


# получение расписания на один день
def get_day_from_timetable(group, day):
    connection = establish_connection()

    sql_time = 'SELECT start_time FROM ' + group
    sql_lessons = 'SELECT ' + day + ' FROM ' + group

    with connection.cursor() as cursor:
        cursor.execute(sql_time)
        time = cursor.fetchall()
        cursor.execute(sql_lessons)
        data = cursor.fetchall()
        cursor.close()
    connection.close()

    message = ""
    for i in range(6):
        message += time[i][0] + " | " + data[i][0] + "\n"

    return message


print(get_day_from_timetable('iv_122', 'Mon'))

#test
import mysql.connector 
import sys

help = """
    -s [args] - старт

    [arguments: Названия проектов, для которых нужно начать тест через пробел]
"""

if len(sys.argv) > 1:
    mydbUpper = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='sdosurp'
            )
    myUpperCursor = mydbUpper.cursor()
    for i in range(1, len(sys.argv)): #Проход по аргументам
        sql = "SELECT * FROM main WHERE dir = '{}'".format(sys.argv[i])
        print('Doing work... {}'.format((sys.argv[i])))
        myUpperCursor.execute(sql)
        result = myUpperCursor.fetchone()

        print("SQL: '{}'\nResult: {}".format(sql, result[1]))
        subDb = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database=result[1]
                )
        #Занесение теста 
        subCursor = subDb.cursor()
        for i in range(1,5):
            sql = '''
            INSERT INTO `current_test`(
                `date`, 
                `test_dir`,
                `group_to_test`,
                `time_to_complete`,
                `subject`,
                `question_num`
                )
            VALUES(
                '2021-4-16',
                `Контрольная работа`,
                `Группа {}`,
                `45`,
                `Математика`,
                `11`
            )
            '''.format(i)
            print('Выполнение запроса: "{}"'.format(sql))

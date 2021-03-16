#test
import mysql.connector 
import sys

help = """

    [arguments: Названия бд, в которых нужно начать тест через пробел]
"""

if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)): #Проход по аргументам
        print('Начинаем тест в {}...'.format((sys.argv[i])))

        subDb = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database=sys.argv[i]
                )
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
                'Контрольная работа',
                'Группа {}',
                '45',
                'Математика',
                '11'
            )
            '''.format(i)
            print('Выполнение запроса: "{}"'.format(sql))
            subCursor.execute(sql)
        subDb.commit()

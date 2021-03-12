import mysql.connector
import shutil
import sys

help = """
    [argument1:имя папки новой сдо] [argument2:имя проекта в панели] 
    (без пробелов и спец. символов, `_` можно)
"""

def copyFolder(newFolderName):
    return shutil.copytree('sdo_template', newFolderName)

def insertData(folderName, projectName):
    """
    Вставляет информацию о новой сдо в таблицу
    @param {folderName} string Имя/путь скопированной папки 
    @param {projectName} string Имя, которое будет отображаться в панели 
    """
    mydbCreateNewEntry = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='sdosurp'
            )
    newEntryCursor = mydbCreateNewEntry.cursor()
    sql = "INSERT INTO `main` (`dir`, `name`) VALUES (%s, %s)"
    val = (folderName, projectName)
    newEntryCursor.execute(sql, val)
    mydbCreateNewEntry.commit()

def cloneDatabase(pathToDatabase):
    """
    Копирует sql файл базы данных в новую сдо
    @param {pathToDatabase} string Путь к базе данных из текущего каталога
    """
    dtbFile = open(pathToDatabase, 'r')
    dtbFile = dtbFile.read().splitlines()
    stmts = []
    stm = ''
    for line in dtbFile:
        if line:
            if line.startswith('--'):
                continue
            stm += line.strip() + ' '
            if ';' in stm:
                stmts.append(stm.strip())
                stm = ''

    for stm in stmts:
        print('{} \n'.format(stm))
        mycursor.execute(stm)
    mydb.commit()

if '-h' in sys.argv:
    print(help)
else:
    if len(sys.argv) < 2:
        newFolderPath = str(input('Имя новой папки сдо: '))
        projectNameS = str(input('Название новой сдо в панели: '))
        print('\n')
    else:
        newFolderPath = copyFolder(str(sys.argv[1]))
        projectNameS = str(sys.argv[2])

    #Создание базы данных отдельным соединением
    mydbCreateDatabase = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''
        )
    mycursorC = mydbCreateDatabase.cursor()
    mycursorC.execute('CREATE DATABASE {}'.format(projectNameS))
    
    #Подключение к созданной базе данных 
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database=projectNameS
        )
    mycursor = mydb.cursor()

    insertData(newFolderPath, projectNameS)
    cloneDatabase('sdo_server.sql', projectNameS)
    print("New folder: {}\nArgument list:{}".format(newFolderPath, str(sys.argv)))


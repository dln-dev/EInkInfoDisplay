import sqlite3

# TODO: let frames create their own tables ? But where to get data, too tedious?
#tables = ["weather", "innerClimate", "training1", "training2", "training3", "pushups"] 
big6 = ["squats", "handstands", "legraises", "bridges", "pushups", "pullups"]
shotgun = ["hangs", "calveraises", "neckholds", "buttraises"]
stamina = ["hiit", "stamina"]

connection = sqlite3.connect("evi.db")

cursor = connection.cursor()

# uncomment to reset
# cursor.execute("""DROP TABLE ;""")

for exercise in big6:
    sql_command = """
    CREATE TABLE """ + exercise + """ (
    session INTEGER PRIMARY KEY,
    level INTEGER,
    set1 INTEGER,
    set2 INTEGER,
    set3 INTEGER,
    completed DATE);"""

    cursor.execute(sql_command)

for exercise in shotgun:
    sql_command = """
    CREATE TABLE """ + exercise + """ (
    session INTEGER PRIMARY KEY,
    level INTEGER,
    set1 INTEGER,
    set2 INTEGER,
    set3 INTEGER,
    completed DATE);"""

    cursor.execute(sql_command)




#sql_command = """INSERT INTO training0 (type, set1, set2, set3, completed)
#            VALUES (pushups, 50, 50, 50, "1970-01-01");"""
#cursor.execute(sql_command)

connection.commit()

connection.close()


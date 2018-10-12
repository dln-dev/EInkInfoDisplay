## 
# connects to sports.db. Entry layout is
#
# integer pk, string, integer, integer, integer, integer, \
# real(minutes?), timestamp (accepts datetime objs str(dt.dt.now()))
# ID, name, level, set1, set2, set3, time, completed
# !ID not necessary, sqlite implicitly defines a rowid 


import sqlite3

# TODO: let frames create their own tables ? But where to get data, too tedious?
#tables = ["weather", "innerClimate", "training1", "training2", "training3", "pushups"] 
#big6 = ["squats", "handstands", "legraises", "bridges", "pushups", "pullups"]
#shotgun = ["hangs", "calveraises", "neckholds", "buttraises"]
#stamina = ["hiit", "stamina"]

connection = sqlite3.connect("sports.db")

cursor = connection.cursor()

# uncomment to reset
#cursor.execute("""DROP TABLE exercises;""")

sql_command = """
CREATE TABLE exercises (
name TEXT NOT NULL,
level INTEGER,
set1 INTEGER,
set2 INTEGER,
set3 INTEGER,
time REAL,
completed TIMESTAMP NOT NULL)"""

cursor.execute(sql_command)


connection.commit()

connection.close()

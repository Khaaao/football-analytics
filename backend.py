import mysql.connector
from mysql.connector import errorcode

try:
  cnx = mysql.connector.connect(user='app_football_analytics', password='5BD7bxvY823K',
                              host='localhost',
                              database='football')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()
from menu import main_menu
import pymysql
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='0926',
                             db='meal_plan',
                             charset='utf8mb4')
cursor = connection.cursor()
main_menu(cursor)
connection.commit()
cursor.close()
print("Closing connection to database...\n")
connection.close()
print("Goodbye!\n")






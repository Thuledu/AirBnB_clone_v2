#!/usr/bin/python3
""" A script that prepares a MySQL server for the project. """
import mysql.connector

def setup_mysql_server():
    try:
	connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_root_password"
        )

	cursor = connection.cursor()

	cursor.execute("CREATE DATABASE IF NOT EXISTS hbnb_dev_db")

	cursor.execute("CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd'")
        cursor.execute("GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost'")
        cursor.execute("GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost'")

	connection.commit()

	cursor.close()
        connection.close()

        return True
	except mysql.connector.Error as error:
        print("Error: {}".format(error))
        return False

setup_result = setup_mysql_server()
print("Setup successful: {}".format(setup_result))

import mysql.connector

def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="cathycerine101",
            database="tickets"
        )
        if connection.is_connected():
            print()
            print("Welcome to Flight Explorer!")
            return connection
    except Exception as e:
        print("Error", e)
        return None

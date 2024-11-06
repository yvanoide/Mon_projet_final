import mysql.connector
from mysql.connector import Error
import pytest

def test_mysql_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="traducteur",
            password="traducteur",
            port="3307",
            database="traducteur",
            ssl_disabled=True  # Utilisez True si vous ne souhaitez pas utiliser SSL
        )
        assert conn.is_connected()  # Vérifie que la connexion est établie
    except Error as e:
        pytest.fail(f"Error connecting to MySQL: {e}")
    finally:
        if conn.is_connected():
            conn.close()  # Assurez-vous de fermer la connexion


import psycopg2
from psycopg2 import _psycopg
from pipeline03 import DATABASE_URL
# URL de conexão fornecida pelo Render
conn_string = "postgres://usuario:senha@host:porta/banco"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    # Execute suas consultas SQL aqui
    cursor.close()
    conn.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)







    






    
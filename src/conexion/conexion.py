import pyodbc

def conectar_db():
    try:
        conn = pyodbc.connect('DRIVER={SQL Server};'
                              'SERVER=DESKTOP-LMQB2J0\\SQLEXPRESS;'
                              'DATABASE=Banco;'
                              'Trusted_Connection=yes')
        return conn
    except pyodbc.Error as e:
        print("Error al conectar a la base de datos:")
        print(e)
        return None

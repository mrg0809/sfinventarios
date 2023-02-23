import mysql.connector
from mysql.connector import errorcode

class HandleDB():
    def __init__(self):
        self._con = mysql.connector.connect(user='admin',
                                            password='RMs1stemas',
                                            host='ofandb.ctnnbczca24z.us-east-1.rds.amazonaws.com',
                                            database='ofandb' )
        self._cur = self._con.cursor()


    def get_users(self):
        self._cur.execute("SELECT * FROM usuarios")
        data = self._cur.fetchall()
        return data

    def get_user(self, data_user):
        self._cur.execute("SELECT * FROM usuarios WHERE correo = '{}'".format(data_user))
        data = self._cur.fetchone()
        return data

    def get_ean_model(self, ean):
        self._cur.execute("SELECT Modelo FROM existencias WHERE EAN = '{}'".format(ean))
        data = self._cur.fetchone()
        return data
    
    def get_existencias(self, model):
        self._cur.execute("SELECT Tienda, Existencia, Talla FROM existencias WHERE Modelo = '{}' ORDER BY Talla".format(model))
        data = self._cur.fetchall()
        return data

    def __del__(self):
        self._con.close()


db = HandleDB()
print(db.get_existencias('TPCN3428'))
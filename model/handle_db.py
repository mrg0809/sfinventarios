import mysql.connector
from mysql.connector import errorcode
import pandas as pd

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
        self._cur.execute("SELECT Tienda, Talla, Existencia FROM existencias WHERE Modelo = '{}'".format(model))
        data = self._cur.fetchall()
        return data

    def __del__(self):
        self._con.close()


db = HandleDB()


df = pd.DataFrame(db.get_existencias('TPGW9250'))
df.columns=["TIENDA", "TALLA", "EXISTENCIA"]
df["EXISTENCIA"] = df["EXISTENCIA"].astype(float)

df2 = df.pivot(index="TIENDA", columns="TALLA", values="EXISTENCIA").fillna(0)
df2.loc['TOTAL',:] = df2.sum(axis=0)
df2.loc[:,'TOTAL'] = df2.sum(axis=1)

print(df2)
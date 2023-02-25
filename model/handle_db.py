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
        try:
            self._cur.execute("SELECT Modelo FROM existencias WHERE EAN = '{}'".format(ean))
            data = self._cur.fetchone()
            trash = self._cur.fetchall()
            return data
        except Exception as e:
            return 'NOT FOUND'
    
    
    def get_existencias(self, model):
        self._cur.execute("SELECT Tienda, Talla, Existencia FROM existencias WHERE Modelo = '{}'".format(model))
        data = self._cur.fetchall()
        return data

    def __del__(self):
        self._con.close()


db = HandleDB()


def tabla_existencias(modelo):
    if db.get_existencias(modelo) == []:
        modelo = db.get_ean_model(modelo)[0]
        print(modelo)

    try:
        df = pd.DataFrame(db.get_existencias(modelo))
        df.columns=["TIENDA", "TALLA", "EXISTENCIA"]
        df["EXISTENCIA"] = df["EXISTENCIA"].astype(float)
        df = df.pivot(index="TIENDA", columns="TALLA", values="EXISTENCIA").fillna(0)
        df.loc['TOTAL',:] = df.sum(axis=0)
        df.loc[:,'TOTAL'] = df.sum(axis=1)
        print(df)
        return df
    except Exception as e:
        return 'NOT FOUND'
    
tabla_existencias('TPGW9250')



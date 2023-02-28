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
    
    def get_model_data(self, model):
        self._cur.execute("SELECT Descripcion, Precio, Descuento, Linea, Marca, Subcategoria FROM existencias WHERE Modelo = '{}' LIMIT 1".format(model))
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
        return df
    except Exception as e:
        return 'NOT FOUND'
    

def get_model_data(modelo):
    query = db.get_model_data(modelo)
    precio = round(float(query[0][1])*1.16)
    descuento = float(query[0][2])
    precio_tienda = precio
    if descuento > 0:
        precio_tienda = precio*(100-descuento)/100
    data = {'descripcion': query[0][0], 'precio': precio, 'descuento': round(descuento, 2), 'precio_tienda': round(precio_tienda), 'linea': query[0][3], 'marca': query[0][4], 'subcategoria' :query[0][5]}
    return data


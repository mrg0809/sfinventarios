import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import numpy as np

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
        self._cur.execute("SELECT Tienda, Talla, Existencia FROM existencias WHERE Modelo = '{}' AND Tienda IN {}".format(model, tiendastransito))
        data = self._cur.fetchall()
        return data
    
    def get_model_data(self, model):
        self._cur.execute("SELECT Descripcion, Precio, Descuento, Linea, Marca, Subcategoria FROM existencias WHERE Modelo = '{}' LIMIT 1".format(model))
        data = self._cur.fetchall()
        return data
    
    def get_model_sales(self, model):
        self._cur.execute("SELECT Tienda, SUM(Unidades) FROM ventas WHERE Fecha >= (curdate()-interval 1 month) AND Modelo='{}' GROUP BY Tienda ORDER BY Tienda".format(model))
        data = self._cur.fetchall()
        return data
    
    def get_cost(self, model):
        self._cur.execute("SELECT AVG(Costo) FROM ventas where Modelo='{}'".format(model))
        cost = self._cur.fetchone()
        return cost
    
    def get_best_model_sales(self, store, fecha1, fecha2):
        if store == 'GENERAL':
            self._cur.execute("SELECT Modelo, Descripcion, SUM(Unidades) FROM ofandb.ventas WHERE Fecha BETWEEN '{}' AND '{}' group by Modelo order by sum(Unidades) desc limit 50;".format(fecha1, fecha2))
            bettermodels = self._cur.fetchall()
            return bettermodels
        self._cur.execute("SELECT Modelo, Descripcion, SUM(Unidades) FROM ofandb.ventas WHERE Fecha BETWEEN '{}' AND '{}' AND Tienda = '{}' group by Modelo order by sum(Unidades) desc limit 25;".format(fecha1, fecha2, store))
        bettermodels = self._cur.fetchall()
        return bettermodels
    
    def get_best_size_sales(self):
        self._cur.execute("SELECT Talla, SUM(Unidades) FROM ofandb.ventas WHERE Fecha >= (curdate()-interval 1 month) group by Modelo order by sum(Unidades) desc limit 10;")
        bettersizes = self._cur.fetchall()
        return bettersizes
    
    def get_five_model_sales(self):
        self._cur.execute("SELECT Modelo, SUM(Unidades) FROM ofandb.ventas WHERE Fecha >= (curdate()-interval 7 day) group by Modelo order by sum(Unidades) desc limit 5;")
        betterfive = self._cur.fetchall()
        return betterfive
    
    def get_max_inventory_model(self):
        self._cur.execute("SELECT Modelo, SUM(Existencia) FROM ofandb.existencias group by Modelo order by sum(Existencia) desc limit 10;")
        maxinventory = self._cur.fetchall()
        return maxinventory
    
    def get_better_discount(self):
        self._cur.execute("SELECT Modelo, Descuento FROM ofandb.existencias WHERE Existencia > 5 group by Modelo order by Descuento desc limit 10;")
        better_discount = self._cur.fetchall()
        return better_discount

    def __del__(self):
        self._con.close()


db = HandleDB()

tiendastransito = ( '1101 BODEGA TIJUANA SPORTS FAN',
                    '1102 TRANSITO BODEGA TIJUANA SPORTSFAN',
                    '1203 RIO 3',
                    '1204 TRANSITO RIO 3',
                    '1205 MACROPLAZA',
                    '1206 TRANSITO MACROPLAZA',
                    '1207 MACROPLAZA 2',
                    '1208 TRANSITO MACROPLAZA 2',
                    '1211 PALMAS',
                    '1212 TRANSITO PALMAS',
                    '1213 SENDEROS TIJUANA I EVF',
                    '1214 TRANSITO SENDEROS TIJUANA',
                    '1215 SENDEROS TIJUANA II SPF',
                    '1216 TRANSITO SENDEROS TIJUANA 2',
                    '1219 MEXICALI 1',
                    '1220 TRANSITO MEXICALI 1',
                    '1221 MEXICALI 2',
                    '1222 TRANSITO MEXICALI 2',
                    '1225 ENSENADA 1',
                    '1226 TRANSITO ENSENADA 1',
                    '1227 ENSENADA 2',
                    '1228 TRANSITO ENSENADA 2',
                    '1229 ENSENADA 3',
                    '1230 TRANSITO ENSENADA 3',
                    '4203 FLORIDA 22 CDMX',
                    '4204 TRANSITO FLORIDA 22 CDMX')

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
        df.loc[:,'T'] = df.sum(axis=1)
        df2 = df.astype(np.int64)
        return df2
    except Exception as e:
        df = pd.DataFrame()
        return df
    

def get_model_data(modelo):
    query = db.get_model_data(modelo)
    costoq = db.get_cost(modelo)
    if type(costoq[0]) == int or type(costoq[0]) == float:
        costo = round(costoq[0], 2)
    else:
        costo = 0    
    precio = round(float(query[0][1])*1.16)
    descuento = float(query[0][2])
    precio_tienda = precio
    if descuento > 0:
        precio_tienda = precio*(100-descuento)/100
    data = {'descripcion': query[0][0], 'precio': precio, 'descuento': round(descuento, 2), 'precio_tienda': round(precio_tienda), 'linea': query[0][3], 'marca': query[0][4], 'subcategoria' :query[0][5], 'costo':costo}
    return data


def get_model_sales(modelo):
    df = pd.DataFrame(db.get_model_sales(modelo))
    try:
        df.columns=["TIENDA", "VENTA"]
        df['VENTA'] = df['VENTA'].astype(np.int64)
        df.loc['TOTAL'] = ["TOTAL", df["VENTA"].sum(axis=0, numeric_only=True)]
        return df
    except:
        return df    


def get_better_models(tienda, fecha1, fecha2):
    df = pd.DataFrame(db.get_best_model_sales(tienda, fecha1, fecha2))
    df.columns=["MODELO", "DESCRIPCION", "VENTA"]
    df['VENTA'] = df['VENTA'].astype(np.int64)
    return df

def dashboard_data():
    five_model_sales = db.get_five_model_sales()
    max_inventory_model = db.get_max_inventory_model()
    better_sizes = db.get_best_size_sales()
    better_discounts = db.get_better_discount()
    return {'betterfive': five_model_sales, 'maxinventory': max_inventory_model, 'bettersizes': better_sizes, "betterdiscounts": better_discounts}
import firebirdsql
from datetime import datetime

"""Datos para conexion a base de datos remota"""
con = firebirdsql.connect(
    host='sfan.ddns.net',
    database='C:\Microsip datos\SPORTS FAN 2016.FDB',
    port=2000,
    user='SYSDBA',
    password='flexracer',
    timeout=20,
    charset='WIN1251'
)

def consultaVentaTiendaHoy():
    try:
        cur =  con.cursor()
        fecha = datetime.today().strftime('%d.%m.%Y')
        par = [fecha, fecha, 0, 'N', 0, 'a', 3, 'S', 0]
        cur.execute("select NOMBRE, VENTA_IMPORTE from VENTA_DESGL_PER(?, ?, ?, ?, ?, ?, ?, ?, ?)", (par))
        ventashoy =  cur.fetchall()
    except:
        print('ERROR')
        cur.close()
        con.close()
        ventashoy = 'ERROR'
    return ventashoy
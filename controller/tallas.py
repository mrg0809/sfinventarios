from model.handle_db import HandleDB
import pandas as pd

db = HandleDB()

def get_existencias(modelo):
    df = pd.DataFrame(db.get_existencias(modelo))
    df.columns=["TIENDA", "TALLA", "EXISTENCIA"]
    df["EXISTENCIA"] = df["EXISTENCIA"].astype(float)
    df2 = df.pivot(index="TIENDA", columns="TALLA", values="EXISTENCIA").fillna(0)
    df2.loc['TOTAL',:] = df2.sum(axis=0)
    df2.loc[:,'TOTAL'] = df2.sum(axis=1)
    return df2

get_existencias('TPGW9250')
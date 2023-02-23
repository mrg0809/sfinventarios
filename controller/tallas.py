from model.handle_db import HandleDB
import pandas as pd


db = HandleDB()

consulta = ''

df = pd.DataFrame(db.get_existencias('TPGW9250'))

print(df)
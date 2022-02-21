
import pandas as pd
import os
from fundamentals.config import config

from sqlalchemy import create_engine

os.chdir(os.path.dirname(os.path.realpath(__file__)))
engine = create_engine(
    f"postgresql+psycopg2://postgres:{config('../users.ini', 'postgres', 'password')}@localhost/pokemon")

df = pd.read_csv('/strength_weakness.csv')

df = pd.melt(df,id_vars='atk',var_name='def',value_name='multiplier', ignore_index=True)
df = df.apply(lambda x: x.astype(str).str.lower())

df.to_sql('strength_weakness',schema='mart',con=engine,if_exists='append',index= False)

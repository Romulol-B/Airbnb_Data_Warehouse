import pandas as pd
from db.utils import *
import os
from dotenv import load_dotenv
import sys

load_dotenv()

usuario = os.getenv('usuario')
senha = os.getenv('senha')
host = os.getenv('host')
porta = os.getenv('porta')
nome_do_banco = os.getenv('nome_do_banco')


def exec_query(query):
    engine = get_db_engine(usuario,senha,host,porta,nome_do_banco)
    df = pd.read_sql(query,engine)

    return df
        
    
if len(sys.argv) <= 1:
    print('Query não encontrada')
    exit(0)

if not os.path.exists('../data/consultas'): os.mkdir('../data/consultas')

for filename in sys.argv[1:]:
    print("executando query", filename)

    with open(f'consultas/{filename}') as f:
        query = f.read()
        df = exec_query(query)
        df.to_csv(f'../data/consultas/{filename[:-4]}_resultado.csv',index=False)



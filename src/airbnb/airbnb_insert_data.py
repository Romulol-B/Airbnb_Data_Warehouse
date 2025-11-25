# %%
from sqlalchemy import create_engine
from dotenv import load_dotenv
import psycopg2
import os

import pandas as pd

load_dotenv()

usuario = os.getenv('usuario')
senha = os.getenv('senha')
host = os.getenv('host')
porta = os.getenv('porta')
nome_do_banco = os.getenv('nome_do_banco')

def create_database(usuario, senha, host, porta):
    conn = psycopg2.connect(user=usuario, password=senha, host=host, port=porta)

    conn.autocommit = True
    cursor = conn.cursor()

    try:
        cursor.execute(f"CREATE DATABASE {nome_do_banco};")
        print(f"Banco de dados '{nome_do_banco}' criado com sucesso.")
    except psycopg2.errors.DuplicateDatabase:
        print(f"O banco de dados '{nome_do_banco}' já existe.")

    cursor.close()
    conn.close()

def db_engine(usuario, senha, host, porta):
    url_conexao = f'postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{nome_do_banco}'
    return create_engine(url_conexao)

def insert_data(engine):
    root_path = os.path.abspath('../..')

    listings_path = root_path + '/data/airbnb-scrap/listings'
    
    for filename in os.listdir(listings_path):
        df = pd.read_csv(listings_path + f'/{filename}')

        #-----------------------#
        return df
    
def get_dates_df(start = '2010-01-01', end='2025-12-31'):
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    #import holidays

    # Gerando todas as datas de 2010
    datas = pd.date_range(start, end)

    # Criando um DataFrame
    df = pd.DataFrame(datas, columns=['data_completa'])

    # Extraindo o ano, mês, dia e dia da semana
    df['ano'] = df['data_completa'].dt.year
    df['mes'] = df['data_completa'].dt.month
    df['dia'] = df['data_completa'].dt.day
    df['dia_da_semana'] = df['data_completa'].dt.day_name()

    # Extraindo o trimestre e semestre
    df['trimestre'] = df['data_completa'].dt.quarter
    df['semestre'] = (df['mes'] - 1) // 6 + 1

    # Criando as colunas booleanas para feriado e fim de semana
    #br_holidays = holidays.Brazil(years=2010)
    #df['feriado'] = df['data_completa'].isin(br_holidays)
    df['fim_de_semana'] = df['data_completa'].dt.dayofweek >= 5  # Sábado e Domingo

    # Exibindo o DataFrames
    return df


# %%
df = insert_data('')
# %%
df.columns
# %%

df_imovel = df[['id','property_type','room_type','beds','bathrooms','bedrooms','latitude','longitude']]
df_imovel = df_imovel.drop_duplicates()
# %%
df_anfitriao = df [['host_id','host_name','host_since','host_location','host_is_superhost','host_response_rate','host_acceptance_rate']]
df_anfitriao = df_anfitriao.drop_duplicates()

# %%
df_datas = get_dates_df()


# %%

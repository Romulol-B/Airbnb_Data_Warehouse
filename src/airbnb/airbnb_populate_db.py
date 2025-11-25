# %%
from dotenv import load_dotenv
import os
from faker import Faker
import random

import pandas as pd

load_dotenv()

usuario = os.getenv('usuario')
senha = os.getenv('senha')
host = os.getenv('host')
porta = os.getenv('porta')
nome_do_banco = os.getenv('nome_do_banco')

relative_path = '../'



def read_data(filename = 'listings'):
    root_path = os.path.abspath(relative_path)

    listings_path = root_path + '/data/airbnb-scrap/' + filename
    
    for filename in os.listdir(listings_path):
        df = pd.read_csv(listings_path + f'/{filename}')
        break

    return df
    
def get_dates_df(start = '2010-01-01', end='2025-12-31'):

    datas = pd.date_range(start, end)

    df = pd.DataFrame(datas, columns=['data_completa'])

    df['ano'] = df['data_completa'].dt.year
    df['mes'] = df['data_completa'].dt.month
    df['dia'] = df['data_completa'].dt.day
    df['dia_da_semana'] = df['data_completa'].dt.day_name()

    df['trimestre'] = df['data_completa'].dt.quarter
    df['semestre'] = (df['mes'] - 1) // 6 + 1

    df['fim_de_semana'] = df['data_completa'].dt.dayofweek >= 5  # Sábado e Domingo

    return df

def generate_users_data(df,save = True):
    fake = Faker()

    countries = ['Brasil', 'Argentina', 'Portugal', 'Estados Unidos', 'Alemanha']
    genders = ['Masculino','Feminino']

    df['nome'] = df['reviewer_name'].apply(lambda x: f'{x} {fake.last_name()}')
    df['idade'] = df.apply(lambda x: random.randint(18, 60), axis=1)
    df['sexo'] = df.apply(lambda x: random.choice(genders), axis=1)
    df['pais_origem'] = df.apply(lambda x: random.choice(countries), axis=1)

    if save:
        df.to_csv(relative_path + 'data/airbnb-scrap/usuarios.csv')
    
    return df


# %%
# df_listings = read_data('listings')

# df_imovel = df_listings[['id','property_type','room_type','beds','bathrooms','bedrooms','latitude','longitude']]
# df_imovel = df_imovel.drop_duplicates()

# df_anfitriao = df_listings [['host_id','host_name','host_since','host_location','host_is_superhost','host_response_rate','host_acceptance_rate']]
# df_anfitriao = df_anfitriao.drop_duplicates()

# df_datas = get_dates_df()

# df_reviews = read_data('reviews')

# df_reviews_uniq = df_reviews[['reviewer_id','reviewer_name']]
# df_reviews_uniq = df_reviews_uniq.drop_duplicates()

# df_usuarios = pd.read_csv(relative_path + 'data/airbnb-scrap/usuarios.csv')

# %%
from db.utils import get_db_engine

engine = get_db_engine(usuario,senha,host,porta,nome_do_banco)
print(engine)
# %%

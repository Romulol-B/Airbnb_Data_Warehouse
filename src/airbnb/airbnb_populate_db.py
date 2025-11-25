# %%
from dotenv import load_dotenv
import os
from faker import Faker
import random
from db.utils import *

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
    
    df_final = None
    for filename in os.listdir(listings_path):
        df = pd.read_csv(listings_path + f'/{filename}')

        if df_final: df_final = df
        else:
            df_final = pd.concat([df_final, df], ignore_index=True)

    return df_final
    
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

def create_dimensions_tables(df_listings,df_reviews,df_locations,df_datas,engine):
    df_imovel = df_listings[['id','sk_imovel','property_type','room_type','beds','bathrooms','bedrooms']]

    df_anfitriao = df_listings [['host_id','host_name','host_since','host_location','host_is_superhost','host_response_rate','host_acceptance_rate']]
    df_anfitriao = df_anfitriao.drop_duplicates()
    df_anfitriao = df_anfitriao.reset_index(drop=True)
    df_anfitriao['sk_anfitriao'] = df_anfitriao.index + 1

    df_reviews_uniq = df_reviews[['reviewer_id','reviewer_name']]
    df_reviews_uniq = df_reviews_uniq.drop_duplicates()

    if os.path.exists(relative_path + 'data/airbnb-scrap/usuarios.csv'):
        df_usuarios = pd.read_csv(relative_path + 'data/airbnb-scrap/usuarios.csv')
    else:
        df_usuarios = generate_users_data(df_reviews_uniq)
    
    df_usuarios = df_usuarios.reset_index(drop=True)
    df_usuarios['sk_usuario'] = df_usuarios.index + 1

    

    df_dim_locations = df_locations.drop(columns=['id_imovel'])

    insertions = [
        (df_imovel,'dim_imoveis'),
        (df_anfitriao,'dim_anfitriao'),
        (df_datas,'dim_data'),
        (df_usuarios,'dim_usuarios'),
        (df_dim_locations,'dim_localizacao')
    ]

    for df,table in insertions:
        df_to_postgres(df,engine,table)


def create_fact_tables(df_listings,df_reviews,df_locations,df_datas,engine):

    # --------------FATO AVALIACAO----------------
    scores_columns_map = {
        'review_scores_rating': 'nota_media',
        'review_scores_cleanliness': 'nota_limpeza',
        'review_scores_communication': 'nota_comunicacao',
        'review_scores_value': 'nota_custo_beneficio'
    }

    df_listings = df_listings.rename(columns=scores_columns_map)

    scores_columns = list(scores_columns_map.values())


    for c in scores_columns:
        df_listings[c] = df_listings[c].fillna(df_listings[c].astype(float).mean())



    df_anfitriao = df_listings [['host_id','host_name','host_since','host_location','host_is_superhost','host_response_rate','host_acceptance_rate']]
    df_anfitriao = df_anfitriao.drop_duplicates()
    df_anfitriao = df_anfitriao.reset_index(drop=True)
    df_anfitriao['sk_anfitriao'] = df_anfitriao.index + 1

    df_listings = df_listings.rename(columns={'id':'id_imovel'})

    df_imovel_anfitriao = df_listings.merge(df_anfitriao,on='host_id')

    df_fato_avaliacao = df_imovel_anfitriao[['sk_imovel','sk_anfitriao'] + scores_columns]

    # --------------FATO RESERVAS ----------------

    df_reviews_uniq = df_reviews[['reviewer_id','reviewer_name']]
    df_reviews_uniq = df_reviews_uniq.drop_duplicates()

    if os.path.exists(relative_path + 'data/airbnb-scrap/usuarios.csv'):
        df_usuarios = pd.read_csv(relative_path + 'data/airbnb-scrap/usuarios.csv')
    else:
        df_usuarios = generate_users_data(df_reviews_uniq)
    
    df_usuarios = df_usuarios.reset_index(drop=True)
    df_usuarios['sk_locador'] = df_usuarios.index + 1

    df_reviews = df_reviews.rename(columns={'listing_id':'id_imovel'})

    df_imovel_localizacao = df_imovel_anfitriao.merge(df_locations,on='id_imovel')


    df_review_imovel = df_reviews.merge(df_imovel_localizacao,on='id_imovel')

    df_fato_locacao = df_review_imovel.merge(df_usuarios,on='reviewer_id')


    df_fato_locacao['price'] = df_fato_locacao['price'].str.replace('$','').str.replace(',','').astype(float)
    df_fato_locacao = df_fato_locacao.rename(columns={'price':'preco','date':'data_completa'})

    df_datas["data_completa"] = pd.to_datetime(df_datas["data_completa"])
    df_fato_locacao["data_completa"] = pd.to_datetime(df_fato_locacao["data_completa"])

    df_final = df_datas.merge(df_fato_locacao,on='data_completa')

    df_fato_locacao = df_final[['sk_imovel','sk_anfitriao','sk_locador','sk_localizacao','sk_data','preco']].copy()
    df_fato_locacao['preco'] = df_fato_locacao['preco'].fillna(df_fato_locacao['preco'].mean())

    # Criar tabelas
    df_to_postgres(df_fato_avaliacao,engine,'fato_avaliacao')
    df_to_postgres(df_fato_locacao,engine,'fato_reservas')

    



if __name__ == '__main__':
    create_database(usuario,senha,host,porta,nome_do_banco)
    engine = get_db_engine(usuario,senha,host,porta,nome_do_banco)

    # Leitura do listings e tratamento de valores faltantes
    df_listings = read_data('listings')
    df_listings['host_location'] = df_listings['host_location'].fillna('Rio de Janeiro, Brazil')

    df_listings['host_acceptance_rate'] = (
        df_listings['host_acceptance_rate']
        .str.replace('%', '', regex=False) 
        .astype(float)                      
    )

    df_listings['host_response_rate'] = (
        df_listings['host_response_rate']
        .str.replace('%', '', regex=False)   
        .astype(float)                       
    )

    df_listings['host_response_rate'] = df_listings['host_response_rate'].fillna(df_listings['host_response_rate'].mean())
    df_listings['host_acceptance_rate'] = df_listings['host_acceptance_rate'].fillna(df_listings['host_acceptance_rate'].mean())

    df_listings = df_listings.reset_index(drop=True)
    df_listings['sk_imovel'] = df_listings.index + 1

    # Leitura do reviews e tratamento de valores faltantes
    df_reviews = read_data('reviews')


    df_locations = read_data('locations')
    df_locations = df_locations.reset_index(drop=True)
    df_locations['sk_localizacao'] = df_locations.index + 1
    
    df_datas = get_dates_df()
    df_datas = df_datas.reset_index(drop=True)
    df_datas['sk_data'] = df_datas.index + 1

    # Salvar no banco
    df_to_postgres(df_listings,engine,'listings')
    print('listings salvo')

    df_to_postgres(df_reviews,engine,'reviews')
    print('reviews salvo')

    # Criar tabelas de dimensões
    print('Criando tabelas de dimensão')
    create_dimensions_tables(df_listings, df_reviews,df_locations,df_datas, engine)

    print('Criando tabelas fato')
    create_fact_tables(df_listings, df_reviews,df_locations,df_datas, engine)

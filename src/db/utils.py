import psycopg2
from sqlalchemy import create_engine

def create_database(usuario, senha, host, porta,nome_do_banco):
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

def get_db_engine(usuario, senha, host, porta,nome_do_banco):
    url_conexao = f'postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{nome_do_banco}'
    return create_engine(url_conexao)

def df_to_postgres(df,engine,table):
    df.to_sql(table, con=engine, if_exists='replace', index=False)
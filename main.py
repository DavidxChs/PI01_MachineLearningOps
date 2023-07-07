import pandas as pd
from fastapi import FastAPI
from datetime import datetime

df = pd.read_excel('Dataset/movies.xlsx')
df['release_date'] = pd.to_datetime(df.release_date)
df['production_countries'].fillna('', inplace = True)
df['production_companies'].fillna('', inplace = True)

app = FastAPI()

@app.get('/peliculas_idioma/{Idioma}')
def peliculas_idioma(Idioma: str):
    # Creo una lista con todos los idiomas en los que fueron producidas las películas
    idiomaslist = df['original_language'].unique().tolist()
    if (Idioma in idiomaslist):
        mask = df['original_language'] == Idioma
        return f'{df[mask].shape[0]} cantidad de películas fueron estrenadas en {Idioma}'
    else:
        return 'Se ingresó un idioma que no se encuentra en ninguna película'
    
@app.get('/peliculas_duracion/{Pelicula}')
def peliculas_duracion(Pelicula: str):
    mask = df['title'].str.lower() == Pelicula.lower()
    duracion = df[mask]['runtime'].to_list()[0]
    año = df[mask]['release_year'].to_list()[0]
    return f'{Pelicula.capitalize()}. Duración: {duracion}. Año: {año}'

@app.get('/franquicia/{Franquicia}')
def franquicia(Franquicia: str):
    collection = Franquicia.replace(' Collection', '')
    mask = df['belongs_to_collection'].str.lower() == Franquicia.lower()
    cantidad = df[mask].shape[0]
    g_promedio = round(df[mask]['revenue'].mean(), 2)
    g_total = round(df[mask]['revenue'].sum(), 2)
    respuesta = f'La franquicia {collection} posee {cantidad} peliculas, una ganancia total de {g_total} y una ganancia promedio de {g_promedio}'
    return respuesta

@app.get('/peliculas_pais/{Pais}')
def peliculas_pais(Pais: str):
    contador = 0
    for item in df['production_countries']:
        if Pais in item:
            contador += 1
    return f'Se produjeron {contador} películas en el país {Pais}'

@app.get('/productoras_exitosas/{Productora}')
def productoras_exitosas(Productora: str):
    productoraList = []
    for item in df['production_companies']:
        if Productora in item:
            productoraList.append(True)
        else:
            productoraList.append(False)
    revenue = df[productoraList]['revenue'].sum()
    peliculas = df[productoraList].shape[0]
    return f'La productora {Productora} ha tenido un revenue de {revenue} y ha realizado en total {peliculas} películas'

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director):
    mask = df['director'] == nombre_director
    exito = df[mask]['return'].sum()
    peliculas = df[mask]['title'].to_list()
    fecha = df[mask]['release_date'].to_list()
    retorno = df[mask]['return'].to_list()
    costo = df[mask]['budget'].to_list()
    ganancia = df[mask]['revenue'].to_list()
    respuesta = {'director' : nombre_director, 'retorno_total_director' : exito, 
                 'peliculas' : peliculas, 'fecha' : fecha, 'retorno_pelicula' : retorno, 
                 'budget_pelicula' : costo, 'revenue_pelicula' : ganancia}
    return respuesta

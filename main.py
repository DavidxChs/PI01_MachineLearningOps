import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
from scipy.sparse import hstack
from fastapi import FastAPI

df = pd.read_excel('Dataset/movies.xlsx')
df['production_countries'].fillna('', inplace = True)
df['production_companies'].fillna('', inplace = True)

app = FastAPI()

@app.get('/peliculas_idioma/{Idioma}')
def peliculas_idioma(Idioma: str):
    # Creo una lista con todos los idiomas en los que fueron producidas las películas
    idiomaslist = df['original_language'].str.lower().unique().tolist()
    if (Idioma.lower() in idiomaslist):
        mask = df['original_language'].str.lower() == Idioma.lower()
        return f'{df[mask].shape[0]} cantidad de películas fueron estrenadas en {Idioma.lower()}'
    else:
        return 'Se ingresó un idioma que no se encuentra en ninguna película'
    
@app.get('/peliculas_duracion/{Pelicula}')
def peliculas_duracion(Pelicula: str):
    peliculaslist = df['title'].str.lower().unique().tolist()
    if (Pelicula.lower() in peliculaslist):
        mask = df['title'].str.lower() == Pelicula.lower()
        duracion = df[mask]['runtime'].to_list()[0]
        año = df[mask]['release_year'].to_list()[0]
        return f'{Pelicula.capitalize()}. Duración: {duracion}. Año: {año}'
    else:
        return 'El nombre o título de esa película no existe'

@app.get('/franquicia/{Franquicia}')
def franquicia(Franquicia: str):
    franquiciaslist = df['belongs_to_collection'].str.lower().unique().tolist()
    if (Franquicia.lower() in franquiciaslist):
        mask = df['belongs_to_collection'].str.lower() == Franquicia.lower()
        cantidad = df[mask].shape[0]
        g_promedio = round(df[mask]['revenue'].mean(), 2)
        g_total = round(df[mask]['revenue'].sum(), 2)
        respuesta = f'La franquicia {Franquicia.capitalize()} posee {cantidad} peliculas, una ganancia total de {g_total} y una ganancia promedio de {g_promedio}'
        return respuesta
    else:
        return 'La franquicia que fue ingresada no existe'

@app.get('/peliculas_pais/{Pais}')
def peliculas_pais(Pais: str):
    paiseslist = df['production_countries'].str.lower().unique().tolist()
    if (Pais.lower() in paiseslist):
        contador = 0
        for item in df['production_countries']:
            if Pais in item:
                contador += 1
        return f'Se produjeron {contador} películas en el país {Pais.capitalize()}'
    else:
        return 'El país ingresado no existe'

@app.get('/productoras_exitosas/{Productora}')
def productoras_exitosas(Productora: str):
    listproductoras = df['production_companies'].str.lower().unique().tolist()
    if (Productora.lower() in listproductoras):
        productoraList = []
        for item in df['production_companies']:
            if Productora in item:
                productoraList.append(True)
            else:
                productoraList.append(False)
        revenue = df[productoraList]['revenue'].sum()
        peliculas = df[productoraList].shape[0]
        return f'La productora {Productora.capitalize()} ha tenido un revenue de {revenue} y ha realizado en total {peliculas} películas'
    else:
        return 'No existen productoras con el nombre que se ha ingresado'

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director):
    directoreslist = df['director'].str.lower().unique().tolist()
    if (nombre_director.lower() in directoreslist):
        mask = df['director'].str.lower() == nombre_director.lower()
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
    else:
        return 'No existe un director con ese nombre'

@app.get('/recomendacion/{recomendacion}')
def recomendacion(titulo):
    titloslist = df['title'].str.lower().unique().tolist()
    if (titulo.lower() in titloslist):
        # Creo un nuevo dataset, con los datos que considero importantes para el sistema de recomendación
        ndf = df[['title','genres', 'original_language', 'popularity']]
        # Defino la fila que contiene el tpitulo de la película seleccionada
        fila_especial = ndf[ndf['title'].str.lower() == titulo.lower()]
        # Tomo una muestra aleatoria de las filas del dataframe para evitar problemas de memoria
        ndf = ndf.sample(frac = 0.2)
        # Incluyo en este dataframe la fila que contiene el título de la película seleccionada
        ndf = pd.concat([fila_especial, ndf])
        # Reseteo lo indices en el dataframe "ndf"
        ndf = ndf.reset_index(drop = True)
        # Hago una lista de las columnas con datos categóricos y excluyo la lista de títulos
        texto = list(ndf.select_dtypes(include = ['object']).columns)
        texto.remove('title')
        # Pongo todos los datos categóricos en una sola columna
        ndf['text_data']= ndf[texto].apply(lambda i: ' '.join(i.dropna().astype(str)),axis=1)
        # Quito los signos de puntuación en los datos categóricos
        ndf['text_data'] = ndf['text_data'].str.translate(str.maketrans('', '', string.punctuation))
        # Con el texto, crear un vector para asignar un valor numérico a todas las palabras
        # En el vector paso a minúsculas todas las palabras y elimino las "stop words"
        vect = TfidfVectorizer(lowercase = True, stop_words = 'english')
        # Creo la matriz que contendrá los valores numéricos que corresponde a cada palabra
        vect_matrix = vect.fit_transform(ndf['text_data'])
        # Creo un nuevo dataframe con sólo los datos numéricos
        df_num = ndf.select_dtypes(include=['float64',"int64"])
        # Transformo los valores numéricos escalándolos a valores entre 0 y 1
        scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
        # Genero un nuevo dataframe con los valores escalados
        scdf = pd.DataFrame((scaler.fit_transform(df_num)))
        scdf.columns = df_num.columns
        # Incluyo las variables numéricas procesadas a la matriz de datos categóricos transformados a valores numéricos
        popularidad = scdf.popularity.values[:, None]
        matrix = hstack((vect_matrix, popularidad))
        # Uso la similitud coseno para ver qué elementos de la matriz tienen mayor similitud
        cos_sim = cosine_similarity(matrix, matrix)
        # Obtengo una lista que contiene los valores calculados con la similitud de coseno junto con su índice
        # El número cero "0" es el índice que pertenece a la película seleccionada
        lista_mejores = list(enumerate(cos_sim[1]))
        # Ordeno las películas con mejor puntaje calculado a partir de la similitud de coseno. De mayor a menor
        lista_mejores = sorted(lista_mejores, key = lambda i: i[1], reverse=True)
        # Selecciono solo las 5 mejores películas
        lista_mejores = lista_mejores[1:6]
        # Obtengo los índices de las mejores películas y después devuelvo la lista de mejores películas que se recomiendan
        indices_peliculas = [i[0] for i in lista_mejores]
        resultado = ndf['title'].iloc[indices_peliculas].values.tolist()
        return {'títulos' : resultado}
    else:
        return 'El nombre o título de esa película no existe'

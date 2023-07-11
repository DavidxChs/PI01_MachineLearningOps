# PI01_MachineLearningOps
Sistema de recomendación de películas
<br><br>
El trabajo realizado es asumiendo el rol de un Data Scientist que comienza a trabajar en una start-up que provee servicios de plataformas de streaming como Netfix, Paramount plus, Prime video, etc. Por lo anteriormente descrito, el objetivo de este proyecto es crear un modelo de ML que solucione el problema de agregar un **sistema de recomendación** a la plataforma de streaming de la start-up.<br>

## Organización de Ficheros y Carpetas
***
Los archivos más importantes en este proyecto son:
1. **Dataset**: Se cuenta con un conjunto de datos que puede ser descargado utilizando el siguiente enlace: [Descargar Dataset](https://drive.google.com/drive/folders/1UG3nGZz0x5D6HppEyPm-YbeVU6AdRNXF?usp=sharing).
2. **ETL Y EDA**: En la carpeta del repositorio llamada "*ETL y EDA*" se encuentran los archivos "*ETL.ipynb*" y "*EDA.ipynb*". Estos archivos contienen el proceso de extracción, transformación y carga de datos, así como el análisis exploratorio de los mismos.
    - **ETL.ipynb**: Este archivo de Jupyter Notebook contiene todas las instrucciones necesarias para ejecutar el proceso de ETL. Deberá ser colocado en la misma carpeta donde se haya colocado la carpeta descargada llamanda Dataset (Nota: En la misma carpeta, no adentro de la carpeta). Se recomienda ejecutar todas las instrucciones contenidas en este archivo.
    - **EDA.ipynb**: Ubicado en la misma carpeta que "*ETL.ipynb*", este archivo también es un Jupyter Notebook que se enfoca en el análisis exploratorio de los datos. Proporciona histogramas, diagramas y otras visualizaciones que ayudan a comprender mejor la información contenida en el dataset. Para que funcione correctamente, tambien tendra que se colocado el la misma carpeta donde está "*ETL.ipynb*".
3. **main.py**: Este archivo contiene funciones o endpoints que están disponibles en una API. Con este archivo realice un deployment, que se encuentra disponible en el siguiente enlace: [Render Deployment](https://pi01-machinelearningops.onrender.com/docs).<br><br>
Es importante destacar que, para asegurar el correcto funcionamiento, se debe asegurar que la carpeta donde se encuentren los archivos "*ETL.ipynb*", "*EDA.pynb*" y "*main.py*", también contenga la carpeta "*Dataset*" con los archivos descargados desde el enlace proporcionado previamente. De esta manera, se mantendrá la integridad y coherencia del proyecto.<br>

## ETL
***
En esta etapa, está el proceso de leer el dataset, transformarlo y generar uno nuevo con los mismos datos, pero más limpio.<br>
El dataset que lee el archivo "*ETL.ipynb*" se llama "*movies_dataset.csv*" y contiene los datos de las películas que provee la start-up.<br>
Las transformaciones que le hago a este dataset son:
- Desanidar las columnas que tienen datos anidados
- Le asigno el valor 0 al los campos **revenue** y **budget**
- Elimino los valores nulos del campo **release date**
- Pongo corectamente el formato de la fecha y creo una columna nueva llamada **release_year** donde se visualiza el año de estreno de cada película.
- Creo la columna retorno de inversión, llamada **return** a partir de los campos **revenue** y **budget**.
- Elimino columnas que no utilice para el proyecto y además agrego un dataset más al dataframe de pandas que tengo inicialmente en el archivo de Jupyter Notebook<br>

## EDA
***
En esta parte inicié el análisis exploratorio de los datos a partir del archivo que creé llamado *EDA.ipynb*. Aquí muestro histogramas y gráficas interesantes que ayudan a analisar y comprender mejor la información del dataset limpio. El cual está en la carpeta *Dataset_transformado* y se llama *movies.xlsx*. Este archivo lo puse en formato de Excel para que no ocupe tanta memoria en el repositori y lo pueda subir sin problemas.<br>

## API
***
Realice una API para disponibilizar de los datos, utilizando el framework **FastAPI**.<br>
Hice en python las siguientes funciones en el archivo *main.py* para los endpoints que se consumirán en la API:
- `def peliculas_idioma(Idioma: str)`: Se ingresa un idioma con el formato abreviado, tal cual como está escrito en el dataset, y devuelve la cantidad de películas producidas en ese idioma.
- `def peliculas_duracion(Pelicula: str)`: Se ingresa una película y devuelve la duración en minutos y el año e que fue estrenada.
- `def franquicia(Franquicia: str)`: Se ingresa la franquicia, retornando la cantidad de películas. la ganancia total y la ganancia promedio.
- `def peliculas_pais( Pais: str )`: Se ingresa un país y se devuelve la cantidad de películas producidas en el mismo.
- `def productoras_exitosas(Productora: str)`: 
- `def get_director(nombre_director)`: Se ingresa el nombre de un director que se encuentre adentro del dataset y se devuelve el retorno que ha tenido con sus películas, el nombre da cada película que ha dirijido, la fecha de lanzamiento, el retorno individual, costo y ganancia de la misma.
- `def recomendacion(titulo)`: Se ingresa el título de una película y devuelve 5 recomendaciones de películas, basado en la película ingresada inicialmente<br>

## Deployment
***
Con el archivo *main.py* hice un deployment usando render. Así las funciones de la API estrán disponibles publicamente.<br>
Si quieres ver como explico las funciones en el deploy, sigue este enlace de YouTube: [Video](https://www.youtube.com/watch?v=ggWeW7rcfVY)

## Sistema de Recomendación
***
El sistema de Recomendación está en la función `def recomendacion(titulo)` de la API, éste lo hice utilizando la librería de Scikit-Learn con la similitud de cosenos. Tomé los datos que yo consideré importantes en el dataset, y a partir de estos hice la similitud de coseno.<br>
Por problemas de memoria tuve que tomar una porción de aleatoria de los datos y a partir de este nuevo set de datos apliqué la similitud coseno para obtener las recomendaciones, es por esto que aunque se ingrese el mismo título en la función, ésta recomendará siempre películas nuevas.
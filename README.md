# PI01_MachineLearningOps
Sistema de recomendación de películas
<br><br>
El trabajo realizado es asumiendo el rol de un Data Scientist que comienza a trabajar en una start-up que provee servicios de plataformas de streaming como Netfix, Paramount plus, Prime video, etc. Por lo anteriormente descrito, el objetivo de este proyecto es crear un modelo de ML que solucione el problema de agregar un **sistema de recomendación** a la plataforma de streaming de la start-up.<br>

## Organización de Ficheros y Carpetas
***
Inicialmente se cuenta con un Dataset que puede ser descargado utilizando este [link](https://drive.google.com/drive/folders/1UG3nGZz0x5D6HppEyPm-YbeVU6AdRNXF?usp=drive_linken/ "DataSet")<br><br>
Los archivos *ETL.ipynb* y *EDA.ipynb* se encuentran el la carpeta del reposito llamada *ETL y EDA*.

- Primero se tienen que ejecutar todas las instruccciones que están el el archivo de jupyter notebook con nombre *ETL.ipynb*. En ese archivo está todo el proceso de cargar el dataset, transformarlo y generar uno nuevo que servirá posteriormente.
- **En la carpeta donde haya sido colocado el archivo ETL.ipynb, también tiene que estar la carpeta Dataset (carpeta con los archivos descargados en el link anterior)**.
- En la carpeta donde está el archivo *ETL.ipynb* se debe colocar el archivo *EDA.ipynb*. Este último contiene el análisis exploratorio de los datos, en el que se anexan histogramas y diagramas que ayudan a entender mejor la información del dataset.
- El archivo *main.py* contiene funciones o endpoints que están disponibles en una API
- Realice un deployment con los endpoints del archivo *main.py* el cualesta disponible en el siguiente link: [Render Deployment](https://pi01-machinelearningops.onrender.com/docs)<br>

## ETL
***
E
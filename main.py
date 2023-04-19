#FastAPI funciona en conjunto con otra librería que usa para ejecutar
# la aplicación: uvicorn[standard] (mumicorn o jeans )
# Para ejecutar script: uvicorn main:app -- reload
#FastAPI incluye OpenAI, un motor de gestión integrado.

from fastapi import FastAPI, status, Response
import pandas as pd
import json
import csv
from models import Iris,inputIris,IrisOutput

#Importamos librerías para la generación del modelo entrenado
import pickle
from model_generator import model_generator



MEDIA_ROOT = 'iris.csv'

#Creamos aplicación
app = FastAPI()



#Utilizamos decoradores como Flask.
#Declaramos diréctamente los métodos tras declarar app + URL
#Dentro de cada método, las funciones se delcararán como asíncronas.

@app.get('/')
async def test():
    return "Bienvenido a mi FastAPI"


#Método Get a la URL '/iris/'
@app.get('/iris/')
async def iris (response: Response):
    try:
        #Creamos dataframe con la información de Iris
        df = pd.read_csv(MEDIA_ROOT)
        data = df.to_json(orient='index')
        data = json.loads(data)
        return data
    except Exception as e:
        print('Error al cargar el csv: %s' %str(e))
        response.status_code = status.HTTP_404_NOT_FOUND
        return '404 Not_Found'


#Método Post para insertar un nuevo dato
#Añadimos el status code que se espera
#Para poder testear la app desde Swagger, es necesario enviar datos
#  bajo un modelo. Este modelo de datos lo declararemos en un archivo
#  aparte al que llamamos models.py

@app.post('/insertData',status_code=201) 
#Item recoje los datos de front, bajo modelo 'Iris'
async def insertData(item: Iris,response: Response):   
    try:
        with open(MEDIA_ROOT,'a',newline='') as file:
            #Nombres de los campos
            fieldnames = ['sepal_length','sepal_width','petal_length',
                          'petal_width','species']
            writer = csv.DictWriter(file,fieldnames=fieldnames)
            writer.writerow({'sepal_length': item.sepal_length,
                            'sepal_width': item.sepal_width,
                            'petal_length': item.petal_length,
                            'petal_width': item.petal_width,
                            'species': item.species,  
                            }) 
        return item
    
    except Exception as e: 
        print('Error al insertar datos en el csv: %s' %str(e))
        response.status_code = status.HTTP_404_NOT_FOUND
        return '404 Not_Found'

#Declaramos método PUT para actualizar los datos de la fila indicada 
# mediante índice  
@app.put('/updateData/{item_id}',status_code=201)
async def updateData(item_id:int, item:Iris, response:Response):
    try:
        #Para cuadrar que e id corresponda al id mostrado en GET
        item_id = item_id -1
        df = pd.read_csv(MEDIA_ROOT)
        df.loc[df.index[item_id],'sepal_length']= item.sepal_length
        df.loc[df.index[item_id],'sepal_width'] = item.sepal_width
        df.loc[df.index[item_id],'petal_length'] = item.petal_length
        df.loc[df.index[item_id],'petal_width'] = item.petal_width
        df.loc[df.index[item_id],'species'] = item.species
        
        #Convertir a csv:
        df.to_csv(MEDIA_ROOT,index=False)
        return {'item_id': item_id, **item.dict()} 
    
    except Exception as e: 
        print('Error al insertar datos en el csv: %s' %str(e))
        response.status_code = status.HTTP_404_NOT_FOUND
        return '404 Not_Found'   

 
#Declaramos el método delete para eliminar la fila que indiquemos 
# mediante índice.
@app.delete('/deleteData/{item_id}')
async def deleteData(item_id:int,response:Response):
    try:
        item_id = item_id -1
        df = pd.read_csv(MEDIA_ROOT)
        df.drop(df.index[item_id], inplace=True)

        df.to_csv(MEDIA_ROOT,index=False)
            
        return {'item_id': item_id, 'msg': 'Deleted'}

    except Exception as e: 
        print('Error al eliminar datos en el csv: %s' %str(e))
        response.status_code = status.HTTP_404_NOT_FOUND
        return '404 Not_Found'
   

@app.post('/predict')
async def predict (input:inputIris,response:Response):  
    try:
       
        # Generamos dataframe con pandas a raíz de los datos obtenidos por input, 
        # Es conveniente generar el dataframe con pandas, el cifrado 
        # binario proviene de un dataframe creado con pandas.

        X = pd.DataFrame({'sepal_length': [input.sepal_length],
                          'sepal_width': [input.sepal_width],
                          'petal_length': [input.petal_length],
                          'petal_width': [input.petal_width]})

        # Generamos archivo de pickle con el modelo SVC de entrenamiento
        #  que usaremos para predecir
        model_generator(MEDIA_ROOT=MEDIA_ROOT)

        # Abrimos el modelo
        with open ('modelo_svc.pkl','rb') as mod:

            # Cargamos modelo en formato binario en la variable model
            model = pickle.load(mod)

            # Realizamos predicción almacenada en variable
            y_pred = model.predict(X)

            # Retorna Predicción, convirtiendo y_pred en str.
            return IrisOutput(species=str(y_pred))
        

    except Exception as e: 
        print('Error al erealizar prediccion: %s' %str(e))
        response.status_code = status.HTTP_404_NOT_FOUND
        return '404 Not_Found' 


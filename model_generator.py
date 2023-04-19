import pickle
from sklearn.svm import SVC
import pandas as pd

def model_generator(MEDIA_ROOT):
    try:
        #Abrimos y generamos un archivo dataframe con pandas
        df = pd.read_csv(MEDIA_ROOT)

        #Definimos valores de eje X (labels) y eje y (target)
        X = df[['sepal_length','sepal_width',
                'petal_length','petal_width']]
        y = df[['species',]]

        #Creamos modelo SVC para predecir
        clf = SVC()
                
        #Entrenamos modelo con los datos
        clf.fit(X,y)

        with open('modelo_svc.pkl', 'wb') as f:
           s =  pickle.dump(clf, f)

        return 'Modelo Generado',s
    
    except Exception as e:
        print(f'Fallo en model_generator{e}')
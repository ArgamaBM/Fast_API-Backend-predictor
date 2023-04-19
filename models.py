#Aquí declararemos el modelo de los datos en forma de clase
#Para ello usaremos librería pydantic

#De esta forma, aseguramos que los datos que vengan 
# de front tengan un formato y puedan ser procesados 
# de manera adecuada.

from pydantic import BaseModel,validator

class Iris(BaseModel):
    sepal_length: float
    sepal_width:  float
    petal_length: float
    petal_width:  float
    species:      str

    #Se añaden validadores a la clase para asegurar que el dato 
    # introducido sea válido. Si el valor es válido, la función 
    # devolverá el dato tal cual sea introducido.
    @validator('species',pre=True,always=True)
    def must_be_str(cls, v):
        if not isinstance(v, str):
            raise ValueError('must be a str')
        return v.title()
    

    @validator('sepal_length','sepal_width','petal_length',
               'petal_width',pre=True,always=True)
    def must_be_int(cls, v):
        if not isinstance(v,float):
            raise ValueError ('must be int')
        return v
    

class inputIris(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    @validator('*',pre=True,always=True)
    def must_be_int(cls, v):
        if not isinstance(v,float):
            raise ValueError ('must be float (add .0 if int)')
        return v


class IrisOutput(BaseModel):
    species: str

    @validator('species',pre=True,always=True)
    def must_be_str(cls, v):
        if not isinstance(v, str):
            raise ValueError('must be a str')
        return v.title()    
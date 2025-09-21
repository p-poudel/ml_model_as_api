from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json

# additional imports for making API public using ngrok
import uvicorn
from pyngrok import ngrok
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio

app = FastAPI()

# configuring CORSMiddleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class model_input(BaseModel):
    Pregnancies : int
    Glucose : int
    BloodPressure : int
    SkinThickness :int
    Insulin : int
    BMI : float
    DiabetesPedigreeFunction : float
    Age : int


# loading the saved model
diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))

@app.post('/diabetes_prediction')
def diabetes_pred(input_parameters : model_input):

    input_data = input_parameters.model_dump_json()
    input_dict = json.loads(input_data)

    preg = input_dict['Pregnancies']
    glu = input_dict['Glucose']
    bp = input_dict['BloodPressure']
    skin = input_dict['SkinThickness']
    insulin = input_dict['Insulin']
    bmi = input_dict['BMI']
    dpf = input_dict['DiabetesPedigreeFunction']
    age = input_dict['Age']

    input_list = [preg,glu,bp,skin,insulin,bmi,dpf,age]
    prediction = diabetes_model.predict([input_list])

    if prediction[0] == 0:
        return 'The person is not Diabetic'
    else:
        return 'The person is Diabetic'
    
# making API publicly available

ngrok_tunnel = ngrok.connect('8000')
print('Public URL: ', ngrok_tunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app=app, port=8000)
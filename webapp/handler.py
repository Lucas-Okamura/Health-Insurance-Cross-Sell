import pickle
import pandas as pd
from flask import Flask, request, Response 
from healthinsurance.healthinsurance import HealthInsurance
import os

#loading model
with open('models/model_logistic_regression.pkl','rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

@app.route('/predict', methods = ['POST'])
def health_insurance_predict():
    test_json = request.get_json()
    print(test_json)
    
    if test_json: # there is data
        if isinstance( test_json, dict ): # unique example
            test_raw = pd.DataFrame( test_json, index=[0] )
            
        else: # multiple example
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys() )
            
        # Instantiate Rossmann class
        pipeline = HealthInsurance()
        
        # feature engineering
        df1 = pipeline.feature_engineering( test_raw )
        
        # data preparation
        df2 = pipeline.data_preparation( df1 )
        
        # prediction
        df_response = pipeline.get_prediction( model, test_raw, df2 )
        
        return df_response
    
    else:
        return Response( '{}', status=200, mimetype='application/json' )
    
if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run( host = "0.0.0.0", port = port )
"""

    Helper functions for the pretrained model to be used within our API.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Plase follow the instructions provided within the README.md file
    located within this directory for guidance on how to use this script
    correctly.

    Importantly, you will need to modify this file by adding
    your own data preprocessing steps within the `_preprocess_data()`
    function.
    ----------------------------------------------------------------------

    Description: This file contains several functions used to abstract aspects
    of model interaction within the API. This includes loading a model from
    file, data preprocessing, and model prediction.  

"""

# Helper Dependencies
import numpy as np
import pandas as pd
import pickle
import json
import datetime

def _preprocess_data(data):
    """Private helper function to preprocess data for model prediction.

    NB: If you have utilised feature engineering/selection in order to create
    your final model you will need to define the code here.


    Parameters
    ----------
    data : str
        The data payload received within POST requests sent to our API.

    Returns
    -------
    Pandas DataFrame : <class 'pandas.core.frame.DataFrame'>
        The preprocessed data, ready to be used our model for prediction.

    """
    # Convert the json string to a python dictionary object
    feature_vector_dict = json.loads(data)
    # Load the dictionary as a Pandas DataFrame.
    feature_vector_df = pd.DataFrame.from_dict([feature_vector_dict])

    # ---------------------------------------------------------------
    # NOTE: You will need to swap the lines below for your own data
    # preprocessing methods.
    #
    # The code below is for demonstration purposes only. You will not
    # receive marks for submitting this code in an unchanged state.
    # ---------------------------------------------------------------

    # ----------- Replace this code with your own preprocessing steps --------
    feature_vector_df = feature_vector_df[['Unnamed: 0', 'time', 'Madrid_wind_speed', 'Valencia_wind_deg',
       'Bilbao_rain_1h', 'Valencia_wind_speed', 'Seville_humidity',
       'Madrid_humidity', 'Bilbao_clouds_all', 'Bilbao_wind_speed',
       'Seville_clouds_all', 'Bilbao_wind_deg', 'Barcelona_wind_speed',
       'Barcelona_wind_deg', 'Madrid_clouds_all', 'Seville_wind_speed',
       'Barcelona_rain_1h', 'Seville_pressure', 'Seville_rain_1h',
       'Bilbao_snow_3h', 'Barcelona_pressure', 'Seville_rain_3h',
       'Madrid_rain_1h', 'Barcelona_rain_3h', 'Valencia_snow_3h',
       'Madrid_weather_id', 'Barcelona_weather_id', 'Bilbao_pressure',
       'Seville_weather_id', 'Valencia_pressure', 'Seville_temp_max',
       'Madrid_pressure', 'Valencia_temp_max', 'Valencia_temp',
       'Bilbao_weather_id', 'Seville_temp', 'Valencia_humidity',
       'Valencia_temp_min', 'Barcelona_temp_max', 'Madrid_temp_max',
       'Barcelona_temp', 'Bilbao_temp_min', 'Bilbao_temp',
       'Barcelona_temp_min', 'Bilbao_temp_max', 'Seville_temp_min',
       'Madrid_temp', 'Madrid_temp_min', 'load_shortfall_3h']]
    
    df_1 = feature_vector_df.copy() #creating a copy of data

    df_1['Valencia_pressure'].fillna(df_1['Valencia_pressure'].mean(), inplace=True) #imputing the null with the mean
    df_1['time'] = pd.to_datetime(df_1['time']) # changing the date datatype


    df_1.drop('Unnamed: 0',inplace = True,axis = 1) #deleting the first column
    cols_to_drop = ['Bilbao_rain_1h','Bilbao_wind_deg','Barcelona_pressure','Barcelona_wind_deg',
               'Barcelona_rain_1h','Seville_rain_1h','Bilbao_pressure','Madrid_pressure','Valencia_pressure'] #columns to drop

    cols = [item for item in df_1.columns if 'max' in item or 'min' in item or '1h' in item] #selecting new columns

    cols_to = cols_to_drop + cols #combining columns

    df_1.drop(cols_to, inplace = True, axis = 1) #dropping unused columns

    #Changing Dtypes of 'time' from object to 'datetime64'

    #Changing Dtypes of 'Valencia_wind_deg', 'Seville_pressure' from object to 'category'


    cat_cols = [item for item in df_1.columns if 'pressure' in item or 'deg' in item]

    df_1[cat_cols] = df_1[cat_cols].astype('category')

    # Encoding 'Valencia_wind_deg', 'Seville_pressure' from 'category' to numeric values using 'cat.codes'

    df_1['Valencia_wind_deg'] = df_1['Valencia_wind_deg'].cat.codes

    df_1['Seville_pressure'] = df_1['Seville_pressure'].cat.codes

    # extracing the date from date time

    df_1['month'] = df_1['time'].dt.month

    df_1['day'] = df_1['time'].dt.day

    df_1['time'] = df_1['time'].dt.time

    # selecting the correct columns and in the correct order

    column_ = [col for col in df_1.columns if col == 'day' or col == 'time' or col == 'month']

    others = [item for item in df_1.columns if 'wind'  in item  or  'pressure' in item 
                      or 'cloud' in item or 'humidity' in item or 'Seville_weather' in item or 'Madrid_temp' in item]

    column = column_ + others # adding columns

    df_1 = df_1.reindex(columns = column_titles) # changing the index

    df_1['time'] = df_1['time'].astype('category') # changing time to category

    df_1['time'] = df_1['time'].cat.codes #changing time to encoding

    X_test = df_1[column]

    X_t = X_test.drop('time',axis = 1)
    
    predict_vector = X_t
    # ------------------------------------------------------------------------

    return predict_vector

def load_model(path_to_model:str):
    """Adapter function to load our pretrained model into memory.

    Parameters
    ----------
    path_to_model : str
        The relative path to the model weights/schema to load.
        Note that unless another file format is used, this needs to be a
        .pkl file.

    Returns
    -------
    <class: sklearn.estimator>
        The pretrained model loaded into memory.

    """
    return pickle.load(open(path_to_model, 'rb'))

def make_prediction(data, model):
    """Prepare request data for model prediciton.

    Parameters
    ----------
    data : str
        The data payload received within POST requests sent to our API.
    model : <class: sklearn.estimator>
        An sklearn model object.

    Returns
    -------
    list
        A 1-D python list containing the model prediction.

    """
    # Data preprocessing.
    prep_data = _preprocess_data(data)
    # Perform prediction with model and preprocessed data.
    prediction = model.predict(prep_data)
    # Format as list for output standerdisation.
    return prediction[0].tolist()

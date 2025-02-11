from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder
import pickle
import tensorflow as tf
import pandas as pd
import streamlit as st

model = tf.keras.models.load_model('churn_model.h5')

## load the scaler
scaler = pickle.load(open('scaler.pkl', 'rb'))

## load the encoder
onehot_encoder = pickle.load(open('oneHot_encoder_geo.pkl', 'rb'))

## load the label encoder
label_encoder = pickle.load(open('label_encoder_gender.pkl', 'rb')) 

## streamlit

st.title("Churn Prediction App")

geography = st.selectbox('Geography', onehot_encoder.categories_[0])
gender = st.selectbox('Gender', label_encoder.classes_)
age = st.slider('Age', 18, 100)
balance = st.number_input('Balance')
creditScore = st.number_input('Credit Score')
estimateSalary = st.number_input('Estimated Salary')
tenure = st.number_input('Tenure')
numOfProducts = st.number_input('Number of Products')
hasCrCard = st.selectbox('Has Credit Card', [0,1])
isActiveMember = st.selectbox('Is Active Member', [0,1])


import pandas as pd

input_data = pd.DataFrame(
    {   
        'CreditScore': [creditScore],
        'Gender': [label_encoder.transform([gender])[0]],     
        'Age': [age],
        'Tenure': [tenure],
        'Balance': [balance],
        'NumOfProducts': [numOfProducts],
        'HasCrCard': [hasCrCard],
        'IsActiveMember': [isActiveMember],
        'EstimatedSalary': [estimateSalary],
    }
)

# Encode geography
encoded_geo = onehot_encoder.transform([[geography]]).toarray()
geo_encode_df = pd.DataFrame(encoded_geo, columns=onehot_encoder.get_feature_names_out(["Geography"]))

# Concatenate encoded features with input
input_data = pd.concat([input_data.reset_index(drop=True), geo_encode_df], axis=1)

# Ensure feature scaling
scaled_input = scaler.transform(input_data)

# Prediction
prediction = model.predict(scaled_input)
prediction_prob = prediction[0] if isinstance(prediction[0], float) else prediction[0][0]

# Display result
st.subheader(f"Prediction Probability: {prediction_prob:.2f}")
if prediction_prob > 0.5:
    st.write("Customer will likely churn")
else:
    st.write("Customer will likely stay")

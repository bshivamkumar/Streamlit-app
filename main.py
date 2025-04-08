import streamlit as st
import pandas as pd
import numpy as np
import pickle
import base64

# Load Model
model = pickle.load(open("RF.sav", "rb"))

# Functions for encoding input
def get_fvalue(val):
    feature_dict = {"No": 1, "Yes": 2}
    return feature_dict.get(val, 0)

def get_value(val, my_dict):
    return my_dict.get(val, 0)

# Sidebar navigation
app_mode = st.sidebar.selectbox("Select Page", ["Home", "Prediction"])

if app_mode == "Home":
    st.title("LOAN PREDICTION APP 💰")
    st.image("loan_image.jpg")
    
    st.markdown("### Dataset Preview")
    data = pd.read_csv("train.csv")
    st.write(data.head())
    
    st.markdown("### Applicant Income vs Loan Amount")
    st.bar_chart(data[['ApplicantIncome', 'LoanAmount']].head(20))

elif app_mode == "Prediction":
    st.subheader("Please fill the form to check loan eligibility")
    
    # Sidebar inputs
    st.sidebar.header("Client Information")
    gender_dict = {"Male":1, "Female":2}
    feature_dict = {"No":1, "Yes":2}
    edu = {"Graduate":1, "Not Graduate":2}
    prop = {"Rural":1, "Urban":2, "Semiurban":3}
    
    ApplicantIncome = st.sidebar.slider('Applicant Income', 0, 10000, 0)
    CoapplicantIncome = st.sidebar.slider('Coapplicant Income', 0, 10000, 0)
    LoanAmount = st.sidebar.slider('Loan Amount (K$)', 9.0, 700.0, 200.0)
    Loan_Amount_Term = st.sidebar.selectbox('Loan Amount Term', (12.0, 36.0, 60.0, 84.0, 120.0, 180.0, 240.0, 300.0, 360.0))
    Credit_History = st.sidebar.radio('Credit History', (0.0, 1.0))
    Gender = st.sidebar.radio('Gender', list(gender_dict.keys()))
    Married = st.sidebar.radio('Married', list(feature_dict.keys()))
    Self_Employed = st.sidebar.radio('Self Employed', list(feature_dict.keys()))
    Dependents = st.sidebar.radio('Dependents', ['0', '1', '2', '3+'])
    Education = st.sidebar.radio('Education', list(edu.keys()))
    Property_Area = st.sidebar.radio('Property Area', list(prop.keys()))

    # Encode values
    class_0, class_1, class_2, class_3 = 0, 0, 0, 0
    if Dependents == '0':
        class_0 = 1
    elif Dependents == '1':
        class_1 = 1
    elif Dependents == '2':
        class_2 = 1
    else:
        class_3 = 1

    Rural, Urban, Semiurban = 0, 0, 0
    if Property_Area == 'Urban':
        Urban = 1
    elif Property_Area == 'Semiurban':
        Semiurban = 1
    else:
        Rural = 1

    # Final feature list
    feature_list = [ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History,
                    get_value(Gender, gender_dict), get_fvalue(Married), class_0, class_1, class_2, class_3,
                    get_value(Education, edu), get_fvalue(Self_Employed), Rural, Urban, Semiurban]
    single_sample = np.array(feature_list).reshape(1, -1)

    # Predict button
    if st.button("Predict"):
        prediction = model.predict(single_sample)

        if prediction[0] == 1:
            st.success("🎉 Congratulations! You're likely to get a loan.")
            gif = open("6m-rain.gif", "rb").read()
        else:
            st.error("❌ Sorry! You may not be eligible for the loan.")
            gif = open("green-cola-no.gif", "rb").read()
            
        data_url = base64.b64encode(gif).decode("utf-8")
        st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="result gif">', unsafe_allow_html=True)




# Imports
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from PIL import  Image
import streamlit as st


# Create title and sub title

st.write("""
# Diabestes Detection
Detect if someone has diabestes using machine learniong and python !

""")

image = Image.open('C:/Users/HSEIN BASSAM/Desktop/ML_WebApp/image.png')
st.image(image, caption='ML', use_column_width=True)

#get the data
df = pd.read_csv('C:/Users/HSEIN BASSAM/Desktop/ML_WebApp/diabetes.csv')

#set a subheader
st.subheader('Data Information:')
#show the data as a table
st.dataframe(df)
#show statistics on the data
st.write(df.describe())
#show the data as a chart
chart = st.bar_chart(df)

#split the data into independent 'X' and dependent 'Y' variables
X = df.iloc[:, 0:8].values
Y = df.iloc[:,-1].values

#split the data into 75% trainign and 25% testing

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=20,random_state=0)

#Get the features input from hte user
def get_user_input():
    Pregnancies = st.sidebar.slider('Pregnancies' , 0 , 17 , 3)
    Glucose = st.sidebar.slider('Glucose' , 0 , 199 , 117)
    BloodPressure = st.sidebar.slider('BloodPressure', 0, 122, 72)
    SkinThickness = st.sidebar.slider('SkinThickness', 0, 99, 23)
    Insulin = st.sidebar.slider('Insulin', 0.0, 846.0, 30.5)
    BMI = st.sidebar.slider('BMI', 0.0, 67.1, 30.0)
    DPF = st.sidebar.slider('DPF', 0.0, 2.42, 0.3725)
    Age = st.sidebar.slider('Age', 21, 81, 29)

    #Store a dictionory into a variable
    user_data = {
        'Pregnancies':Pregnancies,
        'Glucose':Glucose,
        'BloodPressure':BloodPressure,
        'SkinThickness':SkinThickness,
        'Insulin':Insulin,
        'BMI':BMI,
        'DPF':DPF,
        'Age':Age,
    }
    #trsansform the data into data frame
    features = pd.DataFrame(user_data , index= [0])
    return  features

#Store hte user input into a variable
user_input = get_user_input()

# set a subheader and display the usert input
st.subheader('User unput :')
st.write(user_input)

# create and train the model
RandomForestClassifier = RandomForestClassifier()
RandomForestClassifier.fit(X_train, Y_train)

#show the models metrics
st.subheader('Model Test Accuracy Score:')
st.write( str(accuracy_score(Y_test,RandomForestClassifier.predict(X_test))*100)+'%')

# Store the models predictiions in a variables
prediction = RandomForestClassifier.predict(user_input)

#aet a subheader and display the calssification

st.subheader('Classification: ')
st.write(prediction)
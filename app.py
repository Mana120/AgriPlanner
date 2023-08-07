import streamlit as st 
import pandas as pd
import numpy as np
import os
import pickle
import warnings
import base64
from PIL import Image

#agriculture

def load_model(modelfile):
	loaded_model = pickle.load(open(modelfile, 'rb'))
	return loaded_model


def main():
    # title

    html_temp = """
   
    <div>
    <h4 style="color:#000000;text-align:center;font-weight:bold;font-size:58px;"> AgriPlanner </h4>
    <div>
    </div>
    <p></p>
    </div>
    """
    

    
      
    
    def add_bg_from_local(image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            st.markdown(
            f"""
            <style>
            .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
            background-size: cover
            }}
            </style>
            """,
            unsafe_allow_html=True
    )
    add_bg_from_local('crop1.jpg')  
      
    
    st.markdown(html_temp, unsafe_allow_html=True)

         
        

    states=pd.read_csv("dataset/loc.csv")

    col1, col2,col3 = st.columns(3)

    # First column for Nitrogen input
    with col1:
        st.markdown(
            f"""
            <span style="color:black">
            Nitrogen
            </span>
            """,
            unsafe_allow_html=True
        )
        N = st.number_input("N", 1, 140)

    # Second column for Phosphorus input
    with col2:
        st.markdown(
            f"""
            <span style="color:black">
            Phosphorus
            </span>
            """,
            unsafe_allow_html=True
        )
        P = st.number_input("P", 1, 140)
    with col3:
        st.markdown(
            f"""
            <span style="color:black">
            Potassium
            </span>
            """,
        unsafe_allow_html=True)
        K = st.number_input("K", 1,205)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <span style="color:black">
            Temperature
            </span>
            """,
        unsafe_allow_html=True)
        temp = st.number_input("Degrees",8.0,45.0)
    with col2:
        st.markdown(
            f"""
            <span style="color:black">
            Humidity 
            </span>
            """,
        unsafe_allow_html=True)
        humidity = st.number_input("in %", 14.0,100.0)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <span style="color:black">
            Ph
            </span>
            """,
        unsafe_allow_html=True)
        ph = st.number_input("level", 3.5,10.0)
    with col2:
        st.markdown(
            f"""
            <span style="color:black">
            Rainfall 
            </span>
            """,
        unsafe_allow_html=True)
        rainfall = st.number_input("in mm",19.0,300.0)
    st.markdown(
        f"""
        <span style="color:black">
        Enter the Location
        </span>
        """,
    unsafe_allow_html=True)
    state_input=st.selectbox("Choose the state",sorted(['']+list(states['STATE'].unique())),1)
    district_input=st.selectbox("Choose the district",sorted(['']+list(states['DISTRICT'].unique())),1)

    

    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    
    #single_pred = np.array(feature_list).reshape(1,-1)
    single_pred=np.array(feature_list).reshape(1,-1)
    
    
    #print(single_pred)
    button1 = st.button('Find Crop')
    button2 = st.button('Find Fertilizer')
    col1, col2,col3 = st.columns(3)
    if button1:
        
        loaded_model = load_model('models/model.pkl')
        
        prediction = loaded_model.predict(single_pred)

        col1.markdown(
            f"""
            <div style="color:black;background-color:#ffd11a;border: 1px solid black  ;border-radius: 5px;font-size:20px">
            <span>
            {prediction.item().title()} is recommended for your farm.
            </span>
            <br>
            </div>
            """,
            unsafe_allow_html=True
        )

       
    
    if button2:
    

        loaded_model = load_model('models/model1.pkl')
        prediction = loaded_model.predict(single_pred)
        
        a=prediction.item().title()
        b=a.split("_")
        col1.markdown(
            f"""
            <div style="color:black;background-color:#ffd11a;border: 1px   ;border-radius: 5px;font-size:18px">
            <br>
            <span>
            1. {b[0]} is the  recommended fertilizer and its cost is Rs.{b[1]}.
            </span>
            <br>
            </div>
            """,
            unsafe_allow_html=True
        )
   

        loaded_model = load_model('models/model2.pkl')
        prediction = loaded_model.predict(single_pred)
        a=prediction.item().title()
        b=a.split("_")
        col2.markdown(
            f"""
            <div style="color:black;background-color:#ffd11a;border: 1px   ;border-radius: 5px;font-size:18px">
            <br>
            <span>
            2. {b[0]} is the  recommended fertilizer and its cost is Rs.{b[1]}.
            </span>
            <br>
            </div>
            """,
            unsafe_allow_html=True
        )
   
    
        loaded_model = load_model('models/model3.pkl')
        prediction = loaded_model.predict(single_pred)

        a=prediction.item().title()
        b=a.split("_")
        col3.markdown(
            f"""
            <div style="color:black;background-color:#ffd11a;border: 1px  ;border-radius: 5px;font-size:18px">
            <br>
            <span>
            3. {b[0]} is the  recommended fertilizer and its cost is Rs.{b[1]}.
            </span>
            <br>
            </div>
            """,
            unsafe_allow_html=True
        )
        df1=states.loc[states['STATE'] == state_input]
        df2=states.loc[states['DISTRICT']== district_input]

        df3=df2['value']
        df4=df2['month']
        df3=df3.values.tolist()
        df4=df4.values.tolist()
        res = dict(zip(df3, df4))
        m=max(df3)
        
        m=res[m]
        mon=list()
        if(m==1):
            mon.append('JANUARY')
        elif(m==2):
            mon.append('FEBRUARY')
        elif(m==3):
            mon.append('MARCH')
        elif(m==4):
            mon.append('APRIL')
        elif(m==5):
            mon.append('MAY')
        elif(m==6):
            mon.append('JUNE')
        elif(m==7):
            mon.append('JULY')
        elif(m==8):
            mon.append('AUGUST')
        elif(m==9):
            mon.append('SEPTEMBER')
        elif(m==10):
            mon.append('OCTOBER')
        elif(m==11):
            mon.append('NOVEMBER')
        elif(m==12):
            mon.append('DECEMBER')
        #col1.success(f"{mon[0]} is predicted to be the month with the most rainfall")
        col1.markdown(
            f"""
            <div  style="color:black;background-color:#ffd11a;border: 1px  ;border-radius: 5px;font-size:18px">
            <br>
            <span>
            NOTE:<br>
            {mon[0]} is predicted to be the month with the most rainfall
            </span>
            <br>
            </div>
            """,unsafe_allow_html=True
        )
        loaded_model = load_model('models/model.pkl')
        prediction = loaded_model.predict(single_pred)
        crop=prediction.item().title()
        
        df=pd.read_csv("dataset/LINK.csv")
        subset=df[df['CROP']==crop]['link']
        subset=subset.values.tolist()
        col2.markdown(
            f"""
            <div style="color:black;background-color:#ffd11a;border: 1px  ;border-radius: 5px;font-size:18px">
            
            </div>
            """,unsafe_allow_html=True
        )
        
        col3.warning(f"For Further information about {prediction.item().title()}  click  [here]({subset[0]})")
        

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

if __name__ == '__main__':
	main()
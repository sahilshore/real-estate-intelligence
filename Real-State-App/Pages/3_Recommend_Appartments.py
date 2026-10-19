import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Recommend Appartments")

location_df = pickle.load(open('C:\\Users\\SAHIL\\Desktop\\Real-State-Price-Predictor\\DATA\\Model_Data\\location_distances_final.pkl','rb'))

st.dataframe(location_df.head(10))

st.title('Recommend Appartments')

st.header("select Location and Redius to get the recommended appartments")

selected_location = st.selectbox('Select Location',sorted(location_df.columns.to_list()))

radius = st.number_input('Select Redius in KMs',min_value=0.0,max_value=100.0,step=1.0)

if st.button("Search"):
    result_ser = location_df[location_df[selected_location]< radius*1000][selected_location].sort_values().to_dict()
    st.write("Recommended Appartments:")
    for key, value in result_ser.items():
        st.write(str(key)," ----> ", str((value)/1000)," KMs")
import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Viz Demo")



# these are the columns in the df 
# 'property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
#        'agePossession', 'built_up_area', 'servant room', 'store room',
#        'furnishing_type', 'luxury_category', 'floor_category'

with open('C:\\Users\\SAHIL\\Desktop\\Real-State-Price-Predictor\\DATA\\Model_Data\\df.pkl','rb') as file:
    df = pickle.load(file)

with open('C:\\Users\\SAHIL\\Desktop\\Real-State-Price-Predictor\\DATA\\Model_Data\\pipeline.pkl','rb') as file:
    pipeline = pickle.load(file)


st.header('Enter Your Property Details')

# property_type
property_type = st.selectbox('Property Type',["flat", "house"])


# sector
sector = st.selectbox('Sector',sorted(df['sector'].unique().tolist()))

# bedroom
bedrooms = float(st.selectbox('Number of Bedroom',sorted(df['bedRoom'].unique().tolist())))

bathrooms = float(st.selectbox('Number of Bathroom',sorted(df['bathroom'].unique().tolist())))

#balcony
balcony = st.selectbox('Number of Balcony',sorted(df['balcony'].unique().tolist()))

# property_age
property_age = st.selectbox('Property Age',sorted(df['agePossession'].unique().tolist()))

# built_up_area
built_up_area = float(st.number_input('Built Up Area (in sq. ft.)', min_value=0))

# servant_room
servant_room = float(st.selectbox('Servant Room',[0.0, 1.0]))

# store_room
store_room = float(st.selectbox('Store Room',[0.0, 1.0]))

# furnishing_type
furnishing_type = st.selectbox('Furnishing Type',sorted(df['furnishing_type'].unique().tolist()))

# luxury_category
luxury_category = st.selectbox('Luxury Category',sorted(df['luxury_category'].unique().tolist()))

# floor_category
floor_category = st.selectbox('Floor Category',sorted(df['floor_category'].unique().tolist()))

if st.button('Predict Price'):
    input_data = pd.DataFrame([[property_type, sector, bedrooms, bathrooms, balcony, property_age, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]],
                              columns=['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony', 'agePossession', 'built_up_area', 'servant room', 'store room', 'furnishing_type', 'luxury_category', 'floor_category'])
    
    # st.dataframe(input_data)

    base_price = np.expm1(pipeline.predict(input_data))
    low_price = base_price - 0.22
    high_price = base_price + 0.22

    st.success(f'The price (INR) of the flat is between {low_price[0]:,.2f} Cr and {high_price[0]:,.2f} Cr')
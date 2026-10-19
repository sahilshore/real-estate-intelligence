import streamlit as st
import pickle
import pandas as pd
import numpy as np
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "DataSets"

st.set_page_config(page_title="Recommend Appartments")

location_df = pickle.load(open(DATA_DIR / 'location_distances_final.pkl','rb'))

cosine_sim1 = pickle.load(open(DATA_DIR / 'cosine_sim1.pkl','rb'))
cosine_sim2 = pickle.load(open(DATA_DIR / 'cosine_sim2.pkl','rb'))
cosine_sim3 = pickle.load(open(DATA_DIR / 'cosine_sim3.pkl','rb'))

def recommend_properties_with_scores(property_name, top_n=247):
    
    # Combine the cosine similarity matrices with different weights
    cosine_sim_matrix = 0.5*cosine_sim1 + 0.8*cosine_sim2 + 1.0*cosine_sim3
    # cosine_sim_matrix = cosine_sim3
    
    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    
    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n+1]]
    
    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()
    
    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })
    
    return recommendations_df

st.title('Recommend Appartments')

st.header("select Location and Radius")

selected_location = st.selectbox('Select Location',sorted(location_df.columns.to_list()))

radius = st.number_input('Select Radius in KMs',min_value=0.0,max_value=100.0,step=1.0)

if st.button("Search"):
    result_ser = location_df[location_df[selected_location]< radius*1000][selected_location].sort_values().to_dict()
    st.write("Recommended Appartments:")
    for key, value in result_ser.items():
        st.write(str(key)," ----> ", str((value)/1000)," KMs")


st.header("Select an appartment to get the details")
selected_appartment = st.selectbox("Select an appartment to get the details", sorted(location_df.index.to_list()))      

if st.button("Recommend"):
    recommended_df = recommend_properties_with_scores(selected_appartment, top_n=7)
    st.write("Recommended Appartments based on Similarity for '{}':".format(selected_appartment))
    st.dataframe(recommended_df)
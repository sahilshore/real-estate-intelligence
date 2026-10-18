import streamlit as st
import pickle
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gurgaon Real Estate Analytics Using Plots")

st.title("Analysis")

new_df = pd.read_csv(
    r'C:\Users\SAHIL\Desktop\Real-State-Price-Predictor\DATA\Model_Data\data_viz1.csv'
)

# Group data by sector
group_df = new_df.groupby('sector').mean(numeric_only=True)[
    ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']
]

# Create the interactive map
fig = px.scatter_map(
    group_df.reset_index(),
    lat="latitude",
    lon="longitude",
    color="price_per_sqft",
    size="built_up_area",
    hover_name="sector",
    color_continuous_scale="RdYlBu_r",
    zoom=10,
    center={"lat": 28.45, "lon": 76.98},
    map_style="open-street-map",
    size_max=20
)

# Configure the color bar
fig.update_layout(
    height=500,
    width=1000,
    margin=dict(l=20, r=20, t=0, b=0),
    coloraxis_colorbar=dict(
        title="Price per Sqft",
        ticks="outside"
    )
)

# Display map in Streamlit
st.plotly_chart(fig, use_container_width=True)

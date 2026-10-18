import streamlit as st
import pickle
import pandas as pd
import plotly.express as px
import ast
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud


st.set_page_config(page_title="Gurgaon Real Estate Analytics Using Plots")

st.title("Analysis")


new_df = pd.read_csv(
    r'C:\Users\SAHIL\Desktop\Real-State-Price-Predictor\DATA\Model_Data\data_viz1.csv'
)

# Group data by sector
group_df = new_df.groupby('sector').mean(numeric_only=True)[
    ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']
]

st.header("Price per Sqft by Sector (Interactive Map)")
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


df = pd.read_csv('C:\\Users\\SAHIL\\Desktop\\Real-State-Price-Predictor\\DATA\\Featured_Data\\gurgaon_properties_missing_value_imputation.csv')
df1 = pd.read_csv('C:\\Users\\SAHIL\\Desktop\\Real-State-Price-Predictor\\DATA\\Preprocessed_Data\\gurgaon_properties.csv')

st.header("Word Cloud of Features by Sector")

wordcloud_df = df1.merge(df, left_index=True, right_index=True)[['sector','features']]



wordcloud_df['features'] = wordcloud_df['features'].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)

wordcloud_df1 = wordcloud_df.groupby('sector')['features'].sum().reset_index()

sector = st.selectbox("Select Sector", wordcloud_df1['sector'].unique().tolist(), key="sector_select")

if sector:
    text = ' '.join(wordcloud_df1[wordcloud_df1['sector'] == sector]['features'].values[0])
    st.subheader(f"Word Cloud for {sector}")
    

    wordcloud = WordCloud(width = 800, height = 800, 
                        background_color ='white', 
                        stopwords = set(['s']),  # Any stopwords you'd like to exclude
                        min_font_size = 10).generate(text)

    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud, interpolation='bilinear') 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    st.pyplot(plt.gcf())

st.header("Average Price per Sqft by Sector")

property_type = st.selectbox("Select Property Type", df['property_type'].unique().tolist(), key="property_type_select")
if property_type == "flat":
    # Create a bar chart for average price per sqft by sector
    fig1 = px.scatter(new_df[new_df["property_type"] == "flat"], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
else:
    fig2 = px.scatter(new_df[new_df["property_type"] == "house"], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")

    st.plotly_chart(fig2, use_container_width=True)    


st.header('BHK Pie Chart')
sector_option = np.sort(new_df['sector'].unique()).tolist()
sector_option.insert(0, "Overall")
selected_sector = st.selectbox("Select Sector", sector_option, key="sector select")
if selected_sector == "Overall":
    fig2 = px.pie(new_df, names='bedRoom', title='Distribution of Properties by BHK')
    st.plotly_chart(fig2, use_container_width=True)
else:
    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom', title='Distribution of Properties by BHK')
    st.plotly_chart(fig2, use_container_width=True)

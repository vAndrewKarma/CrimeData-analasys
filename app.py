import pandas as pd
import folium
from streamlit_folium import folium_static
import streamlit as st
import plotly.express as px
 
df = pd.read_csv("crime_data.csv")
df["DATE OCC"] = pd.to_datetime(df["DATE OCC"])
df["Year"] = df["DATE OCC"].dt.year
df["Month"] = df["DATE OCC"].dt.month
df["Hour"] = df["TIME OCC"] // 100

st.title("📌 Crime Data Analysis & Map") 

year_selected = st.slider("Select Year", int(df["Year"].min()), int(df["Year"].max()), int(df["Year"].max()))
df_filtered = df[df["Year"] == year_selected]
 
st.subheader("🔍 Top 10 Crimes in Selected Year")
top_crimes = df_filtered["Crm Cd Desc"].value_counts().head(10)
fig = px.bar(x=top_crimes.index, y=top_crimes.values, labels={"x": "Crime Type", "y": "Count"}, title="Top 10 Crimes")
st.plotly_chart(fig)
 
st.subheader("⏳ Crime Frequency by Hour")
fig2 = px.histogram(df_filtered, x="Hour", nbins=24, title="Crimes by Time of Day")
st.plotly_chart(fig2)
 
st.subheader("🌍 Crime Map")
m = folium.Map(location=[df["LAT"].mean(), df["LON"].mean()], zoom_start=12)
 
sample_size = min(500, len(df_filtered))
for _, row in df_filtered.sample(sample_size).iterrows():
    folium.CircleMarker(
        location=[row["LAT"], row["LON"]],
        radius=3,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.5,
        popup=f"{row['Crm Cd Desc']} - {row['DATE OCC'].date()}",
    ).add_to(m)

folium_static(m)

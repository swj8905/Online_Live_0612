import requests
import json
import os
import streamlit as st
import pydeck as pdk
import pandas as pd

api_key = "415272424273776a3130306f62584679"

is_first = True
for i in range(3):
    num1 = i*1000 + 1
    num2 = (i+1)*1000
    if num2 >= 2376:
        num2 = 2376
    url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/bikeList/{num1}/{num2}/"
    data = requests.get(url)
    result = json.loads(data.text) # json -> 딕셔너리
    bikes = result["rentBikeStatus"]["row"]
    if is_first:
        df = pd.DataFrame(bikes)
        is_first = False
    else:
        temp = pd.DataFrame(bikes)
        df = pd.concat([df, temp])
df.reset_index(inplace=True)
df["stationLatitude"] = pd.to_numeric(df["stationLatitude"])
df["stationLongitude"] = pd.to_numeric(df["stationLongitude"])
df["parkingBikeTotCnt"] = pd.to_numeric(df["parkingBikeTotCnt"])

df['정규화'] = df["parkingBikeTotCnt"] / 10
# 좌표 중심값 구하기
lat_sum = 0
lon_sum = 0
for idx, i in df.iterrows():
    lat_sum += float(i["stationLatitude"])
    lon_sum += float(i["stationLongitude"])
lat_avr = lat_sum/len(df.index)
lon_avr = lon_sum/len(df.index)

temp = []
for idx, i in df.iterrows():
    for j in range(int(i["rackTotCnt"])):
        temp.append([i["stationLongitude"], i["stationLatitude"]])

df_positions = pd.DataFrame(temp, columns=["lon", "lat"])

layer = pdk.Layer(
'ScatterplotLayer',
df,
get_position='[stationLongitude, stationLatitude]',
get_radius=60,
get_fill_color='[255*(1-정규화), 255*(1-정규화), 255]',
pickable=True,
)

center = [lon_avr, lat_avr]
view_state = pdk.ViewState(
    longitude=center[0],
    latitude=center[1],
    zoom=10)

# Render
r = pdk.Deck(layers=[layer],
             initial_view_state=view_state,
             tooltip={"html": "정류장 : {stationName}<br/>현재 주차 대수: {parkingBikeTotCnt}", "style": {"color": "white"}},)

st.pydeck_chart(r)

import streamlit as st
import googlemaps
import polyline
import folium
from streamlit_folium import folium_static

# Google Maps APIキーを設定
api_key = "AIzaSyA8eIq6u_7RYwz5Ah9P3YCMtf6Sa0IB4-A"
gmaps = googlemaps.Client(key=api_key)

# 座標情報を入力
location1 = (35.681236, 139.767125)  # 例: (35.681236, 139.767125)
location2 = (35.689487, 139.691706)  # 例: (35.689487, 139.691706)
location3 = (35.658581, 139.745433)  # 例: (35.658581, 139.745433)

# ストリームリットアプリのヘッダー
st.title("最短経路表示アプリ")

# 座標情報のリスト
locations = [location1, location2, location3]

# 最短経路のリクエストを送信
directions_result = gmaps.directions(
    origin=location1,
    destination=location3,
    waypoints=[location2],
    mode="driving"
)

# ポリラインを取得してデコード
route = directions_result[0]['overview_polyline']['points']
decoded_route = polyline.decode(route)

# 地図の作成
m = folium.Map(location=location1, zoom_start=13)

# 経路を地図上に描画
folium.PolyLine(decoded_route, color="blue", weight=5).add_to(m)

# 出発地点、中間地点、到着地点のマーカーを追加
folium.Marker(location1, tooltip="Location 1").add_to(m)
folium.Marker(location2, tooltip="Location 2").add_to(m)
folium.Marker(location3, tooltip="Location 3").add_to(m)

# 地図を表示
folium_static(m)

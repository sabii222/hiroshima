import streamlit as st
import requests
from config import RAKUTEN_API_KEY, OPENWEATHER_API_KEY

# 広島県の座標
latitude = 34.3853
longitude = 132.4553
hiroshima_middle_class_code = "hiroshima"  # 広島県の中分類コード

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        st.error("天気情報の取得に失敗しました。")
        return None

def get_hotels(keyword, limit=5):
    url = "https://app.rakuten.co.jp/services/api/Travel/KeywordHotelSearch/20170426"
    params = {
        "format": "json",
        "keyword": keyword,
        "applicationId": RAKUTEN_API_KEY,
        "middleClassCode": hiroshima_middle_class_code,  # 広島県に限定
        "hits": limit,  # 取得するホテルの数を制限
        "datumType": 1  # 日本測地系を使用
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        hotel_data = response.json()
        return hotel_data["hotels"][:limit]  # 取得したホテルの数を5件に制限
    else:
        st.error("ホテル情報の取得に失敗しました。")
        return None

# Streamlit UI
st.title("広島旅行プラン提案アプリ")

st.write("広島での旅行プランを提案します。")

# 天気情報の表示
st.subheader("現在の天気情報")
weather_data = get_weather()
if weather_data:
    st.write(f"天気: {weather_data['weather'][0]['description']}")
    st.write(f"気温: {weather_data['main']['temp']}℃")
    st.write(f"湿度: {weather_data['main']['humidity']}%")
    st.write(f"風速: {weather_data['wind']['speed']}m/s")

# ユーザーの好みに応じた宿泊施設の提案
st.subheader("おすすめの宿泊施設")

# 選択式のキーワード
keyword_options = {
    "静かで落ち着いている": "静か",
    "便利な立地": "便利",
    "広々としている": "広々",
    "料理がおいしい": "料理",
    "安い": "安い"
}

# ユーザーが選択肢から選ぶ
selected_option = st.selectbox("宿泊施設の好みを選んでください", list(keyword_options.keys()))

# 選択されたキーワードに基づいてホテルを検索
if selected_option:
    keyword = keyword_options[selected_option]
    hotels = get_hotels(keyword)
    if hotels:
        for hotel in hotels:
            hotel_name = hotel["hotel"][0]["hotelBasicInfo"]["hotelName"]
            hotel_address = hotel["hotel"][0]["hotelBasicInfo"]["address1"] + hotel["hotel"][0]["hotelBasicInfo"]["address2"]
            hotel_url = hotel["hotel"][0]["hotelBasicInfo"]["hotelInformationUrl"]
            st.write(f"### {hotel_name}")
            st.write(f"住所: {hotel_address}")
            st.write(f"[詳細はこちら]({hotel_url})")

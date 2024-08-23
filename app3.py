import streamlit as st
import requests
from datetime import datetime, timedelta
from config import RAKUTEN_API_KEY, OPENWEATHER_API_KEY

# 広島県の座標
latitude = 34.3853
longitude = 132.4553
hiroshima_middle_class_code = "hiroshima"  # 広島県の中分類コード

def get_weather_for_dates(days):
    weather_data = []
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        timestamp = int(date.timestamp())
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={OPENWEATHER_API_KEY}&dt={timestamp}"
        response = requests.get(url)
        if response.status_code == 200:
            daily_weather = response.json()
            weather_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "weather": daily_weather['weather'][0]['description'],
                "temp": daily_weather['main']['temp'],
                "humidity": daily_weather['main']['humidity'],
                "wind_speed": daily_weather['wind']['speed']
            })
        else:
            st.error(f"{date.strftime('%Y-%m-%d')} の天気情報の取得に失敗しました。")
            weather_data.append(None)
    return weather_data

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

# 旅行日数の入力
st.subheader("旅行日数を入力してください")
travel_days = st.number_input("旅行日数", min_value=1, max_value=14, value=3)

# 天気情報の表示
st.subheader(f"旅行期間中（{travel_days}日間）の天気情報")
weather_data = get_weather_for_dates(travel_days)
if weather_data:
    for day_weather in weather_data:
        if day_weather:
            st.write(f"### {day_weather['date']}")
            st.write(f"天気: {day_weather['weather']}")
            st.write(f"気温: {day_weather['temp']}℃")
            st.write(f"湿度: {day_weather['humidity']}%")
            st.write(f"風速: {day_weather['wind_speed']}m/s")
        else:
            st.write(f"天気情報を取得できませんでした。")

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
            hotel_info = hotel["hotel"][0]["hotelBasicInfo"]
            hotel_name = hotel["hotel"][0]["hotelBasicInfo"]["hotelName"]
            hotel_address = hotel["hotel"][0]["hotelBasicInfo"]["address1"] + hotel["hotel"][0]["hotelBasicInfo"]["address2"]
            hotel_url = hotel["hotel"][0]["hotelBasicInfo"]["hotelInformationUrl"]

            # サムネイル画像URLを取得
            hotel_thumbnail_url = hotel_info.get("hotelThumbnailUrl")

            st.write(f"### {hotel_name}")
            st.write(f"住所: {hotel_address}")
            if hotel_thumbnail_url:  # サムネイル画像がある場合に表示
                st.image(hotel_thumbnail_url, use_column_width=True)
            st.write(f"[詳細はこちら]({hotel_url})")

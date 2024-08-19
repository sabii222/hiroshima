import streamlit as st

def main():
    st.title("広島旅行プラン提案アプリ")
    
    # ユーザーの入力を受け取る
    st.header("旅行の好みを教えてください")
    
    # 質問1: 旅行の目的
    purpose = st.selectbox(
        "旅行の目的は何ですか？",
        ("観光", "食べ物", "歴史・文化", "リラックス", "アクティビティ")
    )
    
    # 質問2: 旅行日数
    days = st.slider("旅行日数を選んでください", 1, 7, 3)
    
    # 質問3: 好みのアクティビティ
    activities = st.multiselect(
        "興味があるアクティビティを選んでください",
        ["宮島訪問", "平和記念公園", "尾道散策", "原爆ドーム", "広島グルメ（お好み焼き、牡蠣など）"]
    )
    
    # 質問4: 予算
    budget = st.radio(
        "予算はどのくらいですか？",
        ("低予算", "中予算", "高予算")
    )
    
    # 提案ボタン
    if st.button("旅行プランを提案"):
        st.header("おすすめの旅行プラン")
        # 旅行プランを生成
        generate_plan(purpose, days, activities, budget)

def generate_plan(purpose, days, activities, budget):
    # 仮のプラン生成ロジック
    st.write(f"目的: {purpose}")
    st.write(f"日数: {days}日")
    st.write(f"アクティビティ: {', '.join(activities)}")
    st.write(f"予算: {budget}")
    
    st.subheader("おすすめプラン:")
    # 旅行の目的に応じたプラン例
    if purpose == "観光":
        st.write("- 宮島と厳島神社の観光")
        st.write("- 広島市内の観光スポット巡り")
        if "平和記念公園" in activities:
            st.write("- 平和記念公園と原爆ドーム訪問")
    elif purpose == "食べ物":
        st.write("- 広島風お好み焼きの食べ歩き")
        st.write("- 広島の牡蠣料理を堪能")
    elif purpose == "歴史・文化":
        st.write("- 原爆ドームと平和記念資料館訪問")
        st.write("- 広島城と縮景園の歴史探索")
    elif purpose == "リラックス":
        st.write("- 宮島の温泉でリラックス")
        st.write("- 静かな尾道でのんびりとした時間を過ごす")
    elif purpose == "アクティビティ":
        st.write("- 自転車でしまなみ海道を走る")
        st.write("- 瀬戸内海でのクルージング")
    
    st.write("このプランを基に、自分のペースで広島を楽しんでください！")

if __name__ == "__main__":
    main()

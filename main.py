import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="국가별 태양광 발전 현황", layout="wide")

st.title("🌞 국가별 태양광 발전 에너지 사용량")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("data/solar_energy.csv")
    return df

df = load_data()

# 가장 최근 연도 데이터 사용 (컬럼명은 실제 데이터에 맞게 수정하세요)
latest_year = df["year"].max()
latest_df = df[df["year"] == latest_year]

st.subheader(f"{latest_year}년 기준 국가별 태양광 발전량")

# Choropleth 지도 (붉은색 계열)
fig = px.choropleth(
    latest_df,
    locations="country",          # 국가명 컬럼
    locationmode="country names", # 국가명으로 매칭
    color="solar_energy",         # 발전량 컬럼
    color_continuous_scale="Reds",
    labels={"solar_energy": "태양광 발전량(TWh)"},
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig, use_container_width=True)

# 상위 5개국
st.subheader("🏆 태양광 발전 상위 5개국")
top5 = latest_df.sort_values("solar_energy", ascending=False).head(5)

for idx, row in top5.iterrows():
    with st.expander(f"{row['country']} - {row['solar_energy']:.1f} TWh"):
        st.write(f"**{row['country']}**의 상세 데이터를 보려면")
        st.write("왼쪽 사이드바의 '상위국가 분석' 페이지를 확인하세요!")
        # 해당 국가의 연도별 추이 그래프
        country_df = df[df["country"] == row["country"]]
        line_fig = px.line(country_df, x="year", y="solar_energy",
                           title=f"{row['country']} 연도별 태양광 발전량")
        st.plotly_chart(line_fig, use_container_width=True)

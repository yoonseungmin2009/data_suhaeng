import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="국가별 태양광 발전 현황", layout="wide")

st.title("🌞 국가별 태양광 발전 에너지 사용량")

@st.cache_data
def load_data():
    df = pd.read_csv("solar-energy-consumption.csv")
    # 진짜 국가만 남기기: Code가 3글자이고 OWID_로 시작하지 않는 것
    df = df.dropna(subset=["Code"])
    df = df[df["Code"].str.len() == 3]
    df = df[~df["Code"].str.startswith("OWID_")]
    return df

df = load_data()

# 가장 최근 연도 데이터 사용
latest_year = int(df["Year"].max())
latest_df = df[df["Year"] == latest_year]

st.subheader(f"{latest_year}년 기준 국가별 태양광 발전량 (TWh)")

# Choropleth 지도 (붉은색 계열, ISO-3 코드 사용)
fig = px.choropleth(
    latest_df,
    locations="Code",            # ISO-3 코드 컬럼
    color="Solar",               # 발전량
    hover_name="Entity",         # 국가명
    color_continuous_scale="Reds",
    labels={"Solar": "태양광 발전량(TWh)"},
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig, use_container_width=True)

# 상위 5개국
st.subheader("🏆 태양광 발전 상위 5개국")
top5 = latest_df.sort_values("Solar", ascending=False).head(5)

for _, row in top5.iterrows():
    with st.expander(f"{row['Entity']} - {row['Solar']:.1f} TWh"):
        st.write(f"**{row['Entity']}**의 연도별 추이입니다. "
                 "자세한 분석은 왼쪽 사이드바의 페이지를 확인하세요!")
        country_df = df[df["Entity"] == row["Entity"]]
        line_fig = px.line(country_df, x="Year", y="Solar",
                           labels={"Solar": "태양광 발전량(TWh)", "Year": "연도"},
                           title=f"{row['Entity']} 연도별 태양광 발전량")
        st.plotly_chart(line_fig, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="상위국가 분석", layout="wide")

# 페이지 맨 위: 분석 주제(질문)
st.title("🤔 상위 5개국은 왜 태양광 발전을 많이 사용할까?")
st.markdown("""
> **분석 주제:** 태양광 발전량 상위 5개국이 각 국가의 지리적·경제적·정책적 상황과
> 어떤 관련이 있는지 데이터를 통해 살펴본다.
""")

@st.cache_data
def load_data():
    return pd.read_csv("data/solar_energy.csv")

df = load_data()
latest_year = df["year"].max()
latest_df = df[df["year"] == latest_year]
top5 = latest_df.sort_values("solar_energy", ascending=False).head(5)

# 상위 5개국 발전량 비교
st.subheader("📊 상위 5개국 태양광 발전량 비교")
bar_fig = px.bar(top5, x="country", y="solar_energy",
                 color="solar_energy", color_continuous_scale="Reds",
                 labels={"solar_energy": "태양광 발전량(TWh)", "country": "국가"})
st.plotly_chart(bar_fig, use_container_width=True)

# 상위 5개국 연도별 추이
st.subheader("📈 상위 5개국 연도별 발전량 변화")
top5_countries = top5["country"].tolist()
trend_df = df[df["country"].isin(top5_countries)]
line_fig = px.line(trend_df, x="year", y="solar_energy", color="country",
                   labels={"solar_energy": "태양광 발전량(TWh)", "year": "연도"})
st.plotly_chart(line_fig, use_container_width=True)

# 분석 내용 (직접 조사한 결과를 서술)
st.subheader("💡 경향성 분석")
st.markdown("""
**1. 풍부한 일조량과 넓은 국토**  
상위권 국가 중 상당수는 일조량이 풍부하거나 국토가 넓어
태양광 패널 설치에 유리한 환경을 가지고 있다.

**2. 강력한 재생에너지 정책**  
정부 차원의 보조금, 탄소중립 목표 설정 등 정책적 지원이
태양광 발전 확대를 견인하였다.

**3. 높은 전력 수요와 경제 규모**  
경제 규모가 크고 전력 수요가 높은 국가일수록
재생에너지에 대한 투자 여력도 크다.

*(위 내용은 예시입니다. 여러분이 실제 데이터와 자료를 조사해
각 국가의 상황에 맞게 구체적으로 작성하세요.)*
""")

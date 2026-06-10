import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="상승폭 분석", layout="wide")

# 페이지 맨 위: 분석 주제(질문)
st.title("🚀 가장 빠르게 성장한 국가, 그 이유는?")
st.markdown("""
> **분석 주제:** 2000년부터 2025년까지 태양광 발전 사용량의 상승폭이 가장 큰 국가를 찾고,
> 이 변화가 국민 인식 변화, 산업화, 정책 등 어떤 요인과 관련 있는지 분석한다.
""")

@st.cache_data
def load_data():
    return pd.read_csv("data/solar_energy.csv")

df = load_data()

# 2000~2025년 기간 필터링
period_df = df[(df["year"] >= 2000) & (df["year"] <= 2025)]

# 국가별 상승폭 계산
growth = []
for country in period_df["country"].unique():
    cdf = period_df[period_df["country"] == country].sort_values("year")
    if len(cdf) >= 2:
        increase = cdf["solar_energy"].iloc[-1] - cdf["solar_energy"].iloc[0]
        growth.append({"country": country, "growth": increase})

growth_df = pd.DataFrame(growth).sort_values("growth", ascending=False)

# 상승폭 상위 국가 시각화
st.subheader("📊 상승폭 상위 10개국")
bar_fig = px.bar(growth_df.head(10), x="country", y="growth",
                 color="growth", color_continuous_scale="Reds",
                 labels={"growth": "상승폭(TWh)", "country": "국가"})
st.plotly_chart(bar_fig, use_container_width=True)

# 1위 국가 추이
top_growth_country = growth_df.iloc[0]["country"]
st.success(f"가장 상승폭이 큰 국가: **{top_growth_country}**")

cdf = period_df[period_df["country"] == top_growth_country]
line_fig = px.line(cdf, x="year", y="solar_energy",
                   labels={"solar_energy": "태양광 발전량(TWh)", "year": "연도"},
                   title=f"{top_growth_country}의 태양광 발전량 변화 (2000~2025)")
st.plotly_chart(line_fig, use_container_width=True)

# 분석 내용 (직접 조사한 결과를 서술)
st.subheader("💡 급격한 성장 요인 분석")
st.markdown(f"""
**{top_growth_country}**의 태양광 발전량이 급격히 증가한 배경을 분석하면 다음과 같다.

**1. 국민 인식의 변화**  
기후위기에 대한 인식이 높아지면서 재생에너지 수용도가 상승하였다.

**2. 급격한 산업화와 전력 수요 증가**  
산업 성장에 따라 전력 수요가 늘었고, 이를 친환경 에너지로 충당하려는
흐름이 태양광 확대로 이어졌다.

**3. 기술 발전과 설치 비용 하락**  
태양광 패널 가격이 크게 하락하면서 대규모 보급이 가능해졌다.

**4. 정부 정책과 투자**  
보조금, 세제 혜택, 탄소중립 목표 등이 성장을 가속화하였다.

*(위 내용은 예시입니다. 실제 그래프의 변화 시점과 자료를 함께 조사해
구체적인 근거를 들어 작성하세요.)*
""")

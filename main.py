import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="국가별 태양광 발전 현황", page_icon="🌞", layout="wide")

# ---------- 디자인(CSS) ----------
st.markdown("""
<style>
/* 전체 배경: 부드러운 크림색 → 살구색 그라데이션 */
.stApp {
    background: linear-gradient(180deg, #FFF8EE 0%, #FFF0DB 100%);
}

/* 상단 헤더 박스 */
.sun-header {
    background: linear-gradient(135deg, #FFE3B3 0%, #FBC98E 100%);
    padding: 32px 24px;
    border-radius: 24px;
    text-align: center;
    box-shadow: 0 4px 16px rgba(220, 160, 90, 0.25);
    margin-bottom: 24px;
}
.sun-header h1 {
    color: #8A5A1E;
    margin: 0;
    font-size: 2.2rem;
}
.sun-header p {
    color: #A9762F;
    margin-top: 8px;
    font-size: 1.05rem;
}

/* 소제목 색상 */
h2, h3 {
    color: #B5701E !important;
}

/* expander 박스 톤 맞추기 */
div[data-testid="stExpander"] {
    background-color: #FFFDF8;
    border: 1px solid #F2D9B0;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------- 헤더 ----------
st.markdown("""
<div class="sun-header">
    <h1>🌞 국가별 태양광 발전 에너지 사용량</h1>
    <p>따뜻한 햇살처럼 퍼져나가는 전 세계 태양광 에너지의 흐름을 살펴보세요</p>
</div>
""", unsafe_allow_html=True)

# ---------- 데이터 ----------
@st.cache_data
def load_data():
    df = pd.read_csv("solar-energy-consumption.csv")
    df = df.dropna(subset=["Code"])
    df = df[df["Code"].str.len() == 3]
    df = df[~df["Code"].str.startswith("OWID_")]
    return df

df = load_data()
latest_year = int(df["Year"].max())
latest_df = df[df["Year"] == latest_year]

# ---------- 지도 ----------
st.subheader(f"🗺️ {latest_year}년 기준 국가별 태양광 발전량 (TWh)")

# 부드러운 태양 느낌의 커스텀 색상 스케일 (연한 크림 → 차분한 주황)
sun_scale = [
    [0.0, "#FFF3DC"],
    [0.25, "#FCD89B"],
    [0.5, "#F7B45C"],
    [0.75, "#E8893B"],
    [1.0, "#C25E1E"],
]

fig = px.choropleth(
    latest_df,
    locations="Code",
    color="Solar",
    hover_name="Entity",
    color_continuous_scale=sun_scale,
    labels={"Solar": "태양광 발전량(TWh)"},
)
fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    paper_bgcolor="rgba(0,0,0,0)",   # 배경 투명 → 페이지 색과 어울림
    geo=dict(bgcolor="rgba(0,0,0,0)"),
)
st.plotly_chart(fig, use_container_width=True)

# ---------- 상위 5개국 ----------
st.subheader("🏆 태양광 발전 상위 5개국")
top5 = latest_df.sort_values("Solar", ascending=False).head(5)

# 순위를 보기 좋게 카드처럼 나열
medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
cols = st.columns(5)
for col, medal, (_, row) in zip(cols, medals, top5.iterrows()):
    col.markdown(f"""
    <div style="background:#FFFDF8; border:1px solid #F2D9B0;
                border-radius:14px; padding:14px; text-align:center;">
        <div style="font-size:1.6rem;">{medal}</div>
        <div style="color:#8A5A1E; font-weight:bold;">{row['Entity']}</div>
        <div style="color:#C25E1E;">{row['Solar']:.1f} TWh</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")  # 여백

# 각 국가 상세 추이
for _, row in top5.iterrows():
    with st.expander(f"{row['Entity']} 의 연도별 추이 보기"):
        country_df = df[df["Entity"] == row["Entity"]]
        line_fig = px.line(
            country_df, x="Year", y="Solar",
            labels={"Solar": "태양광 발전량(TWh)", "Year": "연도"},
            title=f"{row['Entity']} 연도별 태양광 발전량",
        )
        line_fig.update_traces(line_color="#E8893B")  # 따뜻한 주황 선
        line_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,250,240,0.5)",
        )
        st.plotly_chart(line_fig, use_container_width=True)

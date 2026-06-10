import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="국가별 태양광 발전 현황", page_icon="🌞", layout="wide")

# ---------- 디자인(CSS) ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #FFF8EE 0%, #FFF0DB 100%);
}
.sun-header {
    background: linear-gradient(135deg, #FFE3B3 0%, #FBC98E 100%);
    padding: 32px 24px; border-radius: 24px; text-align: center;
    box-shadow: 0 4px 16px rgba(220, 160, 90, 0.25); margin-bottom: 24px;
}
.sun-header h1 { color: #8A5A1E; margin: 0; font-size: 2.2rem; }
.sun-header p { color: #A9762F; margin-top: 8px; font-size: 1.05rem; }
h2, h3 { color: #B5701E !important; }
div[data-testid="stExpander"] {
    background-color: #FFFDF8; border: 1px solid #F2D9B0; border-radius: 14px;
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

# ---------- ISO 3코드 → 2코드 매핑 (라이브러리 불필요) ----------
# 주요 국가만 있어도 충분하지만, 폭넓게 넣어둠
CODE3_TO_2 = {
    "CHN": "cn", "USA": "us", "IND": "in", "JPN": "jp", "DEU": "de",
    "ESP": "es", "ITA": "it", "AUS": "au", "BRA": "br", "FRA": "fr",
    "KOR": "kr", "GBR": "gb", "NLD": "nl", "MEX": "mx", "TUR": "tr",
    "VNM": "vn", "ZAF": "za", "CHL": "cl", "POL": "pl", "GRC": "gr",
    "CAN": "ca", "TWN": "tw", "CZE": "cz", "BEL": "be", "PRT": "pt",
    "HUN": "hu", "ISR": "il", "AUT": "at", "CHE": "ch", "EGY": "eg",
    "PAK": "pk", "UKR": "ua", "ROU": "ro", "ARG": "ar", "DNK": "dk",
    "ARE": "ae", "SAU": "sa", "BGR": "bg", "JOR": "jo", "THA": "th",
}

def flag_url(code3):
    """ISO 3코드 → flagcdn.com 국기 이미지 URL"""
    code2 = CODE3_TO_2.get(code3)
    if code2:
        return f"https://flagcdn.com/w40/{code2}.png"
    return None

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

sun_scale = [
    [0.0, "#FFF3DC"], [0.25, "#FCD89B"], [0.5, "#F7B45C"],
    [0.75, "#E8893B"], [1.0, "#C25E1E"],
]

fig = px.choropleth(
    latest_df,
    locations="Code",
    color="Solar",
    hover_name="Entity",
    hover_data={"Solar": ":.2f", "Code": False},
    color_continuous_scale=sun_scale,
    labels={"Solar": "태양광 발전량(TWh)"},
)
fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    paper_bgcolor="rgba(0,0,0,0)",
    geo=dict(bgcolor="rgba(0,0,0,0)"),
)
st.plotly_chart(fig, use_container_width=True)

# ---------- 상위 5개국 (국기 이미지 카드) ----------
st.subheader("🏆 태양광 발전 상위 5개국")
top5 = latest_df.sort_values("Solar", ascending=False).head(5)

medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
cols = st.columns(5)
for col, medal, (_, row) in zip(cols, medals, top5.iterrows()):
    url = flag_url(row["Code"])
    flag_img = f'<img src="{url}" width="48" style="border:1px solid #E0C9A0; border-radius:4px;">' if url else "🏳️"
    col.markdown(f"""
    <div style="background:#FFFDF8; border:1px solid #F2D9B0;
                border-radius:14px; padding:14px; text-align:center;">
        <div style="font-size:1.4rem;">{medal}</div>
        <div style="margin:8px 0;">{flag_img}</div>
        <div style="color:#8A5A1E; font-weight:bold;">{row['Entity']}</div>
        <div style="color:#C25E1E;">{row['Solar']:.1f} TWh</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------- 각 국가 상세 추이 ----------
for _, row in top5.iterrows():
    with st.expander(f"{row['Entity']} 의 연도별 추이 보기"):
        country_df = df[df["Entity"] == row["Entity"]]
        line_fig = px.line(
            country_df, x="Year", y="Solar",
            labels={"Solar": "태양광 발전량(TWh)", "Year": "연도"},
            title=f"{row['Entity']} 연도별 태양광 발전량",
        )
        line_fig.update_traces(line_color="#E8893B")
        line_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,250,240,0.5)",
        )
        st.plotly_chart(line_fig, use_container_width=True)

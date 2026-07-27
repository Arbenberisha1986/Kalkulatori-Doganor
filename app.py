import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Kalkulatori Doganor", page_icon="📦", layout="centered")

# ---------------------------------------------------------------------------
# STIL (CSS)
# ---------------------------------------------------------------------------
st.markdown("""
    <style>
    .res-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #007BFF;
        margin-bottom: 15px;
    }
    .big-font { font-size: 30px !important; font-weight: bold; color: #1f2937; }
    .small-font { font-size: 16px !important; font-weight: 600; color: #374151; }
    .field-label { font-size: 14px; color: #6b7280; margin-bottom: -8px; }
    .active-field {
        background-color: #dbeafe;
        border-radius: 8px;
        padding: 4px 10px;
        font-weight: 600;
        color: #1d4ed8;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# KONFIGURIMI I KATEGORIVE (dogana %, TVSH %)
# Ndrysho ose shto kategori sipas nevojës.
# ---------------------------------------------------------------------------
KATEGORITE = {
    "Standarde (10% / 10%)": {"dogana": 0.10, "tvsh": 0.10},
    "Ushqim (0% / 10%)":     {"dogana": 0.00, "tvsh": 0.10},
    "Elektronikë (5% / 10%)": {"dogana": 0.05, "tvsh": 0.10},
    "Tekstil (10% / 10%)":   {"dogana": 0.10, "tvsh": 0.10},
    "Personalizuar":         {"dogana": None, "tvsh": None},
}

# ---------------------------------------------------------------------------
# GJENDJA E SESIONIT (session_state)
# ---------------------------------------------------------------------------
defaults = {
    "c_str": "",          # çmimi si tekst (për tastierën)
    "t_str": "",           # transporti si tekst
    "fusha": "Çmimi",       # fusha aktive e përzgjedhur
    "rezultat": None,       # rezultati i fundit i llogaritur
    "historiku": [],        # historiku i llogaritjeve
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


def parse_input(s: str) -> float:
    """Kthen tekstin në numër në mënyrë të sigurt (pa u rrëzuar)."""
    s = (s or "").strip().rstrip(".")
    if s in ("", "-", "."):
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0


def shto_shifer(fusha_key: str, val: str):
    """Përditëson tekstin e fushës aktive, duke lejuar vetëm një pikë dhjetore."""
    current = st.session_state[fusha_key]
    if val == "⌫":
        st.session_state[fusha_key] = current[:-1]
    elif val == "." and "." in current:
        return  # nuk lejohet më shumë se një pikë dhjetore
    else:
        st.session_state[fusha_key] = current + val


st.title("📦 Kalkulatori Doganor")

col1, col2 = st.columns([1, 1])

# ---------------------------------------------------------------------------
# KOLONA E MAJTË: hyrjet dhe rezultati
# ---------------------------------------------------------------------------
with col1:
    kategoria = st.selectbox("Kategoria e mallit:", list(KATEGORITE.keys()))
    ratet = KATEGORITE[kategoria]

    if ratet["dogana"] is None:
        c1, c2 = st.columns(2)
        rt_dogana = c1.number_input("Dogana (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.5) / 100
        rt_tvsh = c2.number_input("TVSH (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.5) / 100
    else:
        rt_dogana = ratet["dogana"]
        rt_tvsh = ratet["tvsh"]
        st.caption(f"Norma e aplikuar: Dogana {rt_dogana*100:.0f}% · TVSH {rt_tvsh*100:.0f}%")

    fusha = st.radio("Zgjidh fushën për tastierë:", ("Çmimi", "Transporti"), horizontal=True)
    st.session_state.fusha = fusha

    c = parse_input(st.session_state.c_str)
    t = parse_input(st.session_state.t_str)

    st.markdown('<p class="field-label">Çmimi (€)</p>', unsafe_allow_html=True)
    st.markdown(
        f'<span class="{"active-field" if fusha=="Çmimi" else ""}" style="font-size:22px;">'
        f'{st.session_state.c_str or "0"}</span>', unsafe_allow_html=True
    )
    st.markdown('<p class="field-label">Transporti (€)</p>', unsafe_allow_html=True)
    st.markdown(
        f'<span class="{"active-field" if fusha=="Transporti" else ""}" style="font-size:22px;">'
        f'{st.session_state.t_str or "0"}</span>', unsafe_allow_html=True
    )

    if st.button("🧮 Llogarit Tani", use_container_width=True, type="primary"):
        dogana = (c + t) * rt_dogana
        tvsh = (c + t + dogana) * rt_tvsh
        total = c + t + dogana + tvsh

        st.session_state.rezultat = {
            "kategoria": kategoria,
            "cmimi": c,
            "transporti": t,
            "dogana": dogana,
            "tvsh": tvsh,
            "total": total,
        }
        st.session_state.historiku.append({
            "Koha": datetime.now().strftime("%H:%M:%S"),
            "Kategoria": kategoria,
            "Çmimi (€)": round(c, 2),
            "Transporti (€)": round(t, 2),
            "Dogana (€)": round(dogana, 2),
            "TVSH (€)": round(tvsh, 2),
            "Total (€)": round(total, 2),
        })

    if st.session_state.rezultat:
        r = st.session_state.rezultat
        st.markdown(f"""
            <div class="res-box">
                <p>Gjithsej për t'u paguar:</p>
                <p class="big-font">{r['total']:,.2f} €</p>
                <hr>
                <p class="small-font">Dogana: {r['dogana']:,.2f} € &nbsp;|&nbsp; TVSH: {r['tvsh']:,.2f} €</p>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# KOLONA E DJATHTË: tastiera
# ---------------------------------------------------------------------------
with col2:
    st.subheader("⌨️ Tastiera")
    st.caption(f"Duke shkruar në: **{st.session_state.fusha}**")

    fusha_key = "c_str" if st.session_state.fusha == "Çmimi" else "t_str"

    grid = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], [".", "0", "⌫"]]
    for row in grid:
        cols = st.columns(3)
        for i, val in enumerate(row):
            if cols[i].button(val, key=f"key_{val}_{i}_{fusha_key}", use_container_width=True):
                shto_shifer(fusha_key, val)
                st.rerun()

    if st.button("🗑️ Pastro Gjithçka", use_container_width=True):
        st.session_state.c_str = ""
        st.session_state.t_str = ""
        st.session_state.rezultat = None
        st.rerun()

# ---------------------------------------------------------------------------
# HISTORIKU
# ---------------------------------------------------------------------------
if st.session_state.historiku:
    st.divider()
    st.subheader("📋 Historiku i Llogaritjeve")
    df = pd.DataFrame(st.session_state.historiku)
    st.dataframe(df, use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Shkarko Historikun (CSV)",
        data=csv,
        file_name="historiku_doganor.csv",
        mime="text/csv",
        use_container_width=True,
    )

    if st.button("🧹 Fshi Historikun", use_container_width=True):
        st.session_state.historiku = []
        st.rerun()

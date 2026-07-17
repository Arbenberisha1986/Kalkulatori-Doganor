import streamlit as st

st.set_page_config(page_title="Kalkulatori i Doganës", layout="wide")

if "cmimi_str" not in st.session_state: st.session_state.cmimi_str = ""
if "transporti_str" not in st.session_state: st.session_state.transporti_str = ""
if "fusha_aktive" not in st.session_state: st.session_state.fusha_aktive = "cmimi"

st.title("📦 Kalkulatori i Doganës dhe TVSH-së")
st.write("Plotësoni të dhënat duke përdorur tastierën virtuale anash.")

col_left, col_right = st.columns([2, 1])

with col_left:
    fusha = st.radio("Zgjidhni fushën për tastierën:", ("Çmimi i produktit", "Kosto e transportit"), horizontal=True)
    st.session_state.fusha_aktive = "cmimi" if fusha == "Çmimi i produktit" else "transporti"
    
    val_c = float(st.session_state.cmimi_str) if st.session_state.cmimi_str else 0.0
    val_t = float(st.session_state.transporti_str) if st.session_state.transporti_str else 0.0
    
    cmimi = st.number_input("Çmimi i produktit (€)", value=val_c, format="%.2f")
    transporti = st.number_input("Kosto e transportit (€)", value=val_t, format="%.2f")
    
    if st.button("Llogarit"):
        total = (cmimi + transporti) * 1.21 # Shembull thjeshtuar
        st.success(f"Gjithsej: {total:.2f} €")

with col_right:
    st.subheader("⌨️ Tastiera Virtuale")
    def shto(k):
        if st.session_state.fusha_aktive == "cmimi": st.session_state.cmimi_str += k
        else: st.session_state.transporti_str += k
    
    c1, c2, c3 = st.columns(3)
    if c1.button("1"): shto("1"); st.rerun()
    if c2.button("2"): shto("2"); st.rerun()
    if c3.button("3"): shto("3"); st.rerun()
    # Shto pjesën tjetër të rreshtave këtu nëse dëshiron
    if st.button("Pastro"): 
        if st.session_state.fusha_aktive == "cmimi": st.session_state.cmimi_str = ""
        else: st.session_state.transporti_str = ""
        st.rerun()

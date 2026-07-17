import streamlit as st

# Dizajni i përgjithshëm
st.set_page_config(page_title="Kalkulatori Doganor", page_icon="📦", layout="centered")

# CSS për të rregulluar pamjen (Stili modern)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    div.stButton > button { width: 100%; border-radius: 10px; height: 3em; background-color: #007BFF; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Inicializimi i gjendjes
if "c_str" not in st.session_state: st.session_state.c_str = ""
if "t_str" not in st.session_state: st.session_state.t_str = ""
if "fusha" not in st.session_state: st.session_state.fusha = "Çmimi"

st.title("📦 Kalkulatori Doganor")
st.markdown("---") # Vijë ndarëse për dizajn

# Pjesa e plotësimit
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📝 Të dhënat")
    fusha = st.radio("Zgjidhni fushën për tastierën:", ("Çmimi", "Transporti"), horizontal=True)
    st.session_state.fusha = fusha
    
    c = st.number_input("Çmimi i produktit (€)", value=float(st.session_state.c_str or 0.0), format="%.2f")
    t = st.number_input("Kosto e transportit (€)", value=float(st.session_state.t_str or 0.0), format="%.2f")
    
    if st.button("Llogarit"):
        dogana = (c + t) * 0.10
        tvsh = (c + t + dogana) * 0.10
        total = c + t + dogana + tvsh
        
        st.markdown("---")
        st.subheader("📊 Rezultatet")
        # Përdorimi i st.metric për dizajn profesional
        st.metric("Gjithsej për t'u paguar", f"{total:.2f} €")
        st.caption(f"Dogana: {dogana:.2f} € | TVSH: {tvsh:.2f} €")

with col2:
    st.subheader("⌨️ Tastiera")
    # Logjika e butonave e njëjtë, por më kompakte
    grid = [["1","2","3"], ["4","5","6"], ["7","8","9"], [".","0","⌫"]]
    for row in grid:
        cols = st.columns(3)
        for i, val in enumerate(row):
            if cols[i].button(val, key=f"btn_{val}"):
                if val == "⌫":
                    if st.session_state.fusha == "Çmimi": st.session_state.c_str = st.session_state.c_str[:-1]
                    else: st.session_state.t_str = st.session_state.t_str[:-1]
                else:
                    if st.session_state.fusha == "Çmimi": st.session_state.c_str += val
                    else: st.session_state.t_str += val
                st.rerun()

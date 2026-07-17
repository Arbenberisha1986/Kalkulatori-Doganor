import streamlit as st

st.set_page_config(page_title="Kalkulatori Doganor", layout="centered")

# CSS për dizajn më të pastër
st.markdown("""
    <style>
    .res-box { background-color: #f0f2f6; padding: 20px; border-radius: 15px; border-left: 5px solid #007BFF; }
    .big-font { font-size: 30px !important; font-weight: bold; color: #1f2937; }
    .small-font { font-size: 18px !important; font-weight: bold; color: #374151; }
    </style>
    """, unsafe_allow_html=True)

if "c_str" not in st.session_state: st.session_state.c_str = ""
if "t_str" not in st.session_state: st.session_state.t_str = ""
if "fusha" not in st.session_state: st.session_state.fusha = "Çmimi"

st.title("📦 Kalkulatori Doganor")

col1, col2 = st.columns([1, 1])

with col1:
    fusha = st.radio("Zgjidh fushën:", ("Çmimi", "Transporti"), horizontal=True)
    st.session_state.fusha = fusha
    c = st.number_input("Çmimi (€)", value=float(st.session_state.c_str or 0.0), format="%.2f")
    t = st.number_input("Transporti (€)", value=float(st.session_state.t_str or 0.0), format="%.2f")
    
    if st.button("Llogarit Tani", use_container_width=True):
        dogana = (c + t) * 0.10
        tvsh = (c + t + dogana) * 0.10
        total = c + t + dogana + tvsh
        
        # Rezultatet me dizajn të theksuar
        st.markdown(f"""
            <div class="res-box">
                <p>Gjithsej për t'u paguar:</p>
                <p class="big-font">{total:,.2f} €</p>
                <hr>
                <p class="small-font">Dogana: {dogana:,.2f} € | TVSH: {tvsh:,.2f} €</p>
            </div>
        """, unsafe_allow_html=True)

with col2:
    st.subheader("⌨️ Tastiera")
    grid = [["1","2","3"], ["4","5","6"], ["7","8","9"], [".","0","⌫"]]
    for row in grid:
        cols = st.columns(3)
        for i, val in enumerate(row):
            if cols[i].button(val):
                if val == "⌫":
                    if st.session_state.fusha == "Çmimi": st.session_state.c_str = st.session_state.c_str[:-1]
                    else: st.session_state.t_str = st.session_state.t_str[:-1]
                else:
                    if st.session_state.fusha == "Çmimi": st.session_state.c_str += val
                    else: st.session_state.t_str += val
                st.rerun()

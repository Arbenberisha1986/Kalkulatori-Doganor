import streamlit as st

st.set_page_config(page_title="Kalkulatori i Importit", layout="wide")

if "cmimi_str" not in st.session_state: st.session_state.cmimi_str = ""
if "transporti_str" not in st.session_state: st.session_state.transporti_str = ""
if "fusha_aktive" not in st.session_state: st.session_state.fusha_aktive = "cmimi"

st.title("📦 Kalkulatori i Doganës dhe TVSH-së")
st.write("Ky mjet ju ndihmon të llogaritni shpenzimet e importit. Mund të shkruani direkt ose të përdorni tastierën virtuale anash.")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📝 Plotësoni të dhënat")
    
    st.markdown("**Zgjidhni fushën ku dëshironi të shkruani:**")
    fusha = st.radio("Fusha për tastierën virtuale:", ("Çmimi i produktit", "Kosto e transportit"), horizontal=True)
    st.session_state.fusha_aktive = "cmimi" if fusha == "Çmimi i produktit" else "transporti"

    cmimi = st.number_input("Çmimi i produktit (€)", min_value=0.0, value=float(st.session_state.cmimi_str or 0.0), format="%.2f")
    transporti = st.number_input("Kosto e transportit (€)", min_value=0.0, value=float(st.session_state.transporti_str or 0.0), format="%.2f")

    if st.button("Llogarit", type="primary", use_container_width=True):
        vlerat_baze = cmimi + transporti
        dogana = vlerat_baze * 0.10
        tvsh = (vlerat_baze + dogana) * 0.10
        st.subheader("📊 Rezultatet")
        c1, c2, c3 = st.columns(3)
        c1.metric("Dogana (10%)", f"{dogana:.2f} €")
        c2.metric("TVSH (10%)", f"{tvsh:.2f} €")
        c3.metric("Gjithsej", f"{vlerat_baze + dogana + tvsh:.2f} €")

with col_right:
    st.subheader("⌨️ Tastiera Virtuale")
    st.write(f"Po shkruani te: **{fusha}**")
    # (Pjesa tjetër e butonave mbetet e njëjtë, thjesht kam ndryshuar tekstet lart)

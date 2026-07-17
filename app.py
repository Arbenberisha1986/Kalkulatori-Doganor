import streamlit as st

st.set_page_config(page_title="Kalkulatori i Importit", layout="centered")

st.title("📦 Kalkulatori i Importit")

with st.expander("Shto të dhënat e importit", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        cmimi = st.number_input("Çmimi i produktit (€)", min_value=0.0, format="%.2f")
    with col2:
        transporti = st.number_input("Kosto e transportit (€)", min_value=0.0, format="%.2f")

if st.button("Llogarit Koston"):
    vlerat_baze = cmimi + transporti
    dogana = vlerat_baze * 0.10
    tvsh = (vlerat_baze + dogana) * 0.10
    kosto_finale = vlerat_baze + dogana + tvsh
    
    st.divider()
    st.subheader("Rezultatet e Llogaritjes")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Dogana (10%)", f"{dogana:.2f} €")
    c2.metric("TVSH (10%)", f"{tvsh:.2f} €")
    c3.metric("Gjithsej", f"{kosto_finale:.2f} €")
    
    st.success(f"Kostoja përfundimtare: {kosto_finale:.2f} €")

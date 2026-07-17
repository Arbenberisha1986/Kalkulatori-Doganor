import streamlit as st

st.title("Kalkulatori i Doganës dhe TVSH-së")
st.write("Ky është mjeti yt për llogaritjen e kostove të importit në Kosovë.")

# Kutitë për futjen e të dhënave
cmimi = st.number_input("Shkruaj çmimin e produktit (€):", min_value=0.0, format="%.2f")
transporti = st.number_input("Shkruaj koston e transportit (€):", min_value=0.0, format="%.2f")

if st.button("Llogarit"):
    vlerat_baze = cmimi + transporti
    dogana = vlerat_baze * 0.10
    tvsh = (vlerat_baze + dogana) * 0.10
    kosto_finale = vlerat_baze + dogana + tvsh
    
    st.success(f"Kostoja përfundimtare: {kosto_finale:.2f}€")
    st.write(f"Dogana (10%): {dogana:.2f}€")
    st.write(f"TVSH (10%): {tvsh:.2f}€")

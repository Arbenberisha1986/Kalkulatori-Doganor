import streamlit as st

st.title("📦 Kalkulatori i Importit")

# Seksioni i Inputit
col_left, col_right = st.columns([2, 1])

with col_left:
    with st.expander("Shto të dhënat", expanded=True):
        cmimi = st.number_input("Çmimi (€)", min_value=0.0, format="%.2f")
        transporti = st.number_input("Transporti (€)", min_value=0.0, format="%.2f")
        
        if st.button("Llogarit"):
            vlerat_baze = cmimi + transporti
            dogana = vlerat_baze * 0.10
            tvsh = (vlerat_baze + dogana) * 0.10
            kosto_finale = vlerat_baze + dogana + tvsh
            
            st.divider()
            st.metric("Gjithsej për t'u paguar", f"{kosto_finale:.2f} €")

# Kalkulatori anash (Numpad për ata që s'kanë tastierë)
with col_right:
    st.write("⌨️ Përdor mausin:")
    cols = st.columns(3)
    # Këtu mund të shtosh butona për të ndihmuar futjen e të dhënave 
    # ose thjesht për të bërë një pamje më teknike
    if st.button("Pastro fushat"):
        st.rerun()
    st.info("Kliko fushat e sipërme për të shkruar.")

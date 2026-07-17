import streamlit as st

st.set_page_config(page_title="Kalkulatori i Importit", layout="wide")

# Inicializimi i session state për të ruajtur vlerat e klikuara
if "cmimi_str" not in st.session_state:
    st.session_state.cmimi_str = ""
if "transporti_str" not in st.session_state:
    st.session_state.transporti_str = ""
if "fusha_aktive" not in st.session_state:
    st.session_state.fusha_aktive = "cmimi"  # Mund të jetë 'cmimi' ose 'transporti'

st.title("📦 Kalkulatori i Importit me Numpad")
st.write("Mund të shkruash direkt me tastierë, ose të përdorësh mausin për të klikuar numrat anash.")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📝 Plotëso të dhënat")
    
    st.markdown("**Zgjidh cilën fushë dëshiron të plotësosh me mausin anash:**")
    fusha = st.radio(
        "Fusha aktive për Numpad:", 
        ("Çmimi i produktit", "Kosto e transportit"), 
        index=0 if st.session_state.fusha_aktive == "cmimi" else 1,
        horizontal=True
    )
    
    if fusha == "Çmimi i produktit":
        st.session_state.fusha_aktive = "cmimi"
    else:
        st.session_state.fusha_aktive = "transporti"

    # Konverto vlerat nga teksti i klikuar në numra decimale
    val_cmimi = 0.0
    if st.session_state.cmimi_str:
        try:
            val_cmimi = float(st.session_state.cmimi_str)
        except ValueError:
            val_cmimi = 0.0
            
    val_trans = 0.0
    if st.session_state.transporti_str:
        try:
            val_trans = float(st.session_state.transporti_str)
        except ValueError:
            val_trans = 0.0

    # Fushat e inputit - shfaqin vlerat nga numpad por lejojnë edhe shkrimin direkt
    cmimi = st.number_input("Çmimi i produktit (€)", min_value=0.0, value=val_cmimi, format="%.2f", key="cmimi_input")
    transporti = st.number_input("Kosto e transportit (€)", min_value=0.0, value=val_trans, format="%.2f", key="transporti_input")

    if st.button("Llogarit Koston", type="primary", use_container_width=True):
        # Nëse përdoruesi ka shkruar direkt në fusha, përdorim ato vlera
        c_final = cmimi if cmimi > 0 else val_cmimi
        t_final = transporti if transporti > 0 else val_trans
        
        vlerat_baze = c_final + t_final
        dogana = vlerat_baze * 0.10
        tvsh = (vlerat_baze + dogana) * 0.10
        kosto_finale = vlerat_baze + dogana + tvsh
        
        st.divider()
        st.subheader("📊 Rezultatet e Llogaritjes")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Dogana (10%)", f"{dogana:.2f} €")
        c2.metric("TVSH (10%)", f"{tvsh:.2f} €")
        c3.metric("Gjithsej për t'u paguar", f"{kosto_finale:.2f} €")
        
        st.success(f"Kostoja përfundimtare e importit është: {kosto_finale:.2f} €")

# Seksioni i kalkulatorit me butona (Numpad) anash
with col_right:
    st.subheader("⌨️ Kalkulatori (Numpad)")
    st.write(f"Po shkruan te: **{fusha}**")
    
    # Shfaq vlerën që po shtypet
    vlera_shfaqje = st.session_state.cmimi_str if st.session_state.fusha_aktive == "cmimi" else st.session_state.transporti_str
    if not vlera_shfaqje:
        vlera_shfaqje = "0"
    st.info(f"Vlera e shtypur: {vlera_shfaqje} €")

    def shto_karakter(char):
        fusha_aktive = st.session_state.fusha_aktive
        if fusha_aktive == "cmimi":
            if char == "." and "." in st.session_state.cmimi_str:
                return
            st.session_state.cmimi_str += char
        else:
            if char == "." and "." in st.session_state.transporti_str:
                return
            st.session_state.transporti_str += char

    def fshij_karakter():
        fusha_aktive = st.session_state.fusha_aktive
        if fusha_aktive == "cmimi":
            st.session_state.cmimi_str = st.session_state.cmimi_str[:-1]
        else:
            st.session_state.transporti_str = st.session_state.transporti_str[:-1]

    def pastro_gjithcka():
        if st.session_state.fusha_aktive == "cmimi":
            st.session_state.cmimi_str = ""
        else:
            st.session_state.transporti_str = ""

    # Ndërtimi i pamjes së butonave të kalkulatorit
    n_col1, n_col2, n_col3 = st.columns(3)
    
    with n_col1:
        if st.button("1", key="num1", use_container_width=True): shto_karakter("1"); st.rerun()
        if st.button("4", key="num4", use_container_width=True): shto_karakter("4"); st.rerun()
        if st.button("7", key="num7", use_container_width=True): shto_karakter("7"); st.rerun()
        if st.button(".", key="num_dot", use_container_width=True): shto_karakter("."); st.rerun()
        
    with n_col2:
        if st.button("2", key="num2", use_container_width=True): shto_karakter("2"); st.rerun()
        if st.button("5", key="num5", use_container_width=True): shto_karakter("5"); st.rerun()
        if st.button("8", key="num8", use_container_width=True): shto_karakter("8"); st.rerun()
        if st.button("0", key="num0", use_container_width=True): shto_karakter("0"); st.rerun()
        
    with n_col3:
        if st.button("3", key="num3", use_container_width=True): shto_karakter("3"); st.rerun()
        if st.button("6", key="num6", use_container_width=True): shto_karakter("6"); st.rerun()
        if st.button("9", key="num9", use_container_width=True): shto_karakter("9"); st.rerun()
        if st.button("⌫", key="num_back", use_container_width=True): fshij_karakter(); st.rerun()

    if st.button("Fshij të gjitha (C)", key="num_clear", use_container_width=True, type="secondary"):
        pastro_gjithcka()
        st.rerun()

import streamlit as st
from streamlit_option_menu import option_menu
from Inicio import main
from Configuraciones import main1
st.set_page_config(page_title="Productividad en el Área", page_icon=":snake:", layout="wide")
with st.sidebar:
            selected = option_menu(
                menu_title="Menú",  # required
                options=["Inicio", "Registros", "Acerca de"],  # required
                icons=["house", "gear", "tencent-qq"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
            )

if selected == "Inicio":
    main()
if selected == "Registros":
    main1()
if selected == "Acerca de":
    st.title(f"Hola mundo!")

import streamlit as st
import pandas as pd
import os

def main():
    st.title("Cargar y visualizar datos Excel")

    # Subir múltiples archivos Excel
    uploaded_files = st.sidebar.file_uploader("Subir archivos Excel", type=["xlsx", "xls"], accept_multiple_files=True)

    if uploaded_files:
        # Obtener los nombres de los archivos sin extensión
        file_names = [os.path.splitext(file.name)[0] for file in uploaded_files]

        # Seleccionar archivo con un select box
        selected_file_name = st.sidebar.selectbox("Selecciona un archivo para visualizar", file_names, key='file_selector')

        # Obtener el índice del archivo seleccionado
        selected_file_index = file_names.index(selected_file_name)

        # Cargar el archivo seleccionado
        df = pd.read_excel(uploaded_files[selected_file_index])

        # Segundo select box para elegir entre Implantación y QA
        data_type = st.sidebar.selectbox("Selecciona el tipo de datos", ['Implantación', 'QA'])

        if data_type == 'Implantación':
            # Mostrar todas las columnas excepto las relacionadas con QA
            selected_columns = [col for col in df.columns if col not in ['asignado_qa', 'entregables_qa', 'plan_pruebas']]
            df_filtered = df[selected_columns]
            # Obtener nombres disponibles en asignado_im
            available_names = df_filtered['asignado_im'].unique()
        elif data_type == 'QA':
            # Mostrar solo las columnas relacionadas con QA
            df_filtered = df[['asignado_qa', 'proyecto', 'plan_pruebas', 'entregables_qa']]
            # Obtener nombres disponibles en asignado_qa
            available_names = df_filtered['asignado_qa'].unique()
        else:
            # En caso de una opción no válida
            st.sidebar.error("Selecciona un tipo de datos válido.")
            return

        # Tercer multiselect para filtrar por el nombre de alguien
        selected_names = st.sidebar.multiselect(f"Selecciona nombres de {data_type}", available_names)

        # Filtrar el DataFrame por los nombres seleccionados
        if data_type == 'Implantación':
            df_filtered_by_names = df_filtered[df_filtered['asignado_im'].isin(selected_names)]
        else:
            df_filtered_by_names = df_filtered[df_filtered['asignado_qa'].isin(selected_names)]

        # Mostrar los datos filtrados en una tabla
        st.dataframe(df_filtered_by_names)

if __name__ == "__main__":
    main()
           

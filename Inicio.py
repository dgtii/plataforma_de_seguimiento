import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Productividad en el Área", page_icon=":snake:", layout="wide")

def generar_grafica_barras(df_selection, selected_name):
    # Eliminar la columna de productividad si existe
    df_selection = df_selection.drop(columns=['productividad'], errors='ignore')

    # Gráfica de barras para el progreso
    fig = px.bar(
        df_selection,
        x=df_selection.index,
        y=df_selection.columns,
        labels={"value": "Progreso", "variable": "Indicador"}
    )
    fig.update_xaxes(title_text="")
    fig.update_layout(
        xaxis=dict(tickangle=-45),
        barmode='group',
        margin=dict(l=20, r=20, t=50, b=50),
    )
    st.plotly_chart(fig, use_container_width=True)



def generar_tacometro(productividad_value, selected_name):
    # Tacómetro con el valor de productividad
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=productividad_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Productividad de {selected_name}"},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [0, 50], 'color': "lightblue"},
                   {'range': [50, 100], 'color': "lightcoral"}],
               'threshold': {
                   'line': {'color': "red", 'width': 4},
                   'thickness': 0.75, 'value': 70}
               }
    ))
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("Cargar plantillas")

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
        data_type = st.sidebar.selectbox("Selecciona un área", ['Implantación', 'QA'])

        if data_type == 'Implantación':
            # Rellenar valores NaN con cero
            df[['asf_f15_1', 'asf_f15_2', 'asf_f17_1', 'asf_f17_2']] = df[['asf_f15_1', 'asf_f15_2', 'asf_f17_1', 'asf_f17_2']].fillna(0)
            # Sumar y promediar las columnas específicas
            df['asf_f15'] = df[['asf_f15_1', 'asf_f15_2']].sum(axis=1) / 2
            df['asf_f17'] = df[['asf_f17_1', 'asf_f17_2']].sum(axis=1) / 2
            # Calcular la nueva columna 'productividad'
            df['productividad'] = (df['asf_f15'] + df['asf_f17']) / 2 * 0.5 + df['despliegues'] * 0.5
            # Mostrar solo las columnas específicas para Implantación
            selected_columns = [col for col in df.columns if col not in ['asignado_qa', 'entregables_qa', 'plan_pruebas', 'asf_f15_1', 'asf_f15_2', 'asf_f17_1', 'asf_f17_2']]
            df_filtered = df[selected_columns]
            # Obtener nombres disponibles en asignado_im
            available_names = df_filtered['asignado_im'].unique()
        elif data_type == 'QA':
            # Mostrar solo las columnas relacionadas con QA
            df_filtered = df[['asignado_qa', 'proyecto', 'plan_pruebas', 'entregables_qa']]
            # Calcular la nueva columna 'productividad' para QA
            df_filtered['productividad'] = (df_filtered['entregables_qa'] + df_filtered['plan_pruebas']) / 2
            # Obtener nombres disponibles en asignado_qa
            available_names = df_filtered['asignado_qa'].unique()
        else:
            # En caso de una opción no válida
            st.sidebar.error("Selecciona un área.")
            return

        # Tercer multiselect para filtrar por el nombre de alguien
        selected_names = st.sidebar.multiselect(f"Selecciona a una persona de {data_type}", available_names)

        # Verificar si al menos un nombre está seleccionado
        if not selected_names:
            st.sidebar.warning("Selecciona al menos a una persona.")
            return

        # Ajustar el tamaño de la figura según la cantidad de nombres seleccionados
        num_selected_names = len(selected_names)

        # Crear subplots horizontalmente
        columns = st.columns(num_selected_names)

        # Iterar sobre cada nombre seleccionado
        for i, selected_name in enumerate(selected_names):
            with columns[i]:
                st.subheader(f"Progreso de {selected_name}")

                # Filtrar el DataFrame por el nombre seleccionado
                if data_type == 'Implantación':
                    df_individual = df_filtered[df_filtered['asignado_im'] == selected_name]
                else:
                    df_individual = df_filtered[df_filtered['asignado_qa'] == selected_name]

                # Excluir columnas no deseadas y convertir a tipo numérico
                columns_to_exclude = ['asignado_im', 'proyecto'] if data_type == 'Implantación' else ['asignado_qa', 'proyecto']
                df_individual_numeric = df_individual.drop(columns=columns_to_exclude)
                df_individual_numeric = df_individual_numeric.apply(pd.to_numeric, errors='coerce')

                # Calcular el promedio de cada columna
                column_means_individual = df_individual_numeric.mean()

                # Obtener el valor de productividad
                productividad_value = column_means_individual.get('productividad', 0)

                # Mostrar la gráfica de barras
                generar_grafica_barras(pd.DataFrame(column_means_individual).transpose(), selected_name)

                # Mostrar el tacómetro
                generar_tacometro(productividad_value, selected_name)

if __name__ == "__main__":
    main()


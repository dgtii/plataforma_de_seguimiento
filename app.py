import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Productividad en el Área", page_icon=":snake:", layout="wide")

# obtener datos del excel
df = pd.read_excel('recursos.xlsx')
columnas_deseadas = ["Recurso", "P_Asistencia", "Pruebas UAT", "ASD-F15", "ASD-F17","Capacitación", "Total"]
df = df.loc[0:3, columnas_deseadas]  # Limitar el df

#st.dataframe(df)
st.sidebar.header("Filtros:")
recurso = st.sidebar.multiselect(
    "Seleccione personal:",
    options=df["Recurso"].unique(),
    default=df["Recurso"].unique()
)
# Sidebar para seleccionar el tipo de gráfico
st.sidebar.header("Tema:")
grafico_barras = st.sidebar.checkbox("Indicadores de Productividad", value=True)
grafico_tacometro = st.sidebar.checkbox("Avance Total")
grafico_dona = st.sidebar.checkbox("Asistencia")
#poder cambiar los filtros: nota
df_selection = df.query(
    "Recurso == @recurso"
)
# diccionario
nombres_preferidos = {
    "Cabrera Gutiérrez, Jesús": "Jesús 😳",
    "Celaya de la Serna, Blanca del Carmen": "Blanquita 😾",
    "Cortes Villegas, Ana Paola": "Pao 🤷‍♀️",
    "Fonseca Gómez, Marycruz": "Mary 😃"
}
df_selection["Recurso"] = df_selection["Recurso"].replace(nombres_preferidos)
if df_selection.empty:
    st.warning("No se encontraron datos con los filtro seleccionados ):")
    st.stop() # para que no se rompa la wea

st.title("😈 Productividad en el Área")
st.markdown("##")

average_rating = round(df["Total"].mean(), 1)
max_rating = 100  # Puntuación máxima posible

# Calcula el número de estrellas en una escala de 0 a 5
num_estrellas = round((average_rating / max_rating) * 5)

# Limita el número de estrellas a un máximo de 5
num_estrellas = min(num_estrellas, 5)

# Convierte el número de estrellas en el formato de estrella ":star:"
star_rating = ":star:" * num_estrellas

st.subheader("Promedio de productividad:")
st.subheader(f"{average_rating}% {star_rating}")

st.markdown("""---""")

st.write("### Resultados:")
#st.write(df_selection)
# Función para generar la gráfica interactiva basada en el filtro seleccionado
def generar_grafica(df_selection):
    # Generar la gráfica interactiva con Plotly Express
    fig = px.bar(
        df_selection,
        x="Recurso",
        y=["Pruebas UAT", "ASD-F15", "ASD-F17", "Capacitación"],
        title="Indicadores de productividad",
        labels={"value": "Valor del Indicador de Productividad", "variable": "Indicador"}
    )
    fig.update_xaxes(title_text="")

    # Personalizar diseño de la gráfica
    fig.update_layout(
        xaxis=dict(tickangle=-45),
        barmode='group',
        margin=dict(l=20, r=20, t=50, b=50)  # Configurar márgenes
    )
    
    # Mostrar la gráfica interactiva
    st.plotly_chart(fig, use_container_width=True)  # Ajustar al ancho del contenedor

# Llama a la función para generar la gráfica basada en los recursos seleccionados
#generar_grafica(df_selection)

# Función para generar gráficos tipo tacómetro para el progreso de cada empleado
def generar_graficos_tacometro(df_selection):
    figuras = []
    for _, row in df_selection.iterrows():
        total = row["Total"]  # Obtener el valor de la columna Total para el empleado actual
        
        # Calcular el progreso (respetando el máximo de 100)
        progreso = min(total, 100)
        
        # Crear el gráfico tipo tacómetro para el progreso del empleado
        fig = go.Figure()

        # Configurar el gráfico tipo tacómetro
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=progreso,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": f"Progreso para: {row['Recurso']}"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "green"},
                "steps": [
                    {"range": [0, 100], "color": "lightgray"}
                ],
            }
        ))

        # Configurar el diseño del gráfico
        fig.update_layout(height=230, margin=dict(l=20, r=20, t=50, b=50))
        
        # Agregar la figura del gráfico a la lista
        figuras.append(fig)

    return figuras

# Llama a la función para generar gráficos tipo tacómetro para los empleados seleccionados
#figuras_tacometro = generar_graficos_tacometro(df_selection)

# Mostrar los gráficos tipo tacómetro en una fila

# Función para generar gráficos de barras para la asistencia de cada empleado
# Función para generar gráficos de dona para la asistencia de cada empleado
def generar_graficos_dona(df_selection):
    figuras = []
    for _, row in df_selection.iterrows():
        asistencia = row["P_Asistencia"]
        fig_dona = px.pie(
            values=[asistencia, 21 - asistencia],
            names=["Asistencia", "Restante"],
            title=f'Asistencia de {row["Recurso"]}',
            hole=0.6,
            labels={"value": "P_Asistencia"},
        )
        figuras.append(fig_dona)

    return figuras

# Llama a la función para generar gráficos de dona para la asistencia de los empleados seleccionados
#figuras_dona = generar_graficos_dona(df_selection)

# Mostrar los gráficos de dona en una fila horizontal

# Lógica para mostrar los gráficos según las selecciones
if grafico_barras:
    generar_grafica(df_selection)

if grafico_tacometro:
    figuras_tacometro = generar_graficos_tacometro(df_selection)
    columnas = st.columns(len(figuras_tacometro))
    for i, figura in enumerate(figuras_tacometro):
        columnas[i].plotly_chart(figura, use_container_width=True)

if grafico_dona:
    figuras_dona = generar_graficos_dona(df_selection)
    columnas = st.columns(len(figuras_dona))
    for i, figura in enumerate(figuras_dona):
        columnas[i].plotly_chart(figura, use_container_width=True)
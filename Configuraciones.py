# Importar las dependencias
import pandas as pd
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def main1():
    # Configurar el alcance y las credenciales
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

    # Crear el cliente de Google Sheets
    client = build('sheets', 'v4', credentials=creds)

    # ID de tu hoja de Google Sheets
    spreadsheet_id = '19ti7YGTgi-cJa7F8bnG3BzwfFSUbkwRarneeYitfWmA'

    # Nombre de la hoja dentro de la hoja de cálculo
    sheet_name = 'data'

    # Rango de celdas que deseas obtener (A2:D3)
    range_name = 'A2:G'

    # Obtener los datos de las celdas especificadas de la hoja de Google Sheets
    result = client.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=f'{sheet_name}!{range_name}').execute()

    # Obtener los valores de las celdas
    values = result.get('values', [])

    # Inicializar las selecciones y el valor del slider
    selected_user = None
    selected_column = None
    new_value = 0

    # Si hay datos, mostrarlos en Streamlit y permitir la actualización
    if values:
        # Crear un DataFrame con los datos
        df = pd.DataFrame(values, columns=['Actividad', 'Asignado', 'Estatus', 'Progreso UAT', 'Progreso ASF-F15', 'Progreso ASD-F17', 'Progreso Capacitacion'])

        # Widget para seleccionar un usuario
        selected_user = st.selectbox('Selecciona una actividad:', df['Actividad'].tolist())

        # Obtener el índice de la fila correspondiente al usuario seleccionado
        user_index = df.index[df['Actividad'] == selected_user].tolist()[0]
        # Mostrar Asignado y Estatus correspondiente a la actividad seleccionada
        asignado = df.iloc[user_index]['Asignado']
        estatus = df.iloc[user_index]['Estatus']
        st.write(f'Asignado: {asignado}')
        st.write(f'Estatus: {estatus}')

        # Widget para seleccionar una columna
        selected_column = st.selectbox('Selecciona una columna para modificar:', ['Progreso UAT', 'Progreso ASF-F15', 'Progreso ASD-F17', 'Progreso Capacitacion'])

        # Obtener el índice de la columna correspondiente a la contraseña seleccionada
        column_index = df.columns.get_loc(selected_column)

        # Widget de control deslizante para seleccionar un número del 0 al 100
        new_value = st.slider('Selecciona un valor del 0 al 100:', 0, 100)

        # Botón de confirmación
        if st.button('Confirmar y Actualizar'):
            # Actualizar el valor en el DataFrame en función de las selecciones del usuario
            df.iloc[user_index, column_index] = new_value

            # Actualizar el valor en la hoja de Google Sheets
            update_range = f"{sheet_name}!{chr(65 + column_index)}{user_index + 2}"  # +2 porque los datos comienzan en la fila 2 y chr(65) es 'A'
            update_values = [[new_value]]  # Los valores que deseas establecer
            update_body = {
                'values': update_values
            }
            update_result = client.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, body=update_body, valueInputOption='RAW').execute()

            # Mostrar el mensaje de confirmación
            st.success('Datos actualizados exitosamente.')


    # Mostrar el DataFrame actualizado
    st.write('Datos actualizados:')
    st.write(df)

if __name__ == "__main__":
    main1()            
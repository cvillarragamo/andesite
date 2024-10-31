import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
data=pd.read_csv(r'data\estandar.csv')
data['date'] = pd.to_datetime(data['date'])
outliers=pd.read_csv(r'data\outliers.csv')

# Función de la página "Historia y Valores Normales"
def pagina_historia_valores():
    st.markdown("<h1 style='color: #4CAF50;'>Historia y Valores Normales</h1>", unsafe_allow_html=True)
    st.write("En esta sección encontrarás los valores históricos de la operación y los valores normales.")
    
    # Cálculo del heatmap
    trips_per_day = data.groupby(['truck', 'date']).size().reset_index(name='trips')
    trips_per_day.sort_values(by='trips').tail(5)

    heatmap_data = trips_per_day.pivot(index='truck', columns='date', values='trips')

    height = max(600, 20 * len(data['truck'].unique()))  # Ajuste dinámico para el alto
    custom_scale = [
        [0.0, 'rgb(222,217,226)'],  # valores más bajos
        [0.5, 'rgb(192,185,221)'],  # valores medios
        [1.0, 'rgb(117,201,200)']   # más oscuro para los valores más altos
    ]

    heatmap_fig = px.imshow(heatmap_data,
                    labels=dict(x="Fecha", y="Camión", color="Viajes"),
                    x=heatmap_data.columns.strftime('%Y-%m-%d'),  # Formatea las fechas para visualización
                    aspect="auto",
                    color_continuous_scale=custom_scale,
                    )

    heatmap_fig.update_layout(
        title='Heatmap de Viajes por Camión y Día',
        xaxis_title='Fecha',
        yaxis_title='Camión',
        yaxis={'dtick': 1},
        height=height
    )

    #### Agrupar por pala y por dia ###
    grouped_data = data.groupby(['day_of_week', 'loader']).size().reset_index(name='total_trips')

    # Ordenar los días de la semana
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    grouped_data['day_of_week'] = pd.Categorical(grouped_data['day_of_week'], categories=days_order, ordered=True)

    # Crear el gráfico de barras apiladas
    loader_bar_fig = px.bar(
        grouped_data,
        x='day_of_week',
        y='total_trips',
        color='loader',
        title='Total de Viajes por Día de la Semana y Tipo de Pala',
        labels={'total_trips': 'Total de Viajes', 'day_of_week': 'Día de la Semana'},
        text='total_trips'
    )

    # Configurar el diseño
    loader_bar_fig.update_layout(barmode='stack', xaxis_title='Día de la Semana', yaxis_title='Total de Viajes')

    ##################

    # Dividir en dos columnas
    col1, col2 = st.columns([2, 1])  # La primera columna es más grande (2:1)

    # Primera columna: Gráfico del heatmap
    with col1:
        st.plotly_chart(heatmap_fig)

    # Segunda columna: Texto adicional o tablas
    with col2:
        st.subheader("Descripción")
        st.markdown(
            """
            Los valores normales representan el rango esperado durante la operación habitual. 
            Este gráfico te muestra las tendencias diarias de los camiones, con los viajes realizados por día.
            """
        )
        st.markdown(
            """
            Puedes observar si algún camión está realizando más o menos viajes de lo esperado en un día 
            específico, lo que podría ser útil para el análisis de desempeño.
            """
        )

        st.plotly_chart(loader_bar_fig)  



def pagina_valores_criticos():
    st.markdown("<h1>Valores Críticos (Outliers)</h1>", unsafe_allow_html=True)
    st.write("Aquí se muestran los valores fuera del rango esperado (outliers).")
    
    # Usamos columnas para presentar mejor los datos
    st.warning("¡Atención! Se han detectado los siguientes valores fuera de rango:")
    critical_values = pd.DataFrame({
        'Fecha': ['2023-10-10', '2023-10-11', '2023-10-12'],
        'Valor': [120, 150, 180]
    })
    st.dataframe(critical_values)

def pagina_monitoreo_kpis():
    st.markdown("<h1>Monitoreo de Operación y KPIs</h1>", unsafe_allow_html=True)
    st.write("Esta sección te permite hacer un monitoreo en tiempo real de los indicadores clave de operación (KPIs).")

    # Usamos columnas para distribuir los KPIs
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric(label="Producción", value="800 Tn", delta="+5%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric(label="Tiempo de operación", value="10 horas", delta="-2%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric(label="Eficiencia", value="92%", delta="+3%")
        st.markdown('</div>', unsafe_allow_html=True)

    st.bar_chart([20, 30, 40, 50])

# Creación del panel de navegación en el sidebar
def main():
    st.sidebar.title("Navegación")
    pagina_seleccionada = st.sidebar.radio(
        "Selecciona una página:",
        ("Historia y Valores Normales", "Valores Críticos", "Monitoreo y KPIs")
    )

    # Contenedor principal para aplicar estilo
    with st.container():
        if pagina_seleccionada == "Historia y Valores Normales":
            pagina_historia_valores()
        elif pagina_seleccionada == "Valores Críticos":
            pagina_valores_criticos()
        elif pagina_seleccionada == "Monitoreo y KPIs":
            pagina_monitoreo_kpis()

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
data=pd.read_csv(r'data\estandar.csv')
data['date'] = pd.to_datetime(data['date'])
outliers=pd.read_csv(r'data\outliers.csv')

# Función de la página "analisis de valores"
def dashboard_valores_criticos():
    st.markdown("<h1 style='color: #4CAF50;'>Dashbaord de análsis de valores de performancia</h1>", unsafe_allow_html=True)
    st.write("En esta sección se encontrarian los valores históricos de la operación y los valores que se consideran como de referencia de performancia.")
    
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
    st.plotly_chart(heatmap_fig)
    st.markdown(
        """
        **Descripción:** En el heatmap se observa que existen 9 camiones con un mayor  número de viajes diarios en comparación con el resto de la flota. Es importante evaluar si estos valores podrían establecerse como referencia objetivo para los demás vehículos:

- `CAEX25`
- `CAEX31`
- `CAEX41`
- `CAEX44`
- `CAEX55`
- `CAEX66`
- `CAEX81`
- `CAEX93`
- `CAEX98`

Cabe resaltar que los valores de inactividad tienen valores atípicos que superan las 24 horas de trabajo (_valores menores a 0_), lo cual indica posibles inconsistencias en los registros, que podrían corresponder a errores en la captura o reportes irregulares. 

Al analizar los camiones que presentan estas anomalías, se observa que coinciden con los 9 camiones identificados anteriormente como los que realizan la mayor cantidad de viajes por día. Por lo tanto, es crucial monitorear esta parte de la flota para garantizar la precisión y la fiabilidad de los registros operativos.   """
    )

    #### Agrupar por pala y por dia ###
    
    trucks_n=data.groupby(['truck','date']).sum(numeric_only=True).reset_index()
    trips_per_day = data.groupby(['truck', 'date']).size().reset_index(name='trips')

    trucks=pd.merge(trucks_n,trips_per_day, on = ['truck', 'date'], how='left')
    mean_ton = trucks['ton'].mean()
    std_ton = trucks['ton'].std()
    percentile_25 = trucks['ton'].quantile(0.25)
    percentile_75 = trucks['ton'].quantile(0.75)

# Crear los intervalos y etiquetas para clasificación
    st.markdown("### Frecuencia de Camiones por Nivel de Rendimiento")
    bins = [0, mean_ton - std_ton, percentile_25, mean_ton, percentile_75, float('inf')]
    labels = ['Outlier Bajo', 'Aceptable', 'Promedio', 'Óptimo', 'Outlier Alto']

    trucks['rendimiento'] = pd.cut(trucks['ton'], bins=bins, labels=labels, right=False)
    
    bars = px.histogram(trucks, x='truck', color='rendimiento',
                   title="Frecuencia de Camiones por Nivel de Rendimiento",
                   labels={'truck': 'Camión', 'rendimiento': 'Rendimiento'},
                   category_orders={'rendimiento': ['Outlier Bajo', 'Aceptable', 'Promedio', 'Óptimo', 'Outlier Alto']})


    bars.update_layout(barmode='stack', xaxis_title="Camión", yaxis_title="Frecuencia")
    st.plotly_chart(bars)

    st.markdown(""" 
              -  Algunos camiones, como `CAEX21`, `CAEX22`, y `CAEX30`, tienen una alta proporción de observaciones en las categorías Óptimo y Outlier Alto, lo cual indica que estos camiones suelen operar a un nivel de rendimiento superior al promedio.
En contraste, otros camiones como `CAEX01` y `CAEX07` tienen más registros en las categorías de Outlier Bajo y Aceptable, lo que podría sugerir problemas de rendimiento o que están operando en condiciones subóptimas.

- Camiones como `CAEX58`, `CAEX60`, y `CAEX90` muestran una distribución alta en las categorías Promedio y Óptimo, con menos registros en las categorías de outliers. Esto podría indicar que estos camiones tienen un rendimiento más estable y predecible.
                """)
    ##################

def Outliers():
    st.markdown("<h1>Outliers</h1>", unsafe_allow_html=True)
    st.write("Aquí se muestran los valores fuera del rango esperado (outliers) y sus patrones")
    
    # Usamos columnas para presentar mejor los datos
    st.warning("¡Atención! Se han detectado los siguientes valores fuera de rango:")
    st.dataframe(outliers)
    

def Dahsboard_Monitoreo():
    st.markdown("<h1>Monitoreo de Operación y KPIs</h1>", unsafe_allow_html=True)
    st.write("Esta sección te permite hacer un monitoreo en tiempo real de los indicadores clave de operación (KPIs).")
    st.warning("¡Atención! ESTA SECCION NO ESTA IMPLEMENTADA. LOS DATO SON FICTICIOS")
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
        ("Dashboard de Análisis de Factores Críticos", "Outliers", "Dashboard de Monitoreo de Rendimiento Diario")
    )

    # Contenedor principal para aplicar estilo
    with st.container():
        if pagina_seleccionada == "Dashboard de Análisis de Factores Críticos":
            dashboard_valores_criticos()
        elif pagina_seleccionada == "Outliers":
            Outliers()
        elif pagina_seleccionada == "Dashboard de Monitoreo de Rendimiento Diario":
            Dahsboard_Monitoreo()

if __name__ == "__main__":
    main()

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Calculadora de Punto de Equilibrio",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://es.linkedin.com/in/pedrociancaglini',
        'Report a bug': "https://es.linkedin.com/in/pedrociancaglini",
        'About': "# Calculadora de Punto de Equilibrio. Esta app es para calcular el punto de *equilibrio* de un negocio!"
    }
)

with st.sidebar:
    logo_url = "https://github.com/peteciank/equilibrium_point/blob/main/img/comercio_salvaje.jpg?raw=true"
    st.sidebar.image(logo_url)

    st.write("En colaboración con: ")
    components.html(
        """
        <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
        <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="large" data-theme="dark" data-type="HORIZONTAL" data-vanity="pedrociancaglini" data-version="v1">
        <a class="badge-base__link LI-simple-link" href="https://es.linkedin.com/in/pedrociancaglini/en?trk=profile-badge"></a></div>
        """,
    height=300,
    )
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 400px !important; # Set the width to your desired value
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Define la función para calcular el punto de equilibrio
def calcular_punto_equilibrio(costo_produccion, costo_marketing, costo_empleados, costo_almacen, tasa_impuestos, costo_reventa, precio_final, num_revendedores):
    costo_total = costo_produccion + costo_marketing + costo_empleados + costo_almacen
    costo_total_con_impuestos = costo_total * (1 + tasa_impuestos / 100)
    ingresos_totales = (precio_final - costo_reventa) * num_revendedores
    punto_equilibrio = costo_total_con_impuestos / (precio_final - costo_reventa) if precio_final - costo_reventa != 0 else 'Indefinido'
    return punto_equilibrio, costo_total_con_impuestos, ingresos_totales

# Diseño de la aplicación Streamlit
st.title('Calculadora del Punto de Equilibrio')

# Diseño con columnas
col1, col2, col3 = st.columns(3)

# Columna 1: Costos
with col1:
    st.subheader('Entradas de Costos')
    with st.expander("Desplegar para detalles de costos"):
        costo_produccion = st.number_input('Costo de Fábrica del Producto', value=5000)
        costo_marketing = st.number_input('Costo de Marketing', value=400000)
        costo_empleados = st.number_input('Costo de Empleados', value=900000)
        costo_almacen = st.number_input('Costo de Almacén', value=200000)
        tasa_impuestos = st.number_input('Tasa de Impuestos (%)', value=0)

# Columna 2: Precios y Revendedores
with col2:
    st.subheader('Canales de Venta')
    with st.expander("Desplegar para detalles de ventas"):
        costo_reventa = st.number_input('Costo de Acceso para Revendedores', value=8000)
        precio_final = st.number_input('Precio Final de Mercado', value=10000)
        num_revendedores = st.number_input('Número de Revendedores', value=200)

# Columna 3: Resultados del Cálculo
with col3:
    st.subheader('Resultados')
    if st.button('Calcular Punto de Equilibrio'):
        punto_equilibrio, costo_total_con_impuestos, ingresos_totales = calcular_punto_equilibrio(
            costo_produccion, costo_marketing, costo_empleados, costo_almacen, tasa_impuestos, costo_reventa, precio_final, num_revendedores
        )

        punto_equilibrio, costo_total_con_impuestos, ingresos_totales = float(punto_equilibrio), float(costo_total_con_impuestos), float(ingresos_totales)

        # f"{x:,}" or format(1234, "8.,1f")    -->    ' 1.234,0'
        st.metric('Punto de Equilibrio:', str(int(f"{punto_equilibrio:,.0f}")) + " Unidades")
        st.metric('Costo Total con Impuestos:', "$ " + "{:,.0f}".format(costo_total_con_impuestos).replace(',', '.')) # str(f"{costo_total_con_impuestos:'.,0f'}".format(x).replace(',', '.')))
        st.metric('Ingresos Totales:', "$ " + "{:,.0f}".format(ingresos_totales).replace(',', '.'))

# Graficar el gráfico de líneas
import plotly.graph_objects as go

if 'punto_equilibrio' in locals() and isinstance(punto_equilibrio, (int, float)):
    quantity = np.arange(0, int(punto_equilibrio) * 2)
    cost_line = costo_total_con_impuestos * np.ones_like(quantity)
    revenue_line = (precio_final - costo_reventa) * quantity

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=quantity, y=cost_line, mode='lines', name='Total Costos con Impuestos'))
    fig.add_trace(go.Scatter(x=quantity, y=revenue_line, mode='lines', name='Ingreso Margen Total'))
    fig.add_shape(type="line", x0=punto_equilibrio, y0=min(min(cost_line), min(revenue_line)), x1=punto_equilibrio, y1=max(max(cost_line), max(revenue_line)), line=dict(color="red", width=2, dash="dash"), name="Equilibrium Point")

    fig.update_layout(title='Analisis de Costos y Facturación',
                      xaxis_title='Cantidad',
                      yaxis_title='Monto')

    st.plotly_chart(fig)


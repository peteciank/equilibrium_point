import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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
        costo_produccion = st.number_input('Costo de Fábrica del Producto', value=5000.0)
        costo_marketing = st.number_input('Costo de Marketing', value=400000.0)
        costo_empleados = st.number_input('Costo de Empleados', value=900000.0)
        costo_almacen = st.number_input('Costo de Almacén', value=200000.0)
        tasa_impuestos = st.number_input('Tasa de Impuestos (%)', value=0.0)

# Columna 2: Precios y Revendedores
with col2:
    st.subheader('Canales de Venta')
    with st.expander("Desplegar para detalles de ventas"):
        costo_reventa = st.number_input('Costo de Acceso para Revendedores', value=8000.0)
        precio_final = st.number_input('Precio Final de Mercado', value=10000.0)
        num_revendedores = st.number_input('Número de Revendedores', value=200)

# Columna 3: Resultados del Cálculo
with col3:
    st.subheader('Resultados')
    if st.button('Calcular Punto de Equilibrio'):
        punto_equilibrio, costo_total_con_impuestos, ingresos_totales = calcular_punto_equilibrio(
            costo_produccion, costo_marketing, costo_empleados, costo_almacen, tasa_impuestos, costo_reventa, precio_final, num_revendedores
        )
        st.write('Punto de Equilibrio:', punto_equilibrio)
        st.write('Costo Total con Impuestos:', costo_total_con_impuestos)
        st.write('Ingresos Totales:', ingresos_totales)

# Graficar el gráfico de líneas
if 'punto_equilibrio' in locals() and isinstance(punto_equilibrio, (int, float)):
    fig, ax = plt.subplots()
    cantidad = np.arange(0, int(punto_equilibrio) * 2)
    linea_costo = costo_total_con_impuestos * np.ones_like(cantidad)
    linea_ingresos = (precio_final - costo_reventa) * cantidad
    ax.plot(cantidad, linea_costo, label='Costo Total con Impuestos')
    ax.plot(cantidad, linea_ingresos, label='Ingresos Totales')
    ax.axvline(x=punto_equilibrio, color='r', linestyle='--', label='Punto de Equilibrio')
    ax.legend()
    st.pyplot(fig)


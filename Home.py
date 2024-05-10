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

    st.write("in collaboration with: ")
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

# Define the function to calculate the point of equilibrium
def calculate_equilibrium(product_cost, marketing_cost, employee_cost, warehouse_cost, tax_rate, reseller_cost, final_price, num_resellers):
    total_cost = product_cost + marketing_cost + employee_cost + warehouse_cost
    total_cost_with_tax = total_cost * (1 + tax_rate / 100)
    total_revenue = (final_price - reseller_cost) * num_resellers
    equilibrium_point = total_cost_with_tax / (final_price - reseller_cost) if final_price - reseller_cost != 0 else 'Undefined'
    return equilibrium_point, total_cost_with_tax, total_revenue

# Streamlit app layout
st.title('Equilibrium Point Calculator')

# Layout with columns
col1, col2, col3 = st.columns(3)

# Column 1: Costs
with col1:
    st.subheader('Cost Inputs')
    with st.expander("Expand for Cost Details"):
        product_cost = st.number_input('Cost of Product Factory', value=5000)
        marketing_cost = st.number_input('Cost of Marketing', value=400000)
        employee_cost = st.number_input('Cost of Employees', value=900000)
        warehouse_cost = st.number_input('Cost of Warehouse', value=200000)
        tax_rate = st.number_input('Tax Rate (%)', value=0.0)

# Column 2: Prices and Resellers
with col2:
    st.subheader('Sales Channels')
    with st.expander("Expand for Sales Details"):
        reseller_cost = st.number_input('Reseller Access Cost', value=8000)
        final_price = st.number_input('Final Market Price', value=10000)
        num_resellers = st.number_input('Number of Resellers', value=200)

# Column 3: Calculation Results
with col3:
    st.subheader('Results')
    if st.button('Calculate Equilibrium Point'):
        equilibrium_point, total_cost_with_tax, total_revenue = calculate_equilibrium(
            product_cost, marketing_cost, employee_cost, warehouse_cost, tax_rate, reseller_cost, final_price, num_resellers
        )
        # f"{x:,}" or format(1234, "8.,1f")    -->    ' 1.234,0'
        st.metric('Equilibium Point:', str(int(f"{equilibrium_point:,.0f}")) + " Unidades")
        st.metric('Total cost with Taxes:', "$ " + "{:,.0f}".format(total_cost_with_tax).replace(',', '.')) # str(f"{costo_total_con_impuestos:'.,0f'}".format(x).replace(',', '.')))
        st.metric('Total margin income:', "$ " + "{:,.0f}".format(total_revenue).replace(',', '.'))

# Plotting the line graph
import plotly.graph_objects as go

if 'equilibrium_point' in locals() and isinstance(equilibrium_point, (int, float)):
    quantity = np.arange(0, int(equilibrium_point) * 2)
    cost_line = total_cost_with_tax * np.ones_like(quantity)
    revenue_line = (final_price - reseller_cost) * quantity

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=quantity, y=cost_line, mode='lines', name='Total Cost with Tax'))
    fig.add_trace(go.Scatter(x=quantity, y=revenue_line, mode='lines', name='Total Revenue'))
    fig.add_shape(type="line", x0=equilibrium_point, y0=min(min(cost_line), min(revenue_line)), x1=equilibrium_point, y1=max(max(cost_line), max(revenue_line)), line=dict(color="red", width=2, dash="dash"), name="Equilibrium Point")

    fig.update_layout(title='Cost and Revenue Analysis',
                      xaxis_title='Quantity',
                      yaxis_title='Amount')

    st.plotly_chart(fig)


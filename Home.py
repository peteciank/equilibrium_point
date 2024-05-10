import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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
        product_cost = st.number_input('Cost of Product Factory', value=5000.0)
        marketing_cost = st.number_input('Cost of Marketing', value=400000.0)
        employee_cost = st.number_input('Cost of Employees', value=900000.0)
        warehouse_cost = st.number_input('Cost of Warehouse', value=200000.0)
        tax_rate = st.number_input('Tax Rate (%)', value=0.0)

# Column 2: Prices and Resellers
with col2:
    st.subheader('Sales Channels')
    with st.expander("Expand for Sales Details"):
        reseller_cost = st.number_input('Reseller Access Cost', value=8000.0)
        final_price = st.number_input('Final Market Price', value=10000.0)
        num_resellers = st.number_input('Number of Resellers', value=200)

# Column 3: Calculation Results
with col3:
    st.subheader('Results')
    if st.button('Calculate Equilibrium Point'):
        equilibrium_point, total_cost_with_tax, total_revenue = calculate_equilibrium(
            product_cost, marketing_cost, employee_cost, warehouse_cost, tax_rate, reseller_cost, final_price, num_resellers
        )
        st.write('Equilibrium Point:', equilibrium_point)
        st.write('Total Cost with Tax:', total_cost_with_tax)
        st.write('Total Revenue:', total_revenue)

# Plotting the line graph
if 'equilibrium_point' in locals() and isinstance(equilibrium_point, (int, float)):
    fig, ax = plt.subplots()
    quantity = np.arange(0, int(equilibrium_point) * 2)
    cost_line = total_cost_with_tax * np.ones_like(quantity)
    revenue_line = (final_price - reseller_cost) * quantity
    ax.plot(quantity, cost_line, label='Total Cost with Tax')
    ax.plot(quantity, revenue_line, label='Total Revenue')
    ax.axvline(x=equilibrium_point, color='r', linestyle='--', label='Equilibrium Point')
    ax.legend()
    st.pyplot(fig)



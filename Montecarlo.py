import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def monte_carlo_simulation(num_simulations, years, discount_rate, base_sales, sales_deviation,
                           variable_cost_pct, fixed_costs, tax_rate, initial_investment):
    npv_simulations = []
    for _ in range(num_simulations):
        simulated_sales = np.random.normal(base_sales, sales_deviation * base_sales, years)
        net_cash_flows = []
        for s in simulated_sales:
            revenue = s
            costs = (variable_cost_pct * s) + fixed_costs
            gross_profit = revenue - costs
            taxes = gross_profit * tax_rate
            net_cash_flow = gross_profit - taxes
            net_cash_flows.append(net_cash_flow)
        npv = sum(net_cash_flows[t] / (1 + discount_rate) ** (t + 1) for t in range(years)) - initial_investment
        npv_simulations.append(npv)
    return np.array(npv_simulations)

st.title("📊 Project Valuation & NPV Simulation Tool with Monte Carlo")
st.subheader("By: Diego Gonzalez Farias")

st.header("🔧 How to Use the Tool")
st.markdown("""
1. Enter the project parameters such as sales, costs, tax rate, and investment.
2. Set the number of Monte Carlo simulations to run.
3. Click **Run Simulation** to generate the NPV distribution.
4. Analyze the results, including the average NPV and percentiles for risk assessment.
""")

st.header("🔧 Input Parameters")
num_simulations = st.number_input("Number of Simulations", min_value=1000, max_value=50000, value=10000, step=1000)
years = st.number_input("Project Years", min_value=1, max_value=20, value=5)
discount_rate = st.slider("Discount Rate (%)", min_value=0.01, max_value=0.2, value=0.1, step=0.01)
base_sales = st.number_input("Base Sales ($K)", min_value=100, max_value=10000, value=1000, step=100)
sales_deviation = st.slider("Sales Deviation (%)", min_value=0.01, max_value=0.5, value=0.2, step=0.01)
variable_cost_pct = st.slider("Variable Costs (% of Sales)", min_value=0.1, max_value=0.9, value=0.4, step=0.05)
fixed_costs = st.number_input("Annual Fixed Costs ($K)", min_value=0, max_value=5000, value=200, step=50)
tax_rate = st.slider("Tax Rate (%)", min_value=0.1, max_value=0.5, value=0.3, step=0.05)
initial_investment = st.number_input("Initial Investment ($K)", min_value=500, max_value=10000, value=2000, step=100)

if st.button("Run Simulation"):
    npv_simulations = monte_carlo_simulation(num_simulations, years, discount_rate, base_sales,
                                             sales_deviation, variable_cost_pct, fixed_costs,
                                             tax_rate, initial_investment)
    npv_mean = np.mean(npv_simulations)
    percentile_5 = np.percentile(npv_simulations, 5)
    percentile_95 = np.percentile(npv_simulations, 95)

    st.subheader("📈 Simulation Results")
    st.metric(label="Average NPV", value=f"${npv_mean:,.2f}")
    st.metric(label="5% Percentile (Pessimistic Scenario)", value=f"${percentile_5:,.2f}")
    st.metric(label="95% Percentile (Optimistic Scenario)", value=f"${percentile_95:,.2f}")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(npv_simulations, bins=50, color="blue", alpha=0.6, density=True)
    ax.axvline(npv_mean, color="red", linestyle="dashed", linewidth=2, label=f"Mean: ${npv_mean:,.2f}")
    ax.axvline(percentile_5, color="black", linestyle="dashed", linewidth=2, label=f"5% Percentile: ${percentile_5:,.2f}")
    ax.axvline(percentile_95, color="green", linestyle="dashed", linewidth=2, label=f"95% Percentile: ${percentile_95:,.2f}")
    ax.set_title("NPV Distribution - Monte Carlo Simulation")
    ax.set_xlabel("NPV (Thousands of dollars)")
    ax.set_ylabel("Frequency")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

st.markdown("---")
st.markdown("[🔗 Connect with Diego Gonzalez](https://www.linkedin.com/in/diego-gonzalez-farias-248870234/)")

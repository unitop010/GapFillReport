import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine, text

# Database connection
DB_URI = "sqlite:///stock_data.db"

# Function to fetch available symbols from the database
def get_symbols_from_db(db_uri):
    engine = create_engine(db_uri)
    with engine.connect() as conn:
        # Use `sqlalchemy.text` to wrap the query
        result = conn.execute(text("SELECT DISTINCT symbol FROM stock_data;"))
        symbols = [row[0] for row in result.fetchall()]
    return symbols

# Function to fetch data from the API
def fetch_gap_fill_data(symbol):
    api_url = f"https://skilled-tahr-coherent.ngrok-free.app/gap_fill/?symbol={symbol}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data for {symbol}: {response.text}")
        return None

# Function to plot the stacked bar chart
def plot_gap_fill_stacked(insights):
    # Data preparation
    categories = ['Gap Up', 'Gap Down']
    filled = [
        float(insights["gap_up_filled"]["percentage"].strip('%')),
        float(insights["gap_down_filled"]["percentage"].strip('%'))
    ]
    not_filled = [
        float(insights["gap_up_not_filled"]["percentage"].strip('%')),
        float(insights["gap_down_not_filled"]["percentage"].strip('%'))
    ]

    # Bar chart parameters
    bar_width = 0.5
    index = np.arange(len(categories))

    # Plot the stacked bars
    fig, ax = plt.subplots()
    ax.bar(index, filled, bar_width, label='Filled', color='blue')
    ax.bar(index, not_filled, bar_width, bottom=filled, label='Not Filled', color='black')

    # Add text annotations
    for i in range(len(categories)):
        ax.text(index[i], filled[i] / 2, f"{filled[i]}%", ha='center', color='white', fontsize=10)
        ax.text(index[i], filled[i] + not_filled[i] / 2, f"{not_filled[i]}%", ha='center', color='white', fontsize=10)

    # Chart customization
    ax.set_title("Gap Fill Insights", fontsize=14)
    ax.set_xticks(index)
    ax.set_xticklabels(categories, fontsize=12)
    ax.set_ylabel("Percentage", fontsize=12)
    ax.legend(loc="upper right")
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    return fig

# Streamlit App
st.title("Gap Fill Insights Dashboard")
st.sidebar.header("Select Options")

# Fetch available symbols from the database
symbols = get_symbols_from_db(DB_URI)
if symbols:
    selected_symbol = st.sidebar.selectbox("Select Stock Symbol", symbols)

    # Fetch and display data
    if st.sidebar.button("Fetch Data"):
        data = fetch_gap_fill_data(selected_symbol)
        if data:
            st.subheader(f"Insights for {selected_symbol}")
            st.write(data)  # Display raw JSON data (optional)
            fig = plot_gap_fill_stacked(data)
            st.pyplot(fig)
else:
    st.sidebar.warning("No symbols found in the database.")

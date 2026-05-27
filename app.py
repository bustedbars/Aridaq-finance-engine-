import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

st.set_page_config(page_title="ARIDAQ ENGINE", layout="wide")

st.markdown("""
<style>
.main { background-color: #0d0d0c; color: #f7f7f7; }
h1, h2, h3 { color: #ffb3d1; font-family: monospace; }
.stButton>button { background-color: #ffb3d1; color: black; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("ARIDAQ ENGINE")
st.caption("NP-Hard Capital Allocation System")

# --- DATA ---
default_projects = pd.DataFrame([
    {"ID": "P1", "Cost": 25, "NPV": 18, "Risk": 4},
    {"ID": "P2", "Cost": 35, "NPV": 32, "Risk": 6},
    {"ID": "P3", "Cost": 18, "NPV": 12, "Risk": 3},
    {"ID": "P4", "Cost": 40, "NPV": 38, "Risk": 8},
    {"ID": "P5", "Cost": 20, "NPV": 15, "Risk": 5},
])

budget = st.number_input("Budget", 10, 500, 100)
df = st.data_editor(default_projects, num_rows="dynamic")

run = st.button("RUN MODEL")

if run:
    start = time.time()

    costs = df["Cost"].values
    profits = df["NPV"].values
    ids = df["ID"].values
    n = len(df)

    best_score = -1
    best_mask = None

    # --- CORE NP-HARD ENGINE (UNCHANGED LOGIC STYLE) ---
    for mask in range(1, 1 << n):
        total_cost = 0
        total_profit = 0

        for i in range(n):
            if mask & (1 << i):
                total_cost += costs[i]
                total_profit += profits[i]

        if total_cost > budget:
            continue

        score = total_profit  # KEEP YOUR CORE SIMPLIFIED LOGIC HERE

        if score > best_score:
            best_score = score
            best_mask = mask

    selected = []
    total_cost = 0
    total_profit = 0

    for i in range(n):
        if best_mask & (1 << i):
            selected.append(ids[i])
            total_cost += costs[i]
            total_profit += profits[i]

    end = time.time()

    # --- INVESTOR OUTPUT LAYER ---
    result = {
        "selected": selected,
        "profit": float(total_profit),
        "cost": float(total_cost),
        "roi": float(total_profit / total_cost) if total_cost else 0,
        "runtime_sec": end - start
    }

    st.success("OPTIMAL PORTFOLIO FOUND")

    st.json(result)

    # chart
    fig = px.bar(df, x="ID", y="NPV", color="Cost")
    st.plotly_chart(fig, use_container_width=True)

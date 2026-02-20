import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="OEE Dashboard", layout="wide")

st.title("📊 OEE Monitoring Dashboard")

st.sidebar.header("Input Production Data")

planned_time = st.sidebar.number_input("Loading time (min)", 1.0)
downtime = st.sidebar.number_input("Downtime (min)", 0.0)
ideal_cycle = st.sidebar.number_input("Ideal Cycle Time (min/kg)", 0.0)
total_output = st.sidebar.number_input("Total Output (kg)", 0)
defect_output = st.sidebar.number_input("Defect Output(kg)", 0)

# Initialize session state
if "availability" not in st.session_state:
    st.session_state.availability = None
if "performance" not in st.session_state:
    st.session_state.performance = None
if "quality" not in st.session_state:
    st.session_state.quality = None


st.subheader("Calculate Components")

colA, colP, colQ, colO = st.columns(4)

# AVAILABILITY BUTTON
if colA.button("Calculate Availability"):
    operating_time = planned_time - downtime
    st.session_state.availability = (
        operating_time / planned_time if planned_time > 0 else 0
    )

# PERFORMANCE BUTTON
if colP.button("Calculate Performance"):
    operating_time = planned_time - downtime
    st.session_state.performance = (
        (ideal_cycle * total_output) / operating_time
        if operating_time > 0 else 0
    )

# QUALITY BUTTON
if colQ.button("Calculate Quality"):
    good_output = total_output - defect_output
    st.session_state.quality = (
        good_output / total_output if total_output > 0 else 0
    )

# OEE BUTTON
if colO.button("Calculate OEE"):
    if (
        st.session_state.availability is not None and
        st.session_state.performance is not None and
        st.session_state.quality is not None
    ):
        st.session_state.oee = (
            st.session_state.availability *
            st.session_state.performance *
            st.session_state.quality
        )
    else:
        st.warning("Calculate A, P, and Q first!")


# DISPLAY RESULTS
st.subheader("Results")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Availability", 
            f"{st.session_state.availability:.2%}" 
            if st.session_state.availability is not None else "-")

col2.metric("Performance", 
            f"{st.session_state.performance:.2%}" 
            if st.session_state.performance is not None else "-")

col3.metric("Quality", 
            f"{st.session_state.quality:.2%}" 
            if st.session_state.quality is not None else "-")

if "oee" in st.session_state:
    col4.metric("OEE", f"{st.session_state.oee:.2%}")
else:

    col4.metric("OEE", "-")

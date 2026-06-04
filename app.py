import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Smart Water Treatment Plant Monitoring System",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* Hide Streamlit Menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Background */
.main {
    background-color: #f5f7fa;
}

/* KPI Cards */
.kpi-card {
    background-color: #1f2937;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.15);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# KPI CARD FUNCTION
# =====================================================

def kpi_card(title, value):
    st.markdown(
        f"""
        <div class="kpi-card">
            <h4>{title}</h4>
            <h2>{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# TITLE
# =====================================================

st.markdown("""
# 💧 Smart Water Treatment Plant Monitoring System

### Real-Time Water Quality • Plant Health • Operational Analytics
""")

st.markdown("---")

# =====================================================
# =====================================================
df = pd.read_excel(
    "Data/Smart_Water_Treatment_Dummy_Data.xlsx",
    sheet_name=0
)

df.columns = df.columns.str.strip().str.lower()

st.write("Columns Found:")
st.write(df.columns.tolist())

st.stop()
# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("💧 Smart Water")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Water Quality",
        "Equipment",
        "Analytics"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Water Treatment Monitoring Dashboard")

# =====================================================
# OVERVIEW PAGE
# =====================================================

if page == "Overview":

    st.header("📊Overview")

    plant = st.selectbox(
        "Select Plant",
        sorted(df["plant_id"].unique())
    )

    filtered_df = df[df["plant_id"] == plant]

    # KPIs
    avg_ph = round(filtered_df["ph"].mean(), 2)
    avg_tds = round(filtered_df["tds"].mean(), 2)
    avg_flow = round(filtered_df["flow_rate"].mean(), 2)
    total_records = len(filtered_df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card("Average pH", avg_ph)

    with col2:
        kpi_card("Average TDS", avg_tds)

    with col3:
        kpi_card("Flow Rate", avg_flow)

    with col4:
        kpi_card("Records", total_records)

    st.markdown("<br>", unsafe_allow_html=True)

    # Health Monitor
    st.markdown("### 🏥 Plant Health")

    ph_status = "🟢 Good" if 7 <= avg_ph <= 8.5 else "🔴 Critical"
    tds_status = "🟢 Good" if avg_tds <= 500 else "🔴 High"
    flow_status = "🟢 Normal" if avg_flow >= 200 else "🟡 Low"

    c1, c2, c3 = st.columns(3)

    c1.success(f"pH Status: {ph_status}")
    c2.success(f"TDS Status: {tds_status}")
    c3.success(f"Flow Status: {flow_status}")

    st.markdown("---")

    # Water Quality Score
    quality_score = round(
        (
            (avg_ph / 8.5) * 30 +
            ((500 - min(avg_tds, 500)) / 500) * 35 +
            (min(avg_flow, 300) / 300) * 35
        ),
        1
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric(
            "💧 Water Quality Score",
            f"{quality_score}/100"
        )

    with col2:
        score_df = pd.DataFrame({
            "Category": ["Healthy", "Attention"],
            "Value": [quality_score, 100-quality_score]
        })

        fig_score = px.pie(
            score_df,
            names="Category",
            values="Value",
            hole=0.7
        )

        fig_score.update_layout(
            template="plotly_white",
            height=350,
            showlegend=True
        )

        st.plotly_chart(
            fig_score,
            use_container_width=True
        )

    st.markdown("---")

    st.markdown("### 📈 Water Quality Trends")

    # pH Chart
    fig_ph = px.line(
        filtered_df,
        x="timestamp",
        y="ph",
        title="pH Trend"
    )

    fig_ph.update_layout(
        template="plotly_white",
        height=400
    )

    st.plotly_chart(
        fig_ph,
        use_container_width=True
    )

    # TDS & Flow
    col1, col2 = st.columns(2)

    with col1:

        fig_tds = px.line(
            filtered_df,
            x="timestamp",
            y="tds",
            title="TDS Trend"
        )

        fig_tds.update_layout(
            template="plotly_white",
            height=400
        )

        st.plotly_chart(
            fig_tds,
            use_container_width=True
        )

    with col2:

        fig_flow = px.line(
            filtered_df,
            x="timestamp",
            y="flow_rate",
            title="Flow Rate Trend"
        )

        fig_flow.update_layout(
            template="plotly_white",
            height=400
        )

        st.plotly_chart(
            fig_flow,
            use_container_width=True
        )

# =====================================================
# WATER QUALITY PAGE
# =====================================================

elif page == "Water Quality":

    st.header("💧 Water Quality Analysis")

    plant = st.selectbox(
        "Select Plant",
        sorted(df["plant_id"].unique()),
        key="water_quality"
    )

    filtered_df = df[df["plant_id"] == plant]

    col1, col2, col3 = st.columns(3)

    col1.metric("Maximum pH", round(filtered_df["ph"].max(), 2))
    col2.metric("Maximum TDS", round(filtered_df["tds"].max(), 2))
    col3.metric("Maximum Flow Rate", round(filtered_df["flow_rate"].max(), 2))

    fig = px.scatter(
        filtered_df,
        x="tds",
        y="ph",
        title="pH vs TDS Analysis"
    )

    fig.update_layout(
        template="plotly_white",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# =====================================================
# EQUIPMENT PAGE
# =====================================================

elif page == "Equipment":

    st.header("⚙ Equipment Dashboard")

    equipment_df = pd.DataFrame({
        "Equipment": ["Pump", "Valve", "Motor", "RO Unit", "UV Unit"],
        "Count": [12, 18, 8, 6, 4]
    })

    st.dataframe(
        equipment_df,
        use_container_width=True
    )

    fig = px.bar(
        equipment_df,
        x="Equipment",
        y="Count",
        title="Equipment Distribution"
    )

    fig.update_layout(
        template="plotly_white",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# ANALYTICS PAGE
# =====================================================

elif page == "Analytics":

    st.header("📈 Plant Analytics")

    summary = (
        df.groupby("plant_id")
        .agg({
            "ph": "mean",
            "tds": "mean",
            "flow_rate": "mean"
        })
        .reset_index()
    )

    summary.columns = [
        "Plant ID",
        "Average pH",
        "Average TDS",
        "Average Flow Rate"
    ]

    st.dataframe(
        summary,
        use_container_width=True
    )

    fig1 = px.bar(
        summary,
        x="Plant ID",
        y="Average Flow Rate",
        title="Average Flow Rate by Plant"
    )

    fig1.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

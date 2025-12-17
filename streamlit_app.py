import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

# Get active Snowflake session
session = get_active_session()

# Page configuration
st.set_page_config(
    page_title="Stock Health Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS styling
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    /* Global styling */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Animated gradient title */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradient 3s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
        letter-spacing: -1px;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Subtitle with icon */
    .subtitle {
        color: #4b5563;
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 500;
    }
    
    /* Metric cards styling */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 600;
        color: #6b7280;
    }
    
    [data-testid="metric-container"] {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.8);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
    }
    
    /* DataFrame styling */
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.8);
        background: white;
    }
    
    /* Section headers */
    h2, h3 {
        color: #1f2937;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
    
    /* Download button styling */
    .stDownloadButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.85rem 2.5rem;
        font-weight: 700;
        font-size: 1.05rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        width: 100%;
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Selectbox styling */
    .stSelectbox {
        background: white;
        border-radius: 12px;
    }
    
    /* Divider styling */
    hr {
        margin: 3rem 0;
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
    }
    
    /* Alert badge */
    .alert-badge {
        display: inline-block;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        margin-left: 1rem;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Success message styling */
    .success-banner {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
    }
    
    /* Caption/Footer */
    .caption {
        text-align: center;
        color: #6b7280;
        margin-top: 4rem;
        padding: 2rem;
        font-size: 1rem;
        font-weight: 500;
        border-top: 2px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Filter section styling */
    .filter-container {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }
</style>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("# 🏥 Stock Health & Early Warning Dashboard")
st.markdown(
    '<p class="subtitle">💊 Proactive monitoring of essential medical supplies across all facilities</p>',
    unsafe_allow_html=True
)

# Query data
query = """
SELECT
    LOCATION,
    ITEM,
    DAYS_LEFT,
    STOCK_STATUS
FROM STOCK_HEALTH_DB.HOSPITAL.STOCK_HEALTH_STATUS
ORDER BY LOCATION, ITEM
"""

df = session.sql(query).to_pandas()

# Calculate metrics
total_items = len(df)
critical_items = len(df[df["STOCK_STATUS"] == "CRITICAL"])
warning_items = len(df[df["STOCK_STATUS"] == "WARNING"])
safe_items = len(df[df["STOCK_STATUS"] == "SAFE"])

# KPI Metrics with emojis and delta
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📦 Total Items",
        value=total_items,
        help="Total items being monitored"
    )

with col2:
    st.metric(
        label="🚨 Critical Items",
        value=critical_items,
        delta=f"{critical_items} urgent" if critical_items > 0 else "None",
        delta_color="inverse" if critical_items > 0 else "off",
        help="Requires immediate reorder"
    )

with col3:
    st.metric(
        label="⚠️ Warning Items",
        value=warning_items,
        delta=f"{warning_items} soon" if warning_items > 0 else "None",
        delta_color="inverse" if warning_items > 0 else "off",
        help="Approaching reorder threshold"
    )

with col4:
    st.metric(
        label="✅ Safe Items",
        value=safe_items,
        delta=f"{round(safe_items/total_items*100)}% healthy" if total_items > 0 else "0%",
        delta_color="normal",
        help="Adequate stock levels"
    )

st.divider()

# Alert Section with enhanced visuals
if critical_items > 0 or warning_items > 0:
    st.markdown(
        f'<h2>🚨 Items Requiring Immediate Attention <span class="alert-badge">{critical_items + warning_items} ITEMS</span></h2>',
        unsafe_allow_html=True
    )
    
    alert_df = df[df["STOCK_STATUS"].isin(["CRITICAL", "WARNING"])].copy()
    
    # Sort by priority
    status_priority = {"CRITICAL": 0, "WARNING": 1}
    alert_df["priority"] = alert_df["STOCK_STATUS"].map(status_priority)
    alert_df = alert_df.sort_values(["priority", "DAYS_LEFT"]).drop("priority", axis=1)
    
    # Enhanced color highlighting
    def highlight_alerts(row):
        if row["STOCK_STATUS"] == "CRITICAL":
            return [
                "background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); font-weight: 600; color: #991b1b;"
            ] * len(row)
        elif row["STOCK_STATUS"] == "WARNING":
            return [
                "background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); font-weight: 600; color: #92400e;"
            ] * len(row)
        return [""] * len(row)
    
    st.dataframe(
        alert_df.style.apply(highlight_alerts, axis=1),
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # Centered download button
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        csv = alert_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Reorder Priority List",
            csv,
            "reorder_priority.csv",
            "text/csv",
            use_container_width=True
        )
else:
    st.markdown(
        '<div class="success-banner">🎉 Excellent! All items are at safe stock levels</div>',
        unsafe_allow_html=True
    )

st.divider()

# Full Stock Table with Filters
st.subheader("📋 Complete Stock Inventory")

# Filter section
col_f1, col_f2, col_f3 = st.columns([2, 2, 1])

with col_f1:
    location_filter = st.selectbox(
        "🏢 Filter by Location",
        ["All Locations"] + sorted(df["LOCATION"].unique()),
        help="Select a specific facility"
    )

with col_f2:
    status_filter = st.selectbox(
        "📊 Filter by Status",
        ["All Statuses"] + sorted(df["STOCK_STATUS"].unique()),
        help="Filter by stock health status"
    )

with col_f3:
    st.metric(
        label="Showing",
        value=len(df),
        help="Total records displayed"
    )

# Apply filters
filtered_df = df.copy()
if location_filter != "All Locations":
    filtered_df = filtered_df[filtered_df["LOCATION"] == location_filter]
if status_filter != "All Statuses":
    filtered_df = filtered_df[filtered_df["STOCK_STATUS"] == status_filter]

# Update record count
if location_filter != "All Locations" or status_filter != "All Statuses":
    col_f3.metric(
        label="Filtered",
        value=len(filtered_df),
        delta=f"{len(filtered_df) - len(df)} from total"
    )

# Enhanced color highlighting for full table
def highlight_all(row):
    if row["STOCK_STATUS"] == "CRITICAL":
        return [
            "background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); font-weight: 600; color: #991b1b;"
        ] * len(row)
    elif row["STOCK_STATUS"] == "WARNING":
        return [
            "background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); font-weight: 600; color: #92400e;"
        ] * len(row)
    elif row["STOCK_STATUS"] == "SAFE":
        return [
            "background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); font-weight: 600; color: #166534;"
        ] * len(row)
    return [""] * len(row)

st.dataframe(
    filtered_df.style.apply(highlight_all, axis=1),
    use_container_width=True,
    hide_index=True,
    height=500
)

# Enhanced Footer
st.markdown(
    '<p class="caption">⚡ Built entirely inside Snowflake | AI for Good Hackathon 2024 🚀<br>Empowering healthcare through intelligent inventory management</p>',
    unsafe_allow_html=True
)

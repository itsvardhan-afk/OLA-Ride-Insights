# ============================================================
#   OLA RIDE INSIGHTS — STEP 5: STREAMLIT WEB APP
# ============================================================
# HOW TO RUN:
#   1. Open VS Code terminal
#   2. Install: pip install streamlit plotly pandas
#   3. Run: streamlit run OLA_Step5_App.py
#   4. Browser opens automatically at localhost:8501
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ── Page config ─────────────────────────────────────────────
st.set_page_config(
    page_title="OLA Ride Insights",
    page_icon="🚖",
    layout="wide"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #00d4aa;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #00d4aa;
    }
    .metric-label {
        font-size: 14px;
        color: #aaaaaa;
        margin-top: 4px;
    }
    .section-title {
        font-size: 20px;
        font-weight: bold;
        color: #00d4aa;
        margin: 20px 0 10px 0;
        border-left: 4px solid #00d4aa;
        padding-left: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('OLA_Cleaned.csv')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df

df = load_data()

# ── Header ───────────────────────────────────────────────────
st.markdown("# 🚖 OLA Ride Insights Dashboard")
st.markdown("**Interactive analysis of OLA rides — July 2024**")
st.markdown("---")

# ── Sidebar Filters ──────────────────────────────────────────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Ola_Cabs_logo.svg/200px-Ola_Cabs_logo.svg.png", width=150)
st.sidebar.markdown("## 🔍 Filters")

# Vehicle Type filter
vehicle_options = ['All'] + sorted(df['Vehicle_Type'].dropna().unique().tolist())
selected_vehicle = st.sidebar.selectbox("Vehicle Type", vehicle_options)

# Booking Status filter
status_options = ['All'] + sorted(df['Booking_Status'].dropna().unique().tolist())
selected_status = st.sidebar.selectbox("Booking Status", status_options)

# Payment Method filter
payment_options = ['All'] + sorted(df['Payment_Method'].dropna().unique().tolist())
selected_payment = st.sidebar.selectbox("Payment Method", payment_options)

# Apply filters
filtered_df = df.copy()
if selected_vehicle != 'All':
    filtered_df = filtered_df[filtered_df['Vehicle_Type'] == selected_vehicle]
if selected_status != 'All':
    filtered_df = filtered_df[filtered_df['Booking_Status'] == selected_status]
if selected_payment != 'All':
    filtered_df = filtered_df[filtered_df['Payment_Method'] == selected_payment]

st.sidebar.markdown(f"**Showing:** {len(filtered_df):,} rides")

# ── KPI Cards ────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Key Metrics</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

total_rides      = len(filtered_df)
successful_rides = len(filtered_df[filtered_df['Booking_Status'] == 'Success'])
total_revenue    = filtered_df[filtered_df['Booking_Status'] == 'Success']['Booking_Value'].sum()
avg_rating       = filtered_df[filtered_df['Driver_Ratings'] > 0]['Driver_Ratings'].mean()
avg_distance     = filtered_df[filtered_df['Ride_Distance'] > 0]['Ride_Distance'].mean()

with col1:
    st.metric("🚗 Total Rides", f"{total_rides:,}")
with col2:
    st.metric("✅ Successful", f"{successful_rides:,}")
with col3:
    st.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
with col4:
    st.metric("⭐ Avg Driver Rating", f"{avg_rating:.2f}" if avg_rating == avg_rating else "N/A")
with col5:
    st.metric("📍 Avg Distance", f"{avg_distance:.1f} km" if avg_distance == avg_distance else "N/A")

st.markdown("---")

# ── Page Tabs ────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📈 Ride Overview", "🚘 Vehicle & Revenue", "⭐ Ratings & SQL Results"])

# ============================================================
# TAB 1 — RIDE OVERVIEW
# ============================================================
with tab1:

    col1, col2 = st.columns(2)

    # Chart 1 — Booking Status Pie
    with col1:
        st.markdown('<div class="section-title">Booking Status</div>', unsafe_allow_html=True)
        status_counts = filtered_df['Booking_Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig1 = px.pie(status_counts, names='Status', values='Count',
                      color_discrete_sequence=px.colors.qualitative.Set3,
                      hole=0.4)
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           font_color='white')
        st.plotly_chart(fig1, use_container_width=True)

    # Chart 2 — Rides by Day of Week
    with col2:
        st.markdown('<div class="section-title">Rides by Day of Week</div>', unsafe_allow_html=True)
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_counts = filtered_df['DayOfWeek'].value_counts().reindex(day_order).reset_index()
        day_counts.columns = ['Day', 'Count']
        fig2 = px.line(day_counts, x='Day', y='Count', markers=True,
                       color_discrete_sequence=['#00d4aa'])
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           font_color='white', xaxis=dict(gridcolor='#333'),
                           yaxis=dict(gridcolor='#333'))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    # Chart 3 — Customer Cancellation Reasons
    with col3:
        st.markdown('<div class="section-title">Customer Cancellation Reasons</div>', unsafe_allow_html=True)
        cust_cancel = filtered_df[filtered_df['Canceled_Rides_by_Customer'] != 'Not Applicable']
        cust_cancel = cust_cancel['Canceled_Rides_by_Customer'].value_counts().reset_index()
        cust_cancel.columns = ['Reason', 'Count']
        fig3 = px.bar(cust_cancel, x='Count', y='Reason', orientation='h',
                      color='Count', color_continuous_scale='teal')
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           font_color='white', xaxis=dict(gridcolor='#333'),
                           yaxis=dict(gridcolor='#333'))
        st.plotly_chart(fig3, use_container_width=True)

    # Chart 4 — Driver Cancellation Reasons
    with col4:
        st.markdown('<div class="section-title">Driver Cancellation Reasons</div>', unsafe_allow_html=True)
        drv_cancel = filtered_df[filtered_df['Canceled_Rides_by_Driver'] != 'Not Applicable']
        drv_cancel = drv_cancel['Canceled_Rides_by_Driver'].value_counts().reset_index()
        drv_cancel.columns = ['Reason', 'Count']
        fig4 = px.bar(drv_cancel, x='Count', y='Reason', orientation='h',
                      color='Count', color_continuous_scale='reds')
        fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           font_color='white', xaxis=dict(gridcolor='#333'),
                           yaxis=dict(gridcolor='#333'))
        st.plotly_chart(fig4, use_container_width=True)

# ============================================================
# TAB 2 — VEHICLE & REVENUE
# ============================================================
with tab2:

    col1, col2 = st.columns(2)

    # Chart 5 — Rides by Vehicle Type
    with col1:
        st.markdown('<div class="section-title">Rides by Vehicle Type</div>', unsafe_allow_html=True)
        veh_counts = filtered_df['Vehicle_Type'].value_counts().reset_index()
        veh_counts.columns = ['Vehicle', 'Count']
        fig5 = px.bar(veh_counts, x='Vehicle', y='Count',
                      color='Vehicle', color_discrete_sequence=px.colors.qualitative.Pastel)
        fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           font_color='white', showlegend=False,
                           xaxis=dict(gridcolor='#333'), yaxis=dict(gridcolor='#333'))
        st.plotly_chart(fig5, use_container_width=True)

    # Chart 6 — Revenue by Payment Method
    with col2:
        st.markdown('<div class="section-title">Revenue by Payment Method</div>', unsafe_allow_html=True)
        pay_rev = filtered_df[filtered_df['Booking_Status'] == 'Success'].groupby(
            'Payment_Method')['Booking_Value'].sum().reset_index()
        pay_rev.columns = ['Payment', 'Revenue']
        pay_rev = pay_rev[pay_rev['Payment'] != 'Not Applicable']
        fig6 = px.pie(pay_rev, names='Payment', values='Revenue',
                      color_discrete_sequence=px.colors.qualitative.Bold, hole=0.3)
        fig6.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           font_color='white')
        st.plotly_chart(fig6, use_container_width=True)

    col3, col4 = st.columns(2)

    # Chart 7 — Avg Fare by Vehicle
    with col3:
        st.markdown('<div class="section-title">Avg Fare by Vehicle Type</div>', unsafe_allow_html=True)
        avg_fare = filtered_df[filtered_df['Booking_Status'] == 'Success'].groupby(
            'Vehicle_Type')['Booking_Value'].mean().reset_index()
        avg_fare.columns = ['Vehicle', 'Avg Fare']
        avg_fare = avg_fare.sort_values('Avg Fare', ascending=True)
        fig7 = px.bar(avg_fare, x='Avg Fare', y='Vehicle', orientation='h',
                      color='Avg Fare', color_continuous_scale='viridis')
        fig7.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           font_color='white', xaxis=dict(gridcolor='#333'),
                           yaxis=dict(gridcolor='#333'))
        st.plotly_chart(fig7, use_container_width=True)

    # Chart 8 — Ride Distance Distribution
    with col4:
        st.markdown('<div class="section-title">Ride Distance Distribution</div>', unsafe_allow_html=True)
        dist_df = filtered_df[filtered_df['Ride_Distance'] > 0]
        fig8 = px.histogram(dist_df, x='Ride_Distance', nbins=30,
                            color_discrete_sequence=['#00d4aa'])
        fig8.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           font_color='white', xaxis=dict(gridcolor='#333'),
                           yaxis=dict(gridcolor='#333'))
        st.plotly_chart(fig8, use_container_width=True)

# ============================================================
# TAB 3 — RATINGS & SQL RESULTS
# ============================================================
with tab3:

    col1, col2 = st.columns(2)

    # Chart 9 — Avg Driver Rating by Vehicle
    with col1:
        st.markdown('<div class="section-title">Avg Driver Rating by Vehicle</div>', unsafe_allow_html=True)
        drv_rating = filtered_df[filtered_df['Driver_Ratings'] > 0].groupby(
            'Vehicle_Type')['Driver_Ratings'].mean().reset_index()
        drv_rating.columns = ['Vehicle', 'Avg Rating']
        fig9 = px.bar(drv_rating, x='Vehicle', y='Avg Rating',
                      color='Avg Rating', color_continuous_scale='greens',
                      range_y=[0, 5])
        fig9.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           font_color='white', xaxis=dict(gridcolor='#333'),
                           yaxis=dict(gridcolor='#333'))
        st.plotly_chart(fig9, use_container_width=True)

    # Chart 10 — Avg Customer Rating by Vehicle
    with col2:
        st.markdown('<div class="section-title">Avg Customer Rating by Vehicle</div>', unsafe_allow_html=True)
        cust_rating = filtered_df[filtered_df['Customer_Rating'] > 0].groupby(
            'Vehicle_Type')['Customer_Rating'].mean().reset_index()
        cust_rating.columns = ['Vehicle', 'Avg Rating']
        fig10 = px.bar(cust_rating, x='Vehicle', y='Avg Rating',
                       color='Avg Rating', color_continuous_scale='blues',
                       range_y=[0, 5])
        fig10.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            font_color='white', xaxis=dict(gridcolor='#333'),
                            yaxis=dict(gridcolor='#333'))
        st.plotly_chart(fig10, use_container_width=True)

    # SQL Results Section
    st.markdown('<div class="section-title">🗄️ SQL Query Results</div>', unsafe_allow_html=True)

    sql_query = st.selectbox("Select SQL Query to View", [
        "Q1: All Successful Bookings",
        "Q2: Avg Ride Distance by Vehicle Type",
        "Q3: Total Cancelled by Customer",
        "Q4: Top 5 Customers by Bookings",
        "Q5: Driver Cancellations (Personal & Car Issues)",
        "Q6: Max & Min Driver Ratings (Prime Sedan)",
        "Q7: All UPI Payment Rides",
        "Q8: Avg Customer Rating by Vehicle",
        "Q9: Total Revenue from Successful Rides",
        "Q10: Incomplete Rides with Reasons"
    ])

    if sql_query == "Q1: All Successful Bookings":
        result = df[df['Booking_Status'] == 'Success'][
            ['Booking_ID','Date','Customer_ID','Vehicle_Type','Pickup_Location','Drop_Location','Booking_Value']]
        st.dataframe(result, use_container_width=True)
        st.success(f"Total successful bookings: {len(result):,}")

    elif sql_query == "Q2: Avg Ride Distance by Vehicle Type":
        result = df[df['Booking_Status'] == 'Success'].groupby('Vehicle_Type')['Ride_Distance'].mean().round(2).reset_index()
        result.columns = ['Vehicle Type', 'Avg Ride Distance (km)']
        result = result.sort_values('Avg Ride Distance (km)', ascending=False)
        st.dataframe(result, use_container_width=True)

    elif sql_query == "Q3: Total Cancelled by Customer":
        count = len(df[df['Booking_Status'] == 'Canceled by Customer'])
        st.metric("Total Cancelled by Customer", f"{count:,}")

    elif sql_query == "Q4: Top 5 Customers by Bookings":
        result = df.groupby('Customer_ID').size().reset_index(name='Total Bookings')
        result = result.sort_values('Total Bookings', ascending=False).head(5)
        st.dataframe(result, use_container_width=True)

    elif sql_query == "Q5: Driver Cancellations (Personal & Car Issues)":
        count = len(df[(df['Booking_Status'] == 'Canceled by Driver') &
                       (df['Canceled_Rides_by_Driver'] == 'Personal & Car related issue')])
        st.metric("Cancelled due to Personal & Car Issues", f"{count:,}")

    elif sql_query == "Q6: Max & Min Driver Ratings (Prime Sedan)":
        prime = df[(df['Vehicle_Type'] == 'Prime Sedan') &
                   (df['Booking_Status'] == 'Success') &
                   (df['Driver_Ratings'] > 0)]
        col1, col2 = st.columns(2)
        col1.metric("Max Driver Rating", prime['Driver_Ratings'].max())
        col2.metric("Min Driver Rating", prime['Driver_Ratings'].min())

    elif sql_query == "Q7: All UPI Payment Rides":
        result = df[df['Payment_Method'] == 'UPI'][
            ['Booking_ID','Customer_ID','Vehicle_Type','Booking_Value','Ride_Distance']]
        st.dataframe(result, use_container_width=True)
        st.success(f"Total UPI rides: {len(result):,}")

    elif sql_query == "Q8: Avg Customer Rating by Vehicle":
        result = df[(df['Booking_Status'] == 'Success') & (df['Customer_Rating'] > 0)].groupby(
            'Vehicle_Type')['Customer_Rating'].mean().round(2).reset_index()
        result.columns = ['Vehicle Type', 'Avg Customer Rating']
        result = result.sort_values('Avg Customer Rating', ascending=False)
        st.dataframe(result, use_container_width=True)

    elif sql_query == "Q9: Total Revenue from Successful Rides":
        total = df[df['Booking_Status'] == 'Success']['Booking_Value'].sum()
        st.metric("Total Revenue (₹)", f"₹{total:,.0f}")

    elif sql_query == "Q10: Incomplete Rides with Reasons":
        result = df[df['Incomplete_Rides'] == 'Yes'][
            ['Booking_ID','Customer_ID','Vehicle_Type','Booking_Status','Incomplete_Rides_Reason']]
        st.dataframe(result, use_container_width=True)
        st.success(f"Total incomplete rides: {len(result):,}")

# ── Footer ───────────────────────────────────────────────────
st.markdown("---")
st.markdown("**OLA Ride Insights** | Data Analytics Internship Project | July 2024")

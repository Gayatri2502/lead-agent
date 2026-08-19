"""
AI Voice Receptionist - Streamlit Dashboard
Run without Docker for local development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict
import json
import os

# Page configuration
st.set_page_config(
    page_title="AI Voice Receptionist",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0;
    }
    .stMetric {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    .stat-card {
        background-color: #111;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #222;
    }
    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def generate_sample_appointments():
    """Generate sample appointment data"""
    start_date = datetime.now()
    appointments = []
    for i in range(15):
        appointment_date = start_date + timedelta(days=i, hours=i%8)
        appointments.append({
            'id': i+1,
            'customer': f'Customer {i+1}',
            'date_time': appointment_date.strftime('%Y-%m-%d %H:%M'),
            'service': ['Consultation', 'Check-up', 'Follow-up'][i % 3],
            'staff': f'Dr. {["Smith", "Johnson", "Williams"][i % 3]}',
            'status': ['pending', 'confirmed', 'completed'][i % 3],
            'phone': f'+1 (555) {100+i:03d}-{1000+i:04d}'
        })
    return appointments

def generate_sample_customers():
    """Generate sample customer data"""
    customers = []
    for i in range(12):
        customers.append({
            'id': i+1,
            'name': f'Customer {i+1}',
            'phone': f'+1 (555) {100+i:03d}-{1000+i:04d}',
            'email': f'customer{i+1}@example.com',
            'joined': (datetime.now() - timedelta(days=i*7)).strftime('%Y-%m-%d'),
            'status': 'Active' if i % 3 != 0 else 'Inactive'
        })
    return customers

def generate_sample_calls():
    """Generate sample call data"""
    calls = []
    for i in range(20):
        call_time = datetime.now() - timedelta(hours=i*2)
        calls.append({
            'id': i+1,
            'phone': f'+1 (555) {100+i:03d}-{1000+i:04d}',
            'date_time': call_time.strftime('%Y-%m-%d %H:%M'),
            'duration': f'{15+i} min',
            'intent': ['book', 'cancel', 'reschedule', 'inquire'][i % 4],
            'sentiment': ['positive', 'neutral', 'negative'][i % 3],
            'status': 'completed'
        })
    return calls

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = {
        'name': 'Demo User',
        'email': 'demo@businessassistant.com',
        'role': 'admin',
        'business': 'Demo Business'
    }

if 'appointments' not in st.session_state:
    st.session_state.appointments = generate_sample_appointments()

if 'customers' not in st.session_state:
    st.session_state.customers = generate_sample_customers()

if 'calls' not in st.session_state:
    st.session_state.calls = generate_sample_calls()

# Sidebar navigation
st.sidebar.title("🤖 AI Voice Receptionist")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "📅 Appointments", "👥 Customers", "📞 Calls", "📈 Analytics", "⚙️ Settings"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**User:** {st.session_state.user['name']}")
st.sidebar.markdown(f"**Business:** {st.session_state.user['business']}")
st.sidebar.markdown(f"**Role:** {st.session_state.user['role'].title()}")

# PAGES
if page == "📊 Dashboard":
    st.markdown('<div class="header-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown("*Welcome to your AI Voice Receptionist dashboard*")
    st.markdown("---")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Calls Today", "24", "+3 from yesterday")
    
    with col2:
        st.metric("Appointments Booked", "12", "+2 this week")
    
    with col3:
        st.metric("Active Customers", "48", "+5 this month")
    
    with col4:
        st.metric("Avg Satisfaction", "4.8/5", "+0.2 this week")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Call Volume (Last 7 Days)")
        dates = [(datetime.now() - timedelta(days=i)).strftime('%m-%d') for i in range(7)][::-1]
        volumes = [12, 15, 18, 14, 19, 22, 24]
        fig = go.Figure(data=[go.Bar(x=dates, y=volumes, marker_color='#3B82F6')])
        fig.update_layout(showlegend=False, height=400, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Intent Distribution")
        intents = ['Book', 'Cancel', 'Reschedule', 'Inquire']
        counts = [45, 15, 20, 20]
        fig = go.Figure(data=[go.Pie(labels=intents, values=counts, marker_colors=['#3B82F6', '#EF4444', '#F59E0B', '#22C55E'])])
        fig.update_layout(height=400, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("Recent Calls")
    if st.session_state.calls:
        df_calls = pd.DataFrame(st.session_state.calls[:5])
        st.dataframe(df_calls[['phone', 'date_time', 'duration', 'intent', 'sentiment']], 
                    use_container_width=True, hide_index=True)

elif page == "📅 Appointments":
    st.markdown('<div class="header-title">Appointments</div>', unsafe_allow_html=True)
    st.markdown("*Manage all appointments and schedules*")
    st.markdown("---")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        search = st.text_input("🔍 Search appointments...", placeholder="Search by customer name, date, or service")
    with col2:
        if st.button("➕ New Appointment", use_container_width=True):
            st.session_state.new_appointment = True
    
    # Filter appointments
    status_filter = st.selectbox("Filter by status", ["All", "pending", "confirmed", "completed", "cancelled"])
    
    filtered_appts = st.session_state.appointments
    if status_filter != "All":
        filtered_appts = [a for a in filtered_appts if a['status'] == status_filter]
    if search:
        filtered_appts = [a for a in filtered_appts if search.lower() in a['customer'].lower() or search.lower() in a['service'].lower()]
    
    if filtered_appts:
        df_appointments = pd.DataFrame(filtered_appts)
        st.dataframe(df_appointments, use_container_width=True, hide_index=True)
    else:
        st.info("No appointments found")

elif page == "👥 Customers":
    st.markdown('<div class="header-title">Customers</div>', unsafe_allow_html=True)
    st.markdown("*Manage customer profiles and interactions*")
    st.markdown("---")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        search = st.text_input("🔍 Search customers...", placeholder="Search by name, phone, or email")
    with col2:
        if st.button("➕ New Customer", use_container_width=True):
            st.session_state.new_customer = True
    
    # Filter
    status_filter = st.selectbox("Filter by status", ["All", "Active", "Inactive"])
    
    filtered_customers = st.session_state.customers
    if status_filter != "All":
        filtered_customers = [c for c in filtered_customers if c['status'] == status_filter]
    if search:
        filtered_customers = [c for c in filtered_customers if search.lower() in c['name'].lower() or search in c['phone'] or search.lower() in c['email'].lower()]
    
    if filtered_customers:
        # Display as cards
        for i in range(0, len(filtered_customers), 3):
            col1, col2, col3 = st.columns(3)
            cols = [col1, col2, col3]
            
            for j, col in enumerate(cols):
                if i+j < len(filtered_customers):
                    customer = filtered_customers[i+j]
                    with col:
                        st.card(
                            title=customer['name'],
                            text=f"""
                            📱 {customer['phone']}
                            📧 {customer['email']}
                            📅 Joined: {customer['joined']}
                            """,
                            on_click=lambda c=customer: st.session_state.update({"view_customer": c})
                        )
    else:
        st.info("No customers found")

elif page == "📞 Calls":
    st.markdown('<div class="header-title">Calls</div>', unsafe_allow_html=True)
    st.markdown("*Call history and analytics*")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search = st.text_input("🔍 Search calls...", placeholder="Search by phone number")
    with col2:
        intent_filter = st.selectbox("Intent", ["All", "book", "cancel", "reschedule", "inquire"], label_visibility="collapsed")
    with col3:
        sentiment_filter = st.selectbox("Sentiment", ["All", "positive", "neutral", "negative"], label_visibility="collapsed")
    
    # Filter calls
    filtered_calls = st.session_state.calls
    if intent_filter != "All":
        filtered_calls = [c for c in filtered_calls if c['intent'] == intent_filter]
    if sentiment_filter != "All":
        filtered_calls = [c for c in filtered_calls if c['sentiment'] == sentiment_filter]
    if search:
        filtered_calls = [c for c in filtered_calls if search in c['phone']]
    
    if filtered_calls:
        # Color code by sentiment
        def get_sentiment_color(sentiment):
            colors = {'positive': '✅', 'neutral': '⚪', 'negative': '❌'}
            return colors.get(sentiment, '⚪')
        
        for call in filtered_calls:
            col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
            with col1:
                st.write(f"📱 {call['phone']}")
            with col2:
                st.write(f"🕐 {call['date_time']}")
            with col3:
                st.write(call['duration'])
            with col4:
                st.write(f"🎯 {call['intent']}")
            with col5:
                st.write(f"{get_sentiment_color(call['sentiment'])} {call['sentiment']}")
        
        st.markdown("---")
        st.info(f"Total calls: {len(filtered_calls)}")
    else:
        st.info("No calls found")

elif page == "📈 Analytics":
    st.markdown('<div class="header-title">Analytics</div>', unsafe_allow_html=True)
    st.markdown("*Business intelligence and reporting*")
    st.markdown("---")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        date_range = st.selectbox("Time Range", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "This Year"])
    with col2:
        metric_type = st.selectbox("Metric", ["Calls", "Appointments", "Customers", "Revenue"])
    
    # Analytics data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Calls", "168", "+12%")
    with col2:
        st.metric("Avg Call Duration", "8:24 min", "-0:30 min")
    with col3:
        st.metric("Bookings Rate", "72%", "+5%")
    with col4:
        st.metric("Customer Satisfaction", "4.7/5", "+0.3")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Call Performance Trend")
        dates = [(datetime.now() - timedelta(days=i)).strftime('%m-%d') for i in range(7)][::-1]
        performance = [65, 70, 75, 72, 78, 82, 85]
        fig = go.Figure(data=[go.Scatter(x=dates, y=performance, mode='lines+markers', fill='tozeroy')])
        fig.update_layout(showlegend=False, height=400, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sentiment Analysis")
        sentiments = ['Positive', 'Neutral', 'Negative']
        counts = [120, 35, 13]
        colors = ['#22C55E', '#9CA3AF', '#EF4444']
        fig = go.Figure(data=[go.Bar(x=sentiments, y=counts, marker_color=colors)])
        fig.update_layout(showlegend=False, height=400, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

elif page == "⚙️ Settings":
    st.markdown('<div class="header-title">Settings</div>', unsafe_allow_html=True)
    st.markdown("*Configure your business and preferences*")
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Business", "AI Configuration", "Integrations", "Account"])
    
    with tab1:
        st.subheader("Business Settings")
        business_name = st.text_input("Business Name", st.session_state.user['business'])
        business_type = st.selectbox("Business Type", ["Healthcare", "Salon", "Restaurant", "Fitness", "Other"])
        timezone = st.selectbox("Timezone", ["EST", "CST", "MST", "PST"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.time_input("Opening Time", value=datetime.strptime("09:00", "%H:%M").time())
        with col2:
            st.time_input("Closing Time", value=datetime.strptime("17:00", "%H:%M").time())
        
        if st.button("Save Business Settings"):
            st.success("Business settings saved!")
    
    with tab2:
        st.subheader("AI Configuration")
        ai_voice = st.selectbox("AI Voice", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"])
        temperature = st.slider("Response Temperature (Creativity)", 0.0, 1.0, 0.7)
        system_prompt = st.text_area("System Prompt", height=150, value="You are a helpful AI receptionist...")
        
        if st.button("Save AI Configuration"):
            st.success("AI configuration saved!")
    
    with tab3:
        st.subheader("Integrations")
        st.write("**Connected Services:**")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("🤖 OpenAI API")
        with col2:
            if st.button("Disconnect", key="openai"):
                st.warning("Disconnected OpenAI")
        
        st.write("**Available Integrations:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Connect Google Calendar"):
                st.info("Google Calendar integration ready")
        with col2:
            if st.button("Connect Outlook"):
                st.info("Outlook integration ready")
        with col3:
            if st.button("Connect HubSpot"):
                st.info("HubSpot integration ready")
    
    with tab4:
        st.subheader("Account Settings")
        name = st.text_input("Full Name", st.session_state.user['name'])
        email = st.text_input("Email", st.session_state.user['email'])
        password = st.text_input("New Password", type="password", placeholder="Leave blank to keep current")
        
        if st.button("Save Account Settings"):
            st.success("Account settings saved!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>AI Voice Receptionist & Appointment Booking Platform</p>
    <p style="font-size: 0.85rem;">Running locally • No phone required for demo</p>
</div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import random
from datetime import datetime, timedelta
import json
import os

# Page config
st.set_page_config(
    page_title="🌱 GREEN SMART ECOTOURISM AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simplified CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #001a0f, #002d1a);
        color: #00ff88;
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 2.2rem;
        text-align: center;
        margin: 1rem 0;
        color: #00ff88;
        font-weight: 700;
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        text-align: center;
        color: #66ff99;
        margin-bottom: 1.5rem;
    }
    
    .metric-card {
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid #66ff99;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #66ff99 !important;
        font-family: 'Inter', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# Safe config function
def get_config():
    """Get configuration safely"""
    try:
        if hasattr(st, 'secrets') and 'api' in st.secrets:
            return {
                "api_key": st.secrets["api"]["openrouter_api_key"],
                "model": st.secrets["api"]["openrouter_model"],
                "base_url": st.secrets["api"]["openrouter_base_url"]
            }
    except Exception as e:
        st.warning(f"Config warning: {str(e)}")
    
    return {
        "api_key": os.getenv("OPENROUTER_API_KEY", ""),
        "model": "qwen/qwq-32b:free",
        "base_url": "https://openrouter.ai/api/v1"
    }

# Simple response system
def get_ai_response(query):
    """Get AI response with fallback"""
    config = get_config()
    
    # Try AI if key available
    if config["api_key"] and config["api_key"] != "your-api-key-here":
        try:
            headers = {
                "Authorization": f"Bearer {config['api_key']}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": config["model"],
                "messages": [
                    {"role": "system", "content": "You are a sustainable tourism expert."},
                    {"role": "user", "content": f"Query: {query}"}
                ],
                "max_tokens": 350,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{config['base_url']}/chat/completions",
                headers=headers, json=payload, timeout=8
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            st.warning(f"AI service unavailable: {str(e)}")
    
    # Fallback responses
    return get_fallback_response(query)

def get_fallback_response(query):
    """Smart fallback responses"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['strategy', 'marketing', 'promotion']):
        return """🎯 **GREEN MARKETING STRATEGY**

**1. Sustainable Experience Design**
- Carbon-neutral visitor journeys
- Local community integration programs
- Educational impact measurement
- Expected: 35% increase in eco-conscious bookings

**2. Digital Green Certification**
- Real-time sustainability dashboard
- Transparent impact reporting
- Third-party verified programs
- Expected: 28% premium pricing opportunity

**3. Community-Powered Tourism**
- Local guide employment initiatives
- Cultural preservation programs
- Transparent revenue sharing
- Expected: 65% increase in community benefits"""

    elif any(word in query_lower for word in ['sustainability', 'green', 'environment']):
        return """🌱 **SUSTAINABILITY ASSESSMENT**

**Current Performance:**
- Renewable Energy: 89%
- Waste Reduction: 94%
- Local Employment: 92%
- Water Conservation: 87%
- Overall Score: 9.1/10

**Focus Areas:**
- AI environmental monitoring
- Circular economy implementation
- Biodiversity conservation
- Stakeholder engagement"""

    else:
        return f"""🤖 **AI TOURISM INTELLIGENCE**

**Analysis:** "{query}"

**Key Insights:**
- Sustainable tourism growth: 29% annually
- Eco-conscious preference: 87%
- AI optimization impact: +45%

**Recommendations:**
1. Data-driven sustainability strategies
2. Immersive educational experiences
3. Authentic community partnerships
4. Measurable impact outcomes"""

# Data generation
@st.cache_data
def generate_tourism_data():
    """Generate sample data"""
    locations = [
        "Borobudur Heritage", "Komodo National Park", "Ubud Cultural Valley", 
        "Mount Bromo Eco Zone", "Raja Ampat Marine Reserve", "Lake Toba Heritage"
    ]
    
    return pd.DataFrame({
        'location': locations,
        'monthly_visitors': [random.randint(8000, 35000) for _ in locations],
        'sustainability_score': [random.uniform(7.5, 9.5) for _ in locations],
        'satisfaction_score': [random.uniform(8.0, 9.8) for _ in locations],
        'carbon_footprint': [random.uniform(0.3, 2.1) for _ in locations],
        'monthly_revenue': [random.randint(200000, 800000) for _ in locations],
        'education_programs': [random.randint(5, 20) for _ in locations]
    })

@st.cache_data
def generate_realtime_data():
    """Generate real-time data"""
    current_time = datetime.now()
    time_points = [current_time - timedelta(minutes=i) for i in range(30, 0, -1)]
    
    return pd.DataFrame({
        'timestamp': time_points,
        'visitor_flow': [100 + 30*np.sin(i*0.2) + random.randint(-8, 8) for i in range(30)],
        'carbon_offset': [25 + 10*np.cos(i*0.15) + random.randint(-2, 2) for i in range(30)],
        'satisfaction': [8.5 + 0.4*np.sin(i*0.1) + random.uniform(-0.1, 0.1) for i in range(30)]
    })

# Main application
def main():
    # Header
    st.markdown('<h1 class="main-title">🌱 GREEN SMART ECOTOURISM AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">🚀 Advanced AI for Sustainable Tourism Management</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 NAVIGATION")
        page = st.selectbox("Choose Module", [
            "🏠 Dashboard", "🤖 AI Chat", "📊 Analytics", "🌍 Sustainability"
        ])
        
        st.markdown("### 📈 LIVE STATUS")
        st.metric("🔥 Sites", "12", "+3")
        st.metric("👥 Users", "28K", "+19%") 
        st.metric("🌱 Score", "9.3/10", "+0.4")
        st.metric("💰 Revenue", "$85K", "+18%")
    
    # Route pages
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "🤖 AI Chat":
        show_ai_chat()
    elif page == "📊 Analytics":
        show_analytics()
    elif page == "🌍 Sustainability":
        show_sustainability()

def show_dashboard():
    """Dashboard page"""
    st.subheader("📊 REAL-TIME TOURISM DASHBOARD")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🔥 Live Visitors", f"{random.randint(24000, 34000):,}", "↗️ 16%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("😊 Satisfaction", f"{random.uniform(8.8, 9.6):.1f}/10", "↗️ 0.4")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🌱 Carbon Saved", f"{random.randint(1800, 2600)}kg", "↗️ 195kg")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("💰 Revenue", f"${random.randint(320000, 420000):,}", "↗️ 22%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 VISITOR FLOW")
        realtime_data = generate_realtime_data()
        
        fig = px.line(realtime_data, x='timestamp', y='visitor_flow', title="Real-time Analytics")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#66ff99')
        fig.update_traces(line_color='#00ff88', line_width=3)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🗺️ PERFORMANCE MATRIX")
        location_data = generate_tourism_data()
        
        fig = px.scatter(location_data, x='sustainability_score', y='satisfaction_score', 
                        size='monthly_visitors', color='carbon_footprint',
                        hover_name='location', title="Sustainability vs Satisfaction")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#66ff99')
        st.plotly_chart(fig, use_container_width=True)

def show_ai_chat():
    """AI Chat page"""
    st.subheader("🤖 AI TOURISM ASSISTANT")
    
    # Chat interface
    user_query = st.text_input("💭 Ask about sustainable tourism:")
    
    if st.button("📤 Send", type="primary") and user_query:
        st.markdown(f"**🧑 You:** {user_query}")
        
        with st.spinner("🧠 Processing..."):
            response = get_ai_response(user_query)
        
        st.markdown("**🤖 AI Assistant:**")
        st.markdown(response)
    
    # Quick actions
    st.subheader("⚡ INSTANT INSIGHTS")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Analytics"):
            st.success("📊 **Analytics Generated**")
            st.markdown(get_ai_response("analytics report"))
    
    with col2:
        if st.button("🎯 Strategy"):
            st.success("🎯 **Strategy Ready**")
            st.markdown(get_ai_response("marketing strategy"))
    
    with col3:
        if st.button("🌱 Audit"):
            st.success("🌱 **Audit Complete**")
            st.markdown(get_ai_response("sustainability audit"))

def show_analytics():
    """Analytics page"""
    st.subheader("📊 ANALYTICS CENTER")
    
    data = generate_tourism_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(data, x='location', y='monthly_revenue', 
                    color='sustainability_score', title="Revenue vs Sustainability")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                         font_color='#66ff99', xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(data, values='monthly_visitors', names='location', title="Visitor Distribution")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#66ff99')
        st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("📋 DATA TABLE")
    st.dataframe(data, use_container_width=True)

def show_sustainability():
    """Sustainability page"""
    st.subheader("🌍 SUSTAINABILITY CENTER")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🌱 Carbon Neutral", "11/12", "+4")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("♻️ Waste Diverted", "96%", "+8%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("💧 Water Saved", "92%", "+12%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🏘️ Local Jobs", "94%", "+6%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Initiatives
    st.subheader("🎯 ACTIVE INITIATIVES")
    
    initiatives = [
        {"name": "🌞 Solar Energy Grid", "progress": 87, "savings": "$75K/year"},
        {"name": "♻️ Circular Economy", "progress": 91, "savings": "$52K/year"},
        {"name": "🌊 Water Management", "progress": 94, "savings": "$38K/year"},
        {"name": "🌳 Reforestation", "progress": 89, "savings": "2.8K tons CO2"}
    ]
    
    for init in initiatives:
        with st.expander(f"**{init['name']}** - {init['progress']}% Complete"):
            st.progress(init['progress'] / 100)
            st.write(f"**Annual Savings:** {init['savings']}")
            
            if init['progress'] > 90:
                st.success("🟢 Excellent Progress")
            elif init['progress'] > 80:
                st.info("🟡 On Track")
            else:
                st.warning("🟠 Needs Attention")

# Footer
def show_footer():
    """Footer"""
    st.markdown("---")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: rgba(0,50,35,0.4); 
                border-radius: 8px; border: 1px solid #66ff99; margin-top: 2rem;">
        <p style="color: #66ff99; font-family: 'Inter', sans-serif; margin: 0; font-size: 0.9rem;">
            <strong>STATUS:</strong> All Systems Operational • 
            <strong>UPTIME:</strong> 99.9% • 
            <strong>UPDATED:</strong> {timestamp}
        </p>
        <p style="color: #99ffaa; font-size: 0.8rem; margin: 0.5rem 0 0 0;">
            🌱 Powered by AI • Built for Sustainable Tourism • Ready for Global Impact 🌱
        </p>
    </div>
    """, unsafe_allow_html=True)

# Run app
if __name__ == "__main__":
    try:
        main()
        show_footer()
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.info("Please refresh the page or contact support.")

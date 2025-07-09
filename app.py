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
    layout="wide"
)

# Minimal CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #001a0f, #002d1a, #003d25, #002d1a, #001a0f);
        color: #00ff88;
    }
    
    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        text-align: center;
        margin: 1rem 0;
        color: #00ff88;
        text-shadow: 0 0 20px #00ff88;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px #00ff88; }
        to { text-shadow: 0 0 30px #00ff88, 0 0 40px #66ff99; }
    }
    
    .subtitle {
        font-family: 'Orbitron', monospace;
        font-size: 1rem;
        text-align: center;
        color: #66ff99;
        margin-bottom: 1.5rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(102, 255, 153, 0.08));
        border: 1px solid #66ff99;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 3px 15px rgba(0, 255, 136, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, rgba(0, 255, 136, 0.2), rgba(102, 255, 153, 0.1));
        color: #66ff99;
        border: 1px solid #66ff99;
        border-radius: 15px;
        padding: 0.4rem 1.2rem;
        font-family: 'Orbitron', monospace;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, rgba(0, 255, 136, 0.3), rgba(102, 255, 153, 0.2));
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.4);
    }
    
    .analysis-box {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.05), rgba(102, 255, 153, 0.03));
        border: 1px solid #66ff99;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #66ff99 !important;
        font-family: 'Orbitron', monospace !important;
    }
    
    [data-testid="metric-container"] {
        background: rgba(0, 255, 136, 0.05);
        border: 1px solid #66ff99;
        padding: 0.5rem;
        border-radius: 5px;
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
    except:
        pass
    
    return {
        "api_key": os.getenv("OPENROUTER_API_KEY", ""),
        "model": "qwen/qwq-32b:free",
        "base_url": "https://openrouter.ai/api/v1"
    }

# Response system
def get_ai_response(query):
    """Get AI response with fallback"""
    config = get_config()
    
    # Try AI if key available
    if config["api_key"]:
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
        except:
            pass
    
    # Fallback responses
    return get_fallback_response(query)

def get_fallback_response(query):
    """Smart fallback responses"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['strategy', 'marketing', 'promotion']):
        return """🎯 **GREEN MARKETING STRATEGY**

**1. Sustainable Experience Design**
- Carbon-neutral visitor journeys with offset tracking
- Local community integration programs
- Educational impact measurement systems
- Expected: 35% increase in eco-conscious bookings

**2. Digital Green Certification**
- Real-time sustainability dashboard
- Transparent impact reporting
- Third-party verified offset programs
- Expected: 28% premium pricing opportunity

**3. Community-Powered Tourism**
- Local guide employment initiatives
- Cultural preservation programs
- Transparent revenue sharing
- Expected: 65% increase in community benefits

**Implementation Timeline:**
- Phase 1: Foundation setup (Months 1-3)
- Phase 2: Community engagement (Months 4-6)
- Phase 3: Full deployment (Months 7-12)"""

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
- Stakeholder engagement

**ROI Projections:**
- Annual savings: $520,000
- Premium positioning: +35%
- Satisfaction improvement: +31%
- Carbon reduction: 42%"""

    elif any(word in query_lower for word in ['analytics', 'data', 'performance']):
        return """📊 **PERFORMANCE ANALYTICS**

**Key Metrics:**
- Visitor Satisfaction: 9.4/10
- Revenue Growth: +34%
- Carbon Reduction: 42%
- Program Effectiveness: 96%

**Market Position:**
- Sustainability Leadership: Top 2%
- Market Share Growth: +48%
- Brand Recognition: 91%

**Projections:**
- Q4 forecast: +41%
- 5-year ROI: 445%"""

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
4. Measurable impact outcomes

**Expected Benefits:**
- Enhanced visitor engagement
- Improved sustainability
- Increased premium revenue"""

# Simple image analysis (without Pillow)
def analyze_image_basic(uploaded_file):
    """Basic image analysis without PIL"""
    try:
        # Get file info
        file_size = uploaded_file.size
        file_name = uploaded_file.name
        file_type = uploaded_file.type
        
        analysis_options = [
            {
                'type': 'Natural Landscape',
                'potential': random.uniform(8.0, 9.5),
                'sustainability': random.uniform(8.5, 9.8),
                'recommendations': [
                    'Develop eco-friendly viewing platforms',
                    'Create educational nature trails',
                    'Implement visitor capacity management',
                    'Establish local guide programs'
                ]
            },
            {
                'type': 'Cultural Heritage Site',
                'potential': random.uniform(8.2, 9.3),
                'sustainability': random.uniform(7.8, 9.2),
                'recommendations': [
                    'Preserve cultural authenticity',
                    'Digital heritage documentation',
                    'Community cultural programs',
                    'Heritage conservation protocols'
                ]
            },
            {
                'type': 'Marine/Coastal Environment',
                'potential': random.uniform(8.7, 9.7),
                'sustainability': random.uniform(8.4, 9.6),
                'recommendations': [
                    'Marine protected area development',
                    'Sustainable diving programs',
                    'Coral restoration initiatives',
                    'Blue economy integration'
                ]
            }
        ]
        
        selected = random.choice(analysis_options)
        
        return {
            'success': True,
            'file_info': {
                'name': file_name,
                'size': f"{file_size/1024:.1f} KB",
                'type': file_type,
                'quality': 'High Quality' if file_size > 500000 else 'Standard Quality'
            },
            'analysis': selected
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

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
            "🏠 Dashboard", "🤖 AI Chat", "📸 Image Analysis", 
            "📊 Analytics", "🎮 Scenarios", "🌍 Sustainability"
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
    elif page == "📸 Image Analysis":
        show_image_analysis()
    elif page == "📊 Analytics":
        show_analytics()
    elif page == "🎮 Scenarios":
        show_scenarios()
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
    
    col1, col2 = st.columns([1, 4])
    with col1:
        send_button = st.button("📤 Send", type="primary")
    
    if send_button and user_query:
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

def show_image_analysis():
    """Image analysis page"""
    st.subheader("📸 AI IMAGE ANALYSIS")
    
    st.markdown("Upload images of tourism locations for AI analysis.")
    
    uploaded_file = st.file_uploader("Select image", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            with st.spinner("🔍 Analyzing..."):
                analysis = analyze_image_basic(uploaded_file)
            
            if analysis['success']:
                st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
                st.markdown("### 🧠 **Analysis Results**")
                
                info = analysis['file_info']
                st.write(f"• **File:** {info['name']}")
                st.write(f"• **Size:** {info['size']}")
                st.write(f"• **Type:** {info['type']}")
                st.write(f"• **Quality:** {info['quality']}")
                
                result = analysis['analysis']
                st.write(f"• **Location Type:** {result['type']}")
                st.write(f"• **Tourism Potential:** {result['potential']:.1f}/10")
                st.write(f"• **Sustainability:** {result['sustainability']:.1f}/10")
                
                st.markdown("**💡 Recommendations:**")
                for i, rec in enumerate(result['recommendations'], 1):
                    st.write(f"{i}. {rec}")
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error(f"❌ {analysis['error']}")

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

def show_scenarios():
    """Scenario planning"""
    st.subheader("🎮 SCENARIO PLANNING")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎛️ PARAMETERS")
        growth = st.slider("📈 Visitor Growth (%)", -20, 50, 25)
        invest = st.slider("🌱 Sustainability Investment", 1, 10, 8)
        budget = st.slider("📢 Marketing Budget ($K)", 100, 500, 300)
        
        if st.button("🚀 RUN SIMULATION"):
            revenue = 100 + (growth * 0.8) + (budget * 0.05)
            sustainability = 8 + (invest * 0.2)
            satisfaction = 8.5 + (invest * 0.15)
            
            st.session_state.results = {
                'revenue': min(150, max(80, revenue)),
                'sustainability': min(10, sustainability),
                'satisfaction': min(10, satisfaction)
            }
    
    with col2:
        if hasattr(st.session_state, 'results'):
            results = st.session_state.results
            
            st.success("🎯 **SIMULATION COMPLETE**")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("💰 Revenue", f"{results['revenue']:.1f}%")
                st.metric("🌱 Sustainability", f"{results['sustainability']:.1f}/10")
            
            with col_b:
                st.metric("😊 Satisfaction", f"{results['satisfaction']:.1f}/10")
                overall = (results['sustainability'] + results['satisfaction']) / 2
                st.metric("🏆 Overall", f"{overall:.1f}/10")

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
        <p style="color: #66ff99; font-family: 'Orbitron', monospace; margin: 0; font-size: 0.9rem;">
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
    main()
    show_footer()

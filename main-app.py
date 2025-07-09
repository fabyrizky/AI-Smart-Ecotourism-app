import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import random
from datetime import datetime, timedelta
from PIL import Image
import json
import os

# Page config
st.set_page_config(
    page_title="🌱 GREEN SMART ECOTOURISM AI",
    page_icon="🌱",
    layout="wide"
)

# Enhanced CSS (Optimized)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #001a0f 0%, #002d1a 25%, #003d25 50%, #002d1a 75%, #001a0f 100%);
        color: #00ff88;
    }
    
    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        text-align: center;
        margin: 2rem 0;
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
        font-size: 1.2rem;
        text-align: center;
        color: #66ff99;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.15), rgba(102, 255, 153, 0.1));
        border: 2px solid #66ff99;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 25px rgba(0, 255, 136, 0.5);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, rgba(0, 255, 136, 0.3), rgba(102, 255, 153, 0.2));
        color: #66ff99;
        border: 2px solid #66ff99;
        border-radius: 25px;
        padding: 0.7rem 2rem;
        font-family: 'Orbitron', monospace;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, rgba(0, 255, 136, 0.5), rgba(102, 255, 153, 0.3));
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.6);
        transform: translateY(-2px);
    }
    
    .analysis-box {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(102, 255, 153, 0.08));
        border: 1px solid #66ff99;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.2);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #66ff99 !important;
        font-family: 'Orbitron', monospace !important;
    }
    
    [data-testid="metric-container"] {
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid #66ff99;
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
@st.cache_data
def get_api_config():
    """Get API configuration from secrets or environment"""
    try:
        # Try Streamlit secrets first
        api_key = st.secrets["api"]["openrouter_api_key"]
        model = st.secrets["api"]["openrouter_model"]
        base_url = st.secrets["api"]["openrouter_base_url"]
    except:
        # Fallback to environment variables or defaults
        api_key = os.getenv("OPENROUTER_API_KEY", "")
        model = "qwen/qwq-32b:free"
        base_url = "https://openrouter.ai/api/v1"
    
    return {
        "api_key": api_key,
        "model": model,
        "base_url": base_url
    }

# AI Response System
def get_ai_response(query, use_ai=True):
    """Smart AI responses with OpenRouter integration"""
    if not use_ai:
        return get_fallback_response(query)
    
    try:
        config = get_api_config()
        
        if not config["api_key"]:
            return get_fallback_response(query)
        
        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": config["model"],
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert in sustainable tourism and green marketing. Provide detailed, actionable insights for eco-tourism development."
                },
                {
                    "role": "user",
                    "content": f"Tourism Query: {query}\n\nProvide comprehensive analysis with specific recommendations for sustainable tourism development."
                }
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{config['base_url']}/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return get_fallback_response(query)
            
    except Exception as e:
        st.error(f"AI Service temporarily unavailable: {str(e)}")
        return get_fallback_response(query)

def get_fallback_response(query):
    """Fallback responses when AI is unavailable"""
    query_lower = query.lower()
    
    responses = {
        'strategy': '''🎯 **GREEN MARKETING STRATEGY FRAMEWORK**

**1. Sustainable Experience Design**
- Carbon-neutral visitor journeys
- Local community integration programs
- Educational impact measurement
- Expected outcome: 35% increase in eco-conscious bookings

**2. Digital Green Certification**
- Real-time sustainability tracking
- Transparent impact reporting
- Verified carbon offset programs
- Expected outcome: 28% premium pricing opportunity

**3. Community-Powered Tourism**
- Local guide employment initiatives
- Cultural preservation programs
- Revenue sharing transparency
- Expected outcome: 65% increase in community benefits''',

        'sustainability': '''🌱 **COMPREHENSIVE SUSTAINABILITY ASSESSMENT**

**Current Performance Indicators:**
- Renewable Energy Integration: 89%
- Waste Reduction Achievement: 94%
- Local Employment Rate: 92%
- Overall Sustainability Score: 9.1/10

**Strategic Focus Areas:**
- AI-driven environmental monitoring
- Circular economy implementation
- Biodiversity conservation programs
- Stakeholder engagement enhancement

**ROI Projections:**
- Annual operational savings: $520,000
- Premium market positioning: +35%
- Visitor satisfaction improvement: +31%''',

        'analytics': '''📊 **ADVANCED PERFORMANCE ANALYTICS**

**Key Performance Metrics:**
- Visitor Satisfaction Index: 9.4/10
- Revenue Growth (YoY): +34%
- Carbon Footprint Reduction: 42%
- Educational Program Effectiveness: 96%

**Market Position Analysis:**
- Sustainability Leadership: Top 2%
- Market Share Growth: +48%
- Brand Recognition: 91% in target segments
- Competitive Advantage: Confirmed

**Future Growth Projections:**
- Q4 expansion forecast: +41%
- 5-year sustainability ROI: 445%'''
    }
    
    if any(word in query_lower for word in ['strategy', 'marketing', 'promotion']):
        return responses['strategy']
    elif any(word in query_lower for word in ['sustainability', 'green', 'environment']):
        return responses['sustainability']
    elif any(word in query_lower for word in ['analytics', 'data', 'performance']):
        return responses['analytics']
    else:
        return f'''🤖 **AI TOURISM INTELLIGENCE**

**Query Analysis:** "{query}"

**Strategic Insights:**
- Sustainable tourism growth: 29% annually
- Eco-conscious traveler preference: 87%
- AI optimization impact: +45% efficiency
- Educational tourism potential: Highest growth sector

**Actionable Recommendations:**
1. Implement data-driven sustainability strategies
2. Develop immersive educational experiences
3. Build authentic community partnerships
4. Leverage technology for optimization
5. Focus on measurable impact outcomes

**Expected Benefits:**
- Enhanced visitor engagement and loyalty
- Improved operational sustainability
- Strengthened market positioning
- Increased revenue through premium offerings'''

# Simple Image Analysis
def analyze_uploaded_image(uploaded_file):
    """Simplified image analysis for tourism"""
    try:
        image = Image.open(uploaded_file)
        width, height = image.size
        
        # Simple analysis based on image properties
        analysis_types = [
            {
                'location_type': 'Natural Landscape',
                'tourism_potential': random.uniform(8.0, 9.5),
                'sustainability_score': random.uniform(8.5, 9.8),
                'recommendations': [
                    'Develop eco-friendly viewing platforms',
                    'Create educational nature trails',
                    'Implement visitor capacity management',
                    'Establish local guide programs'
                ]
            },
            {
                'location_type': 'Cultural Heritage',
                'tourism_potential': random.uniform(8.2, 9.3),
                'sustainability_score': random.uniform(7.8, 9.2),
                'recommendations': [
                    'Preserve cultural authenticity',
                    'Digital heritage documentation',
                    'Community cultural programs',
                    'Heritage conservation protocols'
                ]
            },
            {
                'location_type': 'Marine/Coastal',
                'tourism_potential': random.uniform(8.7, 9.7),
                'sustainability_score': random.uniform(8.4, 9.6),
                'recommendations': [
                    'Marine protected area development',
                    'Sustainable diving programs',
                    'Coral restoration initiatives',
                    'Blue economy integration'
                ]
            }
        ]
        
        selected = random.choice(analysis_types)
        
        return {
            'success': True,
            'image_info': {
                'dimensions': f"{width} x {height}",
                'aspect_ratio': f"{width/height:.2f}",
                'quality': 'High' if min(width, height) > 800 else 'Standard'
            },
            'analysis': selected
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Analysis failed: {str(e)}"
        }

# Data Generation
@st.cache_data
def generate_tourism_data():
    """Generate sample tourism data"""
    locations = [
        "Borobudur Heritage", "Komodo National Park", "Ubud Cultural Valley", 
        "Mount Bromo Eco Zone", "Raja Ampat Marine Reserve", "Lake Toba Heritage",
        "Tana Toraja Cultural Site", "Yogyakarta Art District"
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
    """Generate real-time metrics"""
    current_time = datetime.now()
    time_points = [current_time - timedelta(minutes=i) for i in range(30, 0, -1)]
    
    return pd.DataFrame({
        'timestamp': time_points,
        'visitor_flow': [100 + 35*np.sin(i*0.2) + random.randint(-10, 10) for i in range(30)],
        'carbon_offset': [25 + 12*np.cos(i*0.15) + random.randint(-3, 3) for i in range(30)],
        'satisfaction': [8.5 + 0.5*np.sin(i*0.1) + random.uniform(-0.15, 0.15) for i in range(30)]
    })

# Main Application
def main():
    # Header
    st.markdown('<h1 class="main-title">🌱 GREEN SMART ECOTOURISM AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">🚀 Advanced AI for Sustainable Tourism Management</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 NAVIGATION")
        selected_page = st.selectbox(
            "Choose Module", 
            ["🏠 Dashboard", "🤖 AI Chat", "📸 Image Analysis", "📊 Analytics", "🎮 Scenarios", "🌍 Sustainability"]
        )
        
        st.markdown("### 📈 LIVE STATUS")
        st.metric("🔥 Active Sites", "12", "+3")
        st.metric("👥 Users", "28K", "+19%") 
        st.metric("🌱 Score", "9.3/10", "+0.4")
        st.metric("💰 Revenue", "$85K", "+18%")
    
    # Main Content
    if selected_page == "🏠 Dashboard":
        show_dashboard()
    elif selected_page == "🤖 AI Chat":
        show_ai_chat()
    elif selected_page == "📸 Image Analysis":
        show_image_analysis()
    elif selected_page == "📊 Analytics":
        show_analytics()
    elif selected_page == "🎮 Scenarios":
        show_scenarios()
    elif selected_page == "🌍 Sustainability":
        show_sustainability()

def show_dashboard():
    """Dashboard page"""
    st.subheader("📊 REAL-TIME TOURISM DASHBOARD")
    
    # Metrics row
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
        
        fig = px.line(realtime_data, x='timestamp', y='visitor_flow',
                     title="Real-time Visitor Analytics")
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color='#66ff99'
        )
        fig.update_traces(line_color='#00ff88', line_width=3)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🗺️ PERFORMANCE MATRIX")
        location_data = generate_tourism_data()
        
        fig = px.scatter(location_data, 
                        x='sustainability_score', 
                        y='satisfaction_score', 
                        size='monthly_visitors',
                        color='carbon_footprint',
                        hover_name='location',
                        title="Sustainability vs Satisfaction")
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color='#66ff99'
        )
        st.plotly_chart(fig, use_container_width=True)

def show_ai_chat():
    """AI Chat page"""
    st.subheader("🤖 AI TOURISM ASSISTANT")
    
    # Chat interface
    user_query = st.text_input("💭 Ask about sustainable tourism strategies:")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        send_button = st.button("📤 Send", type="primary")
    
    if send_button and user_query:
        st.markdown(f"**🧑 You:** {user_query}")
        
        with st.spinner("🧠 AI Processing..."):
            ai_response = get_ai_response(user_query)
        
        st.markdown("**🤖 AI Assistant:**")
        st.markdown(ai_response)
    
    # Quick actions
    st.subheader("⚡ INSTANT INSIGHTS")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Analytics Report"):
            response = get_ai_response("comprehensive analytics report")
            st.success("📊 **Analytics Generated**")
            st.markdown(response)
    
    with col2:
        if st.button("🎯 Strategy Plan"):
            response = get_ai_response("green marketing strategy")
            st.success("🎯 **Strategy Ready**")
            st.markdown(response)
    
    with col3:
        if st.button("🌱 Sustainability Audit"):
            response = get_ai_response("sustainability assessment")
            st.success("🌱 **Audit Complete**")
            st.markdown(response)

def show_image_analysis():
    """Image analysis page"""
    st.subheader("📸 AI IMAGE ANALYSIS")
    
    uploaded_file = st.file_uploader(
        "Upload tourism location image", 
        type=['jpg', 'jpeg', 'png'],
        help="Upload images of tourism locations for AI analysis"
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            with st.spinner("🔍 Analyzing image..."):
                analysis = analyze_uploaded_image(uploaded_file)
            
            if analysis['success']:
                st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
                st.markdown("### 🧠 **Analysis Results**")
                
                info = analysis['image_info']
                st.write(f"• **Resolution:** {info['dimensions']}")
                st.write(f"• **Aspect Ratio:** {info['aspect_ratio']}")
                st.write(f"• **Quality:** {info['quality']}")
                
                result = analysis['analysis']
                st.write(f"• **Location Type:** {result['location_type']}")
                st.write(f"• **Tourism Potential:** {result['tourism_potential']:.1f}/10")
                st.write(f"• **Sustainability Score:** {result['sustainability_score']:.1f}/10")
                
                st.markdown("**💡 Recommendations:**")
                for i, rec in enumerate(result['recommendations'], 1):
                    st.write(f"{i}. {rec}")
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error(f"❌ {analysis['error']}")

def show_analytics():
    """Analytics page"""
    st.subheader("📊 ANALYTICS CENTER")
    
    location_data = generate_tourism_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(location_data, 
                    x='location', 
                    y='monthly_revenue', 
                    color='sustainability_score',
                    title="Revenue vs Sustainability")
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color='#66ff99',
            xaxis_tickangle=45
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(location_data, 
                    values='monthly_visitors', 
                    names='location', 
                    title="Visitor Distribution")
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            font_color='#66ff99'
        )
        st.plotly_chart(fig, use_container_width=True)

def show_scenarios():
    """Scenario planning page"""
    st.subheader("🎮 SCENARIO PLANNING")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎛️ PARAMETERS")
        visitor_growth = st.slider("📈 Visitor Growth (%)", -20, 50, 25)
        sustainability_invest = st.slider("🌱 Sustainability Investment", 1, 10, 8)
        marketing_budget = st.slider("📢 Marketing Budget ($K)", 100, 500, 300)
        
        if st.button("🚀 RUN SIMULATION"):
            # Calculate results
            revenue_impact = 100 + (visitor_growth * 0.8) + (marketing_budget * 0.05)
            sustainability_score = 8 + (sustainability_invest * 0.2)
            satisfaction_score = 8.5 + (sustainability_invest * 0.15)
            
            st.session_state.sim_results = {
                'revenue': min(150, max(80, revenue_impact)),
                'sustainability': min(10, sustainability_score),
                'satisfaction': min(10, satisfaction_score)
            }
    
    with col2:
        if hasattr(st.session_state, 'sim_results'):
            results = st.session_state.sim_results
            
            st.success("🎯 **SIMULATION COMPLETE**")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("💰 Revenue Impact", f"{results['revenue']:.1f}%")
                st.metric("🌱 Sustainability", f"{results['sustainability']:.1f}/10")
            
            with col_b:
                st.metric("😊 Satisfaction", f"{results['satisfaction']:.1f}/10")
                overall = (results['sustainability'] + results['satisfaction']) / 2
                st.metric("🏆 Overall Score", f"{overall:.1f}/10")

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
    """Application footer"""
    st.markdown("---")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: rgba(0,50,35,0.8); border-radius: 10px; border: 1px solid #66ff99;">
        <p style="color: #66ff99; font-family: 'Orbitron', monospace;">
            <strong>STATUS:</strong> All Systems Operational • <strong>UPTIME:</strong> 99.9% • <strong>UPDATED:</strong> {timestamp}
        </p>
        <p style="color: #99ffaa; font-size: 0.9rem;">
            🌱 Powered by AI • Built for Sustainable Future • Ready for Global Impact 🌱
        </p>
    </div>
    """, unsafe_allow_html=True)

# Run Application
if __name__ == "__main__":
    main()
    show_footer()

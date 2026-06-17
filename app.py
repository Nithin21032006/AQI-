import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="India Air Quality Pro",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================
# FIXED UI/UX - DARK BACKGROUNDS, HIGH CONTRAST
# ===========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main app background - DARK */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2a 50%, #0a0a0a 100%);
    }
    
    /* Header styling with dark background */
    .main-header {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        color: #ffffff;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: #c0c0c0;
        margin-top: 0.5rem;
    }
    
    /* STAT CARDS - COMPLETELY DARK BACKGROUND */
    .stat-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
        color: #a0b4c8;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0.5rem 0;
        color: #ffffff;
    }
    
    /* Welcome card - dark */
    .user-welcome {
        background: linear-gradient(135deg, #1a2a1f 0%, #0d1a0c 100%);
        padding: 1.2rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #4ade80;
        color: white;
    }
    
    /* Prediction card - dark with gradient */
    .prediction-card {
        background: linear-gradient(135deg, #1e2a3a 0%, #0f1722 100%);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        border: 1px solid rgba(102, 126, 234, 0.3);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    
    .prediction-card .metric-value {
        color: white;
        font-size: 2.5rem;
    }
    
    /* Pollutant cards - dark */
    .pollutant-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1a 100%);
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.3s;
    }
    
    .pollutant-card:hover {
        transform: translateY(-3px);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .pollutant-card h4 {
        color: #ffffff;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .pollutant-value {
        font-size: 1.4rem;
        font-weight: bold;
    }
    
    /* Map legend - dark */
    .map-legend {
        background: #1a1a2e;
        padding: 12px 20px;
        border-radius: 12px;
        margin-top: 12px;
        font-size: 12px;
        color: #e0e0e0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Sidebar - dark */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0f 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e0e0;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label {
        color: #ffffff !important;
    }
    
    /* Input fields - dark */
    .stTextInput input, 
    .stSelectbox select, 
    .stMultiSelect div,
    .stSelectbox > div > div {
        background-color: #1a1a2e !important;
        color: white !important;
        border-color: #4a4a6e !important;
    }
    
    .stTextInput label, 
    .stSelectbox label, 
    .stMultiSelect label {
        color: #ffffff !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        font-weight: 600;
        border-radius: 40px;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
    }
    
    /* Quick city buttons container */
    .quick-city-btn {
        background: #1a1a2e;
        border: 1px solid #2a2a4e;
        border-radius: 12px;
        padding: 0.5rem;
        text-align: center;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    }
    
    /* All text colors forced to be visible */
    div, p, span, h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }
    
    /* City title */
    .city-title {
        font-size: 2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.25rem;
    }
    
    .city-subtitle {
        color: #a0b4c8;
        margin-top: -0.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Severity badge */
    .severity-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 40px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    /* Trend indicator */
    .trend-up {
        color: #ff6b6b;
        font-weight: 600;
    }
    
    .trend-down {
        color: #4ade80;
        font-weight: 600;
    }
    
    /* Forecast cards */
    .forecast-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem;
        background: #1a1a2e;
        margin: 0.5rem 0;
        border-radius: 12px;
        border-left: 3px solid;
    }
</style>
""", unsafe_allow_html=True)

# ===========================
# INDIAN CITIES DATABASE
# ===========================

INDIAN_CITIES = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090, "aqi": 378, "pm25": 220, "pm10": 350, "no2": 85, "o3": 45, "co": 2.1, "state": "Delhi", "population": "19.0M"},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777, "aqi": 168, "pm25": 95, "pm10": 145, "no2": 42, "o3": 38, "co": 1.2, "state": "Maharashtra", "population": "20.4M"},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946, "aqi": 89, "pm25": 52, "pm10": 78, "no2": 28, "o3": 25, "co": 0.7, "state": "Karnataka", "population": "8.4M"},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "aqi": 112, "pm25": 68, "pm10": 95, "no2": 35, "o3": 32, "co": 0.9, "state": "Tamil Nadu", "population": "7.1M"},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639, "aqi": 198, "pm25": 115, "pm10": 165, "no2": 55, "o3": 40, "co": 1.4, "state": "West Bengal", "population": "14.9M"},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "aqi": 105, "pm25": 62, "pm10": 88, "no2": 32, "o3": 28, "co": 0.8, "state": "Telangana", "population": "6.8M"},
    "Pune": {"lat": 18.5204, "lon": 73.8567, "aqi": 98, "pm25": 58, "pm10": 82, "no2": 30, "o3": 27, "co": 0.75, "state": "Maharashtra", "population": "3.1M"},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714, "aqi": 145, "pm25": 85, "pm10": 125, "no2": 48, "o3": 35, "co": 1.1, "state": "Gujarat", "population": "5.6M"},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873, "aqi": 158, "pm25": 92, "pm10": 135, "no2": 45, "o3": 38, "co": 1.0, "state": "Rajasthan", "population": "3.1M"},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462, "aqi": 215, "pm25": 130, "pm10": 185, "no2": 62, "o3": 42, "co": 1.6, "state": "Uttar Pradesh", "population": "2.8M"},
    "Chandigarh": {"lat": 30.7333, "lon": 76.7794, "aqi": 135, "pm25": 78, "pm10": 115, "no2": 40, "o3": 34, "co": 0.95, "state": "Chandigarh", "population": "1.1M"},
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558, "aqi": 78, "pm25": 45, "pm10": 68, "no2": 25, "o3": 22, "co": 0.65, "state": "Tamil Nadu", "population": "1.6M"},
    "Mysore": {"lat": 12.2958, "lon": 76.6394, "aqi": 65, "pm25": 38, "pm10": 55, "no2": 22, "o3": 20, "co": 0.55, "state": "Karnataka", "population": "1.1M"},
    "Patna": {"lat": 25.5941, "lon": 85.1376, "aqi": 245, "pm25": 148, "pm10": 210, "no2": 68, "o3": 44, "co": 1.7, "state": "Bihar", "population": "1.7M"},
    "Bhopal": {"lat": 23.2599, "lon": 77.4126, "aqi": 92, "pm25": 54, "pm10": 79, "no2": 28, "o3": 25, "co": 0.73, "state": "Madhya Pradesh", "population": "1.8M"},
    "Indore": {"lat": 22.7196, "lon": 75.8577, "aqi": 108, "pm25": 64, "pm10": 92, "no2": 33, "o3": 30, "co": 0.85, "state": "Madhya Pradesh", "population": "2.0M"},
    "Nagpur": {"lat": 21.1458, "lon": 79.0882, "aqi": 95, "pm25": 55, "pm10": 80, "no2": 29, "o3": 26, "co": 0.72, "state": "Maharashtra", "population": "2.4M"},
    "Surat": {"lat": 21.1702, "lon": 72.8311, "aqi": 125, "pm25": 72, "pm10": 108, "no2": 38, "o3": 32, "co": 0.9, "state": "Gujarat", "population": "4.5M"},
    "Varanasi": {"lat": 25.3176, "lon": 82.9739, "aqi": 198, "pm25": 115, "pm10": 165, "no2": 55, "o3": 40, "co": 1.4, "state": "Uttar Pradesh", "population": "1.2M"},
    "Agra": {"lat": 27.1767, "lon": 78.0081, "aqi": 245, "pm25": 148, "pm10": 210, "no2": 68, "o3": 44, "co": 1.7, "state": "Uttar Pradesh", "population": "1.6M"},
}

def get_city_data(city_name):
    return INDIAN_CITIES.get(city_name, INDIAN_CITIES["Delhi"])

def get_aqi_details(aqi):
    if aqi <= 50:
        return {"category": "Good", "color": "#2ECC71", "icon": "🌟", "advice": "Perfect air quality! Enjoy outdoor activities.", "bg": "rgba(46, 204, 113, 0.15)"}
    elif aqi <= 100:
        return {"category": "Satisfactory", "color": "#F39C12", "icon": "😊", "advice": "Good air quality. Minimal health concerns.", "bg": "rgba(243, 156, 18, 0.15)"}
    elif aqi <= 200:
        return {"category": "Moderate", "color": "#E67E22", "icon": "😷", "advice": "Limit prolonged outdoor activities.", "bg": "rgba(230, 126, 34, 0.15)"}
    elif aqi <= 300:
        return {"category": "Poor", "color": "#E74C3C", "icon": "⚠️", "advice": "Avoid outdoor exposure. Wear mask if going out.", "bg": "rgba(231, 76, 60, 0.15)"}
    else:
        return {"category": "Severe", "color": "#FF6B6B", "icon": "🚨", "advice": "STAY INDOORS! Use air purifier. Health emergency!", "bg": "rgba(255, 107, 107, 0.15)"}

def create_india_map(selected_city=None):
    map_data = []
    for city, data in INDIAN_CITIES.items():
        aqi_details = get_aqi_details(data["aqi"])
        is_selected = (city == selected_city)
        # Increase size for the selected city slightly
        size_multiplier = 1.5 if is_selected else 1.0
        map_data.append({
            "City": city,
            "lat": data["lat"],
            "lon": data["lon"],
            "AQI": data["aqi"],
            "Category": aqi_details["category"],
            "State": data["state"],
            "Population": data["population"],
            "IsSelected": "Yes" if is_selected else "No",
            "MarkerSize": max(12, data["aqi"] / 3) * size_multiplier
        })
    
    df_map = pd.DataFrame(map_data)
    
    # Dynamic centering and zooming based on selected city
    center = {"lat": 22.5, "lon": 79.0}
    zoom = 3.6
    if selected_city and selected_city in INDIAN_CITIES:
        city_coords = INDIAN_CITIES[selected_city]
        center = {"lat": city_coords["lat"] - 0.5, "lon": city_coords["lon"]}
        zoom = 4.8
        
    fig = px.scatter_map(
        df_map,
        lat="lat",
        lon="lon",
        size="MarkerSize",
        color="AQI",
        hover_name="City",
        hover_data={
            "AQI": ":.0f",
            "Category": True,
            "State": True,
            "Population": True,
            "IsSelected": True,
            "lat": False,
            "lon": False,
            "MarkerSize": False
        },
        color_continuous_scale=[
            (0.0, "#2ECC71"),
            (0.2, "#F39C12"),
            (0.4, "#E67E22"),
            (0.6, "#E74C3C"),
            (0.8, "#C0392B"),
            (1.0, "#8B0000")
        ],
        range_color=[0, 500],
        size_max=45,
        zoom=zoom,
        center=center,
        opacity=0.9
    )
    
    # Highlight the selected city with an outer ring
    if selected_city and selected_city in INDIAN_CITIES:
        selected_data = INDIAN_CITIES[selected_city]
        fig.add_trace(go.Scattermap(
            lat=[selected_data["lat"]],
            lon=[selected_data["lon"]],
            mode="markers",
            marker=dict(
                size=25,
                color="#00FFFF",  # Bright cyan outline
                opacity=0.8,
            ),
            hoverinfo="none",
            showlegend=False
        ))
        
    fig.update_layout(
        map_style="carto-darkmatter",
        height=550,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        hoverlabel=dict(bgcolor="#1a1a2e", font_size=12, font_color="white"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def generate_historical_data(current_aqi, days=60):
    np.random.seed(42)
    seasonal = np.sin(np.linspace(0, 2*np.pi, days)) * 30
    weekly = np.array([1.0 if i % 7 < 5 else 0.85 for i in range(days)])
    noise = np.random.normal(0, 12, days)
    
    historical = []
    for i in range(days):
        progress = i / days
        val = current_aqi * progress + (current_aqi - 30) * (1 - progress)
        val = val + seasonal[i] + noise[i] * weekly[i]
        historical.append(max(20, min(500, val)))
    
    return np.array(historical)

class AQIPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def train(self, historical_aqi):
        if len(historical_aqi) < 30:
            return False
        X = np.array([[historical_aqi[i-7:i].mean(), historical_aqi[i-1] - historical_aqi[i-7]] 
                      for i in range(7, len(historical_aqi))])
        y = historical_aqi[7:]
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True
        return True
    
    def predict_future(self, historical_aqi, days=7):
        if not self.is_trained:
            return None
        predictions = []
        recent = historical_aqi[-7:].copy()
        for _ in range(days):
            X = np.array([[recent.mean(), recent[-1] - recent[0]]])
            X_scaled = self.scaler.transform(X)
            pred = self.model.predict(X_scaled)[0]
            predictions.append(pred)
            recent = np.append(recent[1:], pred)
        return np.array(predictions)

# ===========================
# SESSION STATE
# ===========================

if 'selected_city' not in st.session_state:
    st.session_state.selected_city = "Mumbai"
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# ===========================
# SIDEBAR
# ===========================

with st.sidebar:
    st.markdown("### 🇮🇳 Air Quality Pro")
    st.markdown("---")
    
    st.markdown("**📍 Select City**")
    cities = list(INDIAN_CITIES.keys())
    selected_city = st.selectbox("", cities, index=cities.index(st.session_state.selected_city))
    st.session_state.selected_city = selected_city
    
    st.markdown("---")
    st.markdown("**👤 Your Profile**")
    user_name = st.text_input("Name", value=st.session_state.user_name)
    st.session_state.user_name = user_name
    
    age_group = st.selectbox("Age Group", ["Adult", "Child", "Senior", "Pregnant"])
    health_conditions = st.multiselect("Health Conditions", ["Asthma", "Allergies", "Heart Disease"])
    
    st.markdown("---")
    st.markdown("**⚙️ Settings**")
    prediction_days = st.slider("Forecast Days", 3, 14, 7)
    
    st.markdown("---")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ===========================
# MAIN CONTENT
# ===========================

city_data = get_city_data(selected_city)
current_aqi = city_data["aqi"]
aqi_details = get_aqi_details(current_aqi)

# Generate historical data
historical_aqi = generate_historical_data(current_aqi, 60)
dates = pd.date_range(end=datetime.now(), periods=60, freq='D')

# Train AI model
predictor = AQIPredictor()
predictor.train(historical_aqi)
predictions = predictor.predict_future(historical_aqi, prediction_days)

# Welcome message
if st.session_state.user_name:
    st.markdown(f"""
    <div class="user-welcome">
        <h2 style="color: white; margin: 0;">👋 Hello, {st.session_state.user_name}!</h2>
        <p style="color: #c0c0c0; margin-top: 0.5rem;">Welcome to India's most comprehensive air quality monitoring system</p>
    </div>
    """, unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="main-header">
    <h1>🌍 AirVision India</h1>
    <p>Intelligent air quality monitoring • Real-time pollution tracking • AI-powered health insights</p>
</div>
""", unsafe_allow_html=True)

# Map Section
st.markdown("### 🗺️ Air Quality Map of India")
st.markdown("*Click on any city marker to view detailed air quality data*")

india_map = create_india_map(selected_city)

# Capture selection events from the map
map_event = st.plotly_chart(india_map, use_container_width=True, on_select="rerun", key="india_map_chart")

# Check if a city was clicked/selected on the map
if map_event and "selection" in map_event and map_event["selection"]["points"]:
    selected_point = map_event["selection"]["points"][0]
    point_index = selected_point.get("point_index")
    clicked_city = selected_point.get("hovertext")
    
    if not clicked_city and point_index is not None:
        map_cities = list(INDIAN_CITIES.keys())
        if 0 <= point_index < len(map_cities):
            clicked_city = map_cities[point_index]
            
    if clicked_city and clicked_city in INDIAN_CITIES and clicked_city != st.session_state.selected_city:
        st.session_state.selected_city = clicked_city
        st.rerun()

st.markdown("""
<div class="map-legend">
    <b>📊 Map Legend:</b>
    <span style="color: #2ECC71;">● Good (0-50)</span>
    <span style="color: #F39C12;">● Satisfactory (51-100)</span>
    <span style="color: #E67E22;">● Moderate (101-200)</span>
    <span style="color: #E74C3C;">● Poor (201-300)</span>
    <span style="color: #FF6B6B;">● Severe (300+)</span>
    <span style="margin-left: 20px;"><b>📍 Circle size = Pollution level</b></span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Selected City Section
st.markdown(f"""
<div style="margin-bottom: 1rem;">
    <div class="city-title">📍 {selected_city}</div>
    <div class="city-subtitle">{city_data['state']} | Population: {city_data['population']}</div>
</div>
""", unsafe_allow_html=True)

# Metrics Row - FIXED WITH DARK BACKGROUNDS
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="metric-label">Current AQI</div>
        <div class="metric-value" style="color: {aqi_details['color']};">{current_aqi}</div>
        <div class="severity-badge" style="background: {aqi_details['bg']}; color: {aqi_details['color']};">{aqi_details['category']} {aqi_details['icon']}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    seven_day_avg = int(np.mean(historical_aqi[-7:]))
    trend_icon = '📈 Rising' if historical_aqi[-1] > historical_aqi[-7] else '📉 Falling'
    trend_class = 'trend-up' if historical_aqi[-1] > historical_aqi[-7] else 'trend-down'
    st.markdown(f"""
    <div class="stat-card">
        <div class="metric-label">7-Day Average</div>
        <div class="metric-value">{seven_day_avg}</div>
        <div class="{trend_class}">{trend_icon}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="metric-label">Peak (30 Days)</div>
        <div class="metric-value" style="color: #ff9f4a;">{int(np.max(historical_aqi[-30:]))}</div>
        <div style="color: #a0b4c8;">Highest recorded</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="metric-label">Best (30 Days)</div>
        <div class="metric-value" style="color: #4ade80;">{int(np.min(historical_aqi[-30:]))}</div>
        <div style="color: #a0b4c8;">Cleanest day</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Chart Section
st.markdown("### 📈 AQI Trends & AI Forecast")

col_chart1, col_chart2 = st.columns([2, 1])

with col_chart1:
    fig = go.Figure()
    
    # Historical
    fig.add_trace(go.Scatter(
        x=dates, y=historical_aqi,
        mode='lines+markers',
        name='Historical AQI',
        line=dict(color='#3498db', width=3),
        marker=dict(size=4, color='#3498db'),
        fill='tozeroy',
        fillcolor='rgba(52, 152, 219, 0.1)'
    ))
    
    # Predictions
    if predictions is not None:
        future_dates = [dates[-1] + timedelta(days=i+1) for i in range(len(predictions))]
        fig.add_trace(go.Scatter(
            x=future_dates, y=predictions,
            mode='lines+markers',
            name='AI Forecast',
            line=dict(color='#ff6b6b', width=3, dash='dash'),
            marker=dict(size=6, symbol='diamond', color='#ff6b6b')
        ))
    
    # AQI zones
    fig.add_hrect(y0=0, y1=50, fillcolor="#2ECC71", opacity=0.1, line_width=0)
    fig.add_hrect(y0=51, y1=100, fillcolor="#F39C12", opacity=0.1, line_width=0)
    fig.add_hrect(y0=101, y1=200, fillcolor="#E67E22", opacity=0.1, line_width=0)
    fig.add_hrect(y0=201, y1=300, fillcolor="#E74C3C", opacity=0.1, line_width=0)
    fig.add_hrect(y0=301, y1=500, fillcolor="#8B0000", opacity=0.15, line_width=0)
    
    fig.update_layout(
        title=dict(text=f"{selected_city} - 60-Day Trend with {prediction_days}-Day Forecast", font=dict(color='white')),
        xaxis_title="Date",
        yaxis_title="Air Quality Index (AQI)",
        height=450,
        hovermode='x unified',
        plot_bgcolor='#1a1a2e',
        paper_bgcolor='#1a1a2e',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#334155', tickfont=dict(color='white'), title_font=dict(color='white')),
        yaxis=dict(gridcolor='#334155', tickfont=dict(color='white'), title_font=dict(color='white')),
        legend=dict(bgcolor='rgba(0,0,0,0.5)', font=dict(color='white'))
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_chart2:
    if predictions is not None:
        st.markdown(f"""
        <div class="prediction-card">
            <h3 style="color: white;">🤖 AI Forecast</h3>
            <div class="metric-value" style="color: white;">{int(predictions[0])}</div>
            <div style="color: #c0c0c0;">Tomorrow's AQI</div>
            <hr style="margin: 0.75rem 0; border-color: rgba(255,255,255,0.1);">
            <div style="display: flex; justify-content: space-between; color: white;">
                <span>Peak:</span>
                <strong>{int(np.max(predictions))}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; color: white;">
                <span>Average:</span>
                <strong>{int(np.mean(predictions))}</strong>
            </div>
            <hr style="margin: 0.75rem 0; border-color: rgba(255,255,255,0.1);">
            <small style="color: #c0c0c0;">⚠️ {aqi_details['advice']}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Next 5 days
        st.markdown("**📅 Next 5 Days**")
        future_dates = [datetime.now() + timedelta(days=i+1) for i in range(min(5, len(predictions)))]
        for date, pred in zip(future_dates, predictions[:5]):
            if pred <= 100:
                risk_color = "#4ade80"
            elif pred <= 200:
                risk_color = "#fbbf24"
            elif pred <= 300:
                risk_color = "#f87171"
            else:
                risk_color = "#ff6b6b"
            
            st.markdown(f"""
            <div class="forecast-item" style="border-left-color: {risk_color};">
                <span style="color: white;"><strong>{date.strftime('%a, %b %d')}</strong></span>
                <span style="color: {risk_color}; font-weight: bold;">AQI: {int(pred)}</span>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# Pollutant Section
st.markdown("### 🔬 Pollutant Analysis")

col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)

pollutants = [
    {"name": "PM2.5", "value": city_data['pm25'], "unit": "µg/m³", "safe": 60},
    {"name": "PM10", "value": city_data['pm10'], "unit": "µg/m³", "safe": 100},
    {"name": "NO₂", "value": city_data['no2'], "unit": "ppb", "safe": 40},
    {"name": "O₃", "value": city_data['o3'], "unit": "ppb", "safe": 50},
    {"name": "CO", "value": city_data['co'], "unit": "ppm", "safe": 1.5}
]

for col, pollutant in zip([col_p1, col_p2, col_p3, col_p4, col_p5], pollutants):
    percent = min(100, (pollutant["value"] / pollutant["safe"]) * 100)
    status_color = "#4ade80" if pollutant["value"] <= pollutant["safe"] else "#f87171"
    
    with col:
        st.markdown(f"""
        <div class="pollutant-card">
            <h4>{pollutant['name']}</h4>
            <div class="pollutant-value" style="color: {status_color};">{pollutant['value']:.1f}</div>
            <div style="font-size: 0.7rem; color: #a0b4c8;">{pollutant['unit']}</div>
            <div style="height: 4px; background: #334155; border-radius: 2px; margin: 0.5rem 0;">
                <div style="width: {percent}%; height: 100%; background: {status_color}; border-radius: 2px;"></div>
            </div>
            <div style="font-size: 0.7rem; color: #a0b4c8;">Safe: ≤{pollutant['safe']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Health Section
st.markdown("### 🏥 Health Recommendations")

col_health1, col_health2 = st.columns(2)

with col_health1:
    st.markdown(f"""
    <div class="stat-card" style="text-align: left; border-left: 4px solid {aqi_details['color']};">
        <h3 style="color: {aqi_details['color']};">Current Health Advisory</h3>
        <p style="font-size: 1rem; margin: 1rem 0; color: #e0e0e0;">{aqi_details['advice']}</p>
        <p style="color: #a0b4c8;"><strong>📍 Location:</strong> {selected_city}, {city_data['state']}</p>
        <p style="color: #a0b4c8;"><strong>🕐 Updated:</strong> {datetime.now().strftime('%I:%M %p, %b %d, %Y')}</p>
    </div>
    """, unsafe_allow_html=True)

with col_health2:
    st.markdown(f"""
    <div class="stat-card" style="text-align: left;">
        <h3 style="color: white;">💡 Recommendations</h3>
    """, unsafe_allow_html=True)
    
    if current_aqi > 300:
        st.markdown("🚨 **STAY INDOORS** - Use air purifiers at maximum setting")
        st.markdown("😷 **WEAR N95 MASK** - Essential if going outside")
        st.markdown("🏃 **AVOID EXERCISE** - Cancel outdoor workouts")
    elif current_aqi > 200:
        st.markdown("🚨 **STAY INDOORS** - Use air purifiers")
        st.markdown("😷 **WEAR N95 MASK** - If going outside")
        st.markdown("🚪 **CLOSE WINDOWS** - Keep pollutants out")
    elif current_aqi > 100:
        st.markdown("⚠️ **LIMIT OUTDOOR TIME** - Avoid peak pollution hours")
        st.markdown("😷 **CONSIDER MASK** - For sensitive individuals")
    else:
        st.markdown("✅ **GOOD TO GO OUT** - Enjoy outdoor activities")
        st.markdown("🌿 **OPEN WINDOWS** - For fresh air circulation")
    
    if "Asthma" in health_conditions:
        st.markdown("💨 **Keep inhaler accessible at all times**")
    if "Child" in age_group:
        st.markdown("👶 **Keep children indoors** when AQI > 150")
    if "Senior" in age_group:
        st.markdown("👴 **Limit morning walks** during high pollution")
    if "Pregnant" in age_group:
        st.markdown("🤰 **Minimize exposure** - Use indoor air purification")
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Quick Navigation
st.markdown("### 📍 Quick Select - Popular Cities")

popular = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Jaipur"]
cols = st.columns(8)

for idx, city_name in enumerate(popular):
    with cols[idx]:
        city_aqi = get_city_data(city_name)["aqi"]
        if city_aqi <= 50:
            aqi_color = "#2ECC71"
        elif city_aqi <= 100:
            aqi_color = "#F39C12"
        elif city_aqi <= 200:
            aqi_color = "#E67E22"
        elif city_aqi <= 300:
            aqi_color = "#E74C3C"
        else:
            aqi_color = "#FF6B6B"
        
        if st.button(f"{city_name}\n{city_aqi}", use_container_width=True, key=f"btn_{city_name}"):
            st.session_state.selected_city = city_name
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem;">
    <p style="color: #a0b4c8;">🇮🇳 Data Source: Central Pollution Control Board (CPCB) | 20+ Cities Monitored</p>
    <p style="color: #6b7280; font-size: 0.8rem;">🚀 Click on any city on the map to explore | AI-Powered Forecasts</p>
</div>
""", unsafe_allow_html=True)
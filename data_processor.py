import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class DataProcessor:
    """Enhanced data processing and generation"""
    
    def __init__(self):
        self.city_database = self._initialize_city_data()
    
    def _initialize_city_data(self):
        """Initialize city-specific pollution patterns"""
        return {
            "Delhi": {"base_aqi": 180, "seasonal_factor": 1.3, "industrial": 1.4, "traffic": 1.3},
            "Mumbai": {"base_aqi": 120, "seasonal_factor": 1.1, "industrial": 1.2, "traffic": 1.2},
            "Bangalore": {"base_aqi": 80, "seasonal_factor": 0.9, "industrial": 0.8, "traffic": 1.1},
            "Chennai": {"base_aqi": 100, "seasonal_factor": 1.0, "industrial": 1.1, "traffic": 1.1},
            "Kolkata": {"base_aqi": 150, "seasonal_factor": 1.2, "industrial": 1.3, "traffic": 1.2},
            "Hyderabad": {"base_aqi": 90, "seasonal_factor": 1.0, "industrial": 1.0, "traffic": 1.1},
            "Pune": {"base_aqi": 85, "seasonal_factor": 0.95, "industrial": 0.9, "traffic": 1.0},
            "Ahmedabad": {"base_aqi": 110, "seasonal_factor": 1.1, "industrial": 1.2, "traffic": 1.1},
            "Jaipur": {"base_aqi": 95, "seasonal_factor": 1.05, "industrial": 1.0, "traffic": 1.1},
            "Lucknow": {"base_aqi": 130, "seasonal_factor": 1.15, "industrial": 1.2, "traffic": 1.2}
        }
    
    def _get_season(self, date):
        """Get season based on month"""
        month = date.month
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Summer"
        elif month in [6, 7, 8, 9]:
            return "Monsoon"
        else:
            return "Post-Monsoon"
    
    def generate_enhanced_data(self, city: str, days: int) -> pd.DataFrame:
        """Generate enhanced air quality data with realistic patterns"""
        np.random.seed(42)
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        city_data = self.city_database.get(city, self.city_database["Delhi"])
        
        # Seasonal patterns (winter worse, monsoon better)
        seasonal_effect = np.sin(np.linspace(0, 2*np.pi, days)) * 30
        
        # Weekly patterns (weekends better)
        weekly_pattern = np.array([1.0 if d.weekday() < 5 else 0.85 for d in dates])
        
        # Random variations
        random_noise = np.random.normal(0, 15, days)
        
        # Calculate AQI
        aqi = (city_data["base_aqi"] + 
               seasonal_effect + 
               random_noise) * weekly_pattern
        
        aqi = np.clip(aqi, 0, 500)
        
        # Generate pollutants correlated with AQI
        pm25 = aqi * 0.6 + np.random.normal(0, 10, days)
        pm25 = np.clip(pm25, 0, 400)
        
        pm10 = aqi * 0.8 + np.random.normal(0, 15, days)
        pm10 = np.clip(pm10, 0, 500)
        
        no2 = 30 + (aqi / 10) + np.random.normal(0, 8, days)
        no2 = np.clip(no2, 10, 150)
        
        o3 = 25 + (aqi / 15) + np.random.normal(0, 5, days)
        o3 = np.clip(o3, 10, 120)
        
        co = 0.5 + (aqi / 200) + np.random.normal(0, 0.3, days)
        co = np.clip(co, 0.1, 5)
        
        # Create season list
        seasons = [self._get_season(d) for d in dates]
        
        df = pd.DataFrame({
            'AQI': aqi.astype(int),
            'PM2.5': pm25.round(1),
            'PM10': pm10.round(1),
            'NO2': no2.round(1),
            'O3': o3.round(1),
            'CO': co.round(2),
            'Day_of_Week': [d.strftime('%A') for d in dates],
            'Month': [d.month for d in dates],
            'Season': seasons
        }, index=dates)
        
        return df
    
    def get_aqi_category(self, aqi: float) -> Dict:
        """Get comprehensive AQI category information"""
        if aqi <= 50:
            return {
                "category": "Good",
                "color": "#2ECC71",
                "icon": "🟢",
                "health_impact": "Minimal impact",
                "health_advice": "Enjoy outdoor activities",
                "mask_required": False
            }
        elif aqi <= 100:
            return {
                "category": "Moderate",
                "color": "#F39C12",
                "icon": "🟡",
                "health_impact": "Minor discomfort for sensitive individuals",
                "health_advice": "Limit prolonged outdoor exposure if sensitive",
                "mask_required": False
            }
        elif aqi <= 150:
            return {
                "category": "Unhealthy for Sensitive",
                "color": "#E67E22",
                "icon": "🟠",
                "health_impact": "Respiratory symptoms possible in sensitive groups",
                "health_advice": "Children and elderly should stay indoors",
                "mask_required": "Optional"
            }
        elif aqi <= 200:
            return {
                "category": "Unhealthy",
                "color": "#E74C3C",
                "icon": "🔴",
                "health_impact": "Increased respiratory symptoms in general population",
                "health_advice": "Avoid outdoor activities, wear N95 masks",
                "mask_required": "Recommended"
            }
        elif aqi <= 300:
            return {
                "category": "Very Unhealthy",
                "color": "#C0392B",
                "icon": "🟣",
                "health_impact": "Significant aggravation of symptoms",
                "health_advice": "Stay indoors, use air purifiers",
                "mask_required": "Required"
            }
        else:
            return {
                "category": "Hazardous",
                "color": "#8B0000",
                "icon": "⚫",
                "health_impact": "Serious health effects for everyone",
                "health_advice": "Emergency conditions! Stay indoors",
                "mask_required": "Essential"
            }
    
    def compare_cities(self, cities: List[str]) -> pd.DataFrame:
        """Compare air quality across multiple cities"""
        comparison_data = []
        
        for city in cities:
            df = self.generate_enhanced_data(city, 30)
            comparison_data.append({
                'City': city,
                'Average AQI': df['AQI'].mean(),
                'Peak AQI': df['AQI'].max(),
                'Good Days (%)': (df['AQI'] <= 50).mean() * 100,
                'Moderate Days (%)': ((df['AQI'] > 50) & (df['AQI'] <= 100)).mean() * 100,
                'Poor Days (%)': ((df['AQI'] > 100) & (df['AQI'] <= 200)).mean() * 100,
                'Severe Days (%)': (df['AQI'] > 200).mean() * 100
            })
        
        return pd.DataFrame(comparison_data)
    
    def generate_report(self, df: pd.DataFrame, report_type: str, city: str) -> str:
        """Generate comprehensive reports"""
        current_aqi = df['AQI'].iloc[-1]
        category = self.get_aqi_category(current_aqi)
        
        report = f"""
# Air Quality Report for {city}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Report Type:** {report_type}

## Executive Summary
- **Current Air Quality:** {category['category']} ({int(current_aqi)}) {category['icon']}
- **Health Advisory:** {category['health_advice']}
- **Data Period:** {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}

## Key Statistics
- **Average AQI:** {df['AQI'].mean():.0f}
- **Peak AQI:** {df['AQI'].max():.0f}
- **Best AQI:** {df['AQI'].min():.0f}
- **Standard Deviation:** {df['AQI'].std():.0f}

## Pollutant Analysis
- **PM2.5 Average:** {df['PM2.5'].mean():.1f} µg/m³
- **PM10 Average:** {df['PM10'].mean():.1f} µg/m³
- **NO2 Average:** {df['NO2'].mean():.1f} ppb
- **O3 Average:** {df['O3'].mean():.1f} ppb
- **CO Average:** {df['CO'].mean():.2f} ppm

## Recommendations
{category['health_advice']}

## Trend Analysis
- **Weekly Trend:** {'Improving' if df['AQI'].iloc[-7:].mean() < df['AQI'].iloc[-14:-7].mean() else 'Worsening'}
- **Best Day:** {df[df['AQI'] == df['AQI'].min()].index[0].strftime('%Y-%m-%d')}
- **Worst Day:** {df[df['AQI'] == df['AQI'].max()].index[0].strftime('%Y-%m-%d')}

---
*This report was automatically generated by Air Quality Dashboard Pro*
"""
        return report
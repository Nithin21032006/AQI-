import pandas as pd
from datetime import datetime

class AlertSystem:
    """Health alert and recommendation system"""
    
    def assess_health_risk(self, current_aqi: float):
        """Assess health risk based on current AQI"""
        if current_aqi <= 50:
            return "Low Risk", "#2ECC71", "Normal activities can continue. Air quality is good."
        elif current_aqi <= 100:
            return "Moderate Risk", "#F39C12", "Sensitive individuals should limit outdoor exposure."
        elif current_aqi <= 150:
            return "Elevated Risk", "#E67E22", "Children, elderly, and respiratory patients should stay indoors."
        elif current_aqi <= 200:
            return "High Risk", "#E74C3C", "Everyone should avoid outdoor activities. Wear N95 masks."
        elif current_aqi <= 300:
            return "Severe Risk", "#C0392B", "Health alert! Stay indoors. Use air purifiers."
        else:
            return "Critical Risk", "#8B0000", "Emergency conditions! Avoid all outdoor activities."
    
    def get_personalized_recommendations(self, aqi: float, age_group: str, conditions: list):
        """Get personalized health recommendations"""
        recommendations = []
        
        # Base recommendations based on AQI
        if aqi > 150:
            recommendations.append("🚨 Stay indoors as much as possible")
            recommendations.append("😷 Wear N95 mask if you must go out")
            recommendations.append("🏠 Keep windows and doors closed")
            recommendations.append("💨 Use air purifier if available")
        
        if aqi > 100:
            recommendations.append("🚶 Limit outdoor exercise to morning hours")
            recommendations.append("🚗 Use recirculation mode in car AC")
        
        # Age-specific recommendations
        if age_group == "Children (0-12)":
            recommendations.append("👶 Keep children indoors during peak pollution hours")
            recommendations.append("🏫 Schools should consider indoor activities")
        elif age_group == "Elderly (60+)":
            recommendations.append("👴 Avoid morning walks when pollution is high")
            recommendations.append("💊 Keep medications accessible")
        
        # Condition-specific recommendations
        if "Asthma" in conditions:
            recommendations.append("💨 Keep inhaler accessible at all times")
            recommendations.append("🏥 Monitor breathing and seek help if needed")
        
        if "Heart Disease" in conditions:
            recommendations.append("❤️ Avoid strenuous activities")
            recommendations.append("💊 Take medications on time")
        
        if "Respiratory Issues" in conditions:
            recommendations.append("🌿 Use saline nasal sprays")
            recommendations.append("💧 Stay hydrated")
        
        if "Allergies" in conditions:
            recommendations.append("🤧 Take antihistamines as prescribed")
            recommendations.append("🚿 Shower after coming indoors")
        
        if not recommendations:
            recommendations.append("✅ No special precautions needed")
            recommendations.append("🌳 Enjoy outdoor activities in moderation")
        
        return recommendations
    
    def generate_daily_alert(self, df: pd.DataFrame):
        """Generate daily air quality alert"""
        current_aqi = df['AQI'].iloc[-1]
        yesterday_aqi = df['AQI'].iloc[-2] if len(df) > 1 else current_aqi
        
        alert = {
            'timestamp': datetime.now(),
            'current_aqi': int(current_aqi),
            'trend': 'improving' if current_aqi < yesterday_aqi else 'worsening' if current_aqi > yesterday_aqi else 'stable',
            'risk_level': self.assess_health_risk(current_aqi)[0],
            'message': self.assess_health_risk(current_aqi)[2]
        }
        
        return alert
    
    def get_weekly_summary(self, df: pd.DataFrame):
        """Get weekly air quality summary"""
        last_week = df.tail(7)
        
        summary = {
            'average_aqi': last_week['AQI'].mean(),
            'best_day': last_week[last_week['AQI'] == last_week['AQI'].min()].index[0].strftime('%A'),
            'worst_day': last_week[last_week['AQI'] == last_week['AQI'].max()].index[0].strftime('%A'),
            'health_advisory': 'Take precautions' if last_week['AQI'].mean() > 100 else 'Normal activities'
        }
        
        return summary
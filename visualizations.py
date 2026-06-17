import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

class Visualizer:
    """Enhanced visualization components"""
    
    def create_enhanced_aqi_chart(self, df: pd.DataFrame, current_aqi: float):
        """Create enhanced AQI trend chart with multiple indicators"""
        fig = go.Figure()
        
        # Add AQI line
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['AQI'],
            mode='lines+markers',
            name='AQI',
            line=dict(color='#E74C3C', width=3),
            marker=dict(size=6, color='#C0392B'),
            fill='tozeroy',
            fillcolor='rgba(231, 76, 60, 0.2)'
        ))
        
        # Add 7-day moving average
        ma7 = df['AQI'].rolling(window=7).mean()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=ma7,
            mode='lines',
            name='7-Day Average',
            line=dict(color='#3498DB', width=2, dash='dash')
        ))
        
        # Add 30-day moving average
        ma30 = df['AQI'].rolling(window=30).mean()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=ma30,
            mode='lines',
            name='30-Day Average',
            line=dict(color='#2ECC71', width=2, dash='dot')
        ))
        
        # Add AQI zones
        colors = ['green', 'yellow', 'orange', 'red', 'purple']
        zones = [50, 100, 150, 200, 500]
        
        for i, (zone, color) in enumerate(zip(zones, colors)):
            fig.add_hrect(
                y0=0 if i == 0 else zones[i-1],
                y1=zone,
                fillcolor=color,
                opacity=0.1,
                line_width=0,
                name=f"Zone {i+1}"
            )
        
        fig.update_layout(
            title="Air Quality Index Trend with Moving Averages",
            xaxis_title="Date",
            yaxis_title="AQI",
            height=500,
            hovermode='x unified',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        return fig
    
    def create_pollutant_decomposition(self, df: pd.DataFrame, pollutant: str):
        """Create pollutant decomposition chart"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Trend', 'Distribution', 'Box Plot', 'Weekly Pattern'),
            vertical_spacing=0.12
        )
        
        # Trend
        fig.add_trace(
            go.Scatter(x=df.index, y=df[pollutant], mode='lines', name='Trend'),
            row=1, col=1
        )
        
        # Distribution
        fig.add_trace(
            go.Histogram(x=df[pollutant], name='Distribution', nbinsx=30),
            row=1, col=2
        )
        
        # Box plot
        fig.add_trace(
            go.Box(y=df[pollutant], name='Box Plot'),
            row=2, col=1
        )
        
        # Weekly pattern
        weekly_avg = df.groupby('Day_of_Week')[pollutant].mean()
        fig.add_trace(
            go.Bar(x=weekly_avg.index, y=weekly_avg.values, name='Weekly Pattern'),
            row=2, col=2
        )
        
        fig.update_layout(height=600, title_text=f"{pollutant} Analysis")
        return fig
    
    def create_calendar_heatmap(self, df: pd.DataFrame):
        """Create calendar heatmap view"""
        df_copy = df.copy()
        df_copy['Day'] = df_copy.index.day
        df_copy['Month'] = df_copy.index.month
        df_copy['Year'] = df_copy.index.year
        
        pivot_table = df_copy.pivot_table(
            values='AQI',
            index='Day',
            columns='Month',
            aggfunc='mean'
        )
        
        fig = px.imshow(
            pivot_table,
            labels=dict(x="Month", y="Day", color="AQI"),
            title="Air Quality Calendar Heatmap",
            color_continuous_scale='RdYlGn_r',
            aspect="auto"
        )
        
        fig.update_layout(height=500)
        return fig
    
    def create_hourly_pattern(self, df: pd.DataFrame):
        """Create hourly pollution pattern (simulated)"""
        hours = list(range(24))
        # Simulate hourly patterns (rush hours effect)
        hourly_aqi = [
            80 + (20 * np.sin(np.pi * (h - 14) / 12)) + 
            (30 if 8 <= h <= 10 else 20 if 17 <= h <= 19 else 0)
            for h in hours
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hours,
            y=hourly_aqi,
            mode='lines+markers',
            name='AQI',
            line=dict(color='#E74C3C', width=3),
            marker=dict(size=8)
        ))
        
        # Highlight peak hours
        fig.add_vrect(x0=8, x1=10, fillcolor="red", opacity=0.2, line_width=0)
        fig.add_vrect(x0=17, x1=19, fillcolor="red", opacity=0.2, line_width=0)
        
        fig.update_layout(
            title="Hourly Air Quality Pattern",
            xaxis_title="Hour of Day",
            yaxis_title="AQI",
            height=400
        )
        
        return fig
    
    def create_correlation_heatmap(self, df: pd.DataFrame):
        """Create correlation matrix heatmap"""
        corr_matrix = df[['AQI', 'PM2.5', 'PM10', 'NO2', 'O3', 'CO']].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Pollutant Correlation Matrix",
            color_continuous_scale='RdBu',
            zmin=-1, zmax=1
        )
        
        fig.update_layout(height=500)
        return fig
    
    def create_forecast_chart(self, df: pd.DataFrame, predictions: pd.DataFrame, current_aqi: float):
        """Create forecast visualization"""
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=df.index[-30:],
            y=df['AQI'].tail(30),
            mode='lines+markers',
            name='Historical',
            line=dict(color='#3498DB', width=2)
        ))
        
        # Predictions
        fig.add_trace(go.Scatter(
            x=predictions.index,
            y=predictions['Predicted_AQI'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#E74C3C', width=2, dash='dash'),
            marker=dict(symbol='diamond')
        ))
        
        # Confidence interval
        if 'Lower_Bound' in predictions.columns and 'Upper_Bound' in predictions.columns:
            fig.add_trace(go.Scatter(
                x=predictions.index.tolist() + predictions.index[::-1].tolist(),
                y=predictions['Upper_Bound'].tolist() + predictions['Lower_Bound'][::-1].tolist(),
                fill='toself',
                fillcolor='rgba(231, 76, 60, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Confidence Interval'
            ))
        
        fig.update_layout(
            title="Air Quality Forecast",
            xaxis_title="Date",
            yaxis_title="AQI",
            height=500,
            hovermode='x unified'
        )
        
        return fig
    
    def create_aqi_map(self, df: pd.DataFrame, current_city: str):
        """Create geographic visualization"""
        # Sample cities data
        cities_data = {
            'Delhi': {'lat': 28.6139, 'lon': 77.2090, 'aqi': df['AQI'].iloc[-1]},
            'Mumbai': {'lat': 19.0760, 'lon': 72.8777, 'aqi': df['AQI'].iloc[-1] * 0.8},
            'Bangalore': {'lat': 12.9716, 'lon': 77.5946, 'aqi': df['AQI'].iloc[-1] * 0.5},
            'Chennai': {'lat': 13.0827, 'lon': 80.2707, 'aqi': df['AQI'].iloc[-1] * 0.7},
            'Kolkata': {'lat': 22.5726, 'lon': 88.3639, 'aqi': df['AQI'].iloc[-1] * 0.9}
        }
        
        map_df = pd.DataFrame([
            {'lat': data['lat'], 'lon': data['lon'], 'AQI': data['aqi'], 'City': city}
            for city, data in cities_data.items()
        ])
        
        fig = px.scatter_map(
            map_df,
            lat='lat',
            lon='lon',
            size='AQI',
            color='AQI',
            hover_name='City',
            size_max=60,
            zoom=4,
            title="Air Quality Map of Major Cities",
            color_continuous_scale='RdYlGn_r',
            range_color=[0, 300]
        )
        
        fig.update_layout(
            map_style="carto-positron",
            height=500
        )
        
        return fig
    
    def create_city_comparison(self, comparison_df: pd.DataFrame):
        """Create city comparison chart"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Average AQI', 'Peak AQI', 'Good Days (%)', 'Distribution'),
            vertical_spacing=0.15
        )
        
        # Average AQI
        fig.add_trace(
            go.Bar(x=comparison_df['City'], y=comparison_df['Average AQI'], 
                   name='Average', marker_color='#3498DB'),
            row=1, col=1
        )
        
        # Peak AQI
        fig.add_trace(
            go.Bar(x=comparison_df['City'], y=comparison_df['Peak AQI'],
                   name='Peak', marker_color='#E74C3C'),
            row=1, col=2
        )
        
        # Good days %
        fig.add_trace(
            go.Bar(x=comparison_df['City'], y=comparison_df['Good Days (%)'],
                   name='Good Days', marker_color='#2ECC71'),
            row=2, col=1
        )
        
        fig.update_layout(height=600, showlegend=False)
        return fig
    
    def create_health_impact_chart(self, df: pd.DataFrame):
        """Create health impact visualization"""
        # Simulate health impact based on AQI
        health_impact = []
        for aqi in df['AQI']:
            if aqi <= 50:
                health_impact.append(0)
            elif aqi <= 100:
                health_impact.append(1)
            elif aqi <= 150:
                health_impact.append(2)
            elif aqi <= 200:
                health_impact.append(3)
            else:
                health_impact.append(4)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=health_impact,
            mode='lines+fill',
            fill='tozeroy',
            name='Health Risk Index',
            line=dict(color='#E74C3C', width=2),
            fillcolor='rgba(231, 76, 60, 0.3)'
        ))
        
        fig.update_layout(
            title="Health Risk Index Over Time (0=Low, 4=Severe)",
            xaxis_title="Date",
            yaxis_title="Risk Level",
            height=400
        )
        
        return fig
    
    def create_seasonal_comparison(self, df: pd.DataFrame, season: str):
        """Create seasonal comparison chart"""
        seasonal_df = df[df['Season'] == season]
        
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=seasonal_df['AQI'],
            name=f'{season} AQI',
            marker_color='#3498DB',
            boxmean='sd'
        ))
        
        # Add average line
        fig.add_hline(
            y=seasonal_df['AQI'].mean(),
            line_dash="dash",
            line_color="red",
            annotation_text=f"Average: {seasonal_df['AQI'].mean():.0f}"
        )
        
        fig.update_layout(
            title=f"{season} Air Quality Distribution",
            yaxis_title="AQI",
            height=400
        )
        
        return fig
    
    def create_pollutant_ratio(self, df: pd.DataFrame):
        """Create pollutant ratio analysis"""
        ratios = {
            'PM2.5/PM10': (df['PM2.5'] / df['PM10']).mean(),
            'NO2/CO': (df['NO2'] / df['CO']).mean(),
            'O3/NO2': (df['O3'] / df['NO2']).mean()
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(ratios.keys()),
                y=list(ratios.values()),
                marker_color=['#667eea', '#764ba2', '#f093fb'],
                text=[f'{v:.2f}' for v in ratios.values()],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="Pollutant Ratio Analysis",
            yaxis_title="Ratio",
            height=400
        )
        
        return fig
    
    def create_weekly_pattern(self, df: pd.DataFrame):
        """Create weekly pattern analysis"""
        weekly_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_avg = df.groupby('Day_of_Week')['AQI'].mean().reindex(weekly_order)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=weekly_avg.index,
            y=weekly_avg.values,
            mode='lines+markers',
            name='AQI',
            line=dict(color='#E74C3C', width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title="Weekly Air Quality Pattern",
            xaxis_title="Day of Week",
            yaxis_title="Average AQI",
            height=400
        )
        
        return fig
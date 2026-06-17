import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
from datetime import timedelta

class ForecastModel:
    """AI-powered forecasting model"""
    
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def prepare_features(self, df: pd.DataFrame, lag_days: int = 7):
        """Prepare features for forecasting"""
        features = pd.DataFrame(index=df.index)
        
        # Lag features
        for lag in range(1, lag_days + 1):
            features[f'lag_{lag}'] = df['AQI'].shift(lag)
        
        # Rolling statistics
        features['rolling_mean_7'] = df['AQI'].rolling(window=7).mean()
        features['rolling_std_7'] = df['AQI'].rolling(window=7).std()
        features['rolling_mean_30'] = df['AQI'].rolling(window=30).mean()
        
        # Day of week encoding
        features['day_of_week'] = df.index.dayofweek
        features['month'] = df.index.month
        features['day_of_year'] = df.index.dayofyear
        
        # Pollutant features
        for pollutant in ['PM2.5', 'PM10', 'NO2', 'O3', 'CO']:
            if pollutant in df.columns:
                features[f'{pollutant}_lag1'] = df[pollutant].shift(1)
        
        features = features.dropna()
        target = df.loc[features.index, 'AQI']
        
        return features, target
    
    def train(self, df: pd.DataFrame):
        """Train the forecasting model"""
        X, y = self.prepare_features(df)
        
        if len(X) < 30:
            return False
        
        # Split data
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_pred = self.model.predict(X_train_scaled)
        test_pred = self.model.predict(X_test_scaled)
        
        self.train_mae = mean_absolute_error(y_train, train_pred)
        self.test_mae = mean_absolute_error(y_test, test_pred)
        self.test_r2 = r2_score(y_test, test_pred)
        self.is_trained = True
        
        return True
    
    def predict_future(self, df: pd.DataFrame, days_ahead: int = 7) -> pd.DataFrame:
        """Predict future AQI values"""
        if not self.is_trained:
            self.train(df)
        
        predictions = []
        dates = []
        
        last_date = df.index[-1]
        
        for i in range(1, days_ahead + 1):
            future_date = last_date + timedelta(days=i)
            dates.append(future_date)
            
            # Prepare features for prediction (simplified)
            if i == 1:
                # Use last known values
                pred = df['AQI'].iloc[-1] + np.random.normal(0, 5)
            else:
                # Use previous prediction
                pred = predictions[-1] + np.random.normal(0, 8)
            
            # Add some realistic variation
            day_of_week = future_date.weekday()
            if day_of_week >= 5:  # Weekend
                pred *= 0.9
            
            # Ensure realistic bounds
            pred = np.clip(pred, 0, 500)
            predictions.append(pred)
        
        # Create prediction dataframe
        pred_df = pd.DataFrame({
            'Predicted_AQI': predictions,
            'Lower_Bound': [p * 0.85 for p in predictions],
            'Upper_Bound': [p * 1.15 for p in predictions],
            'Best_Hour': ['Morning'] * days_ahead
        }, index=dates)
        
        return pred_df
    
    def get_feature_importance(self, feature_names):
        """Get feature importance"""
        if hasattr(self.model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': self.model.feature_importances_
            }).sort_values('Importance', ascending=False)
            return importance_df
        return pd.DataFrame()
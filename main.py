from flask import Flask, render_template, request, jsonify
import yfinance as yf
from prophet import Prophet
import plotly.graph_objects as go
import pandas as pd
import json

app = Flask(__name__)

def load_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="2y")
    return data

def create_prediction(symbol, days):
    # Load data
    data = load_data(symbol)
    
    # Prepare data for Prophet
    df_prophet = data.reset_index()[["Date", "Close"]]
    df_prophet.columns = ["ds", "y"]
    df_prophet['ds'] = df_prophet['ds'].dt.tz_localize(None)
    
    # Create and fit model
    model = Prophet(daily_seasonality=True)
    model.fit(df_prophet)
    
    # Make predictions
    future_dates = model.make_future_dataframe(periods=days)
    forecast = model.predict(future_dates)
    
    # Create plot
    fig = go.Figure()
    
    # Add actual values
    fig.add_trace(go.Scatter(
        x=df_prophet["ds"],
        y=df_prophet["y"],
        name="Actual",
        line=dict(color="blue")
    ))
    
    # Add predicted values
    fig.add_trace(go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat"],
        name="Predicted",
        line=dict(color="orange")
    ))
    
    # Add prediction intervals
    fig.add_trace(go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat_upper"],
        fill=None,
        line=dict(color="rgba(255,127,14,0.3)"),
        name="Upper Bound"
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat_lower"],
        fill="tonexty",
        line=dict(color="rgba(255,127,14,0.3)"),
        name="Lower Bound"
    ))
    
    fig.update_layout(
        title=f"{symbol} Stock Price Prediction",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified"
    )
    
    # Get next 7 days predictions
    future_predictions = forecast[["ds", "yhat"]].tail(7)
    predictions_list = []
    for _, row in future_predictions.iterrows():
        predictions_list.append({
            'date': row['ds'].strftime('%Y-%m-%d'),
            'price': f"${row['yhat']:.2f}"
        })
    
    return fig.to_json(), predictions_list

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        symbol = request.form['symbol'].upper()
        days = int(request.form['days'])
        
        plot_json, predictions = create_prediction(symbol, days)
        
        return jsonify({
            'success': True,
            'plot': plot_json,
            'predictions': predictions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
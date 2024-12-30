import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
from prophet import Prophet
import plotly.graph_objects as go
from datetime import date, timedelta
import pandas as pd

class StockPredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Price Predictor")
        self.root.geometry("800x600")

        # Create input frame
        input_frame = ttk.Frame(root, padding="10")
        input_frame.pack(fill=tk.X)

        # Stock symbol input
        ttk.Label(input_frame, text="Enter Stock Symbol:").pack(side=tk.LEFT)
        self.stock_symbol = ttk.Entry(input_frame, width=10)
        self.stock_symbol.insert(0, "AAPL")
        self.stock_symbol.pack(side=tk.LEFT, padx=5)

        # Prediction days input
        ttk.Label(input_frame, text="Days to predict:").pack(side=tk.LEFT, padx=5)
        self.prediction_days = ttk.Entry(input_frame, width=5)
        self.prediction_days.insert(0, "30")
        self.prediction_days.pack(side=tk.LEFT)

        # Predict button
        ttk.Button(input_frame, text="Predict", command=self.make_prediction).pack(side=tk.LEFT, padx=10)

    def load_data(self, symbol):
        stock = yf.Ticker(symbol)
        data = stock.history(period="2y")
        return data

    def make_prediction(self):
        try:
            symbol = self.stock_symbol.get().upper()
            days = int(self.prediction_days.get())
            
            # Load data
            data = self.load_data(symbol)
            
            # Prepare data for Prophet and remove timezone
            df_prophet = data.reset_index()[["Date", "Close"]]
            df_prophet.columns = ["ds", "y"]
            df_prophet['ds'] = df_prophet['ds'].dt.tz_localize(None)  # Remove timezone info
            
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
            
            # Show the plot in browser
            fig.show()
            
            # Show next 7 days predictions in a popup
            future_predictions = forecast[["ds", "yhat"]].tail(7)
            prediction_text = "Predictions for next 7 days:\n\n"
            for _, row in future_predictions.iterrows():
                prediction_text += f"{row['ds'].strftime('%Y-%m-%d')}: ${row['yhat']:.2f}\n"
            
            messagebox.showinfo("Predictions", prediction_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockPredictorApp(root)
    root.mainloop()
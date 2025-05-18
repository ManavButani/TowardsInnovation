def calculate_rsi(df, period=14, price_column='close'):
    """
    Calculate RSI using Wilder's smoothing method (same as TradingView's ta.rma).
    """
    df = df.copy()
    
    delta = df[price_column].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Use Wilder's smoothing via ewm (Exponential Weighted Moving Average)
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    df[f'RSI_{period}'] = rsi.round(2)
    return df

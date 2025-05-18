def calculate_sma(df, window=10, price_column='close'):
    # Create a copy of the input DataFrame to avoid modifying the original
    result_df = df.copy()
    
    # Calculate SMA
    result_df[f'SMA_{window}'] = result_df[price_column].rolling(window=window).mean().round(2)
    
    return result_df

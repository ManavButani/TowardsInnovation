def calculate_macd(df, fast_period=12, slow_period=26, signal_period=9, price_column='close'):
    """
    Calculate Moving Average Convergence Divergence (MACD) for a given DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame containing price data
    fast_period : int, optional
        The period for fast EMA (default is 12)
    slow_period : int, optional
        The period for slow EMA (default is 26)
    signal_period : int, optional
        The period for signal line (default is 9)
    price_column : str, optional
        The column name containing price data (default is 'close')
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with added MACD columns
    """
    result_df = df.copy()
    
    # Calculate EMAs
    result_df[f'EMA_{fast_period}'] = result_df[price_column].ewm(span=fast_period, adjust=False).mean()
    result_df[f'EMA_{slow_period}'] = result_df[price_column].ewm(span=slow_period, adjust=False).mean()
    
    # Calculate MACD Line
    result_df['MACD_Line'] = result_df[f'EMA_{fast_period}'] - result_df[f'EMA_{slow_period}']
    
    # Calculate Signal Line
    result_df['Signal_Line'] = result_df['MACD_Line'].ewm(span=signal_period, adjust=False).mean()
    
    # Calculate Histogram
    result_df['Histogram'] = result_df['MACD_Line'] - result_df['Signal_Line']
    
    # Drop intermediate columns
    result_df = result_df.drop([f'EMA_{fast_period}', f'EMA_{slow_period}'], axis=1)
    
    return result_df

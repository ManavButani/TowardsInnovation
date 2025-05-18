def calculate_atr(df, window=14):
    """
    Calculate Average True Range (ATR) for a given DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame containing High, Low, Close prices
    window : int, optional
        The window size for ATR calculation (default is 14)
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with added ATR column
    """
    result_df = df.copy()
    
    # Calculate True Range (TR)
    result_df['H-L'] = result_df['high'] - result_df['low']
    result_df['H-PC'] = abs(result_df['high'] - result_df['close'].shift(1))
    result_df['L-PC'] = abs(result_df['low'] - result_df['close'].shift(1))
    
    result_df['TR'] = result_df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    
    # Calculate ATR using Wilder's smoothing (EMA)
    result_df[f'ATR_{window}'] = result_df['TR'].ewm(span=window, adjust=False).mean().round(2)
    
    # Drop intermediate columns
    result_df = result_df.drop(['H-L', 'H-PC', 'L-PC', 'TR'], axis=1)
    
    return result_df

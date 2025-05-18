def calculate_dmi(df, period=14):
    """
    Calculate Directional Movement Index (DMI) for a given DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame containing High, Low, Close prices
    period : int, optional
        The period for DMI calculation (default is 14)
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with added DMI columns (+DI, -DI, ADX)
    """
    result_df = df.copy()
    
    # Calculate True Range (TR)
    result_df['prev_close'] = result_df['Close'].shift(1)
    result_df['TR'] = result_df[['High', 'prev_close']].max(axis=1) - result_df[['Low', 'prev_close']].min(axis=1)
    
    # Calculate Directional Movement
    result_df['up_move'] = result_df['High'] - result_df['High'].shift(1)
    result_df['down_move'] = result_df['Low'].shift(1) - result_df['Low']
    
    result_df['+DM'] = result_df.apply(
        lambda row: row['up_move'] if row['up_move'] > row['down_move'] and row['up_move'] > 0 else 0, 
        axis=1
    )
    result_df['-DM'] = result_df.apply(
        lambda row: row['down_move'] if row['down_move'] > row['up_move'] and row['down_move'] > 0 else 0, 
        axis=1
    )
    
    # Calculate smoothed averages
    result_df['TR14'] = result_df['TR'].ewm(span=period, adjust=False).mean()
    result_df['+DM14'] = result_df['+DM'].ewm(span=period, adjust=False).mean()
    result_df['-DM14'] = result_df['-DM'].ewm(span=period, adjust=False).mean()
    
    # Calculate +DI and -DI
    result_df['+DI14'] = 100 * (result_df['+DM14'] / result_df['TR14'])
    result_df['-DI14'] = 100 * (result_df['-DM14'] / result_df['TR14'])
    
    # Calculate DX
    result_df['DX'] = 100 * (abs(result_df['+DI14'] - result_df['-DI14']) / (result_df['+DI14'] + result_df['-DI14']))
    
    # Calculate ADX
    result_df['ADX'] = result_df['DX'].ewm(span=period, adjust=False).mean()
    
    # Keep only the final columns
    final_columns = ['+DI14', '-DI14', 'ADX']
    result_df = result_df[final_columns]
    
    return result_df

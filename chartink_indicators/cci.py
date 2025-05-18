def calculate_cci(df, window=80):
    """
    Calculate Commodity Channel Index (CCI) for a given DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame containing high, Low, Close prices
    window : int, optional
        The window size for CCI calculation (default is 80)
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with added CCI column
    """
    result_df = df.copy()
    
    # Calculate Typical Price (TP)
    result_df['TP'] = (result_df['high'] + result_df['low'] + result_df['close']) / 3
    
    # Calculate SMA of TP
    result_df[f'SMA_{window}'] = result_df['TP'].rolling(window=window).mean()
    
    # Calculate Mean Deviation
    result_df['Mean_Dev'] = result_df['TP'].rolling(window=window).apply(
        lambda x: abs(x - x.mean()).mean(), raw=True
    )
    
    # Calculate CCI
    result_df[f'CCI_{window}'] = (result_df['TP'] - result_df[f'SMA_{window}']) / (0.015 * result_df['Mean_Dev'])
    
    # Drop intermediate columns
    result_df = result_df.drop(['TP', f'SMA_{window}', 'Mean_Dev'], axis=1)
    
    return result_df

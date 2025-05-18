def calculate_ema(df, window=10, price_column='Close'):
    """
    Calculate Exponential Moving Average (EMA) for a given DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame containing price data
    window : int, optional
        The window size for EMA calculation (default is 10)
    price_column : str, optional
        The column name containing price data (default is 'Close')
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with added EMA column
    """
    result_df = df.copy()
    result_df[f'EMA_{window}'] = result_df[price_column].ewm(span=window, adjust=False).mean()
    return result_df

# Example usage
if __name__ == "__main__":
    data = {'Close': [100, 102, 101, 105, 104, 106, 108, 107, 110, 111]}
    df = pd.DataFrame(data)
    result = calculate_ema(df, window=10)
    print(result)

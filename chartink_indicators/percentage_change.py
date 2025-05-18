import pandas as pd

def calculate_percentage_change(df, value_column='value', periods=1):
    """
    Calculate percentage change for a given DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame containing the value column
    value_column : str, optional
        The column name containing values to calculate percentage change (default is 'value')
    periods : int, optional
        The number of periods to look back (default is 1)
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with added percentage change column
    """
    result_df = df.copy()
    result_df[f'pct_change_{periods}'] = result_df[value_column].pct_change(periods=periods) * 100
    return result_df

# Example usage
if __name__ == "__main__":
    data = {
        'date': pd.date_range(start='2024-01-01', periods=10, freq='W'),
        'value': [896.8, 894.8, 844.65, 852.35, 829, 871.65, 801.55, 855.85, 896.75, 941.55]
    }
    df = pd.DataFrame(data)
    df.set_index('date', inplace=True)
    result = calculate_percentage_change(df)
    print(result)


import pandas as pd

series = pd.Series([896.8, 894.8, 844.65, 852.35, 829, 871.65, 801.55, 855.85, 896.75, 941.55])

# Manual pct_change
previous = series.shift(1)
pct_change = (series - previous) / previous * 100

print(pct_change)

import pandas as pd
import numpy as np

def calculate_parabolic_sar(df, af_start=0.02, af_step=0.02, af_max=0.2):
    """
    Calculate Parabolic SAR for a given DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame containing High and Low prices
    af_start : float, optional
        Initial acceleration factor (default is 0.02)
    af_step : float, optional
        Step size for acceleration factor (default is 0.02)
    af_max : float, optional
        Maximum acceleration factor (default is 0.2)
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with added SAR column
    """
    result_df = df.copy()
    
    # Initialize arrays
    sar = [result_df['Low'].iloc[0]]  # Start SAR below the first candle
    ep = result_df['High'].iloc[0]    # Highest price seen (EP)
    af = af_start
    uptrend = True
    
    # Loop through data to calculate SAR
    for i in range(1, len(result_df)):
        prev_sar = sar[-1]
        
        if uptrend:
            sar_next = prev_sar + af * (ep - prev_sar)
            sar_next = min(sar_next, result_df['Low'].iloc[i-1], result_df['Low'].iloc[i])
            
            if result_df['Low'].iloc[i] < sar_next:
                uptrend = False
                sar_next = ep
                ep = result_df['Low'].iloc[i]
                af = af_start
            else:
                if result_df['High'].iloc[i] > ep:
                    ep = result_df['High'].iloc[i]
                    af = min(af + af_step, af_max)
        else:
            sar_next = prev_sar + af * (ep - prev_sar)
            sar_next = max(sar_next, result_df['High'].iloc[i-1], result_df['High'].iloc[i])
            
            if result_df['High'].iloc[i] > sar_next:
                uptrend = True
                sar_next = ep
                ep = result_df['High'].iloc[i]
                af = af_start
            else:
                if result_df['Low'].iloc[i] < ep:
                    ep = result_df['Low'].iloc[i]
                    af = min(af + af_step, af_max)
        
        sar.append(sar_next)
    
    result_df['SAR'] = sar
    return result_df

# Example usage
if __name__ == "__main__":
    data = {
        'High': [10, 10.5, 10.8, 11, 11.2, 11.5, 11.7, 11.6, 11.4, 11.3],
        'Low': [9.5, 10.0, 10.2, 10.5, 10.8, 11.0, 11.2, 11.1, 11.0, 10.9]
    }
    df = pd.DataFrame(data)
    result = calculate_parabolic_sar(df)
    print(result)

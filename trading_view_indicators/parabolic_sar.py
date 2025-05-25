def SAR(df, af_start=0.02, af_step=0.02, af_max=0.2):
    high = df['high'].values
    low = df['low'].values
    length = len(df)

    sar = [low[0]]
    af_values = [af_start]
    trend_up = True
    ep = high[0]
    af = af_start

    for i in range(1, length):
        prev_sar = sar[-1]

        if trend_up:
            sar_next = prev_sar + af * (ep - prev_sar)
            if i >= 2:
                sar_next = min(sar_next, low[i - 1], low[i - 2])
            else:
                sar_next = min(sar_next, low[i - 1])
            if low[i] < sar_next:
                trend_up = False
                sar_next = ep
                ep = low[i]
                af = af_start
            else:
                if high[i] > ep:
                    ep = high[i]
                    af = min(af + af_step, af_max)
        else:
            sar_next = prev_sar - af * (prev_sar - ep)
            if i >= 2:
                sar_next = max(sar_next, high[i - 1], high[i - 2])
            else:
                sar_next = max(sar_next, high[i - 1])
            if high[i] > sar_next:
                trend_up = True
                sar_next = ep
                ep = high[i]
                af = af_start
            else:
                if low[i] < ep:
                    ep = low[i]
                    af = min(af + af_step, af_max)

        sar.append(sar_next)
        af_values.append(af)

    df['parabolic_sar'] = sar
    # df['af_value'] = af_values
    return df


from numba import njit
import numpy as np


@njit
def FAST_SAR(high, low, af_start=0.02, af_step=0.02, af_max=0.2):

    n = len(high)
    sar = np.zeros(n)
    sar[0] = low[0]

    trend_up = True
    ep = high[0]
    af = af_start

    for i in range(1, n):
        prev_sar = sar[i - 1]

        if trend_up:
            sar_next = prev_sar + af * (ep - prev_sar)
            if i >= 2:
                sar_next = min(sar_next, low[i - 1], low[i - 2])
            else:
                sar_next = min(sar_next, low[i - 1])

            if low[i] < sar_next:
                trend_up = False
                sar_next = ep
                ep = low[i]
                af = af_start
            else:
                if high[i] > ep:
                    ep = high[i]
                    af = min(af + af_step, af_max)
        else:
            sar_next = prev_sar - af * (prev_sar - ep)
            if i >= 2:
                sar_next = max(sar_next, high[i - 1], high[i - 2])
            else:
                sar_next = max(sar_next, high[i - 1])

            if high[i] > sar_next:
                trend_up = True
                sar_next = ep
                ep = high[i]
                af = af_start
            else:
                if low[i] < ep:
                    ep = low[i]
                    af = min(af + af_step, af_max)

        sar[i] = sar_next

    return sar

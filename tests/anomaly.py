# -*- coding: utf-8 -*-
"""
Created on Tue May 20 11:15:15 2025

@author: dphilippus
"""

import pandas as pd
import numpy as np
from libschema.model import anomilize


def anom_test(rtn=False):
    """
    This is a simple test where we build a correct anomaly and see if the
    anomilize function produces it correctly.
    
    If rtn is True, it also returns the actual input DataFrame so you
    can examine behaviors directly.
    """
    periodic = np.array([1,2,3,4,5] * 10)
    timestep = list(range(50))
    anomaly = np.array(list(range(25)) + list(range(25, 0, -1))) / 10
    anomaly = anomaly - anomaly.mean()
    cycle = np.sin(periodic / 5 * 6.28) * 5
    df = pd.DataFrame({
        "timestep": timestep,
        "period": periodic,
        "value": anomaly + cycle
        })
    anoms = anomilize(df, "timestep", "period", ["value"])
    error = abs(anoms["value"].to_numpy() - anomaly).max()
    tol = abs(anomaly).mean() * 1e-10
    # It's a floating point, equality won't be exact
    if error < tol:
        print("Passed anomaly test")
        return True
    else:
        print("Failed anomaly test")
        if rtn:
            return (False, df, anomaly, anoms)
        return False
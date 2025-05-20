# -*- coding: utf-8 -*-
"""
Created on Tue May 20 12:10:25 2025

@author: dphilippus

This file tests a full model workflow.
"""

from libschema.classes import *
from libschema import SCHEMA
import numpy as np
import pandas as pd


class TestSeasonality(Seasonality):
    def __init__(self, mean, phase, amplitude, period):
        self.mean = mean
        self.phase = phase
        self.amplitude = amplitude
        self.period = period
    
    def apply(self, period):
        return self.mean + np.sin((period - self.phase)/self.period*6.28) * self.amplitude
    
    def apply_vec(self, period):
        return self.apply(period)
    

class TestAnomaly(Anomaly):
    def __init__(self, sensitivity, window):
        self.sensitivity = sensitivity
        self.window = window
    
    def apply(self, periodic, period, anom_history):
        return self.sensitivity * np.mean(
            anom_history["x"][-self.window:])
    
    def apply_vec(self, periodic, period, anom_history):
        return self.sensitivity * anom_history["x"].rolling(
            self.window, min_periods=1).mean()
    

def test_model(rtn=False):
    sensitivity = 1
    window = 3
    mean = 5
    phase = 12
    amplitude = 8
    period = 36
    periodic_steps = np.array(list(range(36)) * 5) % 36
    refval = np.cos(periodic_steps)
    actual = np.arange(len(periodic_steps)) * 0.1
    anomaly = actual - refval
    timestep = np.arange(len(periodic_steps))
    
    analytic = (mean + np.sin((periodic_steps - phase)/period*6.28) * amplitude +
                pd.Series(anomaly).rolling(window, min_periods=1).mean() * sensitivity)
    data = pd.DataFrame({
        "T": timestep,
        "tp": periodic_steps,
        "x": actual,
        "y": analytic
        })
    periodics = pd.DataFrame({
        "period": periodic_steps[:36],
        "x": refval[:36]
        })
    model = SCHEMA(
        TestSeasonality(mean, phase, amplitude, period),
        TestAnomaly(sensitivity, window),
        periodics,
        [],
        ["T", "tp", "x"],
        period,
        window
        )
    full_run = model.run_series(data, "T", 0, "tp")[1]
    pass_fr = abs(full_run["prediction"] - full_run["y"]).max() < 0.001
    if pass_fr:
        print("Passed full-run version")
    else:
        print("Failed full-run version")
    incr_run = np.array(list(model.run_series_incremental(data, "tp")))
    pass_incr = abs(incr_run - analytic).max() < 0.001
    if pass_incr:
        print("Passed incremental version")
    else:
        print("Failed incremental version")
    if pass_incr and pass_fr:
        return True
    if rtn:
        return (False, data, full_run, incr_run, model)
    return False

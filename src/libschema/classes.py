# -*- coding: utf-8 -*-
"""
This file defines a modification engine class.
"""

class ModEngine(object):
    def apply(self, seasonality, anomaly, periodics, history):
        raise NotImplementedError("ModEngine.apply")
        return (seasonality, anomaly, periodics)
    
    def coefficients(self):
        raise NotImplementedError("ModEngine.coefficients")
        return {}
    
    def from_data():
        raise NotImplementedError("ModEngine.from_data")
    
    def to_dict(self):
        raise NotImplementedError("ModEngine.to_dict")

    def from_dict(d):
        raise NotImplementedError("ModEngine.from_dict")
        

class Seasonality(object):
    def apply(self, period):
        raise NotImplementedError("Seasonality.apply")
        
    def to_dict(self):
        raise NotImplementedError("Seasonality.to_dict")

    def from_dict(d):
        raise NotImplementedError("Seasonality.from_dict")


class Anomaly(object):
    def apply(self, periodic, period, anom_history):
        raise NotImplementedError("Anomaly.apply")
        
    def to_dict(self):
        raise NotImplementedError("Anomaly.to_dict")

    def from_dict(d):
        raise NotImplementedError("Anomaly.from_dict")

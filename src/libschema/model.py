"""
Author: Daniel Philippus
Date: 2025-02-05

This file implements the core SCHEMA model class.
"""

import pandas as pd
import numpy as np
from yaml import load, dump, Loader
# import classes


def anomilize(data, by, variables):
    """
    Generate anomaly data.

    Parameters
    ----------
    data : pd.DataFrame
        Data to be processed
    by : str
        Column identifying the recurring timestep, e.g., day-of-year.
    variables : list[str]
        Columns to analyze.

    Returns
    -------
    pd.DataFrame
        DataFrame indexed on `by`, with `variables` anomalies

    """
    data = data[[by] + variables].dropna()
    return data.groupby(by).apply(lambda x: x-x.mean(), include_groups=False).droplevel(1)


class SCHEMA(object):
    # TODO: timestep tracking
    def __init__(self, seasonality, anomaly, periodics, engines, columns, window=1, stepsize=1, logfile=None):
        """
        Parameters
        ----------
        seasonality : classes.Seasonality
            Seasonality implementation.
        anomaly : classes.Anomaly
            Anomaly implementation.
        periodics : pd.DataFrame with [period, columns]
            Periodic values of all columns.
        engines : list of [(frequency, classes.ModEngine)]
            Modification engines to apply at specified frequencies.
        columns : [str]
            List of required column names.
        window : int
            Lookback window for anomaly history.
        stepsize : number
            Number of steps (in periodic function) per runtime step
        logfile : str, optional
            Where to log, if any. The default is None.

        Returns
        -------
        SCHEMA
            The SCHEMA object.

        """
        self.step = None
        self.period = None
        self.seasonality = seasonality
        self.anomaly = anomaly
        self.periodics = periodics
        self.engine_periods = [i[0] for i in engines]
        self.engines = {i[0]: i[1] for i in engines}
        self.columns = columns
        self.window = window
        self.stepsize = stepsize
        self.logfile = logfile
        self.output = None
        self.periodic_output = None
        self.values = {}
    
    @classmethod
    def from_file(cls, filename):
        try:
            with open(filename) as f:
                coefs = load(f, Loader)
            # TODO: do stuff to coefs
            return cls(**coefs)
        except Exception as e:
            with open("unspecified_log.txt", "w") as f:
                f.write(f"Error in loading {filename}: {e}")
    
    def to_file(self, filename):
        data = {
            "seasonality": self.seasonality,
            "anomaly": self.anomaly,
            "engines": [(i, self.engines[i]) for i in self.engine_periods],
            "columns": self.columns,
            "window": self.window,
            "stepsize": self.stepsize,
            "logfile": self.logfile
            }
        with open(filename, "w") as f:
            dump(data, f)
    
    def to_dict(self):
        coefs = {"window": self.window}
        for item in [self.seasonality, self.anomaly, self.engines.values()]:
            coefs = coefs | item.to_dict()
        return coefs
    
    def log(self, text, reset=False):
        if self.logfile is not None:
            with open(self.logfile, "w" if reset else "a") as f:
                f.write(text + "\n")

    def initialize_run(self, period):
        # Logs allow efficient handling of a rolling anomaly
        self.output = None
        self.periodic_output = None
        self.step = 0
        self.period = period
        self.history = {x: [] for x in self.columns}
    
    def get_history(self):
        return pd.DataFrame(self.history)
        
    def trigger_engine(self, engine):
        (self.seasonality, self.anomaly, self.periodics) =\
            engine.apply(self.seasonality, self.anomaly, self.periodics,
                         self.get_history())
    
    def set_val(self, key, value):
        self.values[key] = value

    def step(self, inputs=None, period=None):
        """
        Run a single step, incrementally.  Updates history and returns
        today's prediction.
        """
        for k in self.columns:
            if not k in inputs:
                if not k in self.values:
                    raise ValueError(f"In step, must provide all specified data. Missing: {k}")
                inputs[k] = self.values[k]
            self.history[k].append(inputs[k])
        self.step += 1
        if period is None:
            self.period += 1
        else:
            self.period = period
        today = self.periodics[self.periodics["period"] == self.period]
        # Now, build the prediction
        ssn = self.seasonality.apply(self.period)
        self.periodic_output = ssn
        # Compute anomaly history
        window = self.window if self.window <= self.step else self.step
        history = pd.DataFrame({"period": self.step} | {k: self.history[k][-window:] for k in self.columns})
        anom_hist = (history - today)[self.columns]
        anom = self.anomaly.apply(ssn, self.period, anom_hist)
        # Final result
        pred = ssn + anom
        self.output = pred
        # Run triggers
        for eng_step in self.engine_periods:
            if self.step % eng_step == 0:
                self.trigger_engine(self.engines[eng_step])
        return pred
    
    def run_series_incremental(self, data):
        """
        Run a full timeseries at once, but internally use the stepwise approach.
        data must have columns date (as an actual date type), tmax.
        Will be returned with columns date, day, at, actemp, anom, temp.mod
        """
        self.initialize_run()
        for row in data.itertuples():
            inputs = {k: getattr(row, k) for k in self.columns}
            yield self.step(inputs)
        

    def run_series(self, data):
        """
        Run a full timeseries at once.
        data must have columns date (as an actual date type), tmax.
        Will be returned with new columns day, actemp, anom, temp.mod
        This runs things all at once, so it's much faster, but ignores engines.
        """
        output = list(self.run_series_incremental(data))
        return self.get_history().assign(output=output)

    def from_data(data):
        raise NotImplementedError("SCHEMA.from_data")

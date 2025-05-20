# libSCHEMA
Generic Python implementation of the SCHEMA modeling framework with built-in BMI/ngen support.

The SCHEMA (Seasonal Conditions Historical Expectation with Modeled Anomaly) framework for hydrologic models, a generalization of stochastic modeling, was introduced in TempEst 2 (Philippus et al. 2025) for the TempEst family of ungauged stream temperature models, but it is applicable to a wide range of models.  This provides the opportunity to (1) avoid a lot of boilerplate code and (2) provide a ready-to-go [NextGen](https://www.weather.gov/media/owp/oh/docs/2021-OWP-NWM-NextGen-Framework.pdf)-compatible [Basic Model Interface](https://joss.theoj.org/papers/10.21105/joss.02317) (BMI) implementation, easing the development process for future models.  Much of the SCHEMA logic is totally model-agnostic, so that portion of the code can be pre-written.

For that reason, this is a model-agnostic Python implementation of SCHEMA, which specifies a general framework as well as providing whatever functionality doesn't depend on model specifics.  All you have to do for a specific implementation is define a few functions computing seasonality and anomaly, as well as coefficient estimation if your purpose is ungaged modeling.

Note: in Python, it is libschema (`import libschema`), not libSCHEMA. Easier to type.

## General Concept

A SCHEMA model has three basic components: coefficient estimation, seasonality, and anomaly.  Coefficient estimation is too application-specific for a generic implementation to be useful, so that's left to be handled externally.  This implementation handles seasonality (or any periodic component) and anomaly logic.

The basic approach is simple: compute the periodic component for the timestep of interest, then compute the anomaly and add them together.  Why do we even need a library for that?  With a simple implementation, we do not, but the library can handle a lot of tricky legwork to provide convenience features.  Also, the library can provide a full-blown BMI implementation out of the box that's tested with NextGen, so that's a handy feature.

What sort of convenience features?

- Smart "modification engines" that run periodically to adjust model components at runtime.  These are great for handling things like climate change and drought, in the hydrologic use case.
- Exporting coefficients to a data frame for analysis - super useful for the coefficient estimation part
- Exporting models to, and reading them from, configuration files, which is a required capability for BMI/NextGen
- Having the logic to run the model fast as a single series if there are no modification engines, or step-by-step if there are
- And did I mention a BMI implementation?

More generally, it also separates concerns: the user just writes the actual model mathematics without worrying about the implementation logic. And this is huge, because practically any lumped model can be implemented as SCHEMA with a little contortion. For instance, I'm fairly sure you could just have no seasonal component and an LSTM for anomaly, and you get a BMI-compatible LSTM for free. Or you could easily write a unit hydrograph-based hydrologic model (seasonality = baseflow, anomaly = unit hydrograph) with a couple of simple functions.

## Implemented Functionality

### Current Status

Core functionality has been implemented and tested with a simplified model concept (see `tests/full_model.py`). BMI support is drafted, but has not been tested. A "full-fledged" model implementation, with the full complexity of something like TempEst 2, has not been tested, but in principle should work.

### Core Functionality

- Model initialization
- Running the model
- Exporting and importing model files
- BMI, e.g. for NextGen

### Convenience Features

LibSCHEMA comes with a couple of utilities I built for my own use that might be handy more broadly:

- A suite of goodness-of-fit metrics (R2, RMSE, NSE, percent bias, max-miss/min-miss)
- A flexible cross-validation function

## Required Functionality

The big pieces that needs to be implemented are the actual seasonality and anomaly functions, which are provided as classes to make life easier with configuration files, coefficient exporting, etc. Templates are provided in `classes.py`.  Additionally, the implementation needs to specify data requirements and the like. Seasonality and anomaly functions should be capable of running vectorized if you intend to use `run_series` to run in a single pass.

If you want the model to be able to fit itself, you also need to define a `from_data` method. Without that, a model can still be specified with coefficients, and you could calibrate it in the traditional way, but it can't automatically identify a fit.

If your implementation uses any modification engines, implementation for those needs to be provided, and it may be useful to develop a custom configuration-file retriever (otherwise libSCHEMA will try to pickle them in the main config file).



Reference: Philippus, Corona, Schneider, Rust, and Hogue, 2025, "Satellite-Based Spatial-Statistical Modeling of Daily Stream Water Temperatures at the CONUS Scale", *Journal of Hydrology*, in press.
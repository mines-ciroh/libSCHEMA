# libSCHEMA
Generic Python implementation of the SCHEMA modeling framework with built-in BMI/ngen support.

The SCHEMA (Seasonal Conditions Historical Expectation with Modeled Anomaly) framework for hydrologic models, a generalization of stochastic modeling, was introduced in TempEst 2 (Philippus et al., in review) for the TempEst family of ungauged stream temperature models, but it is applicable to a wide range of models.  This provides the opportunity to (1) avoid a lot of boilerplate code and (2) provide a ready-to-go [NextGen](https://www.weather.gov/media/owp/oh/docs/2021-OWP-NWM-NextGen-Framework.pdf)-compatible [Basic Model Interface](https://joss.theoj.org/papers/10.21105/joss.02317) (BMI) implementation, easing the development process for future models.  Much of the SCHEMA logic is totally model-agnostic, so a lot of the code can be pre-written.

For that reason, this is a model-agnostic Python implementation of SCHEMA, which specifies a general framework as well as providing whatever functionality doesn't depend on model specifics.  All you have to do for a specific implementation is define a few functions computing seasonality and anomaly.

## General Concept

A SCHEMA model has three basic components: coefficient estimation, seasonality, and anomaly.  Coefficient estimation is too application-specific for a generic implementation to be useful, so that's left to be handled externally.  This implementation handles seasonality (or any periodic component) and anomaly logic.

The basic approach is simple: compute the periodic component for the timestep of interest, then compute the anomaly and add them together.  Why do we even need a library for that?  With a simple implementation, we do not, but the library can handle a lot of tricky legwork to provide convenience features.  Also, the library can provide a full-blown BMI implementation out of the box that's tested with NextGen, so that's a handy feature.

What sort of convenience features?

- Smart "modification engines" that run periodically to adjust model components at runtime.  These are great for handling things like climate change and drought, in the hydrologic use case.
- Exporting coefficients to a data frame for analysis - super useful for the coefficient estimation part
- Exporting models to, and reading them from, configuration files, which is a required capability for BMI/NextGen
- Having the logic to run the model fast as a single series if there are no modification engines, or step-by-step if there are
- And did I mention a BMI implementation?

More generally, it also separates concerns: the user just writes the actual model mathematics without worrying about the implementation logic.

## Implemented Functionality

### Core Functionality

### Convenience Features

LibSCHEMA comes with a couple of utilities I built for my own use that might be handy more broadly:

- A suite of goodness-of-fit metrics (R2, RMSE, NSE, percent bias, max-miss/min-miss)
- A flexible cross-validation function

## Required Functionality

The big pieces that needs to be implemented are the actual seasonality and anomaly functions.  Additionally, the implementation needs to specify data requirements and the like.

If your implementation uses any modification engines, implementation for those needs to be provided, as well as logic for how to retrieve them from configuration files.  If you do not intend to load configuration files, you can leave that last part out.
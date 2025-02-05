# libSCHEMA
Generic Python implementation of the SCHEMA modeling framework with built-in BMI/ngen support.

The SCHEMA (Seasonal Conditions Historical Expectation with Modeled Anomaly) framework for hydrologic models, a generalization of stochastic modeling, was introduced in TempEst 2 (Philippus et al., in review) for the TempEst family of ungauged stream temperature models, but it is applicable to a wide range of models.  This provides the opportunity to (1) avoid a lot of boilerplate code and (2) provide a ready-to-go [NextGen](https://www.weather.gov/media/owp/oh/docs/2021-OWP-NWM-NextGen-Framework.pdf)-compatible [Basic Model Interface](https://joss.theoj.org/papers/10.21105/joss.02317) implementation, easing the development process for future models.  Much of the SCHEMA logic is totally model-agnostic, so a lot of the code can be pre-written.

For that reason, this is a model-agnostic Python implementation of SCHEMA, which specifies a general framework as well as providing whatever functionality doesn't depend on model specifics.  All you have to do for a specific implementation is define a few functions computing seasonality and anomaly.

## General Concept

## Implemented Functionality

## Required Functionality

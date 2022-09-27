import numpy as np
import pandas as pd
from scipy.stats import norm, gamma, dirichlet
from statsmodels.nonparametric.smoothers_lowess import lowess

default_lowess_kwargs = {"frac": 0.2, "it": 0}


def _smoothed_gaussian_random_walk(
    gaussian_random_walk_mu, gaussian_random_walk_sigma, N, lowess_kwargs
):
    x = np.arange(N)
    y = norm(gaussian_random_walk_mu, gaussian_random_walk_sigma).rvs(N).cumsum()
    filtered = lowess(y, x, **lowess_kwargs)
    y = filtered[:, 1]
    return (x, y)


def generate_synthetic_control_data(
    N=100,
    treatment_time=70,
    grw_mu=0.25,
    grw_sigma=1,
    lowess_kwargs=default_lowess_kwargs,
):

    # 1. Generate non-treated variables
    df = pd.DataFrame(
        {
            "a": _smoothed_gaussian_random_walk(grw_mu, grw_sigma, N, lowess_kwargs)[1],
            "b": _smoothed_gaussian_random_walk(grw_mu, grw_sigma, N, lowess_kwargs)[1],
            "c": _smoothed_gaussian_random_walk(grw_mu, grw_sigma, N, lowess_kwargs)[1],
            "d": _smoothed_gaussian_random_walk(grw_mu, grw_sigma, N, lowess_kwargs)[1],
            "e": _smoothed_gaussian_random_walk(grw_mu, grw_sigma, N, lowess_kwargs)[1],
            "f": _smoothed_gaussian_random_walk(grw_mu, grw_sigma, N, lowess_kwargs)[1],
            "g": _smoothed_gaussian_random_walk(grw_mu, grw_sigma, N, lowess_kwargs)[1],
        }
    )

    # 2. Generate counterfactual, based on weighted sum of non-treated variables. This is the counterfactual with NO treatment.
    weightings_true = dirichlet(np.ones(7)).rvs(1)
    df["counterfactual"] = np.dot(df.to_numpy(), weightings_true.T)

    # 3. Generate the causal effect
    causal_effect = gamma(10).pdf(np.arange(0, N, 1) - treatment_time)
    df["causal effect"] = causal_effect * -50

    # 4. Generate the actually observed data, ie the treated with the causal effect applied
    df["actual"] = df["counterfactual"] + df["causal effect"]

    # 5. apply observation noise to all relevant variables
    for var in ["actual", "a", "b", "c", "d", "e", "f", "g"]:
        df[var] += norm(0, 0.25).rvs(N)

    return df, weightings_true


def generate_interrupted_time_series_data(
    N=100, treatment_time=70, beta_temp=-1, beta_linear=0.5, beta_intercept=3
):
    x = np.arange(0, 100, 1)
    df = pd.DataFrame(
        {
            "temperature": np.sin(x * 0.5) + 1,
            "linear": np.linspace(0, 1, 100),
            "causal effect": 10 * gamma(10).pdf(np.arange(0, 100, 1) - treatment_time),
        }
    )

    df["deaths_counterfactual"] = (
        beta_intercept + beta_temp * df["temperature"] + beta_linear * df["linear"]
    )

    # generate the actually observed data
    # ie the treated with the causal effect applied
    df["deaths_actual"] = df["deaths_counterfactual"] + df["causal effect"]

    # apply observation noise to all relevant variables
    # NOTE: no observation noise on the linear trend component
    for var in ["deaths_actual", "temperature"]:
        df[var] += norm(0, 0.1).rvs(N)

    # add intercept
    df["intercept"] = np.ones(df.shape[0])

    return df
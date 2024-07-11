#   Copyright 2024 The PyMC Labs Developers
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
Miscellaneous unit tests
"""

import arviz as az
import pandas as pd
from matplotlib import pyplot as plt

import causalpy as cp

sample_kwargs = {"tune": 20, "draws": 20, "chains": 2, "cores": 2}


def test_regression_kink_gradient_change():
    """Test function to numerically calculate the change in gradient around the kink
    point in regression kink designs"""
    # test no change in gradient
    assert cp.RegressionKink._eval_gradient_change(-1, 0, 1, 1) == 0.0
    assert cp.RegressionKink._eval_gradient_change(1, 0, -1, 1) == 0.0
    assert cp.RegressionKink._eval_gradient_change(0, 0, 0, 1) == 0.0
    # test positive change in gradient
    assert cp.RegressionKink._eval_gradient_change(0, 0, 1, 1) == 1.0
    assert cp.RegressionKink._eval_gradient_change(0, 0, 2, 1) == 2.0
    assert cp.RegressionKink._eval_gradient_change(-1, -1, 2, 1) == 3.0
    assert cp.RegressionKink._eval_gradient_change(-1, 0, 2, 1) == 1.0
    # test negative change in gradient
    assert cp.RegressionKink._eval_gradient_change(0, 0, -1, 1) == -1.0
    assert cp.RegressionKink._eval_gradient_change(0, 0, -2, 1) == -2.0
    assert cp.RegressionKink._eval_gradient_change(-1, -1, -2, 1) == -1.0
    assert cp.RegressionKink._eval_gradient_change(1, 0, -2, 1) == -1.0


def test_inverse_prop():
    """Test the InversePropensityWeighting class."""
    df = cp.load_data("nhefs")
    sample_kwargs = {
        "tune": 100,
        "draws": 500,
        "chains": 2,
        "cores": 2,
        "random_seed": 100,
    }
    result = cp.InversePropensityWeighting(
        df,
        formula="trt ~ 1 + age + race",
        outcome_variable="outcome",
        weighting_scheme="robust",
        model=cp.pymc_models.PropensityScore(sample_kwargs=sample_kwargs),
    )
    assert isinstance(result.idata, az.InferenceData)
    ps = result.idata.posterior["p"].mean(dim=("chain", "draw"))
    w1, w2, _, _ = result.make_doubly_robust_adjustment(ps)
    assert isinstance(w1, pd.Series)
    assert isinstance(w2, pd.Series)
    w1, w2, n1, nw = result.make_raw_adjustments(ps)
    assert isinstance(w1, pd.Series)
    assert isinstance(w2, pd.Series)
    w1, w2, n1, n2 = result.make_robust_adjustments(ps)
    assert isinstance(w1, pd.Series)
    assert isinstance(w2, pd.Series)
    w1, w2, n1, n2 = result.make_overlap_adjustments(ps)
    assert isinstance(w1, pd.Series)
    assert isinstance(w2, pd.Series)
    ate_list = result.get_ate(0, result.idata)
    assert isinstance(ate_list, list)
    ate_list = result.get_ate(0, result.idata, method="raw")
    assert isinstance(ate_list, list)
    ate_list = result.get_ate(0, result.idata, method="robust")
    assert isinstance(ate_list, list)
    ate_list = result.get_ate(0, result.idata, method="overlap")
    assert isinstance(ate_list, list)
    fig, axs = result.plot_ate(prop_draws=1, ate_draws=10)
    assert isinstance(fig, plt.Figure)
    assert isinstance(axs, list)
    assert all(isinstance(ax, plt.Axes) for ax in axs)
    fig, axs = result.plot_balance_ecdf("age")
    assert isinstance(fig, plt.Figure)
    assert isinstance(axs, list)
    assert all(isinstance(ax, plt.Axes) for ax in axs)

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
import arviz as az

import causalpy.pymc_models as pymc_models
import causalpy.skl_models as skl_models
from causalpy.version import __version__

from .data import load_data
from .experiments.diff_in_diff import DifferenceInDifferences
from .experiments.instrumental_variable import InstrumentalVariable
from .experiments.inverse_propensity_weighting import InversePropensityWeighting
from .experiments.prepostfit import InterruptedTimeSeries, SyntheticControl
from .experiments.prepostnegd import PrePostNEGD
from .experiments.regression_discontinuity import RegressionDiscontinuity
from .experiments.regression_kink import RegressionKink

az.style.use("arviz-darkgrid")

__all__ = [
    "__version__",
    "DifferenceInDifferences",
    "InstrumentalVariable",
    "InterruptedTimeSeries",
    "InversePropensityWeighting",
    "load_data",
    "PrePostNEGD",
    "pymc_models",
    "RegressionDiscontinuity",
    "RegressionKink",
    "skl_models",
    "SyntheticControl",
]

from dataclasses import dataclass
from typing import Any
import numpy as np
import pwlf


@dataclass
class PwlfResult:
    tp: np.ndarray  # turning points
    slopes: np.ndarray
    xHat: np.ndarray
    yHat: np.ndarray
    p_values: np.ndarray
    se: np.ndarray
    predict: Any


def regression(
    x: np.ndarray, y: np.ndarray, n_segments: int, step_size: float = 0.0001
) -> PwlfResult:
    # fit your data (x and y)
    # pwlf uses np internally, but accepts either np.ndarray or pd.core.series.Series
    myPWLF = pwlf.PiecewiseLinFit(x, y)

    # fit the data for n line segments
    z = myPWLF.fit(n_segments)  # returns np.ndarray of np.float64

    # calculate slopes
    slopes = myPWLF.calc_slopes()

    # predict for the determined points
    xHat = x
    yHat = myPWLF.predict(xHat)

    # calculate statistics
    p = myPWLF.p_values(method="non-linear", step_size=step_size)  # p-values
    se = myPWLF.se  # standard errors

    return PwlfResult(z, slopes, xHat, yHat, p, se, myPWLF.predict)

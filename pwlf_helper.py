from dataclasses import dataclass
from time import perf_counter
import numpy as np
import pwlf

@dataclass
class PwlfResult:
    tp: np.ndarray # turning points
    slopes: np.ndarray
    xHat: np.ndarray
    yHat: np.ndarray
    p_values: np.ndarray
    se: np.ndarray

def regression(x: np.ndarray, y: np.ndarray, n_segments: int, step_size: float = 0.0001) -> PwlfResult:
    # fit your data (x and y)
    # pwlf uses np internally, but accepts either np.ndarray or pd.core.series.Series
    myPWLF = pwlf.PiecewiseLinFit(x, y)

    # fit the data for n line segments
    z = myPWLF.fit(n_segments) # returns np.ndarray of np.float64

    # calculate slopes
    slopes = myPWLF.calc_slopes()

    # predict for the determined points
    xHat = x
    yHat = myPWLF.predict(xHat)

    # calculate statistics
    p = myPWLF.p_values(method='non-linear', step_size=step_size) # p-values
    se = myPWLF.se  # standard errors

    return PwlfResult(z, slopes, xHat, yHat, p, se)

def main(x: np.ndarray, y: np.ndarray, n_segments: int, step_size: float = 0.0001) -> int:
    start = perf_counter()

    # regression
    PwlfResult = regression(x, y, n_segments, step_size)
    print(PwlfResult.tp)
    print(PwlfResult.slopes)
    print(PwlfResult.p_values)
    print(PwlfResult.se)

    end = perf_counter()
    print('time elapsed: ' + str(end-start) + ' s')

    return 0

if __name__ == '__main__':
    main()

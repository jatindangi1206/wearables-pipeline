import numpy as np
from scipy import stats
from typing import List, Optional, Dict, Any


def mean(data: List[float]) -> Optional[float]:
    if not data:
        return None
    return float(np.mean(data))


def median(data: List[float]) -> Optional[float]:
    if not data:
        return None
    return float(np.median(data))


def mode(data: List[float]) -> Optional[float]:
    if not data:
        return None
    mode_res = stats.mode(data, nan_policy='omit')
    # In newer scipy versions, mode can be a scalar if there's one mode.
    # In older versions, it's always an array.
    mode_val = mode_res.mode
    if isinstance(mode_val, np.ndarray):
        if mode_res.count == 0:
            return None
        return float(mode_val[0])
    return float(mode_val)


def stddev(data: List[float]) -> Optional[float]:
    if not data:
        return None
    return float(np.std(data, ddof=1)) if len(data) > 1 else 0.0


def correlation(x: List[float], y: List[float]) -> Optional[float]:
    if not x or not y or len(x) != len(y) or len(x) < 2:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def correlation_matrix(data: Dict[str, List[float]]) -> Dict[str, Dict[str, Optional[float]]]:
    keys = list(data.keys())
    matrix = {}
    for i, k1 in enumerate(keys):
        matrix[k1] = {}
        for j, k2 in enumerate(keys):
            if i == j:
                matrix[k1][k2] = 1.0
            else:
                matrix[k1][k2] = correlation(data[k1], data[k2])
    return matrix


def detect_outliers(data: List[float], threshold: float = 3.0) -> List[float]:
    if not data or len(data) < 2:
        return []
    z_scores = np.abs(stats.zscore(data, nan_policy='omit'))
    return [val for val, z in zip(data, z_scores) if z > threshold]


def daily_trends(timestamps: List[Any], values: List[float]) -> Dict[str, Any]:
    # Placeholder: implement time-based grouping if needed
    return {}
import numpy as np
from sklearn.linear_model import LinearRegression


col_index = {
    'year': 0,
    'week': 1,
    'mortality': 2
}


def generate_onehot(rows: int, cols: int):
    """

    :param rows:
    :param cols:
    :return:
    """
    arr = np.zeros((rows, cols))
    set_col = 0
    for row in range(rows):
        if set_col == cols:
            set_col = 0
        arr[row, set_col] = 1
        set_col += 1
    return arr


def concatenate_cols(arr_1: np.ndarray, arr_2: np.ndarray):
    """

    :param arr_1:
    :param arr_2:
    :return:
    """
    return np.concatenate((arr_1, arr_2), axis=1)


def get_prev_years_indices(all_mort: np.ndarray):
    """

    :param all_mort:
    :return:
    """
    return all_mort[:, col_index['year']] < 2020


def get_analyzed_year_indices(all_mort: np.ndarray):
    """

    :param all_mort:
    :return:
    """
    current_year = np.max(all_mort[:, col_index['year']])
    return all_mort[:, col_index['year']] == current_year


def get_timeframe_count(all_mort: np.ndarray, indices: np.ndarray):
    """

    :param all_mort:
    :param indices:
    :return:
    """
    return np.unique(all_mort[indices, col_index['week']]).size


def generate_predictors(all_mort: np.ndarray, indices: np.ndarray, timeframe: int):
    """

    :param all_mort:
    :param indices:
    :param timeframe:
    :return:
    """
    one_hot = generate_onehot(np.sum(indices), timeframe)
    return concatenate_cols(all_mort[indices, :col_index['week']], one_hot)


def predict_baseline(xs: np.ndarray, y: int, predict: np.ndarray):
    """

    :param xs:
    :param y:
    :param predict:
    :return:
    """
    mod = LinearRegression(fit_intercept=False).fit(xs, y)
    return mod.predict(predict)


def get_mortality_eea_info(all_mort: np.ndarray, indices_ay: np.ndarray, baseline):
    """

    :param all_mort:
    :param indices_ay:
    :param baseline:
    :return:
    """
    diff_expected_actual = all_mort[indices_ay, col_index['mortality']] - baseline
    total_excess = np.sum(diff_expected_actual)
    sum_expected = np.sum(baseline)
    sum_actual = np.sum(all_mort[indices_ay, col_index['mortality']])

    return total_excess, sum_expected, sum_actual


def generate_std(all_mort, prev_years, train_on, predict_for, time_frame_pys):
    """

    :param all_mort:
    :param prev_years:
    :param train_on:
    :param predict_for:
    :param time_frame_pys:
    :return:
    """
    y = all_mort[prev_years, col_index['mortality']][:, np.newaxis]
    beta = np.linalg.pinv(train_on.T @ train_on) @ train_on.T @ y
    yhat = train_on @ beta
    sigma2 = np.sum((y - yhat) ** 2) / (y.size - train_on.shape[1])
    S = np.linalg.pinv(train_on.T @ train_on)
    w = np.ones((time_frame_pys, 1))
    p = 0
    for i, ww in enumerate(w):
        p += predict_for[i] * ww
    p = p[:, np.newaxis]
    predictive_var = sigma2 * np.sum(w) + sigma2 * p.T @ S @ p
    total_excess_std = np.sqrt(predictive_var)[0][0]

    return total_excess_std


def is_significant(num):
    if np.isnan(num):
        return 'Undetermined'
    if num > 1.96:
        return 'Significant Increase'
    if num < -1.96:
        return 'Significant Decrease'
    if abs(num) < 1.96:
        return 'Not Significant'

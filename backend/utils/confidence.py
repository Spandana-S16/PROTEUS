import numpy as np


def normalize_inverse(value, minimum, maximum):
    """
    Lower error -> higher score
    """

    score = 1 - ((value - minimum) / (maximum - minimum))

    score = max(0, min(score, 1))

    return score


def calculate_confidence(mae,
                         rmse,
                         mape,
                         stability_score):

    mae_score = normalize_inverse(mae, 0, 500000)

    rmse_score = normalize_inverse(rmse, 0, 600000)

    mape_score = normalize_inverse(mape, 0, 80)
    historical_score = (

        0.4 * mae_score +

        0.3 * rmse_score +

        0.3 * mape_score

    )

    confidence = (

        0.5 * historical_score +

        0.5 * (stability_score / 100)

    ) * 100

    return round(confidence,2)
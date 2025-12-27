"""Probability and Statistics Utilities"""

import math


def convert_dec_to_prob(dec: float) -> float:
    """Convert decimal odds to probability.

    Arguments:
        dec: Decimal odds (e.g., 2.5 means 2.5 to 1).

    Returns:
        Probability rounded to 4 decimal places.

    Example:
        >>> convert_dec_to_prob(2.5)
        0.4
        >>> convert_dec_to_prob(4.0)
        0.25
    """
    return round(1 / dec, 4)


def convert_prob_to_dec(prob: float) -> float:
    """Convert probability to decimal odds.

    Arguments:
        prob: Probability (between 0 and 1).

    Returns:
        Decimal odds rounded to 4 decimal places.

    Example:
        >>> convert_prob_to_dec(0.25)
        4.0
        >>> convert_prob_to_dec(0.5)
        2.0
    """
    return round(1 / prob, 4)


def convert_frac_to_prob(nom: int, denom: int) -> float:
    """Convert fractional odds to probability.

    Arguments:
        nom: Numerator of fractional odds.
        denom: Denominator of fractional odds.

    Returns:
        Probability rounded to 4 decimal places.

    Example:
        >>> convert_frac_to_prob(3, 1)  # 3/1 odds
        0.25
        >>> convert_frac_to_prob(1, 1)  # Even odds
        0.5
    """
    return round(1 - (nom / (nom + denom)), 4)


def convert_frac_to_dec(nom: int, denom: int) -> float:
    """Convert fractional odds to decimal odds.

    Arguments:
        nom: Numerator of fractional odds.
        denom: Denominator of fractional odds.

    Returns:
        Decimal odds rounded to 4 decimal places.

    Example:
        >>> convert_frac_to_dec(3, 1)  # 3/1 odds
        4.0
        >>> convert_frac_to_dec(5, 2)  # 5/2 odds
        3.5
    """
    return round(1 / (1 - (nom / (nom + denom))), 4)


def exact_binomial_probability(
    number_of_trials: int, number_of_successes: int, success_probability: float
) -> float:
    """Calculate exact binomial probability P(X = k).

    Calculates the probability of exactly k successes in n trials,
    where each trial has probability p of success.

    Arguments:
        number_of_trials: Total number of trials (n).
        number_of_successes: Number of successes (k).
        success_probability: Probability of success on each trial (p).

    Returns:
        Exact probability P(X = k) where X ~ Binomial(n, p).

    Example:
        >>> exact_binomial_probability(10, 5, 0.5)
        0.24609375
        >>> exact_binomial_probability(10, 1, 0.33)
        0.1395...
    """
    n_choose_k = math.factorial(number_of_trials) / (
        math.factorial(number_of_successes)
        * math.factorial(number_of_trials - number_of_successes)
    )
    exact = (
        n_choose_k
        * (success_probability**number_of_successes)
        * ((1 - success_probability) ** (number_of_trials - number_of_successes))
    )
    return exact


def cumulative_binomial_probabilities(
    number_of_trials: int, number_of_successes: int, success_probability: float
) -> tuple[float, float, float, float]:
    """Calculate cumulative binomial probabilities.

    Calculates P(X < k), P(X <= k), P(X > k), and P(X >= k) for X ~ Binomial(n, p).

    Arguments:
        number_of_trials: Total number of trials (n).
        number_of_successes: Number of successes (k).
        success_probability: Probability of success on each trial (p).

    Returns:
        Tuple of (P(X < k), P(X <= k), P(X > k), P(X >= k)).

    Example:
        >>> cumulative_binomial_probabilities(10, 5, 0.5)
        (0.377..., 0.623..., 0.377..., 0.623...)
    """
    X_lt_x = 0.0
    X_lt_eq_x = 0.0
    X_gt_x = 0.0
    X_gt_eq_x = 0.0

    for i in range(number_of_trials + 1):
        exact = exact_binomial_probability(number_of_trials, i, success_probability)
        if i < number_of_successes:
            X_lt_x += exact
            X_lt_eq_x += exact
        elif i == number_of_successes:
            X_lt_eq_x += exact
            X_gt_eq_x += exact
        elif i > number_of_successes:
            X_gt_x += exact
            X_gt_eq_x += exact

    return X_lt_x, X_lt_eq_x, X_gt_x, X_gt_eq_x

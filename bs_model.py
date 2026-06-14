import math
from scipy.stats import norm


def _d1(S, K, T, r, sigma):
    return (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))


def _d2(S, K, T, r, sigma):
    return _d1(S, K, T, r, sigma) - sigma * math.sqrt(T)


def _validate(S, K, T, sigma):
    if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        raise ValueError("S, K, T, sigma 必須為正數")


def call_price(S, K, T, r, sigma):
    _validate(S, K, T, sigma)
    d1, d2 = _d1(S, K, T, r, sigma), _d2(S, K, T, r, sigma)
    return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)


def put_price(S, K, T, r, sigma):
    _validate(S, K, T, sigma)
    d1, d2 = _d1(S, K, T, r, sigma), _d2(S, K, T, r, sigma)
    return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def greeks(S, K, T, r, sigma):
    _validate(S, K, T, sigma)
    d1, d2 = _d1(S, K, T, r, sigma), _d2(S, K, T, r, sigma)
    return {
        "delta_call": norm.cdf(d1),
        "delta_put":  norm.cdf(d1) - 1,
        "gamma":      norm.pdf(d1) / (S * sigma * math.sqrt(T)),
        "vega":       S * norm.pdf(d1) * math.sqrt(T) / 100,
        "theta_call": (-(S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * norm.cdf(d2)) / 365,
        "theta_put":  (-(S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * norm.cdf(-d2)) / 365,
    }

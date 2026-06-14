import pytest
import math
from bs_model import call_price, put_price, greeks

# 標準測試參數：S=100, K=100, T=1yr, r=5%, sigma=20%
S, K, T, r, sigma = 100, 100, 1, 0.05, 0.20


# ── 價格正確性 ────────────────────────────────────────────

def test_call_price_atm():
    """平值 call 已知答案約 10.45"""
    assert abs(call_price(S, K, T, r, sigma) - 10.4506) < 0.01


def test_put_price_atm():
    """平值 put 已知答案約 5.57"""
    assert abs(put_price(S, K, T, r, sigma) - 5.5735) < 0.01


def test_put_call_parity():
    """Put-Call Parity：C - P = S - K * e^(-rT)"""
    C = call_price(S, K, T, r, sigma)
    P = put_price(S, K, T, r, sigma)
    parity = S - K * math.exp(-r * T)
    assert abs((C - P) - parity) < 1e-8


def test_deep_itm_call_approaches_intrinsic():
    """深度價內 call 接近 S - K*e^(-rT)"""
    C = call_price(200, 100, T, r, sigma)
    intrinsic = 200 - 100 * math.exp(-r * T)
    assert abs(C - intrinsic) < 1.0


def test_deep_otm_call_approaches_zero():
    """深度價外 call 接近 0"""
    C = call_price(50, 200, T, r, sigma)
    assert C < 0.01


# ── Greeks 合理性 ─────────────────────────────────────────

def test_delta_call_between_0_and_1():
    """Call delta 必須在 0 到 1 之間"""
    g = greeks(S, K, T, r, sigma)
    assert 0 < g["delta_call"] < 1


def test_delta_put_between_minus1_and_0():
    """Put delta 必須在 -1 到 0 之間"""
    g = greeks(S, K, T, r, sigma)
    assert -1 < g["delta_put"] < 0


def test_gamma_positive():
    """Gamma 必須為正"""
    g = greeks(S, K, T, r, sigma)
    assert g["gamma"] > 0


def test_vega_positive():
    """Vega 必須為正"""
    g = greeks(S, K, T, r, sigma)
    assert g["vega"] > 0


def test_theta_call_negative():
    """Theta (call) 必須為負（時間流逝損耗）"""
    g = greeks(S, K, T, r, sigma)
    assert g["theta_call"] < 0


# ── 輸入驗證 ─────────────────────────────────────────────

def test_negative_stock_price_raises():
    with pytest.raises(ValueError):
        call_price(-100, K, T, r, sigma)


def test_zero_volatility_raises():
    with pytest.raises(ValueError):
        call_price(S, K, T, r, 0)


def test_negative_time_raises():
    with pytest.raises(ValueError):
        put_price(S, K, -1, r, sigma)

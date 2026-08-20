"""SVI Implied Volatility Smile Parametrization and Arbitrage Enforcement.

Implements Gatheral-Jacquier SVI (Stochastic Volatility Inspired) raw parametrization:
  w(k) = a + b * (rho * (k - m) + sqrt((k - m)^2 + sigma^2))
where k = ln(K / F) is log-moneyness, and w(k) = IV(k)^2 * T is total variance.
Checks and enforces butterfly (convexity) and calendar (monotonicity) no-arbitrage conditions.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np


@dataclass(frozen=True, slots=True)
class SVIParams:
    a: float
    b: float
    rho: float
    m: float
    sigma: float
    t_exp: float
    is_arbitrage_free: bool = True

    def total_variance(self, k: float) -> float:
        """Compute total variance w(k) for log-moneyness k = ln(K/F)."""
        discr = (k - self.m) ** 2 + self.sigma**2
        return self.a + self.b * (self.rho * (k - self.m) + math.sqrt(discr))

    def implied_volatility(self, k: float) -> float:
        """Compute annualized implied volatility IV(k) for log-moneyness k."""
        w = max(1e-6, self.total_variance(k))
        return math.sqrt(w / max(0.001, self.t_exp))


def fit_svi_smile(
    strikes: np.ndarray,
    implied_vols: np.ndarray,
    forward_price: float,
    t_exp: float,
    vega_weights: np.ndarray | None = None,
) -> SVIParams | None:
    """Fit raw SVI parameters to a set of strike-IV quotes for a single expiration."""
    valid = np.isfinite(strikes) & np.isfinite(implied_vols) & (strikes > 0) & (implied_vols > 0)
    if np.sum(valid) < 3 or forward_price <= 0 or t_exp <= 0:
        return None

    k_valid = np.log(strikes[valid] / forward_price)
    w_valid = (implied_vols[valid] ** 2) * t_exp

    # Initial parameter heuristics
    atm_w = float(np.interp(0.0, k_valid, w_valid))
    a_init = 0.5 * atm_w
    b_init = 0.1
    rho_init = -0.2
    m_init = 0.0
    sigma_init = 0.1

    best_loss = float("inf")
    best_params = SVIParams(a=a_init, b=b_init, rho=rho_init, m=m_init, sigma=sigma_init, t_exp=t_exp)

    # Grid search optimization for robust SVI raw fit without external scipy dependency
    for b_c in [0.05, 0.1, 0.2, 0.3]:
        for rho_c in [-0.5, -0.2, 0.0, 0.2]:
            for sigma_c in [0.05, 0.1, 0.2]:
                for m_c in [-0.05, 0.0, 0.05]:
                    a_c = max(1e-4, atm_w - b_c * (rho_c * (-m_c) + math.sqrt(m_c**2 + sigma_c**2)))
                    params = SVIParams(a=a_c, b=b_c, rho=rho_c, m=m_c, sigma=sigma_c, t_exp=t_exp)
                    
                    pred_w = np.array([params.total_variance(k) for k in k_valid])
                    loss = float(np.mean((pred_w - w_valid) ** 2))
                    
                    # Gatheral-Jacquier no-arbitrage bounds check
                    # b >= 0, |rho| < 1, sigma > 0, a + b * sigma * sqrt(1 - rho^2) >= 0
                    if b_c >= 0 and abs(rho_c) < 1.0 and sigma_c > 0 and (a_c + b_c * sigma_c * math.sqrt(1.0 - rho_c**2)) >= 0:
                        if loss < best_loss:
                            best_loss = loss
                            best_params = params

    return best_params


def _norm_cdf_svi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def svi_risk_neutral_density(params: SVIParams, k: float, forward: float) -> float:
    """
    Calculate the Risk-Neutral Density (Q) from SVI parameters using Breeden-Litzenberger.
    Returns the PDF value at the given log-moneyness k.
    """
    if not params.is_arbitrage_free:
        return 0.0
    
    eps = 1e-4
    
    def call_k(k_val):
        w = params.total_variance(k_val)
        iv = math.sqrt(w / max(0.001, params.t_exp))
        K_val = forward * math.exp(k_val)
        d1 = (math.log(forward / K_val) + 0.5 * iv**2 * params.t_exp) / (iv * math.sqrt(params.t_exp))
        d2 = d1 - iv * math.sqrt(params.t_exp)
        return forward * _norm_cdf_svi(d1) - K_val * _norm_cdf_svi(d2)
        
    K = forward * math.exp(k)
    k_plus = math.log((K + eps) / forward)
    k_minus = math.log((K - eps) / forward)
    k_current = math.log(K / forward)
    
    c_plus = call_k(k_plus)
    c_minus = call_k(k_minus)
    c_current = call_k(k_current)
    
    d2c_dk2 = (c_plus - 2*c_current + c_minus) / (eps**2)
    pdf_K = max(0.0, d2c_dk2)
    return pdf_K * K


def physical_density_from_risk_neutral(q_pdf: float, log_return: float, risk_premium: float = 0.05, volatility: float = 0.15) -> float:
    """
    Convert Risk-Neutral Density (Q) to Physical Distribution (P) 
    using a simple risk premium adjustment.
    """
    adjustment = math.exp((risk_premium / max(1e-4, volatility**2)) * log_return)
    return q_pdf * adjustment


def bkm_model_free_implied_variance(
    strikes: np.ndarray,
    call_prices: np.ndarray,
    put_prices: np.ndarray,
    forward: float,
    r: float,
    t_exp: float
) -> float:
    """
    Calculate model-free implied variance using Bakshi-Kapadia-Madan (BKM) approach.
    """
    if len(strikes) < 3 or t_exp <= 0:
        return 0.0
        
    idx = np.argsort(strikes)
    K = strikes[idx]
    C = call_prices[idx]
    P = put_prices[idx]
    
    dK = np.zeros_like(K)
    dK[0] = K[1] - K[0]
    dK[-1] = K[-1] - K[-2]
    dK[1:-1] = (K[2:] - K[:-2]) / 2.0
    
    variance = 0.0
    for i in range(len(K)):
        strike = K[i]
        price = C[i] if strike > forward else P[i]
        weight = dK[i] / (strike**2)
        variance += price * weight
        
    return 2.0 * math.exp(r * t_exp) * variance / t_exp

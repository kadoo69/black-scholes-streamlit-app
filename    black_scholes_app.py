 1 import streamlit as st
     2 import numpy as np
     3 from scipy.stats import norm
     4 
     5 # Cumulative standard normal distribution function
     6 def N(x):
     7     return norm.cdf(x)
     8 
     9 # Probability density function of the standard normal distribution
    10 def phi(x):
    11     return norm.pdf(x)
    12 
    13 def calculate_black_scholes(S, K, T, r, sigma, q, option_type):
    14     if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
    15         raise ValueError("Input parameters S, K, T, and sigma must be positive.")
    16     if r < 0 or q < 0:
    17         raise ValueError("Interest rate and dividend yield cannot be negative.")
    18 
    19     d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    20     d2 = d1 - sigma * np.sqrt(T)
    21 
    22     if option_type == 'call':
    23         price = S * np.exp(-q * T) * N(d1) - K * np.exp(-r * T) * N(d2)
    24         delta = np.exp(-q * T) * N(d1)
    25         theta = -(S * np.exp(-q * T) * phi(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * N(d2) + q * S * np.exp(-q *
       T) * N(d1)
    26         rho = K * T * np.exp(-r * T) * N(d2)
    27     else:  # put
    28         price = K * np.exp(-r * T) * N(-d2) - S * np.exp(-q * T) * N(-d1)
    29         delta = np.exp(-q * T) * (N(d1) - 1)
    30         theta = -(S * np.exp(-q * T) * phi(d1) * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * N(-d2) - q * S * np.exp(-q
       * T) * N(-d1)
    31         rho = -K * T * np.exp(-r * T) * N(-d2)
    32 
    33     gamma = (phi(d1) * np.exp(-q * T)) / (S * sigma * np.sqrt(T))
    34     vega = S * np.exp(-q * T) * phi(d1) * np.sqrt(T)
    35 
    36     intrinsic_value = max(0, S - K) if option_type == 'call' else max(0, K - S)
    37     time_value = max(0, price - intrinsic_value)
    38 
    39     if option_type == 'call':
    40         moneyness = 'ITM' if S > K else ('ATM' if S == K else 'OTM')
    41     else:  # put
    42         moneyness = 'ITM' if S < K else ('ATM' if S == K else 'OTM')
    43 
    44     return {
    45         "price": price,
    46         "delta": delta,
    47         "gamma": gamma,
    48         "theta": theta,
    49         "vega": vega,
    50         "rho": rho,
    51         "intrinsic_value": intrinsic_value,
    52         "time_value": time_value,
    53         "moneyness": moneyness,
    54     }
    55 
    56 st.set_page_config(layout="wide", page_title="Black-Scholes Options Calculator")
    57 
    58 st.title("Black-Scholes Options Pricing Model")
    59 
    60 st.sidebar.header("Input Parameters")
    61 
    62 S = st.sidebar.number_input("Current Stock Price (S)", value=100.0, min_value=0.01, format="%.2f")
    63 K = st.sidebar.number_input("Strike Price (K)", value=100.0, min_value=0.01, format="%.2f")
    64 T = st.sidebar.number_input("Time to Expiration (T, years)", value=1.0, min_value=0.01, format="%.2f")
    65 r = st.sidebar.number_input("Risk-free Interest Rate (r, %)", value=5.0, min_value=0.0, format="%.2f") / 100
    66 sigma = st.sidebar.number_input("Volatility (σ, %)", value=20.0, min_value=0.01, format="%.2f") / 100
    67 q = st.sidebar.number_input("Dividend Yield (q, %)", value=0.0, min_value=0.0, format="%.2f") / 100
    68 option_type = st.sidebar.radio("Option Type", ('call', 'put'))
    69 
    70 if st.sidebar.button("Calculate"):
    71     try:
    72         results = calculate_black_scholes(S, K, T, r, sigma, q, option_type)
    73 
    74         st.subheader("Results")
    75         col1, col2, col3 = st.columns(3)
    76         with col1:
    77             st.metric("Option Price", f"{results['price']:.4f}")
    78         with col2:
    79             st.metric("Intrinsic Value", f"{results['intrinsic_value']:.4f}")
    80         with col3:
    81             st.metric("Time Value", f"{results['time_value']:.4f}")
    82         st.write(f"**Moneyness:** {results['moneyness']}")
    83 
    84         st.subheader("Greeks")
    85         col1, col2, col3, col4, col5 = st.columns(5)
    86         with col1:
    87             st.metric("Delta", f"{results['delta']:.4f}")
    88         with col2:
    89             st.metric("Gamma", f"{results['gamma']:.4f}")
    90         with col3:
    91             st.metric("Theta", f"{results['theta']:.4f}")
    92         with col4:
    93             st.metric("Vega", f"{results['vega']:.4f}")
    94         with col5:
    95             st.metric("Rho", f"{results['rho']:.4f}")
    96 
    97     except ValueError as e:
    98         st.error(f"Input Error: {e}")
    99     except Exception as e:
   100         st.error(f"An unexpected error occurred: {e}")
   101 
   102 st.markdown("---")
   103 st.markdown("Disclaimer: This calculator is for educational purposes only and should not be used for actual trading decisions.")
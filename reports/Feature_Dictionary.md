# Feature Dictionary (PRD 2)

This document describes the engineered features generated to capture engine degradation patterns more effectively than raw sensor readings.

| Feature | Motivation | Window / Parameters |
|---|---|---|
| `rolling_mean_<sensor>` | Smooths high-frequency sensor noise to clearly capture the underlying monotonic degradation trend. | 15 cycles (initial heuristic) |
| `rolling_std_<sensor>` | Captures increasing signal instability and variance as the engine approaches failure. | 15 cycles (initial heuristic) |
| `ema_<sensor>` | Emphasizes recent engine behavior while smoothing out older noise (reacts faster than rolling mean). | span=15 cycles |
| `diff_<sensor>` | Captures the immediate rate of change and stability between consecutive cycles. | shift=1 |
| `log_cycle` | Degradation often accelerates non-linearly over time; the log of the cycle provides a transformed time scale that tree models can easily split on. | N/A |

"""
Ajuste de curva contínua para a tabela de benchmark B(t, $1M).
Testa múltiplos modelos e encontra o melhor fit.
"""
import numpy as np
from scipy.optimize import curve_fit

# Dados da tabela
years = np.array([1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2013, 2015, 2017, 2019, 2021, 2023, 2025])
bits  = np.array([33,   36,   37,   40,   41,   51,   56,   59,   62,   62,   72,   76,   77,   79,   78,   80,   81])

# ── Modelo 1: Linear ──
c1 = np.polyfit(years, bits, 1)
pred1 = np.polyval(c1, years)
mse1 = np.mean((bits - pred1)**2)
print(f"Linear:   B(t) = {c1[0]:.4f}*t + ({c1[1]:.1f})")
print(f"          MSE = {mse1:.2f}")

# ── Modelo 2: Quadrático ──
c2 = np.polyfit(years, bits, 2)
pred2 = np.polyval(c2, years)
mse2 = np.mean((bits - pred2)**2)
print(f"\nQuad:     B(t) = {c2[0]:.6f}*t² + {c2[1]:.4f}*t + ({c2[2]:.1f})")
print(f"          MSE = {mse2:.2f}")

# ── Modelo 3: Cúbico ──
c3 = np.polyfit(years, bits, 3)
pred3 = np.polyval(c3, years)
mse3 = np.mean((bits - pred3)**2)
print(f"\nCubico:   MSE = {mse3:.2f}")

# ── Modelo 4: Logarítmico  B(t) = a * ln(t - 1960) + b ──
def log_model(t, a, b):
    return a * np.log(t - 1960) + b

p4, _ = curve_fit(log_model, years, bits)
pred4 = log_model(years, *p4)
mse4 = np.mean((bits - pred4)**2)
print(f"\nLog:      B(t) = {p4[0]:.4f} * ln(t - 1960) + ({p4[1]:.2f})")
print(f"          MSE = {mse4:.2f}")

# ── Modelo 5: Logístico  B(t) = L / (1 + exp(-k*(t - t_mid))) + b ──
def logistic(t, L, k, t_mid, b):
    return L / (1 + np.exp(-k * (t - t_mid))) + b

p5, _ = curve_fit(logistic, years, bits, p0=[60, 0.05, 1995, 30], maxfev=10000)
pred5 = logistic(years, *p5)
mse5 = np.mean((bits - pred5)**2)
print(f"\nLogistic: L={p5[0]:.2f}, k={p5[1]:.4f}, mid={p5[2]:.1f}, b={p5[3]:.2f}")
print(f"          MSE = {mse5:.2f}")

# ── Modelo 6: Gompertz  B(t) = a * exp(-b * exp(-c * (t - 1960))) ──
def gompertz(t, a, b, c):
    return a * np.exp(-b * np.exp(-c * (t - 1960)))

p6, _ = curve_fit(gompertz, years, bits, p0=[90, 3, 0.05], maxfev=10000)
pred6 = gompertz(years, *p6)
mse6 = np.mean((bits - pred6)**2)
print(f"\nGompertz: a={p6[0]:.4f}, b={p6[1]:.6f}, c={p6[2]:.6f}")
print(f"          B(t) = {p6[0]:.4f} * exp(-{p6[1]:.6f} * exp(-{p6[2]:.6f} * (t - 1960)))")
print(f"          MSE = {mse6:.2f}")

# ── Modelo 7: Log-linear  B(t) = a*ln(t-1960) + b*t + c ──
def log_linear(t, a, b, c):
    return a * np.log(t - 1960) + b * t + c

p7, _ = curve_fit(log_linear, years, bits, p0=[10, 0.5, -900])
pred7 = log_linear(years, *p7)
mse7 = np.mean((bits - pred7)**2)
print(f"\nLogLin:   B(t) = {p7[0]:.4f}*ln(t-1960) + {p7[1]:.4f}*t + ({p7[2]:.2f})")
print(f"          MSE = {mse7:.2f}")

# ── Modelo 8: Power  B(t) = a * (t-1960)^b + c ──
def power_model(t, a, b, c):
    return a * (t - 1960)**b + c

p8, _ = curve_fit(power_model, years, bits, p0=[1, 0.8, 30], maxfev=10000)
pred8 = power_model(years, *p8)
mse8 = np.mean((bits - pred8)**2)
print(f"\nPower:    B(t) = {p8[0]:.4f} * (t-1960)^{p8[1]:.4f} + ({p8[2]:.2f})")
print(f"          MSE = {mse8:.2f}")

# ── Modelo 9: Sqrt-log  B(t) = a * sqrt(t-1960) + b * ln(t-1960) + c ──
def sqrt_log(t, a, b, c):
    return a * np.sqrt(t - 1960) + b * np.log(t - 1960) + c

p9, _ = curve_fit(sqrt_log, years, bits, p0=[5, 5, 20])
pred9 = sqrt_log(years, *p9)
mse9 = np.mean((bits - pred9)**2)
print(f"\nSqrtLog:  B(t) = {p9[0]:.4f}*√(t-1960) + {p9[1]:.4f}*ln(t-1960) + ({p9[2]:.2f})")
print(f"          MSE = {mse9:.2f}")

# ── Ranking ──
print("\n" + "="*50)
print("RANKING POR MSE:")
print("="*50)
models = {
    "Linear": (mse1, pred1),
    "Quad": (mse2, pred2),
    "Cubico": (mse3, pred3),
    "Log": (mse4, pred4),
    "Logistic": (mse5, pred5),
    "Gompertz": (mse6, pred6),
    "LogLinear": (mse7, pred7),
    "Power": (mse8, pred8),
    "SqrtLog": (mse9, pred9),
}
for name, (mse, _) in sorted(models.items(), key=lambda x: x[0][0]):
    print(f"  {name:12s}  MSE = {mse:.2f}")

# ── Tabela detalhada dos 2 melhores ──
best_names = sorted(models.keys(), key=lambda n: models[n][0])[:2]
for bname in best_names:
    mse_val, preds = models[bname]
    print(f"\n{'─'*50}")
    print(f"Verificação: {bname}  (MSE={mse_val:.2f})")
    print(f"{'─'*50}")
    print(f"  {'Ano':>4s}  {'Real':>4s}  {'Pred':>6s}  {'Erro':>5s}")
    for y, b, p in zip(years, bits, preds):
        print(f"  {y:4d}  {b:4d}  {p:6.1f}  {b-p:+5.1f}")

# ── Extrapolação ──
print(f"\n{'─'*50}")
print("Extrapolação comparativa:")
print(f"{'─'*50}")
print(f"  {'Ano':>4s}  {'Logistic':>8s}  {'Gompertz':>8s}  {'LogLin':>8s}  {'Power':>8s}")
for y in [2026, 2027, 2028, 2029, 2030, 2035, 2040, 2050, 2060, 2080, 2100]:
    pl = logistic(y, *p5)
    pg = gompertz(y, *p6)
    pll = log_linear(y, *p7)
    pp = power_model(y, *p8)
    print(f"  {y:4d}  {pl:8.1f}  {pg:8.1f}  {pll:8.1f}  {pp:8.1f}")

print(f"\nAssíntota Logistic: {p5[0]+p5[3]:.1f} bits")
print(f"Assíntota Gompertz: {p6[0]:.1f} bits")

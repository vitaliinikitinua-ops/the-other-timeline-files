"""Real data loaders (files in ../data). Every on-screen number must come from here."""
import csv, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

def sp500():
    """{'YYYY-MM': monthly average price} Shiller S&P 500 (price only)."""
    return {r["Date"][:7]: float(r["SP500"]) for r in csv.DictReader(open(os.path.join(D, "sp500.csv")))}

def fred(code, monthly=True):
    out = {}
    for r in csv.DictReader(open(os.path.join(D, f"fred_{code}.csv"))):
        k = list(r.keys())
        try:
            v = float(r[k[1]])
        except ValueError:
            continue
        key = r[k[0]][:7] if monthly else r[k[0]]
        if monthly and key in out:
            continue  # keep first observation of the month
        out[key] = v
    return out

def gold():
    return {r["Date"]: float(r["Price"]) for r in csv.DictReader(open(os.path.join(D, "gold.csv")))}

def dca(prices, start, end, monthly):
    """Invest `monthly` on each month start..end at that month's price. Returns lists (months, invested, value)."""
    ks = [k for k in sorted(prices) if start <= k <= end]
    sh = inv = 0.0; I = []; V = []
    for k in ks:
        sh += monthly / prices[k]; inv += monthly
        I.append(inv); V.append(sh * prices[k])
    return ks, I, V

def card_payoff(balance, apr, fixed=None, min_pct=0.01, floor=25.0):
    """Monthly simulation. Minimum = max(floor, min_pct*balance + interest). Returns months, total paid, balances list."""
    r = apr / 100 / 12; b = balance; paid = 0.0; bal = [b]; m = 0
    while b > 0.005 and m < 1200:
        i = b * r
        p = fixed if fixed else max(floor, b * min_pct + i)
        p = min(p, b + i); b = b + i - p; paid += p; m += 1; bal.append(max(b, 0))
    return m, paid, bal

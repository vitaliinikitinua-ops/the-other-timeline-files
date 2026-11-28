"""Karl #02 numbers - every number in script.md comes from here or from the cited sources. Run: python3 karl02_numbers.py
Data: FRED TERMCBCCALLNS (card APR on accounts assessed interest, Aug 2026) in ../data. Facts: CFPB Jan 2025 (63% stacked),
LendingTree 2025 (41% late) / 2026 (47%), Adobe holiday 2025 (~$20.0B BNPL). Wage $20/h after tax = EXAMPLE."""
import csv, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, '..', 'data')
apr = next(float(r[1]) for r in csv.reader(open(os.path.join(D, 'fred_TERMCBCCALLNS.csv'))) if r[0] == '2026-08-01') / 100
WAGE = 20  # EXAMPLE take-home pay per hour

def minimum_payments(bal):  # 1% of balance + interest, min $25
    months = paid = 0
    while bal > 0.005:
        i = bal * apr / 12; p = min(max(25, bal * 0.01 + i), bal + i); bal += i - p; paid += p; months += 1
    return months, paid

full = 2000; cart = full * 0.6; m, paid = minimum_payments(cart)
print(f'hours at ${WAGE}/h: $120={120/WAGE:.0f} h, $400={400/WAGE:.0f} h, $240={240/WAGE:.0f} h, $1,200={cart/WAGE:.0f} h, $600={600/WAGE:.0f} h, $18={18/WAGE*60:.0f} min')
print(f'Max cart ${full:,} -40% = ${cart:,.0f} = 6 x ${cart/6:,.0f} = 24 x ${cart/24:,.0f}')
print(f'APR {apr*100:.2f}% -> {m} months ({m/12:.1f} y), interest ${paid-cart:,.0f}, total ${paid:,.0f} > full ${full:,}: {paid > full}')
print('blender 4 x $22.50 =', 4 * 22.5, '| chair $400/4 =', 400 / 4, '| truck 499 x 72 =', 499 * 72, '| Mia 240/8 =', 240 / 8, 'h | $6 =', 6 / WAGE * 60, 'min')
txt = open(os.path.join(HERE, 'script.md')).read().split('---', 1)[1]
vo = [l for l in txt.splitlines() if l.strip() and not l.startswith(('#', '['))]
print('VO lines:', len(vo), 'words:', sum(len(l.split()) for l in vo), '-> at 190 wpm ~', round(sum(len(l.split()) for l in vo) / 190, 1), 'min')

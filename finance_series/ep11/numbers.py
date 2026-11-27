"""EP11 numbers - every value in script.md comes from here. Run: python3 numbers.py"""
import csv, os, re
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

def fred(name, date):
    for r in csv.reader(open(os.path.join(D, f'fred_{name}.csv'))):
        if r[0] == date:
            return float(r[1])

apr = fred('TERMCBCCALLNS', '2026-08-01') / 100
wage = fred('CES0500000003', '2026-10-01')
sp = {r['Date']: float(r['SP500']) for r in csv.DictReader(open(os.path.join(D, 'sp500.csv'))) if r['SP500']}

full, disc = 2000, 0.40
cart = full * (1 - disc)
plans, plan_price = 6, cart / 6

def minimum_payments(bal):
    months = paid = 0
    while bal > 0.005:
        i = bal * apr / 12
        p = min(max(25, bal * 0.01 + i), bal + i)
        bal += i - p; paid += p; months += 1
    return months, paid

m, paid = minimum_payments(cart)
grow = sp['2026-09-01'] / sp['2016-09-01']
print(f'cart ${cart:,.0f} = {plans} x ${plan_price:,.0f} = {plans*4} payments of ${plan_price/4:,.0f}')
print(f'hours: {cart/wage:.1f} (wage ${wage:.2f}); unspent $800 = {800/wage:.1f} h')
print(f'APR {apr*100:.2f}% -> {m} months ({m/12:.1f} y), interest ${paid-cart:,.0f}, total ${paid:,.0f} vs full ${full:,}')
print(f'$800 S&P 2016-09 -> 2026-09: x{grow:.2f} = ${800*grow:,.0f}')
txt = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'script.md')).read()
vo = ' '.join(re.findall(r'^(?:VO|CASHIER[^:]*):\s*(.*)$', txt, re.M))
vo += ' ' + ' '.join(re.findall(r'^(Rule \w+:.*|This is education.*)$', txt, re.M))
print('VO words:', len(vo.split()))

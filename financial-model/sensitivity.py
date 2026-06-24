# -*- coding: utf-8 -*-
"""
تحليل الحساسية — استوديو Reformer Pilates الرياض.
يختبر متانة النموذج تجاه: رسوم الدفع الإلكتروني، احتياطي الإهلاك، ومعالجة ضريبة
القيمة المضافة (VAT). شغّل: python3 sensitivity.py
"""
CAP = 1092          # الطاقة الشهرية (6 أجهزة × 7 حصص × 26 يوم)
INVEST = 275000
OCC_RAMP = [0.38, 0.55, 0.63, 0.68, 0.70]
OPEX_YEAR = [762000, 754000, 885000, 911000, 938000]


def npv(rate, flows):
    return sum(c / (1 + rate) ** t for t, c in enumerate(flows))


def irr(flows):
    lo, hi = -0.9, 5.0
    flo = npv(lo, flows)
    for _ in range(300):
        m = (lo + hi) / 2
        fm = npv(m, flows)
        if (flo > 0) == (fm > 0):
            lo, flo = m, fm
        else:
            hi = m
    return (lo + hi) / 2


def model(net_price, fixed_opex, fee_rate, depreciation_year, label):
    maxrev = CAP * net_price
    be = fixed_opex / (maxrev * (1 - fee_rate))
    net_m = lambda occ: occ * maxrev * (1 - fee_rate) - fixed_opex
    cf = [-INVEST]
    for i in range(5):
        rev = OCC_RAMP[i] * maxrev * 12
        cf.append(rev * (1 - fee_rate) - (OPEX_YEAR[i] + depreciation_year))
    return dict(label=label, be=be, n50=net_m(0.5), n70=net_m(0.7),
                npv=npv(0.15, cf), irr=irr(cf), y1=cf[1])


DEP = 700 * 12  # احتياطي إهلاك/إحلال 700 ريال/شهر
cases = [
    model(150, 61000, 0.0, 0, "أ) الأساسي (سعر صافٍ 150)"),
    model(150, 61700, 0.015, DEP, "ب) + رسوم دفع 1.5% + إهلاك"),
    model(150 / 1.15, 61700, 0.015, DEP, "ج) الأكثر تحفظاً (السعر شامل الضريبة + رسوم + إهلاك)"),
]
print(f"{'الحالة':<48}{'تعادل':>8}{'50%/شهر':>12}{'70%/شهر':>12}{'NPV@15%':>12}{'IRR':>7}")
for c in cases:
    print(f"{c['label']:<48}{c['be']:>7.1%}{c['n50']:>12,.0f}{c['n70']:>12,.0f}{c['npv']:>12,.0f}{c['irr']:>7.0%}")

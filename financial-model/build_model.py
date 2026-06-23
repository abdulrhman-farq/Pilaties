# -*- coding: utf-8 -*-
"""
بناء النموذج المالي لاستوديو Reformer Pilates النسائي - الرياض.

ملاحظة مهمة: تُكتب الأرقام كقيَم محسوبة (وليست صيغاً) لتظهر بشكل صحيح على
كل البرامج وأجهزة الجوال (iPhone/Android) دون الحاجة لإعادة حساب.
عند تعديل أي افتراض في قسم INPUTS أدناه، أعد تشغيل السكربت لتحديث الملف:
    pip install openpyxl && python3 build_model.py
"""
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ============================================================
# INPUTS — الافتراضات (عدّل هنا ثم أعد تشغيل السكربت)
# ============================================================
FX = 3.75
MACHINES = 6
SEAT_PER_MACHINE = 1
CLASSES_DAY = 7
DAYS = 26
PRICE = 150
RENT_YEAR = 204000
SALARIES = 27000
GOSI = 2200
UTILITIES = 3800
SOFTWARE = 1500
MARKETING = 5000
SUPPLIES = 2000
MAINT = 1000
ADMIN = 1500
DISCOUNT = 0.15

# CapEx
CAPEX = [
    ("أجهزة Reformer مُورّدة (FOB+شحن+جمارك+نقل)", 41000),
    ("أدوات مساعدة (Props)", 15000),
    ("ديكور وتجهيز داخلي وأثاث", 80000),
    ("لوحة خارجية وأنظمة تقنية وكاميرات", 15000),
    ("رخص وتراخيص حكومية", 15000),
    ("احتياطي طوارئ", 9000),
]
WORKING_CAPITAL = 100000

# توقعات 5 سنوات
OCC_RAMP = [0.38, 0.55, 0.63, 0.68, 0.70]
OPEX_YEAR = [762000, 754000, 885000, 911000, 938000]

# ============================================================
# الحسابات
# ============================================================
RENT_MONTH = RENT_YEAR / 12
OPEX_ITEMS = [
    ("الإيجار (سنوي ÷ 12)", RENT_MONTH),
    ("رواتب الموظفات", SALARIES),
    ("التأمينات + نهاية الخدمة", GOSI),
    ("كهرباء وماء", UTILITIES),
    ("نظام الحجز + اتصالات", SOFTWARE),
    ("التسويق", MARKETING),
    ("مستهلكات وغسيل وتنظيف", SUPPLIES),
    ("صيانة الأجهزة", MAINT),
    ("محاسبة وإداريات", ADMIN),
]
OPEX_MONTH = sum(v for _, v in OPEX_ITEMS)
CAPEX_TOTAL = sum(v for _, v in CAPEX)
INVEST = CAPEX_TOTAL + WORKING_CAPITAL

CAPACITY = MACHINES * SEAT_PER_MACHINE * CLASSES_DAY * DAYS  # حصة-عميلة/شهر
MAX_REV = CAPACITY * PRICE
BREAK_EVEN = OPEX_MONTH / MAX_REV

SCEN = [0.30, 0.50, 0.70, 0.90]


def scenario(occ):
    rev = occ * MAX_REV
    seats = round(occ * CAPACITY)
    per_class = round(occ * MACHINES, 1)
    net_m = rev - OPEX_MONTH
    net_y = net_m * 12
    payback = (INVEST / net_m) if net_m > 0 else None
    roi = net_y / INVEST
    return dict(occ=occ, rev=rev, seats=seats, per_class=per_class,
                net_m=net_m, net_y=net_y, payback=payback, roi=roi)


SCEN_DATA = [scenario(o) for o in SCEN]

# تدفقات 5 سنوات
cashflows = [-INVEST]
rev_year, net_year, cum = [], [], []
running = -INVEST
for i in range(5):
    rev = OCC_RAMP[i] * CAPACITY * PRICE * 12
    net = rev - OPEX_YEAR[i]
    rev_year.append(rev)
    net_year.append(net)
    cashflows.append(net)
    running += net
    cum.append(running)


def npv(rate, flows):
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(flows))


def irr(flows):
    lo, hi = -0.9, 5.0
    f_lo = npv(lo, flows)
    for _ in range(200):
        mid = (lo + hi) / 2
        f_mid = npv(mid, flows)
        if abs(f_mid) < 1e-4:
            return mid
        if (f_lo > 0) == (f_mid > 0):
            lo, f_lo = mid, f_mid
        else:
            hi = mid
    return (lo + hi) / 2


NPV15 = npv(DISCOUNT, cashflows)
NPV12 = npv(0.12, cashflows)
IRR = irr(cashflows)
TOTAL_CF = sum(cashflows[1:])

# ============================================================
# الأنماط
# ============================================================
TITLE = Font(name="Arial", size=14, bold=True, color="FFFFFF")
HEAD = Font(name="Arial", size=11, bold=True, color="FFFFFF")
BOLD = Font(name="Arial", size=11, bold=True)
NORM = Font(name="Arial", size=11)
INPUT_FONT = Font(name="Arial", size=11, bold=True, color="1F4E78")
NAVY = PatternFill("solid", fgColor="1F4E78")
TEAL = PatternFill("solid", fgColor="2E8B8B")
LGREY = PatternFill("solid", fgColor="D9E1F2")
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
GREEN = PatternFill("solid", fgColor="C6EFCE")
RED = PatternFill("solid", fgColor="FFC7CE")
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
RIGHT = Alignment(horizontal="right", vertical="center")
NUM = "#,##0"
PCT = "0%"
PCT1 = "0.0%"

wb = openpyxl.Workbook()


def setup(ws, title, span):
    ws.sheet_view.rightToLeft = True
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=span)
    c = ws.cell(row=1, column=1, value=title)
    c.font = TITLE; c.fill = NAVY; c.alignment = CENTER
    ws.row_dimensions[1].height = 28


def put(ws, r, col, val, font=NORM, fill=None, fmt=None, align=None):
    cell = ws.cell(row=r, column=col, value=val)
    cell.font = font
    cell.border = BORDER
    if fill:
        cell.fill = fill
    if fmt:
        cell.number_format = fmt
    if align:
        cell.alignment = align
    return cell


# ---------- 1) الافتراضات ----------
a = wb.active
a.title = "الافتراضات"
setup(a, "الافتراضات الأساسية", 3)
put(a, 2, 1, "البند", HEAD, TEAL, align=CENTER)
put(a, 2, 2, "القيمة", HEAD, TEAL, align=CENTER)
put(a, 2, 3, "الوحدة", HEAD, TEAL, align=CENTER)
rows = [
    ("سعر الصرف (USD/SAR)", FX, "ريال/دولار", NUM if FX >= 100 else "0.00"),
    ("عدد أجهزة Reformer", MACHINES, "جهاز", "0"),
    ("سعة الجهاز", SEAT_PER_MACHINE, "عميلة/حصة", "0"),
    ("عدد الحصص اليومية", CLASSES_DAY, "حصة", "0"),
    ("أيام التشغيل شهرياً", DAYS, "يوم", "0"),
    ("سعر الحصة المفردة", PRICE, "ريال", NUM),
    ("الإيجار السنوي", RENT_YEAR, "ريال/سنة", NUM),
    ("الطاقة الشهرية القصوى", CAPACITY, "حصة-عميلة", NUM),
    ("الإيراد الشهري عند 100%", MAX_REV, "ريال", NUM),
    ("معدل الخصم لـ NPV", DISCOUNT, "نسبة", PCT),
]
r = 3
for label, val, unit, fmt in rows:
    put(a, r, 1, label)
    is_input = label in ("سعر الصرف (USD/SAR)", "عدد أجهزة Reformer", "سعة الجهاز",
                         "عدد الحصص اليومية", "أيام التشغيل شهرياً", "سعر الحصة المفردة",
                         "الإيجار السنوي", "معدل الخصم لـ NPV")
    put(a, r, 2, val, INPUT_FONT if is_input else BOLD,
        INPUT_FILL if is_input else LGREY, fmt, CENTER)
    put(a, r, 3, unit)
    r += 1
a.column_dimensions["A"].width = 30
a.column_dimensions["B"].width = 14
a.column_dimensions["C"].width = 14

# ---------- 2) التكلفة التأسيسية ----------
c = wb.create_sheet("التكلفة التأسيسية")
setup(c, "التكلفة التأسيسية (CapEx) — ريال", 2)
put(c, 2, 1, "البند", HEAD, TEAL, align=CENTER)
put(c, 2, 2, "القيمة (ريال)", HEAD, TEAL, align=CENTER)
r = 3
for label, val in CAPEX:
    put(c, r, 1, label); put(c, r, 2, val, NORM, fmt=NUM, align=CENTER); r += 1
put(c, r, 1, "إجمالي التأسيس (قبل رأس المال العامل)", BOLD, LGREY)
put(c, r, 2, CAPEX_TOTAL, BOLD, LGREY, NUM, CENTER); r += 1
put(c, r, 1, "رأس المال العامل"); put(c, r, 2, WORKING_CAPITAL, NORM, fmt=NUM, align=CENTER); r += 1
put(c, r, 1, "إجمالي الاستثمار المطلوب", HEAD, NAVY)
put(c, r, 2, INVEST, HEAD, NAVY, NUM, CENTER)
c.column_dimensions["A"].width = 42; c.column_dimensions["B"].width = 16

# ---------- 3) التكاليف التشغيلية ----------
o = wb.create_sheet("التكاليف التشغيلية")
setup(o, "التكاليف التشغيلية الشهرية (OpEx)", 2)
put(o, 2, 1, "البند", HEAD, TEAL, align=CENTER)
put(o, 2, 2, "القيمة (ريال/شهر)", HEAD, TEAL, align=CENTER)
r = 3
for label, val in OPEX_ITEMS:
    put(o, r, 1, label); put(o, r, 2, val, NORM, fmt=NUM, align=CENTER); r += 1
put(o, r, 1, "إجمالي المصروف التشغيلي الشهري", HEAD, NAVY)
put(o, r, 2, OPEX_MONTH, HEAD, NAVY, NUM, CENTER)
o.column_dimensions["A"].width = 34; o.column_dimensions["B"].width = 18

# ---------- 4) سيناريوهات الإشغال ----------
s = wb.create_sheet("سيناريوهات الإشغال")
setup(s, "سيناريوهات الإشغال", 5)
heads = ["المؤشر", "إشغال 30%", "إشغال 50%", "إشغال 70%", "إشغال 90%"]
for i, h in enumerate(heads, 1):
    put(s, 2, i, h, HEAD, TEAL, align=CENTER)


def srow(r, label, key, fmt=NUM, fill=None, font=NORM, pct=False):
    put(s, r, 1, label, BOLD, align=RIGHT)
    for i, d in enumerate(SCEN_DATA, start=2):
        v = d[key]
        if v is None:
            put(s, r, i, "لا يُسترد", font, fill, None, CENTER)
        else:
            put(s, r, i, v, font, fill, fmt, CENTER)


put(s, 3, 1, "نسبة الإشغال", BOLD, align=RIGHT)
for i, d in enumerate(SCEN_DATA, start=2):
    put(s, 3, i, d["occ"], NORM, None, PCT, CENTER)
srow(4, "المقاعد المباعة/شهر", "seats", "0")
srow(5, "متوسط العميلات/حصة", "per_class", "0.0")
srow(6, "الإيراد الشهري (ريال)", "rev", NUM)
put(s, 7, 1, "المصروف التشغيلي الشهري", BOLD, align=RIGHT)
for i in range(2, 6):
    put(s, 7, i, -OPEX_MONTH, NORM, None, NUM, CENTER)
srow(8, "صافي الربح الشهري", "net_m", NUM, GREEN, BOLD)
srow(9, "صافي الربح السنوي", "net_y", NUM, GREEN, BOLD)
srow(10, "فترة الاسترداد (شهر)", "payback", "0.0")
srow(11, "ROI سنوي", "roi", PCT)
put(s, 13, 1, "نقطة التعادل (نسبة إشغال)", HEAD, LGREY)
put(s, 13, 2, BREAK_EVEN, HEAD, LGREY, PCT1, CENTER)
s.column_dimensions["A"].width = 24
for col in "BCDE":
    s.column_dimensions[col].width = 13

# ---------- 5) توقعات 5 سنوات ----------
p = wb.create_sheet("توقعات 5 سنوات")
setup(p, "التوقعات المالية 5 سنوات والمؤشرات (NPV / IRR / Payback)", 7)
cols = ["البند", "السنة 0", "السنة 1", "السنة 2", "السنة 3", "السنة 4", "السنة 5"]
for i, h in enumerate(cols, 1):
    put(p, 2, i, h, HEAD, TEAL, align=CENTER)
put(p, 3, 1, "متوسط الإشغال", BOLD, align=RIGHT)
put(p, 4, 1, "الإيراد السنوي", BOLD, align=RIGHT)
put(p, 5, 1, "المصروف السنوي", BOLD, align=RIGHT)
put(p, 6, 1, "صافي التدفق النقدي", BOLD, align=RIGHT)
put(p, 7, 1, "التدفق التراكمي", BOLD, align=RIGHT)
put(p, 3, 2, "—", NORM, align=CENTER)
put(p, 4, 2, "—", NORM, align=CENTER)
put(p, 5, 2, "—", NORM, align=CENTER)
put(p, 6, 2, -INVEST, BOLD, RED, NUM, CENTER)
put(p, 7, 2, -INVEST, NORM, None, NUM, CENTER)
for i in range(5):
    col = 3 + i
    put(p, 3, col, OCC_RAMP[i], NORM, None, PCT, CENTER)
    put(p, 4, col, rev_year[i], NORM, None, NUM, CENTER)
    put(p, 5, col, OPEX_YEAR[i], NORM, None, NUM, CENTER)
    put(p, 6, col, net_year[i], BOLD, GREEN, NUM, CENTER)
    put(p, 7, col, cum[i], NORM, None, NUM, CENTER)
# المؤشرات
put(p, 9, 1, "المؤشرات المالية", HEAD, NAVY)
put(p, 9, 2, "", HEAD, NAVY)
metrics = [
    ("NPV @ 15%", NPV15, NUM),
    ("NPV @ 12%", NPV12, NUM),
    ("IRR (معدل العائد الداخلي)", IRR, PCT1),
    ("إجمالي صافي التدفقات (5 سنوات)", TOTAL_CF, NUM),
    ("نقطة التعادل (إشغال)", BREAK_EVEN, PCT1),
]
r = 10
for label, val, fmt in metrics:
    put(p, r, 1, label, BOLD, LGREY)
    put(p, r, 2, val, BOLD, LGREY, fmt, CENTER)
    r += 1
p.column_dimensions["A"].width = 30
for col in "BCDEFG":
    p.column_dimensions[col].width = 12

# فرض إعادة الحساب عند الفتح في Excel (للنسخ التي تدعمه)
wb.calculation.fullCalcOnLoad = True

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "النموذج-المالي-بيلاتس.xlsx")
wb.save(out)

print("تم إنشاء الملف بقيَم محسوبة.")
print(f"  الطاقة الشهرية: {CAPACITY:,} | المصروف الشهري: {OPEX_MONTH:,.0f} | الاستثمار: {INVEST:,}")
print(f"  نقطة التعادل: {BREAK_EVEN:.1%} | NPV@15%: {NPV15:,.0f} | IRR: {IRR:.1%}")
print(f"  صافي السنة 2: {net_year[1]:,.0f} | صافي السنة 3: {net_year[2]:,.0f}")

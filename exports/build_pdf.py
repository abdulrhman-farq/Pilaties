# -*- coding: utf-8 -*-
"""
توليد نسخة PDF احترافية من دراسة الجدوى — استوديو Reformer Pilates الرياض.
يعالج النص العربي (تشكيل الحروف + اتجاه RTL) باستخدام arabic_reshaper + python-bidi،
ويستخدم خط Cairo. شغّل: python3 build_pdf.py
"""
import os
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, Image)

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
# يُسجَّل خط Amiri تحت الاسمين Cairo / Cairo-Bold لتبسيط الإشارات في الأنماط
pdfmetrics.registerFont(TTFont("Cairo", os.path.join(FONTS, "Amiri-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Cairo-Bold", os.path.join(FONTS, "Amiri-Bold.ttf")))

NAVY = colors.HexColor("#1F4E78")
TEAL = colors.HexColor("#2E8B8B")
LGREY = colors.HexColor("#D9E1F2")
GREEN = colors.HexColor("#C6EFCE")
RED = colors.HexColor("#FFC7CE")
GOLD = colors.HexColor("#FFF2CC")
DARK = colors.HexColor("#2C2C2C")


def ar(t):
    """تشكيل النص العربي وضبط اتجاهه للعرض الصحيح في PDF."""
    t = str(t).replace("≈", "~")  # خط Amiri لا يحتوي رمز التقريب ≈
    return get_display(arabic_reshaper.reshape(t))


# أنماط الفقرات
def style(name, size, font="Cairo", color=DARK, align=2, leading=None, space=4):
    return ParagraphStyle(name, fontName=font, fontSize=size, textColor=color,
                          alignment=align, leading=leading or size * 1.6,
                          spaceAfter=space, wordWrap="RTL")


H1 = style("H1", 20, "Cairo-Bold", NAVY, align=1, space=6)
H2 = style("H2", 14, "Cairo-Bold", colors.white, align=2)
SEC = style("SEC", 15, "Cairo-Bold", NAVY, align=2, space=8)
BODY = style("BODY", 10.5, "Cairo", DARK, align=2, leading=20)
BULLET = style("BULLET", 10.5, "Cairo", DARK, align=2, leading=19)
SMALL = style("SMALL", 8.5, "Cairo", colors.HexColor("#666666"), align=2)
CELL = style("CELL", 9.5, "Cairo", DARK, align=1, leading=15, space=0)
CELLB = style("CELLB", 9.5, "Cairo-Bold", DARK, align=1, leading=15, space=0)
CELLW = style("CELLW", 9.5, "Cairo-Bold", colors.white, align=1, leading=15, space=0)
COVERSUB = style("CS", 13, "Cairo", colors.white, align=1, space=2)


def P(t, s=BODY):
    return Paragraph(ar(t), s)


def section(t):
    tbl = Table([[Paragraph(ar(t), H2)]], colWidths=[17 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return tbl


def bullets(items):
    return [Paragraph(ar("•  " + x), BULLET) for x in items]


def mktable(rows, header=True, widths=None, body_color=None,
            zebra=True, highlight_rows=None):
    """rows: قائمة صفوف (كل صف قائمة نصوص). الصف الأول رأس."""
    highlight_rows = highlight_rows or {}
    data = []
    for r, row in enumerate(rows):
        cells = []
        for cell in row:
            if r == 0 and header:
                cells.append(Paragraph(ar(cell), CELLW))
            else:
                st = CELLB if (len(row) and cell == row[0] and len(rows[0]) > 2) else CELL
                cells.append(Paragraph(ar(cell), st))
        data.append(cells)
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    ts = [
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFBFBF")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        ts.append(("BACKGROUND", (0, 0), (-1, 0), TEAL))
    if zebra:
        for r in range(1, len(rows)):
            if r % 2 == 0:
                ts.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#F2F5FA")))
    for r, color in highlight_rows.items():
        ts.append(("BACKGROUND", (0, r), (-1, r), color))
    t.setStyle(TableStyle(ts))
    return t


# ============================================================
# المحتوى
# ============================================================
story = []
S = Spacer

# --- الغلاف ---
story.append(S(1, 4 * cm))
story.append(Paragraph(ar("دراسة جدوى اقتصادية"), H1))
story.append(S(1, 0.3 * cm))
story.append(Paragraph(ar("استوديو Reformer Pilates نسائي — الرياض"),
                       style("c2", 16, "Cairo-Bold", TEAL, align=1)))
story.append(S(1, 0.8 * cm))
cover = Table([[Paragraph(ar("وثيقة مُعدّة لعرضها على مستثمر / صندوق استثماري"),
                          style("cv", 12, "Cairo", colors.white, align=1))]],
              colWidths=[12 * cm])
cover.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY),
                           ("TOPPADDING", (0, 0), (-1, -1), 10),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
story.append(cover)
story.append(S(1, 0.6 * cm))
story.append(Paragraph(ar("120 م²  |  6 أجهزة Reformer  |  يونيو 2026"),
                       style("cv2", 11, "Cairo", DARK, align=1)))
story.append(S(1, 5 * cm))
story.append(Paragraph(ar("جميع الأرقام بالريال السعودي (SAR) — سعر الصرف 1 USD = 3.75 SAR"),
                       style("disc", 8.5, "Cairo", colors.HexColor("#666666"), align=1)))

story.append(PageBreak())

# --- الملخص التنفيذي ---
story.append(section("الملخص التنفيذي"))
story.append(S(1, 0.3 * cm))
exec_rows = [
    ["البند", "القيمة"],
    ["النشاط والموقع", "استوديو ريفورمر بيلاتس نسائي — الرياض"],
    ["المساحة / الإيجار السنوي", "120 م² / 204,000 ريال"],
    ["عدد الأجهزة", "6 أجهزة (قابلة للتوسعة إلى 8)"],
    ["إجمالي الاستثمار المطلوب", "≈ 275,000 ريال"],
    ["التكاليف التشغيلية الشهرية", "≈ 61,000 ريال"],
    ["نقطة التعادل", "≈ 37% إشغال (≈ 2.2 عميلة/حصة)"],
    ["فترة الاسترداد (إشغال 50%)", "≈ 13 شهر"],
    ["العائد على الاستثمار ROI (50%)", "≈ 91% سنوياً"],
    ["صافي القيمة الحالية NPV (5 سنوات @15%)", "≈ +653,000 ريال"],
    ["معدل العائد الداخلي IRR", "≈ 66%"],
    ["التوصية النهائية", "المشروع مجدٍ اقتصادياً بدرجة عالية — المضي قدماً"],
]
story.append(mktable(exec_rows, widths=[9 * cm, 8 * cm],
                     highlight_rows={11: GREEN}))
story.append(S(1, 0.5 * cm))
story.append(P("الخلاصة: رأسمال تأسيسي منخفض، هامش ربح تشغيلي مرتفع، ونقطة تعادل منخفضة (37%). المخاطرة الرئيسية ليست في حجم الاستثمار بل في سرعة اكتساب العميلات والاحتفاظ بهنّ وتقليل الاعتماد على مدربة بعينها."))
story.append(PageBreak())

# --- دراسة السوق ---
story.append(section("1) دراسة السوق"))
story.append(S(1, 0.3 * cm))
story.append(Paragraph(ar("حجم السوق ومؤشرات النمو"), SEC))
story.append(mktable([
    ["المؤشر", "القيمة"],
    ["سوق نوادي اللياقة في السعودية (2025)", "≈ 1.26–1.56 مليار دولار"],
    ["التوقع لعام 2030–2034", "≈ 2.8–3.0 مليار دولار"],
    ["نمو القطاع البوتيكي (CAGR)", "≈ 13.6% سنوياً"],
    ["نمو شريحة النساء (الأسرع)", "≈ 13.25% سنوياً"],
    ["مستهدف النشاط البدني (رؤية 2030)", "40% بحلول 2030"],
], widths=[10 * cm, 7 * cm]))
story.append(S(1, 0.4 * cm))
story.append(Paragraph(ar("الفجوة السوقية والفرصة"), SEC))
story.extend(bullets([
    "السوق منقسم بين فاخر جداً (>300 ريال/حصة) واقتصادي مزدحم — توجد فجوة لاستوديو بوتيكي راقٍ بسعر في المتناول (150 ريال).",
    "تجربة حميمية شبه شخصية (6 عميلات كحد أقصى) مقابل الأندية الكبيرة.",
    "تخصص نسائي كامل (خصوصية تامة) + تكامل مع ما بعد الولادة والعلاج الطبيعي.",
]))
story.append(S(1, 0.3 * cm))
story.append(Paragraph(ar("مقارنة الأسعار في الرياض"), SEC))
story.append(mktable([
    ["النموذج", "نطاق السوق", "تموضع المشروع"],
    ["الحصة المفردة", "175 – 375 ريال", "150 ريال"],
    ["باقة 8 حصص (سعر/حصة)", "150 – 250 ريال", "≈ 125 ريال"],
    ["اشتراك شهري غير محدود", "1,600 – 5,500 ريال", "≈ 1,600 ريال"],
], widths=[6 * cm, 6 * cm, 5 * cm]))
story.append(PageBreak())

# --- الدراسة الفنية ---
story.append(section("2) الدراسة الفنية"))
story.append(S(1, 0.3 * cm))
story.append(Paragraph(ar("توزيع المساحة (120 م²)"), SEC))
story.append(mktable([
    ["المنطقة", "المساحة"],
    ["استوديو التمرين (6 أجهزة + متسع لـ 8)", "65 م²"],
    ["استقبال + انتظار + متجر صغير", "14 م²"],
    ["غرف تبديل + خزائن", "14 م²"],
    ["دورات مياه + دش", "10 م²"],
    ["غرفة Props + مخزن", "7 م²"],
    ["مكتب المديرة", "6 م²"],
    ["ممرات وخدمات", "4 م²"],
    ["الإجمالي", "120 م²"],
], widths=[12 * cm, 5 * cm], highlight_rows={8: LGREY}))
story.append(S(1, 0.4 * cm))
story.append(Paragraph(ar("الطاقة الاستيعابية"), SEC))
story.append(mktable([
    ["المؤشر", "القيمة"],
    ["سعة الحصة", "6 عميلات"],
    ["عدد الحصص اليومية", "7 حصص"],
    ["الطاقة الشهرية القصوى", "1,092 حصة-عميلة"],
    ["الإيراد الشهري عند 100%", "163,800 ريال"],
], widths=[10 * cm, 7 * cm]))
story.append(S(1, 0.4 * cm))
story.append(Paragraph(ar("الطاقم المطلوب"), SEC))
story.append(mktable([
    ["الوظيفة", "العدد", "الراتب (ريال)"],
    ["مدرّبة رئيسية معتمدة", "1", "11,000"],
    ["مدرّبة ثانية", "1", "9,000"],
    ["موظفة استقبال", "1", "5,000"],
    ["عاملة نظافة (جزئي)", "1", "2,000"],
    ["الإجمالي", "4", "27,000"],
], widths=[8 * cm, 4 * cm, 5 * cm], highlight_rows={5: LGREY}))
story.append(PageBreak())

# --- مخطط الطابق والتوزيع ---
story.append(section("2-ب) مخطط الطابق والتوزيع (10م × 12م)"))
story.append(S(1, 0.3 * cm))
_fp = os.path.join(HERE, "charts", "floorplan.png")
if os.path.exists(_fp):
    story.append(Image(_fp, width=17 * cm, height=12.52 * cm))
story.append(S(1, 0.2 * cm))
story.append(P("وحدة زاوية بأول العمارة؛ المدخل من الفتحة الثانية (5م) مع جدار خصوصية منحنٍ والاستقبال خلفه. الأبعاد بالأمتار مدرجة لكل غرفة، وجدول المساحات يجمع على 120 م².", SMALL))
story.append(PageBreak())

# --- الدراسة المالية ---
story.append(section("3) الدراسة المالية"))
story.append(S(1, 0.3 * cm))
story.append(Paragraph(ar("التكلفة التأسيسية"), SEC))
story.append(mktable([
    ["البند", "القيمة (ريال)"],
    ["أجهزة Reformer مُورّدة (6 أجهزة)", "41,000"],
    ["أدوات مساعدة (Props)", "15,000"],
    ["ديكور وتجهيز داخلي وأثاث", "80,000"],
    ["لوحة وأنظمة تقنية وكاميرات", "15,000"],
    ["رخص وتراخيص", "15,000"],
    ["احتياطي طوارئ", "9,000"],
    ["رأس المال العامل", "100,000"],
    ["إجمالي الاستثمار المطلوب", "275,000"],
], widths=[11 * cm, 6 * cm], highlight_rows={8: GREEN}))
story.append(S(1, 0.4 * cm))
story.append(Paragraph(ar("التكاليف التشغيلية الشهرية"), SEC))
story.append(mktable([
    ["البند", "ريال/شهر"],
    ["الإيجار (204,000 ÷ 12)", "17,000"],
    ["رواتب + تأمينات", "29,200"],
    ["كهرباء وماء", "3,800"],
    ["نظام الحجز + اتصالات", "1,500"],
    ["التسويق", "5,000"],
    ["مستهلكات وصيانة وإداريات", "4,500"],
    ["الإجمالي الشهري", "61,000"],
], widths=[11 * cm, 6 * cm], highlight_rows={7: LGREY}))
story.append(PageBreak())

# --- سيناريوهات الإشغال ---
story.append(section("4) سيناريوهات الإشغال والمؤشرات المالية"))
story.append(S(1, 0.3 * cm))
story.append(Paragraph(ar("سيناريوهات الإشغال (سعر الحصة 150 ريال)"), SEC))
story.append(mktable([
    ["المؤشر", "30%", "50%", "70%", "90%"],
    ["الإيراد الشهري", "49,140", "81,900", "114,660", "147,420"],
    ["المصروف الشهري", "61,000", "61,000", "61,000", "61,000"],
    ["صافي الربح الشهري", "(11,860)", "20,900", "53,660", "86,420"],
    ["صافي الربح السنوي", "(142,320)", "250,800", "643,920", "1,037,040"],
    ["ROI سنوي", "سالب", "91%", "234%", "377%"],
    ["فترة الاسترداد", "—", "13 شهر", "5.1 شهر", "3.2 شهر"],
], widths=[5 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm],
    highlight_rows={3: GREEN, 4: GREEN}))
story.append(S(1, 0.3 * cm))
_sc = os.path.join(HERE, "charts", "scenarios.png")
if os.path.exists(_sc):
    story.append(Image(_sc, width=12 * cm, height=6.86 * cm))
story.append(S(1, 0.4 * cm))
story.append(Paragraph(ar("المؤشرات المالية الرئيسية"), SEC))
story.append(mktable([
    ["المؤشر", "القيمة"],
    ["نقطة التعادل", "≈ 37% إشغال (≈ 2.2 عميلة/حصة)"],
    ["NPV (5 سنوات @15%)", "≈ +653,000 ريال"],
    ["IRR (معدل العائد الداخلي)", "≈ 66%"],
    ["فترة الاسترداد (50%)", "≈ 13 شهر"],
    ["أرباح أول 3 سنوات", "≈ 665,000 ريال"],
], widths=[9 * cm, 8 * cm]))
story.append(S(1, 0.4 * cm))
story.append(Paragraph(ar("التوقعات المالية 5 سنوات (السيناريو المتوقع)"), SEC))
story.append(mktable([
    ["السنة", "الإشغال", "الإيراد", "صافي التدفق"],
    ["السنة 1", "38%", "746,928", "(15,072)"],
    ["السنة 2", "55%", "1,081,080", "327,080"],
    ["السنة 3", "63%", "1,238,328", "353,328"],
    ["السنة 4", "68%", "1,336,608", "425,608"],
    ["السنة 5", "70%", "1,375,920", "437,920"],
], widths=[4 * cm, 3.5 * cm, 5 * cm, 4.5 * cm]))
story.append(S(1, 0.4 * cm))
story.append(Paragraph(ar("تحليل الحساسية (Sensitivity) — متانة النموذج"), SEC))
story.append(mktable([
    ["الحالة", "التعادل", "صافي 50%/شهر", "NPV@15%", "IRR"],
    ["أ) الأساسي (سعر صافٍ 150)", "37%", "20,900", "≈653,000", "66%"],
    ["ب) + رسوم دفع + إهلاك", "38%", "18,970", "≈568,000", "60%"],
    ["ج) الأكثر تحفظاً (شامل الضريبة)", "44%", "8,450", "≈89,000", "23%"],
], widths=[5.5 * cm, 2.5 * cm, 3.5 * cm, 3 * cm, 2.5 * cm],
    highlight_rows={1: GREEN}))
story.append(S(1, 0.2 * cm))
story.append(P("القرار المعتمد: سعر القائمة ≈172.5 ريال شامل الضريبة (الصافي 150) — الحالة (أ). رسوم الدفع والإهلاك أثرهما طفيف؛ معالجة الضريبة هي المتغيّر الحاسم، والنموذج يبقى مجدياً حتى في الحالة الأكثر تحفظاً.", SMALL))
story.append(PageBreak())

# --- منحنى التدفق النقدي الشهري ---
story.append(section("4-ب) التدفق النقدي الشهري لسنة الإطلاق (Launch Runway)"))
story.append(S(1, 0.3 * cm))
_jc = os.path.join(HERE, "charts", "jcurve.png")
if os.path.exists(_jc):
    story.append(Image(_jc, width=16 * cm, height=8.2 * cm))
story.append(S(1, 0.2 * cm))
story.append(P("التدفق التشغيلي يتحوّل موجباً من الشهر السادس، والتراكمي من الشهر الثاني عشر. أعمق قاع نقدي ≈ -106,000 ريال (الشهر 5)، لذا يُوصى بتمويل 300,000 ريال (رأس مال عامل ≈ 120,000) لتجاوز أشهر الإطلاق بأمان.", BODY))
story.append(PageBreak())

# --- المخاطر ---
story.append(section("5) تحليل المخاطر"))
story.append(S(1, 0.3 * cm))
story.append(mktable([
    ["المخاطرة", "الأثر", "إجراء التخفيف"],
    ["المنافسة", "متوسط", "تموضع بوتيكي + ولاء للعلامة لا للسعر"],
    ["انخفاض الإشغال", "مرتفع", "نقطة تعادل منخفضة (37%) + إحالات + باقات"],
    ["ارتفاع الرواتب", "متوسط", "عقود سنوية + تدريب داخلي لإعداد مدربات"],
    ["ارتفاع الإيجار", "متوسط", "عقد طويل بسقف زيادة متفق عليه"],
    ["الاعتماد على مدربة محددة", "مرتفع", "تعدد المدربات + توثيق المنهجية + علامة قوية"],
], widths=[5 * cm, 3 * cm, 9 * cm]))
story.append(S(1, 0.5 * cm))

# --- التوصيات ---
story.append(section("6) التوصيات النهائية"))
story.append(S(1, 0.3 * cm))
story.extend(bullets([
    "هل المشروع مجدٍ؟ نعم بدرجة عالية — نقطة تعادل منخفضة، NPV موجبة كبيرة، وIRR استثنائي (66%).",
    "الحد الأدنى للربحية: تجاوز 37% إشغال (≈ 85 عميلة نشطة).",
    "أفضل سعر: 150 ريال للحصة المفردة + باقات واشتراكات لتعظيم الولاء والتدفق النقدي.",
    "ابدأ بـ 6 أجهزة، وأضف جهازين عند تجاوز 70% إشغال (المساحة تستوعب 8 بنفس الإيجار).",
    "السيولة: التدفق التراكمي يبلغ قاعه ≈ -106 ألف في الشهر 5؛ لذا التمويل 300 ألف (رأس مال عامل ~120 ألف) ضروري لتجاوز أشهر الإطلاق.",
    "أرباح أول 3 سنوات ≈ 665,000 ريال، مع استرداد رأس المال خلال السنة الثانية.",
]))
story.append(S(1, 0.4 * cm))
rec = Table([[Paragraph(ar("التوصية الاستثمارية النهائية: المضي قدماً (GO) — تمويل مقترح 300,000 ريال مع مراجعة أداء عند الشهر السادس."),
                        style("rec", 11, "Cairo-Bold", colors.white, align=1, leading=20))]],
            colWidths=[17 * cm])
rec.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), TEAL),
                         ("TOPPADDING", (0, 0), (-1, -1), 12),
                         ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                         ("LEFTPADDING", (0, 0), (-1, -1), 12),
                         ("RIGHTPADDING", (0, 0), (-1, -1), 12)]))
story.append(rec)
story.append(S(1, 0.6 * cm))
story.append(P("إخلاء مسؤولية: أرقام السوق تقديرية إرشادية مستندة إلى تقارير منشورة حتى منتصف 2026. الأرقام المالية مبنية على افتراضات موضّحة في الدراسة الكاملة وتتطلب تحديثاً عند تثبيت العقود الفعلية. يُنصح بمراجعة محاسب قانوني ومستشار ضريبي.", SMALL))


# ترقيم الصفحات + شريط علوي
def footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, A4[1] - 1.1 * cm, A4[0], 1.1 * cm, fill=1, stroke=0)
        canvas.setFont("Cairo", 8)
        canvas.setFillColor(colors.white)
        canvas.drawRightString(A4[0] - 1.5 * cm, A4[1] - 0.75 * cm,
                               ar("دراسة جدوى — استوديو ريفورمر بيلاتس الرياض"))
        canvas.setFillColor(colors.HexColor("#888888"))
        canvas.setFont("Cairo", 8)
        canvas.drawCentredString(A4[0] / 2, 0.8 * cm, ar(f"صفحة {doc.page}"))
    canvas.restoreState()


out = os.path.join(HERE, "دراسة-الجدوى-بيلاتس.pdf")
doc = SimpleDocTemplate(out, pagesize=A4, topMargin=1.6 * cm,
                        bottomMargin=1.4 * cm, leftMargin=2 * cm, rightMargin=2 * cm,
                        title="دراسة جدوى - استوديو ريفورمر بيلاتس الرياض")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("تم إنشاء:", out)

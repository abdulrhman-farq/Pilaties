# -*- coding: utf-8 -*-
"""
مخطط الطابق والتوزيع — استوديو Reformer Pilates نسائي، الرياض.
الأبعاد: 10م واجهة (شارع) × 12م عمق = 120 م² | وحدة زاوية | مدخل من الفتحة الثانية
مع جدار خصوصية منحنٍ والاستقبال خلفه. شغّل: python3 build_floorplan.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
from matplotlib import font_manager
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display

HERE = os.path.dirname(os.path.abspath(__file__))
for f in ["Amiri-Regular.ttf", "Amiri-Bold.ttf"]:
    font_manager.fontManager.addfont(os.path.join(HERE, "fonts", f))
plt.rcParams["font.family"] = "Amiri"
plt.rcParams["axes.unicode_minus"] = False

NAVY = "#1F4E78"; TEAL = "#2E8B8B"; GOLD = "#C9A227"
WALL = "#222222"; GLASS = "#3FA7D6"; ROOM = "#EAF0F7"; STUDIO = "#E7F3F1"


def ar(t):
    return get_display(arabic_reshaper.reshape(str(t).replace("≈", "~").replace("²", "م2")))


def lbl(ax, x, y, t, s=12, c="#222", b=False):
    ax.text(x, y, ar(t), ha="center", va="center", fontsize=s,
            color=c, fontweight=("bold" if b else "normal"), zorder=6)


def dim(ax, x, y, t):
    ax.text(x, y, ar(t), ha="center", va="center", fontsize=9,
            color="#7a7a7a", style="italic", zorder=6)


def room(ax, x0, y0, x1, y1, fc=ROOM):
    ax.add_patch(mp.Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=fc,
                              edgecolor=WALL, lw=1.6, zorder=2))


fig = plt.figure(figsize=(16.5, 11.7))  # A3 landscape
ax = fig.add_axes([0.04, 0.06, 0.62, 0.88])
ax.set_xlim(-1.2, 11.2); ax.set_ylim(-1.6, 13.2)
ax.set_aspect("equal"); ax.axis("off")

# ===== الجدران الخارجية =====
ax.add_patch(mp.Rectangle((0, 0), 10, 12, facecolor="white",
                          edgecolor=WALL, lw=3.5, zorder=1))

# ===== الغرف والتوزيع =====
# استوديو التمرين (الخلف)
room(ax, 0, 6, 10, 12, STUDIO)
lbl(ax, 5, 11.5, "استوديو التمرين (Reformer Studio)", 14, NAVY, True)
lbl(ax, 5, 11.05, "60 م²", 12, NAVY)
dim(ax, 5, 10.65, "10.0 × 6.0 م")

# الكتلة اليسرى (خدمات رطبة)
room(ax, 0, 0, 3.5, 2.2)         # دورات مياه + دش
lbl(ax, 1.75, 1.2, "دورات مياه + دش\n8 م²", 11)
dim(ax, 1.75, 0.55, "3.5 × 2.2 م")
room(ax, 0, 2.2, 3.5, 6)         # تبديل + خزائن
lbl(ax, 1.75, 4.2, "تبديل الملابس\n+ خزائن (Lockers)\n13 م²", 11)
dim(ax, 1.75, 3.3, "3.5 × 3.8 م")

# الكتلة الوسطى
room(ax, 3.5, 0, 6.5, 2)         # غرفة الأدوات
lbl(ax, 5.0, 1.15, "غرفة الأدوات Props · 6 م²", 10)
dim(ax, 5.0, 0.6, "3.0 × 2.0 م")
room(ax, 3.5, 2, 6.5, 3.8)       # مكتب المديرة
lbl(ax, 5.0, 3.0, "مكتب المديرة · 5 م²", 10)
dim(ax, 5.0, 2.5, "3.0 × 1.8 م")
room(ax, 3.5, 3.8, 6.5, 6)       # ركن التعافي
lbl(ax, 5.0, 5.05, "ركن التعافي (Recovery) · 7 م²", 10, TEAL, True)
dim(ax, 5.0, 4.45, "3.0 × 2.2 م")

# الكتلة اليمنى (مدخل + استقبال + انتظار)
room(ax, 6.5, 0, 10, 6, "#F3F7FB")
lbl(ax, 8.25, 5.5, "المدخل + الاستقبال + الانتظار · 21 م²", 10, NAVY, True)
dim(ax, 8.25, 5.1, "3.5 × 6.0 م")

# ===== الواجهة الأمامية (شارع) — فتحتان 5م =====
# زجاج واجهة: فتحة أولى 0–5، فتحة ثانية 5–10 (المدخل)
ax.plot([0.2, 4.8], [0, 0], color=GLASS, lw=6, solid_capstyle="butt", zorder=4)
ax.plot([5.2, 6.9], [0, 0], color=GLASS, lw=6, solid_capstyle="butt", zorder=4)
ax.plot([8.6, 9.8], [0, 0], color=GLASS, lw=6, solid_capstyle="butt", zorder=4)
lbl(ax, 2.5, -0.55, "الفتحة الأولى (5م) — واجهة زجاجية معتمة", 10, GLASS)
lbl(ax, 7.6, -0.95, "الفتحة الثانية (5م) — المدخل", 10.5, NAVY, True)

# باب المدخل (في الفتحة الثانية) مع حركة الفتح
ax.plot([6.9, 8.6], [0, 0], color="white", lw=7, zorder=4)   # فتحة الباب
ax.plot([6.9, 6.9], [0, 1.5], color=NAVY, lw=2.2, zorder=5)  # ورقة الباب
ax.add_patch(mp.Arc((6.9, 0), 3.0, 3.0, angle=0, theta1=0, theta2=58,
                    color=NAVY, lw=1.0, ls="--", zorder=5))
lbl(ax, 7.75, 0.35, "باب", 9, NAVY)

# ===== الواجهة الجانبية (الزاوية) =====
ax.plot([10, 10], [0.3, 5.6], color=GLASS, lw=5, solid_capstyle="butt", zorder=4)
ax.text(10.75, 3, ar("واجهة جانبية (زاوية العمارة)"), ha="center", va="center",
        rotation=90, fontsize=10, color=GLASS)

# ===== جدار الخصوصية المنحني + الاستقبال =====
# جدار منحنٍ أمام الباب مباشرة لحجب الرؤية للداخل
arc = mp.Arc((8.4, 1.3), 3.4, 3.4, angle=0, theta1=95, theta2=210,
             color="#B0413E", lw=7, zorder=6)
ax.add_patch(arc)
lbl(ax, 6.7, 1.5, "جدار خصوصية\nمنحنٍ", 10, "#B0413E", True)
# مكتب الاستقبال خلف الجدار المنحني
ax.add_patch(mp.FancyBboxPatch((7.5, 2.6), 2.0, 0.8,
             boxstyle="round,pad=0.02,rounding_size=0.1",
             facecolor=GOLD, edgecolor=WALL, lw=1.4, zorder=6))
lbl(ax, 8.5, 3.0, "الاستقبال", 10, "white", True)
# كراسي انتظار
for cx in (8.6, 9.3):
    ax.add_patch(mp.Circle((cx, 4.4), 0.28, facecolor="#ccd6e0",
                           edgecolor=WALL, lw=1, zorder=6))
lbl(ax, 8.9, 4.95, "انتظار", 9, "#555")

# ===== أجهزة Reformer (6) =====
def reformer(cx, cy):
    ax.add_patch(mp.FancyBboxPatch((cx - 1.1, cy - 0.38), 2.2, 0.76,
                 boxstyle="round,pad=0.02,rounding_size=0.12",
                 facecolor="#D7E9E5", edgecolor=TEAL, lw=1.8, zorder=5))
    ax.add_patch(mp.Rectangle((cx - 0.95, cy - 0.22), 0.5, 0.44,
                 facecolor=TEAL, alpha=0.6, edgecolor="none", zorder=5))


for ry in (7.3, 9.8):
    for rx in (2.1, 5.0, 7.9):
        reformer(rx, ry)
lbl(ax, 5, 6.45, "6 أجهزة Reformer (قابلة للتوسعة إلى 8) — ممرات أمان بين الأجهزة", 10, TEAL)

# ===== أبعاد القياس =====
# عرض 10م (واجهة)
ax.annotate("", xy=(0, 12.7), xytext=(10, 12.7),
            arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.6))
lbl(ax, 5, 13.0, "10 م (واجهة الشارع)", 12, NAVY, True)
# عمق 12م
ax.annotate("", xy=(-0.9, 0), xytext=(-0.9, 12),
            arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.6))
ax.text(-1.15, 6, ar("12 م (العمق)"), ha="center", va="center",
        rotation=90, fontsize=12, color=NAVY, fontweight="bold")
# منتصف الواجهة (فتحتان 5م)
ax.plot([5, 5], [-0.2, 0.2], color="#999", lw=1)
lbl(ax, 5, -1.35, "الواجهة = فتحتان × 5 م  |  المساحة الإجمالية = 120 م²", 11, "#444", True)

# سهم الشمال + مقياس
ax.annotate(ar("شمال"), xy=(0.4, 12.0), xytext=(0.4, 13.0),
            ha="center", fontsize=9, color="#333",
            arrowprops=dict(arrowstyle="->", color="#333", lw=1.4))
ax.plot([7.5, 9.5], [-1.35, -1.35], color="#333", lw=2)
for xx in (7.5, 8.5, 9.5):
    ax.plot([xx, xx], [-1.45, -1.25], color="#333", lw=1)
lbl(ax, 8.5, -1.62, "مقياس: 2 م", 8.5, "#333")

ax.set_title(ar("مخطط الطابق والتوزيع — استوديو Reformer Pilates نسائي · الرياض"),
             fontsize=16, color=NAVY, fontweight="bold", pad=14)

# ===== لوحة جانبية: جدول المساحات + ملاحظات =====
ax2 = fig.add_axes([0.68, 0.06, 0.30, 0.88]); ax2.axis("off")
ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
ax2.add_patch(mp.Rectangle((0, 0.62), 1, 0.36, facecolor="#F3F7FB",
                           edgecolor=NAVY, lw=1.4))
ax2.text(0.5, 0.95, ar("جدول المساحات"), ha="center", fontsize=14,
         color=NAVY, fontweight="bold")
areas = [("استوديو التمرين (6 أجهزة)", "60"),
         ("المدخل + الاستقبال + الانتظار", "21"),
         ("تبديل الملابس + خزائن", "13"),
         ("دورات مياه + دش", "8"),
         ("ركن التعافي (Recovery)", "7"),
         ("غرفة الأدوات (Props)", "6"),
         ("مكتب المديرة", "5"),
         ("الإجمالي", "120")]
y = 0.90
for name, a in areas:
    bold = name == "الإجمالي"
    if bold:
        ax2.add_patch(mp.Rectangle((0.02, y - 0.018), 0.96, 0.035,
                                   facecolor=TEAL, alpha=0.25, edgecolor="none"))
    ax2.text(0.96, y, ar(name), ha="right", fontsize=11,
             fontweight=("bold" if bold else "normal"))
    ax2.text(0.10, y, ar(a + " م2"), ha="left", fontsize=11,
             fontweight=("bold" if bold else "normal"), color=NAVY)
    y -= 0.042

# ملاحظات المفهوم
ax2.text(0.96, 0.52, ar("مفاهيم التصميم"), ha="right", fontsize=13,
         color=NAVY, fontweight="bold")
notes = [
    "وحدة زاوية بأول العمارة (واجهتان: شارع + جانب).",
    "المدخل من الفتحة الثانية (الـ5م الأخرى).",
    "جدار منحنٍ للخصوصية فور الدخول يحجب",
    "   رؤية الاستوديو من الشارع.",
    "الاستقبال خلف الجدار المنحني مباشرة.",
    "واجهة زجاجية معتمة (خصوصية نسائية تامة).",
    "أجهزة Reformer في الخلف مع ممرات أمان.",
    "كتلة الخدمات الرطبة (تبديل/دش/مياه) يساراً.",
    "ركن التعافي يفصل الخدمات عن الاستوديو.",
]
yy = 0.47
for n in notes:
    ax2.text(0.97, yy, ar("• " + n), ha="right", fontsize=10.5, color="#333")
    yy -= 0.038

ax2.text(0.5, 0.04, ar("الإيجار السنوي 204,000 ريال · يونيو 2026"),
         ha="center", fontsize=9, color="#777")

out_pdf = os.path.join(HERE, "مخطط-الطابق-بيلاتس.pdf")
with PdfPages(out_pdf) as pdf:
    pdf.savefig(fig, dpi=200)
fig.savefig(os.path.join(HERE, "charts", "floorplan.png"), dpi=130, bbox_inches="tight")
plt.close(fig)
print("تم إنشاء:", out_pdf)

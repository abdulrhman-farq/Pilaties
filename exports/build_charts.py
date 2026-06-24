# -*- coding: utf-8 -*-
"""
توليد الرسوم البيانية للدراسة (PNG) — استوديو Reformer Pilates الرياض.
يستخدم خط Amiri مع تشكيل عربي صحيح. شغّل: python3 build_charts.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import arabic_reshaper
from bidi.algorithm import get_display

HERE = os.path.dirname(os.path.abspath(__file__))
CHARTS = os.path.join(HERE, "charts")
os.makedirs(CHARTS, exist_ok=True)

# تسجيل خط Amiri
for f in ["Amiri-Regular.ttf", "Amiri-Bold.ttf"]:
    font_manager.fontManager.addfont(os.path.join(HERE, "fonts", f))
plt.rcParams["font.family"] = "Amiri"
plt.rcParams["axes.unicode_minus"] = False

NAVY = "#1F4E78"
TEAL = "#2E8B8B"
GOLD = "#C9A227"
RED = "#C0392B"
GREEN = "#27AE60"


def ar(t):
    t = str(t).replace("≈", "~")  # خط Amiri لا يحتوي رمز ≈
    return get_display(arabic_reshaper.reshape(t))


# ===== 1) منحنى التدفق النقدي الشهري لسنة الإطلاق (J-Curve) =====
months = list(range(1, 13))
monthly = [-43240, -36688, -15136, -8584, -2032, 4520,
           7796, 11072, 14348, 20900, 24176, 29090]
cumulative = []
c = 0
for m in monthly:
    c += m
    cumulative.append(c)

fig, ax1 = plt.subplots(figsize=(9, 4.6))
bars = ax1.bar(months, monthly, color=[RED if v < 0 else GREEN for v in monthly],
               alpha=0.55, width=0.6, label=ar("التدفق التشغيلي الشهري"))
ax1.axhline(0, color="#888", lw=0.8)
ax1.set_ylabel(ar("التدفق الشهري (ريال)"), fontsize=11)
ax1.set_xlabel(ar("الشهر"), fontsize=11)
ax1.set_xticks(months)

ax2 = ax1.twinx()
ax2.plot(months, cumulative, color=NAVY, lw=2.6, marker="o",
         markersize=5, label=ar("التدفق التراكمي"))
ax2.axhline(-100000, color=GOLD, ls="--", lw=1.6,
            label=ar("رأس المال العامل 100 ألف"))
# تمييز القاع
trough_i = cumulative.index(min(cumulative))
ax2.annotate(ar("القاع ≈ -105,680"),
             xy=(months[trough_i], cumulative[trough_i]),
             xytext=(months[trough_i] + 0.3, cumulative[trough_i] - 26000),
             fontsize=10, color=RED,
             arrowprops=dict(arrowstyle="->", color=RED))
ax2.set_ylabel(ar("التدفق التراكمي (ريال)"), fontsize=11)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="lower right", fontsize=9)
plt.title(ar("منحنى التدفق النقدي الشهري لسنة الإطلاق (Launch Runway)"),
          fontsize=13, color=NAVY, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "jcurve.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

# ===== 2) سيناريوهات صافي الربح السنوي =====
scen = ["30%", "50%", "70%", "90%"]
net_y = [-142320, 250800, 643920, 1037040]
fig, ax = plt.subplots(figsize=(7, 4))
b = ax.bar([ar(s) for s in scen], net_y,
           color=[RED if v < 0 else TEAL for v in net_y], width=0.6)
ax.axhline(0, color="#888", lw=0.8)
ax.set_ylabel(ar("صافي الربح السنوي (ريال)"), fontsize=11)
ax.set_xlabel(ar("نسبة الإشغال"), fontsize=11)
for rect, v in zip(b, net_y):
    ax.text(rect.get_x() + rect.get_width() / 2,
            v + (30000 if v > 0 else -55000),
            f"{v:,}", ha="center", fontsize=9,
            color=(GREEN if v > 0 else RED))
plt.title(ar("صافي الربح السنوي حسب الإشغال (سعر 150)"),
          fontsize=12, color=NAVY, pad=10)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "scenarios.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

print("تم إنشاء الرسوم:", os.listdir(CHARTS))

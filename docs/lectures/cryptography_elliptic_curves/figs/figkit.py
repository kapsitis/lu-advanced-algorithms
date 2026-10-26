# -*- coding: utf-8 -*-
"""Kopīgas Matplotlib palīgfunkcijas šīs lekcijas attēlu skriptiem.

Katrs attēlu skripts izsauc main(build, "vards.svg"), kur build() atgriež Matplotlib
figūru. Uzrakstu valodu izvēlas komandrindā (kā ../../cryptography_aes_and_hashing/figs):

    python dh_cycle.py              # abas valodas: dh-cycle-z23.svg un dh-cycle-z23.en.svg
    python dh_cycle.py --lang en    # tikai angļu: dh-cycle-z23.en.svg
    python dh_cycle.py --lang lv    # tikai latviešu: dh-cycle-z23.svg

Latviešu un angļu uzraksti attēlu skriptos ir pierakstīti kā T("latviski", "in English").
"""

import argparse
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

matplotlib.rcParams.update({
    "svg.fonttype": "none",            # teksts paliek tekstā (mazāks fails, var meklēt)
    "svg.hashsalt": "ecc-lecture",     # stabili ID -- git diff nemainās bez vajadzības
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "mathtext.fontset": "dejavusans",
})

BLUE, ORANGE, GREEN, PURPLE, RED, TEAL, GREY = (
    "#4C78A8", "#F58518", "#54A24B", "#B279A2", "#E45756", "#72B7B2", "#7f7f7f")
L_BLUE, L_ORANGE, L_GREEN, L_PURPLE, L_RED, L_TEAL, L_GREY = (
    "#dbe6f3", "#fde5cc", "#dcecd8", "#ecdcea", "#f9dcdc", "#dcefee", "#f1f3f5")

LANG = "lv"                            # uzrakstu valoda: "lv" vai "en" (sk. main)


def T(lv, en):
    """Uzraksts izvēlētajā valodā LANG."""
    return en if LANG == "en" else lv


def svg_name(name, lang):
    return name if lang == "lv" else name[:-4] + ".en.svg"


def main(build, name):
    global LANG
    ap = argparse.ArgumentParser(description="Ģenerē " + name)
    ap.add_argument("--lang", choices=["lv", "en", "both"], default="both",
                    help="uzrakstu valoda (noklusējums: abas)")
    ap.add_argument("--outdir", default=os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args()
    for lang in (["lv", "en"] if args.lang == "both" else [args.lang]):
        LANG = lang
        fig = build()
        out = os.path.join(args.outdir, svg_name(name, lang))
        fig.savefig(out, format="svg", bbox_inches="tight", metadata={"Date": None})
        plt.close(fig)
        print("->", out)

# -*- coding: utf-8 -*-
"""Ģenerē tls13-ecdhe.svg -- TLS 1.3 pilnais (1-RTT) rokasspiediens ar ECDHE (RFC 8446, 2. nodaļa).

Klients paplašinājumā key_share sūta A = aG, serveris -- B = bG. Sānos atzīmēts brīdis,
kad katra puse zina kopīgo noslēpumu abG; {...} -- šifrēts ar rokasspiediena atslēgām,
[...] -- ar lietotnes datu atslēgām. Pa vidu -- ko redz pasīvs noklausītājs.

    python tls13_ecdhe.py [--lang lv|en|both]
"""

import figkit as K
from figkit import T, plt
from matplotlib.patches import FancyBboxPatch


def build():
    fig, ax = plt.subplots(figsize=(10.5, 7.4))
    ax.axis("off")
    xc, xs, top = 0.0, 6.0, 0.0
    msgs = [
        (1, "ClientHello", T("key_share: $A = aG$ (+ nejaušs skaitlis, šifri)",
                             "key_share: $A = aG$ (+ random, cipher suites)"), "plain"),
        (-1, "ServerHello", T("key_share: $B = bG$ (+ izvēlētais šifrs)",
                              "key_share: $B = bG$ (+ chosen cipher suite)"), "plain"),
        (-1, "{EncryptedExtensions}", "", "hs"),
        (-1, "{Certificate}", T("servera sertifikātu ķēde", "server certificate chain"), "hs"),
        (-1, "{CertificateVerify}", T("ECDSA paraksts kopsavilkumam", "ECDSA signature of transcript"), "hs"),
        (-1, "{Finished}", "HMAC", "hs"),
        (1, "{Finished}", "HMAC", "hs"),
        (0, "[Application Data]", "AES-GCM", "app"),
    ]
    dy = 0.9
    yend = top - dy * (len(msgs) + 0.3)
    for x, who in [(xc, T("Klients", "Client")), (xs, T("Serveris", "Server"))]:
        ax.add_patch(FancyBboxPatch((x - 0.8, top + 0.35), 1.6, 0.55, boxstyle="round,pad=0.05",
                                    fc=K.L_GREY, ec="#5a6a7a"))
        ax.text(x, top + 0.62, who, ha="center", va="center", fontsize=12.5, weight="bold")
        ax.plot([x, x], [top + 0.33, yend], color="#9aa5b1", lw=1.3, ls=(0, (4, 4)))
    colors = {"plain": "#333", "hs": K.TEAL, "app": K.GREEN}
    for i, (d, name, note, kind) in enumerate(msgs):
        y = top - dy * (i + 0.6)
        col = colors[kind]
        if d == 0:
            ax.annotate("", xy=(xs - 0.05, y), xytext=(xc + 0.05, y),
                        arrowprops=dict(arrowstyle="<|-|>", color=col, lw=1.8))
        else:
            a, b = (xc, xs) if d == 1 else (xs, xc)
            ax.annotate("", xy=(b - 0.05 * d, y), xytext=(a + 0.05 * d, y),
                        arrowprops=dict(arrowstyle="-|>", color=col, lw=1.8))
        ax.text(3.0, y + 0.12, name, ha="center", va="bottom", fontsize=11.5, family="DejaVu Sans Mono",
                color=col, weight="bold")
        if note:
            ax.text(3.0, y - 0.1, note, ha="center", va="top", fontsize=9.5, color="#444")

    # kad katra puse zina abG
    ys = top - dy * 1.15
    ax.add_patch(FancyBboxPatch((xs + 0.25, ys - 0.32), 3.6, 0.66, boxstyle="round,pad=0.05",
                                fc=K.L_ORANGE, ec=K.ORANGE))
    ax.text(xs + 2.05, ys + 0.01, T("serveris: $abG = b \\cdot A$\n(pirms ServerHello sūtīšanas)",
                                   "server: $abG = b \\cdot A$\n(before sending ServerHello)"),
            ha="center", va="center", fontsize=10)
    yc = top - dy * 2.0
    ax.add_patch(FancyBboxPatch((xc - 3.85, yc - 0.32), 3.6, 0.66, boxstyle="round,pad=0.05",
                                fc=K.L_ORANGE, ec=K.ORANGE))
    ax.text(xc - 2.05, yc + 0.01, T("klients: $abG = a \\cdot B$\n(pēc ServerHello saņemšanas)",
                                   "client: $abG = a \\cdot B$\n(after receiving ServerHello)"),
            ha="center", va="center", fontsize=10)
    ax.text(xs + 2.05, top - dy * 2.4, T("$abG$ x koordināte → HKDF\n→ rokasspiediena atslēgas",
                                        "x coordinate of $abG$ → HKDF\n→ handshake keys"),
            ha="center", va="top", fontsize=9.5, color="#444")

    # noklausītājs
    ax.add_patch(FancyBboxPatch((xc - 3.85, yend - 1.05), 13.7, 0.72, boxstyle="round,pad=0.05",
                                fc=K.L_RED, ec=K.RED))
    ax.text(3.0, yend - 0.69, T("Noklausītājs redz $A = aG$ un $B = bG$, bet lai atrastu $abG$, jāatrisina "
                                "ECDH problēma (piemēram, ar ECDLP);\n"
                                "{...} šifrēts ar rokasspiediena atslēgām, [...] – ar lietotnes datu atslēgām",
                                "An eavesdropper sees $A = aG$ and $B = bG$; to get $abG$ it must solve "
                                "the ECDH problem (e.g. via ECDLP);\n"
                                "{...} encrypted with handshake keys, [...] with application traffic keys"),
            ha="center", va="center", fontsize=10)
    ax.set_xlim(-4.0, 10.0)
    ax.set_ylim(yend - 1.2, top + 1.0)
    ax.set_title(T("TLS 1.3 rokasspiediens ar ECDHE (1-RTT)", "TLS 1.3 handshake with ECDHE (1-RTT)"),
                 fontsize=13.5)
    return fig


if __name__ == "__main__":
    K.main(build, "tls13-ecdhe.svg")

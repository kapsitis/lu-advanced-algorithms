# -*- coding: utf-8 -*-
"""Ģenerē certificate-chain.svg -- TLS sertifikāta dzīves cikls.

Augšējā rindā -- izsniegšana: (1) atslēgu pāris, (2) CSR, (3) CA pārbauda domēna
kontroli, (4) starpniek-CA paraksta sertifikātu. Apakšējā rindā -- pārbaude:
(5) serveris sūta ķēdi "servera sertifikāts + starpniek-CA", (6) pārlūks to pārbauda
līdz saknes sertifikātam savā uzticamo sertifikātu krātuvē.

    python cert_chain.py [--lang lv|en|both]
"""

import figkit as K
from figkit import T, plt
from matplotlib.patches import FancyBboxPatch


def box(ax, x, y, w, h, head, lines, fc, ec, num=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06", fc=fc, ec=ec, lw=1.5))
    ax.text(x + w / 2, y + h - 0.22, head, ha="center", va="top", fontsize=11, weight="bold")
    for i, ln in enumerate(lines):
        ax.text(x + 0.15, y + h - 0.68 - 0.34 * i, ln, ha="left", va="top", fontsize=9.3, color="#333")
    if num is not None:
        ax.add_patch(plt.Circle((x + 0.05, y + h + 0.02), 0.2, fc=ec, ec="white", lw=1.2, zorder=5))
        ax.text(x + 0.05, y + h + 0.02, str(num), ha="center", va="center", color="white", fontsize=10,
                weight="bold", zorder=6)


def arrow(ax, a, b, col="#444", text=None, off=(0, 0.12), style="-|>", ls="-"):
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle=style, color=col, lw=1.6, ls=ls,
                                                    mutation_scale=13))
    if text:
        ax.text((a[0] + b[0]) / 2 + off[0], (a[1] + b[1]) / 2 + off[1], text, ha="center", va="bottom",
                fontsize=9, color=col)


def build():
    fig, ax = plt.subplots(figsize=(13, 6.6))
    ax.axis("off")
    W, H = 3.0, 2.1
    yt, yb = 3.3, 0.0
    # --- izsniegšana --------------------------------------------------------
    box(ax, 0, yt, W, H, T("Atslēgu pāris", "Key pair"),
        [T("privātā atslēga $d$ (paliek", "private key $d$ (stays"),
         T("serverī: server.key)", "on the server: server.key)"),
         T("publiskā $Q = dG$ (P-256)", "public $Q = dG$ (P-256)")], K.L_GREY, "#5a6a7a", 1)
    box(ax, 3.6, yt, W, H, "CSR (PKCS #10)",
        [T("subjekts: CN, SAN = domēni", "subject: CN, SAN = domains"),
         T("publiskā atslēga $Q$", "public key $Q$"),
         T("parakstīts ar $d$ (pierāda,", "signed with $d$ (proves"),
         T("ka $d$ ir pieprasītājam)", "the requester holds $d$)")], K.L_BLUE, K.BLUE, 2)
    box(ax, 7.2, yt, W, H, T("CA pārbauda domēnu", "CA validates domain"),
        ["ACME (RFC 8555):",
         T("HTTP-01: fails /.well-known/...", "HTTP-01: file /.well-known/..."),
         T("DNS-01: TXT ieraksts", "DNS-01: TXT record"),
         T("+ CT žurnālu ieraksti", "+ CT log entries")], K.L_PURPLE, K.PURPLE, 3)
    box(ax, 10.8, yt, W, H, T("Sertifikāts (X.509)", "Certificate (X.509)"),
        [T("subjekts, $Q$, izdevējs,", "subject, $Q$, issuer,"),
         T("derīgs no/līdz, paplašinājumi", "validity, extensions"),
         T("+ starpniek-CA paraksts", "+ intermediate CA signature"),
         "server.crt (PEM / DER)"], K.L_GREEN, K.GREEN, 4)
    for x in (3.0, 6.6, 10.2):
        arrow(ax, (x + 0.08, yt + H / 2), (x + 0.52, yt + H / 2))

    # --- ķēde un pārbaude ------------------------------------------------------
    cw, ch = 3.0, 1.35
    chain = [(0.0, T("Servera sertifikāts", "Server certificate"), "CN=www.example.lv", K.L_GREEN, K.GREEN),
             (4.4, T("Starpniek-CA", "Intermediate CA"), T("CN=Piemēra starpniek-CA", "CN=Example Intermediate CA"), K.L_ORANGE, K.ORANGE),
             (8.8, T("Saknes CA", "Root CA"), T("CN=Piemēra saknes CA", "CN=Example Root CA"), K.L_RED, K.RED)]
    for x, head, cn, fc, ec in chain:
        ax.add_patch(FancyBboxPatch((x, yb + 0.5), cw, ch, boxstyle="round,pad=0.06", fc=fc, ec=ec, lw=1.5))
        ax.text(x + cw / 2, yb + 0.5 + ch - 0.2, head, ha="center", va="top", fontsize=11, weight="bold")
        ax.text(x + cw / 2, yb + 0.5 + ch - 0.66, cn, ha="center", va="top", fontsize=8.3,
                family="DejaVu Sans Mono", color="#333")
    for x in (3.08, 7.48):
        arrow(ax, (x + 1.3, yb + 0.5 + ch / 2), (x, yb + 0.5 + ch / 2), "#333",
              T("paraksta", "signs"))
    ax.add_patch(FancyBboxPatch((-0.15, yb + 0.25), 7.75, 1.9, boxstyle="round,pad=0.06", fc="none",
                                ec=K.TEAL, lw=1.4, ls=(0, (5, 3))))
    ax.text(3.7, yb + 0.02, T("serveris sūta ziņojumā Certificate", "sent by the server in Certificate"),
            ha="center", va="top", fontsize=9.5, color=K.TEAL, weight="bold")
    ax.add_patch(FancyBboxPatch((8.65, yb + 0.25), 3.3, 1.9, boxstyle="round,pad=0.06", fc="none",
                                ec=K.RED, lw=1.4, ls=(0, (5, 3))))
    ax.text(10.3, yb + 0.02, T("jau ir pārlūka / OS krātuvē", "already in browser / OS trust store"),
            ha="center", va="top", fontsize=9.5, color=K.RED, weight="bold")
    for num, x in [(5, -0.15), (6, 8.65)]:
        ax.add_patch(plt.Circle((x, yb + 2.15), 0.2, fc=K.TEAL if num == 5 else K.RED, ec="white", lw=1.2,
                                zorder=5))
        ax.text(x, yb + 2.15, str(num), ha="center", va="center", color="white", fontsize=10, weight="bold",
                zorder=6)
    arrow(ax, (12.3, yt - 0.1), (1.5, yb + 1.95), K.GREEN, None, ls="--")
    ax.text(12.5, yb + 1.0, T("Pārlūks pārbauda:\n• katru parakstu ķēdē\n• vārdu (SAN)\n"
                              "• derīguma termiņu\n• CT apliecinājumus\n• (atsaukšanu)",
                              "The browser checks:\n• every signature\n• the name (SAN)\n"
                              "• validity period\n• CT proofs (SCTs)\n• (revocation)"),
            ha="left", va="center", fontsize=9.5, color="#333")
    ax.set_xlim(-0.4, 14.6)
    ax.set_ylim(-0.5, yt + H + 0.5)
    ax.set_title(T("TLS sertifikāta izsniegšana (1–4) un pārbaude (5–6)",
                   "Issuing (1–4) and verifying (5–6) a TLS certificate"), fontsize=13.5)
    return fig


if __name__ == "__main__":
    K.main(build, "certificate-chain.svg")

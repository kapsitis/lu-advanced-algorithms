# -*- coding: utf-8 -*-
"""MP3 un Opus salīdzinājums uz sintētiska 8 sekunžu mūzikas parauga.

Skripts
1. sintezē stereo signālu (48 kHz):
     0.0-3.0 s  akordi (harmonikas ar dziestošu apvalku) -- toņu signāls;
     3.0-5.5 s  tie paši akordi + "hi-hat" troksnis + asi klikšķi -- plats spektrs, pārejas;
     5.5-7.0 s  viens kluss 1 kHz tonis;
     7.0-8.0 s  klusums;
2. saglabā to FLAC formātā (bezzudumu atsauce) un nokodē ar ffmpeg (libmp3lame, libopus):
     MP3 128 kbit/s CBR, MP3 VBR (-q:a 5), MP3 64 kbit/s CBR,
     Opus 64 kbit/s VBR, Opus 64 kbit/s CBR, Opus 32 kbit/s VBR;
3. no ffprobe pakešu izmēriem uzzīmē bitu ātrumu laika gaitā (audio-bitrate.svg),
   atkodē visus failus un uzzīmē vidējo spektru trokšņainajā daļā (audio-spectrum.svg)
   un viļņa formu ap vienu klikšķi (audio-preecho.svg; atkodētos signālus
   izlīdzina ar kroskorelāciju);
4. izdrukā Markdown tabulu (faili, izmēri, vidējais bitu ātrums).

Vajadzīgs ffmpeg un ffprobe ar libmp3lame un libopus, kā arī numpy un scipy.

    python audio_examples.py
"""

import json
import os
import subprocess
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import welch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svgplot as G  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "audio-examples")
FS = 48000
DUR = 8.0
CLICK_T = 6.25                        # izolēts klikšķis klusā vietā, ap kuru zīmē viļņa formu

ENCODINGS = [
    ("mp3_cbr128", "MP3", "128 kbit/s CBR", ["-c:a", "libmp3lame", "-b:a", "128k"], ".mp3"),
    ("mp3_vbr_v5", "MP3", "VBR (-q:a 5)", ["-c:a", "libmp3lame", "-q:a", "5"], ".mp3"),
    ("mp3_cbr64", "MP3", "64 kbit/s CBR", ["-c:a", "libmp3lame", "-b:a", "64k"], ".mp3"),
    ("opus_vbr64", "Opus", "64 kbit/s VBR", ["-c:a", "libopus", "-b:a", "64k", "-vbr", "on"], ".opus"),
    ("opus_cbr64", "Opus", "64 kbit/s CBR", ["-c:a", "libopus", "-b:a", "64k", "-vbr", "off"], ".opus"),
    ("opus_vbr32", "Opus", "32 kbit/s VBR", ["-c:a", "libopus", "-b:a", "32k", "-vbr", "on"], ".opus"),
]


# --- 1. sintēze ---------------------------------------------------------------

def note(freq, start, length, t, amp=0.18):
    """Klavierveida nots: 6 harmonikas, ātrs uzbrukums, eksponenciāla dzišana."""
    tau = t - start
    env = np.where((tau >= 0) & (tau < length), np.minimum(tau / 0.005, 1.0) * np.exp(-tau / 0.6), 0.0)
    wave = sum((0.6 ** (h - 1)) * np.sin(2 * np.pi * freq * h * tau) for h in range(1, 7))
    return amp * env * wave


def synth():
    t = np.arange(int(FS * DUR)) / FS
    rng = np.random.default_rng(2024)
    chords = [(0.0, [261.63, 329.63, 392.00]), (0.75, [349.23, 440.00, 523.25]),
              (1.5, [392.00, 493.88, 587.33]), (2.25, [261.63, 329.63, 392.00]),
              (3.0, [220.00, 261.63, 329.63]), (3.75, [349.23, 440.00, 523.25]),
              (4.5, [392.00, 493.88, 587.33]), (5.0, [261.63, 329.63, 392.00])]
    left = np.zeros_like(t)
    right = np.zeros_like(t)
    for start, freqs in chords:
        for k, f in enumerate(freqs):
            v = note(f, start, 0.75 if start < 5.0 else 0.5, t)
            pan = 0.35 + 0.15 * k
            left += (1 - pan) * v
            right += pan * v
    # hi-hat: augstfrekvenču troksnis ik pēc 125 ms (3.0-5.5 s)
    noise = rng.standard_normal(len(t))
    hp = noise - np.convolve(noise, np.ones(4) / 4, mode="same")      # vienkāršs augstfrekvenču filtrs
    for k in range(20):
        s0 = 3.0 + 0.125 * k
        tau = t - s0
        env = np.where((tau >= 0) & (tau < 0.08), np.exp(-np.clip(tau, 0, None) / 0.02), 0.0)
        left += 0.12 * env * hp
        right += 0.10 * env * np.roll(hp, 17)
    # asi klikšķi (kastanjetes) katrā 0.5 s
    for s0 in np.arange(3.125, 5.5, 0.5):
        tau = t - s0
        env = np.where((tau >= 0) & (tau < 0.01), np.exp(-np.clip(tau, 0, None) / 0.0015), 0.0)
        click = env * np.sin(2 * np.pi * 2500 * tau)
        left += 0.6 * click
        right += 0.6 * click
    # viens izolēts klikšķis klusā vietā (klasiskais pirmsatbalss tests)
    tau = t - CLICK_T
    env = np.where((tau >= 0) & (tau < 0.01), np.exp(-np.clip(tau, 0, None) / 0.0015), 0.0)
    left += 0.6 * env * np.sin(2 * np.pi * 2500 * tau)
    right += 0.6 * env * np.sin(2 * np.pi * 2500 * tau)
    # kluss 1 kHz tonis 5.5-7.0 s
    tone = np.where((t >= 5.5) & (t < 7.0), 0.05 * np.sin(2 * np.pi * 1000 * t), 0.0)
    left += tone
    right += tone
    x = np.stack([left, right], axis=1)
    return 0.9 * x / np.abs(x).max()


# --- 2. kodēšana un analīze ----------------------------------------------------

def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, encoding="utf-8").stdout


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(FS),
                          "-f", "f32le", "-"], check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype="<f4").astype(float)


def packets(path):
    js = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                         "packet=pts_time,duration_time,size", "-of", "json", path]))
    return [(float(p["pts_time"]), float(p.get("duration_time", 0) or 0), int(p["size"]))
            for p in js["packets"] if p.get("pts_time") not in (None, "N/A")]


def bitrate_curve(pk, win=0.25):
    edges = np.arange(0, DUR + 1e-9, win)
    bits = np.zeros(len(edges) - 1)
    for t0, _, size in pk:
        k = int(t0 // win)
        if 0 <= k < len(bits):
            bits[k] += 8 * size
    return edges[:-1] + win / 2, bits / win / 1000.0


def align(ref, sig, maxlag=4000):
    """Nobīde, kas vislabāk izlīdzina sig ar ref (kroskorelācija ap klikšķi)."""
    a = int((CLICK_T - 0.3) * FS)
    b = int((CLICK_T + 0.3) * FS)
    r = ref[a:b]
    best = max(range(-maxlag, maxlag + 1), key=lambda d: float(np.dot(r, sig[a + d:b + d])))
    return best


# --- 3. attēli -----------------------------------------------------------------

COLORS = {"mp3_cbr128": G.BLUE, "mp3_vbr_v5": G.PURPLE, "mp3_cbr64": "#1f3b5c",
          "opus_vbr64": G.ORANGE, "opus_cbr64": G.RED, "opus_vbr32": G.GREEN}


def bitrate_svg(curves):
    W, H = 900, 420
    s = G.head(W, H, "Bitu ātrums laika gaitā")
    p = G.Plot(80, 60, 620, 290, (0, DUR), (0, 220))
    s += p.frame([(k, str(k)) for k in range(9)], [(v, str(v)) for v in range(0, 221, 40)],
                 "laiks, s", "kbit/s (0.25 s logos)")
    for x0, x1, lab in [(0, 3, "akordi"), (3, 5.5, "akordi + troksnis + klikšķi"), (5.5, 7, "kluss tonis"),
                        (7, 8, "klusums")]:
        s += G.txt((p.X(x0) + p.X(x1)) / 2, 50, lab, 11, "#555")
        s += ('<line x1="%.1f" y1="60" x2="%.1f" y2="350" stroke="#c9d3de" stroke-dasharray="3 3"/>\n'
              % (p.X(x0), p.X(x0)))
    for k, (key, label, (xs, ys)) in enumerate(curves):
        s += p.line(xs, ys, COLORS[key], 2.2, "6 3" if "cbr" in key else None)
        s += ('<line x1="715" y1="%d" x2="745" y2="%d" stroke="%s" stroke-width="2.4"%s/>\n'
              % (80 + 22 * k, 80 + 22 * k, COLORS[key], ' stroke-dasharray="6 3"' if "cbr" in key else ""))
        s += G.txt(752, 84 + 22 * k, label, 11.5, "#333", "start")
    s += G.txt(80, 395, "CBR (raustītās līnijas) tērē vienādi daudz bitu gan troksnim, gan klusumam; "
               "VBR bitus pārdala uz sarežģītākajām vietām.", 11.5, "#333", "start")
    return s + "</svg>\n"


def spectrum_svg(spectra):
    W, H = 900, 420
    s = G.head(W, H, "Vidējais spektrs")
    p = G.Plot(80, 30, 620, 320, (100, 24000), (-120, -20), xlog=True)
    xt = [(100, "100"), (200, "200"), (500, "500"), (1000, "1k"), (2000, "2k"), (5000, "5k"),
          (10000, "10k"), (20000, "20k")]
    s += p.frame(xt, [(v, str(v)) for v in range(-120, -19, 20)], "frekvence, Hz", "jauda, dB")
    for k, (key, label, (f, db)) in enumerate(spectra):
        col = COLORS.get(key, G.GRAY)
        m = f >= 100
        s += p.line(f[m], db[m], col, 2.6 if key == "ref" else 1.8, None, 0.55 if key == "ref" else 1)
        s += ('<line x1="715" y1="%d" x2="745" y2="%d" stroke="%s" stroke-width="2.4"/>\n'
              % (60 + 22 * k, 60 + 22 * k, col))
        s += G.txt(752, 64 + 22 * k, label, 11.5, "#333", "start")
    s += G.txt(80, 395, "Trokšņainās daļas (3–5.5 s) vidējais spektrs: pie mazāka bitu ātruma "
               "kodeki nogriež augstās frekvences.", 11.5, "#333", "start")
    return s + "</svg>\n"


def preecho_svg(waves):
    """Augšā oriģinālais signāls ap klikšķi, zemāk -- kļūdas signāls (atkodētais - oriģināls)."""
    W, H = 900, 118 * len(waves) + 80
    s = G.head(W, H, "Pirmsatbalss ap klikšķi")
    for k, (key, label, (tt, y)) in enumerate(waves):
        if key == "ref":
            yr, yt = (-0.7, 0.7), [(-0.5, "−0.5"), (0, "0"), (0.5, "0.5")]
        else:
            yr, yt = (-0.06, 0.06), [(-0.05, "−0.05"), (0, "0"), (0.05, "0.05")]
        p = G.Plot(220, 20 + 118 * k, 640, 84, (-30, 30), yr)
        last = k == len(waves) - 1
        s += p.frame([(v, str(v) if last else "") for v in range(-30, 31, 10)], yt)
        s += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="0.08"/>\n'
              % (p.X(-30), p.y, p.X(0) - p.X(-30), p.h, G.PURPLE))
        s += p.line(tt, np.clip(y, *yr), COLORS.get(key, G.GRAY), 1.2)
        s += G.txt(205, 20 + 118 * k + 38, label, 12, G.INK, "end", "bold")
        s += G.txt(205, 20 + 118 * k + 55, "signāls" if key == "ref" else "kļūda", 11, "#555", "end")
    s += G.txt(540, H - 44, "laiks, ms (0 — klikšķa sākums)", 12)
    s += G.txt(20, H - 22, "Augšā: oriģinālais signāls — kluss 1 kHz tonis un ass klikšķis. Zemāk: "
               "kodēšanas kļūda (atkodētais − oriģināls, cits mērogs).", 11.5, "#333", "start")
    s += G.txt(20, H - 6, "Kļūda, kas parādās jau pirms klikšķa (iekrāsotajā apgabalā), ir pirmsatbalss: "
               "kvantizācijas troksnis izplūst pa visu transformācijas logu.", 11.5, "#333", "start")
    return s + "</svg>\n"


def main():
    os.makedirs(OUT, exist_ok=True)
    x = synth()
    wav = os.path.join(OUT, "sample.wav")
    wavfile.write(wav, FS, (x * 32767).astype(np.int16))
    flac = os.path.join(OUT, "sample_ref.flac")
    run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-c:a", "flac", flac])
    files = [("ref", "FLAC", "bezzudumu atsauce", flac)]
    for key, codec, mode, args, ext in ENCODINGS:
        out = os.path.join(OUT, "sample_" + key + ext)
        run(["ffmpeg", "-y", "-v", "error", "-i", wav] + args + [out])
        files.append((key, codec, mode, out))
    os.remove(wav)

    ref = decode(flac)
    curves, spectra, waves, rows = [], [], [], []
    a, b = int(3.0 * FS), int(5.5 * FS)
    c0 = int(CLICK_T * FS)
    tt = (np.arange(c0 - int(0.03 * FS), c0 + int(0.03 * FS)) - c0) / FS * 1000
    for key, codec, mode, path in files:
        size = os.path.getsize(path)
        sig = decode(path)
        sig = np.pad(sig, (0, max(0, len(ref) + 8000 - len(sig))))
        d = 0 if key == "ref" else align(ref, sig)
        f, psd = welch(sig[a + d:b + d], FS, nperseg=4096)
        spectra.append((key, "%s %s" % (codec, mode), (f, 10 * np.log10(psd + 1e-20))))
        seg = sig[c0 + d - int(0.03 * FS):c0 + d + int(0.03 * FS)]
        rseg = ref[c0 - int(0.03 * FS):c0 + int(0.03 * FS)]
        if key == "ref":
            waves.append((key, "oriģināls", (tt, rseg)))
        elif key in ("mp3_cbr128", "mp3_cbr64", "opus_vbr64", "opus_vbr32"):
            waves.append((key, "%s %s" % (codec, mode), (tt, seg - rseg)))
        avg = None
        if key != "ref":
            pk = packets(path)
            curves.append((key, "%s %s" % (codec, mode), bitrate_curve(pk)))
            avg = sum(8 * s_ for _, _, s_ in pk) / DUR / 1000
        rows.append((key, codec, mode, os.path.basename(path), size, avg, d))

    G.save(os.path.join(HERE, "audio-bitrate.svg"), bitrate_svg(curves))
    G.save(os.path.join(HERE, "audio-spectrum.svg"), spectrum_svg(spectra))
    G.save(os.path.join(HERE, "audio-preecho.svg"), preecho_svg(waves))
    print("\n| Fails | Kodeks | Režīms | Izmērs | Vidējais bitu ātrums |")
    print("| --- | --- | --- | --- | --- |")
    for key, codec, mode, name, size, avg, d in rows:
        print("| %s | %s | %s | %.1f KB | %s |" % (name, codec, mode, size / 1000,
                                                 "%.0f kbit/s" % avg if avg else "—"))
    print("\nizlīdzināšanas nobīdes (paraugi):", {r[0]: r[6] for r in rows})


if __name__ == "__main__":
    main()

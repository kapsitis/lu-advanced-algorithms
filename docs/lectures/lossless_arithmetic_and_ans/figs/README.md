# Attēlu ģenerēšana

ANS nodaļas SVG attēlus ģenerē Python skripti, kuru nosaukumi sakrīt ar
izveidojamo failu nosaukumiem. Vajadzīgs tikai Python 3 (bez papildu
bibliotēkām).

| Skripts | Rezultāts | Ko attēlo |
| --- | --- | --- |
| `ans-slots.py` | `ans-slots.svg` | dabisko skaitļu sadalījums starp simboliem |
| `ans-encode.py` | `ans-encode.svg` | rANS stāvokļa augšana, kodējot ziņojumu |
| `ans-decode.py` | `ans-decode.svg` | rANS atkodēšanas soļu tabula |
| `ans-renorm.py` | `ans-renorm.svg` | straumējošā rANS stāvokļa logs |
| `zstd-pipeline.py` | `zstd-pipeline.svg` | Zstandard bloka apstrādes shēma |

`ansfig.py` ir kopīgais palīgmodulis (SVG primitīvi un ANS modelis); to
neizsauc tieši.

Pārģenerēt visus attēlus:

```bash
cd docs/applied_algorithms/lossless_arithmetic_and_ans/figs
for f in ans-slots ans-encode ans-decode ans-renorm zstd-pipeline; do
    python "$f.py"
done
```

## Citi ievaddati

Trīs pirmie skripti pieņem citu alfabētu, frekvences un ziņojumu, tāpēc ar
tiem var uztaisīt attēlus arī citiem piemēriem:

```bash
# noklusētais piemērs: alfabēts {A,C,G,U,$}, ziņojums GACGU$
python ans-encode.py

# monētas piemērs no uzdevumiem: p(A) = 3/4, p(B) = 1/4, ziņojums ABAA
python ans-slots.py  -f "A:3,B:1" -c 16 -p 16      -o ab-slots.svg
python ans-encode.py -f "A:3,B:1" -m "ABAA" -x 4   -o abaa-encode.svg
python ans-decode.py -f "A:3,B:1" -m "ABAA" -x 4   -o abaa-decode.svg
```

Galvenās iespējas (pilnu sarakstu rāda `python <skripts>.py --help`):

* `-f, --freq` -- kvantētās frekvences formā `"A:3,C:1,G:3,U:2,$:1"`;
  to summa ir $M$, un krāsas simboliem piešķir automātiski;
* `-m, --message` -- kodējamais ziņojums (ja alfabēta simboli ir garāki par
  vienu burtu, ziņojumu atdala ar komatiem);
* `-x, --start` -- sākuma stāvoklis $x_0$ (noklusēti 0);
* `-o, --out` -- izvades fails;
* `-c/--count` un `-p/--per-row` -- cik skaitļu attēlot `ans-slots.py`.

Pārējie attēli mapē (`arithmetic-*.png`, `dice-rolling-example.png` u.c.) ir
vecāki, zīmēti ar roku (`.odg` faili ir LibreOffice Draw pirmavoti).

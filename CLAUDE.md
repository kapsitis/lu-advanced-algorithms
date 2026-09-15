# CLAUDE.md

Course materials for the University of Latvia seminar *Algorithms in Telecommunications
and Security Solutions*. The website is a Jekyll site in `docs/`, published on GitHub Pages
at https://kapsitis.github.io/lu-advanced-algorithms/ (`baseurl: /lu-advanced-algorithms`).

## What is published

Only the pages listed in `docs/_data/nav.yml` are published and translated:

- `docs/index.lv.md`, `docs/index.en.md` (home page)
- `docs/lectures/lossless_*/index.lv.md`, `docs/lectures/lossless_*/index.en.md`

Do **not** translate `README.md` files, `*.rst` files, `slides.md` files, or code
(including Latvian comments in `.py` scripts). They are not ready for publishing.

## Bilingual pages: Latvian is the master copy

Each published page exists as two files in the **same directory**:

| File | Language | Role | URL |
| --- | --- | --- | --- |
| `index.lv.md` | Latvian | **master copy**, edited by humans | `<dir>/index.lv.html` |
| `index.en.md` | English | derived translation | `<dir>/` (default landing) |

- Humans edit the Latvian files. The English file is **derived** from the Latvian file and
  must follow it section by section. Never make content changes only in the English file.
- If you notice an error in the content (math, pseudocode, numbers, facts), do not silently
  fix it in English: report it so it can be fixed in the Latvian master first, then
  propagate. Obvious spelling typos may be corrected in the English version.
- Both files sit in one directory so relative links such as `figs/foo.png` work for both.
  Keep image paths, math, code blocks, tables and HTML anchors (`<a id="Ble13">`) identical;
  translate only prose, headings, alt texts, captions and comments inside code/pseudocode.
- Front matter (both files need `lang`, and the permalinks must follow this pattern):

  ```yaml
  # index.lv.md                                  # index.en.md
  lang: lv                                       lang: en
  permalink: /lectures/<topic>/index.lv.html     permalink: /lectures/<topic>/
  ```
  (Home page: `/index.lv.html` and `/`.)
- Internal links in content use the language-neutral directory URL, e.g.
  `{{ '/lectures/lossless_lempel_ziv/' | relative_url }}`, in both languages.
- A new page needs both files plus a nav entry with both titles:
  `title: { en: ..., lv: ... }` and `url: /lectures/<topic>/`.

### How the language switch works (`docs/_layouts/default.html`)

- The layout finds the page's twin: the page in `site.pages` with the same `dir` and the other
  `lang`. The EN/LV buttons link to the twin with `?lang=xx`; nav links use the page in the
  item's directory that has the current `lang`.
- A small inline script remembers the choice in `localStorage` (`lu-advanced-algorithms.lang`):
  opening a Latvian page remembers `lv`. Opening an English (directory) URL while `lv` is
  remembered redirects to the Latvian twin, and `?lang=en` switches back.

## Updating the English translation

1. Find what changed in the master since the English file was last updated:
   ```bash
   git log -1 --format=%H -- docs/lectures/<topic>/index.en.md      # -> <sha>
   git diff <sha> -- docs/lectures/<topic>/index.lv.md              # committed changes
   git diff HEAD -- docs/lectures/<topic>/index.lv.md               # uncommitted changes
   ```
2. Translate only the changed parts and keep the English structure parallel to the Latvian one
   (same headings, same order, same problem numbers).
3. Use US English and the terminology from `glossary.csv` (below).

## Glossary (`glossary.csv`)

A hand-edited CSV at the repository root with columns `lv,en,kind,note`. It exists so that
terminology stays consistent between translation sessions: do not invent a new English
term every time you translate.

- Before translating, look up the Latvian terms in the glossary and use the `en` column
  exactly (adapting only grammatical form). Latvian entries are in base form (nominative);
  alternatives are separated by `;`, related pairs by `/`.
- `kind` values: `standard` = established English term; `course` = a term chosen for this course
  (no common translation exists, or the Latvian term is course-specific); `name` = people,
  theorems and named objects whose Latvian transliteration hides the original spelling
  (e.g. *Hafmans* → *Huffman*, *Berouzs-Vīlers* → *Burrows–Wheeler*); `label` = recurring
  paragraph labels such as *Definīcija* → *Definition*.
- Add a row when you meet a Latvian term (a concept of 1–3 words) that is
  **not** in the glossary and either cannot be confirmed in
  [termini.gov.lv](https://termini.gov.lv/) or similar terminology sources, or does not look
  stable (the Latvian text uses several variants, e.g. *strings* / *virkne* / *virknīte*).
  Mark it `course` and say in `note` why it was chosen.
- Humans curate existing rows. Do not change an existing translation on your own. If you
  think a row is wrong, say so and suggest a replacement.
- Quote a CSV field with `"..."` if it contains a comma, and double any quote inside it.

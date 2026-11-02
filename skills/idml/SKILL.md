---
name: idml
description: "Unpack an Adobe InDesign .idml into editable XML, edit the XML directly, and repack a valid .idml — no InDesign running. Use when the user wants to inspect, diff, translate, or programmatically edit an .idml (story text, styles, colors, spreads, linked images) and produce a valid .idml back; when they say 'unpack/repack IDML', 'edit the InDesign XML', 'swap text in a .idml', or 'an .idml InDesign won't open'; or to convert between an .idml and its extracted folder."
---

# IDML Unpack / Pack (XML editing)

An **IDML** (`.idml`) file is Adobe InDesign Markup — a **ZIP package** of XML
files (an OCF container, the same family as EPUB). Unpacking it gives you a tree
of human- and AI-readable XML you can read, diff, and edit directly, then pack
back into a valid `.idml` that InDesign opens.

This skill is **Python 3 stdlib only** — no `pip install`, nothing to set up, OS-independent.
The companion script is [`scripts/idmlutil.py`](scripts/idmlutil.py).

## The one rule that makes an IDML valid

A plain `zip -r out.idml folder/` produces a file InDesign **rejects**. The
package must contain a `mimetype` entry that is:

1. the **first** entry in the archive, and
2. **STORED** (uncompressed), holding exactly
   `application/vnd.adobe.indesign-idml-package`.

InDesign reads those magic bytes from a fixed offset, so order and compression
matter. `idmlutil.py pack` does this for you (every other file is DEFLATED).
**Always repack with this script** — never with `zip`, `jar`, or Finder's Compress.

## How to run it

Resolve these against this skill's directory; pass **absolute** paths for the IDML and folders.

```bash
# Extract an .idml into a folder of XML
python3 <skilldir>/scripts/idmlutil.py unpack /abs/path/in.idml /abs/path/out_dir

# Repack a folder back into a valid .idml
python3 <skilldir>/scripts/idmlutil.py pack /abs/path/out.idml /abs/path/src_dir
```

- The folder argument is optional and defaults to `./workspace`.
- `unpack` **clears the destination folder first**, so each extraction is clean,
  and refuses archive entries that would escape it (zip-slip guard).
- `pack` reads `mimetype` from the source folder if present, otherwise writes the
  standard constant; it skips `.DS_Store`.
- If the project has the venv convention (`.venv/bin/python`), use that interpreter.
  Never `pip install` — the script needs no dependencies.

## What's in the package

- `designmap.xml` — top-level map tying the package together.
- `Stories/Story_*.xml` — the actual **text content**. The visible words live in `<Content>` elements.
- `Spreads/Spread_*.xml` — page geometry, frames, and `<Link>` entries for placed images.
- `Resources/Styles.xml` — paragraph/character/object/table styles.
- `Resources/Graphic.xml` — **colors / swatches**, strokes.
- `Resources/Fonts.xml`, `Resources/Preferences.xml`.
- `MasterSpreads/`, `XML/`, `META-INF/container.xml`.

## Workflow

1. **Unpack** into a work folder.
2. **Locate the story by its content** — `grep -rl "the visible words" work/Stories/`.
   Never by a remembered filename (see gotchas).
3. **Edit** the XML with normal file tools. Keep it well-formed UTF-8, no BOM.
4. **Repack** with `idmlutil.py pack`.
5. **Verify** the container (below) before handing the file back.

### Rules for editing text

A story's words are split across `<Content>` runs inside `ParagraphStyleRange` /
`CharacterStyleRange` elements.

- To change wording, edit the text **inside** the existing `<Content>…</Content>` tags
  rather than adding or removing runs — that preserves per-run styling. This is the
  whole job for translation and copy edits.
- A forced line break is a `<Br/>` element *between* runs; leave those in place.
  A new paragraph is a sibling `<ParagraphStyleRange>`.
- Non-ASCII is safe: the XML is UTF-8, so CJK content round-trips unchanged.
- Cross-references use `self="…"` IDs (e.g. a spread referencing a story). Prefer
  **editing values in place** over adding/removing objects; if you do delete or rename
  one, update every reference or InDesign reports a damaged file.

## Verifying a repacked IDML

Without launching InDesign you can confirm structural validity:

```bash
python3 - <<'PY'
import zipfile, sys
z = zipfile.ZipFile(sys.argv[1] if len(sys.argv) > 1 else 'out.idml')
i0 = z.infolist()[0]
assert i0.filename == 'mimetype' and i0.compress_type == zipfile.ZIP_STORED, 'bad mimetype entry'
assert z.read('mimetype') == b'application/vnd.adobe.indesign-idml-package'
print('OK — valid IDML container,', len(z.infolist()), 'entries')
PY
```

Also well-formedness-check every XML you touched
(`python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse(sys.argv[1])" f.xml`).

The authoritative "does InDesign accept it" test is a render check: open the file in
InDesign and export PNG/PDF. This skill has no InDesign driver — do that step manually,
or import the upstream sibling `indd` skill (see `ATTRIBUTION.md`) if you need it scripted.

## Gotchas

- **Story `Self` IDs and filenames are not stable across an InDesign re-export.** After a
  round-trip (open → export IDML) the same story may move from `Story_u101.xml` to
  `Story_u10f.xml`. A hard-coded path will 404 after a re-export. Always re-`unpack` and
  re-grep for the text.
- `pack` writes file entries only, so an **empty directory is dropped** on round-trip.
  Harmless to InDesign, but don't expect `diff -r` of build vs repacked-extract to be clean
  because of it.
- Structural work — creating or restyling paragraph styles, reflowing frames, building
  tables (`<Table>`/`<Cell>` markup is extremely verbose to hand-author) — belongs in
  InDesign, not in the XML. Edit text, styles-by-name, colors, and links here.

## Reference Files

| File | When to load |
|------|--------------|
| [edit-recipes.md](references/edit-recipes.md) | A specific XML edit beyond plain text: adding a line or paragraph, bolding part of a line, swapping a linked image (and the re-fit rule), applying a paragraph style, vertical Japanese text (縦書き) |

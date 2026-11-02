# Attribution

Adapted from **mindboard/indesign-extendscript-plugins** —
https://github.com/mindboard/indesign-extendscript-plugins (`skills/idml`, vendored 2026-11).
MIT License, Copyright (c) mindboard. `LICENSE` here is the upstream license file.

## Kept from upstream (verbatim)
- `scripts/idmlutil.py` — unchanged: unpack/pack, the first-entry + STORED `mimetype`
  rule, the zip-slip guard, `.DS_Store` skipping.
- The validity rule, the package map, the "edit inside `<Content>` runs" rule, the
  unstable-story-ID gotcha, and every recipe in `references/edit-recipes.md` (adding a
  line/paragraph, bold runs, image relink + the re-fit rule, paragraph styles, vertical
  Japanese text) with the author's "verified" notes intact.

## Local modifications
- Split the 189-line upstream `SKILL.md` into a 122-line router plus
  `references/edit-recipes.md` (repo convention: recipes only some tasks need), with a
  routing table.
- Frontmatter rewritten to repo convention ("Use when…" + trigger phrases, double-quoted
  description).
- Invocation paths changed from the upstream Claude-plugin layout
  (`skills/idml/scripts/…`) to resolve against this skill's directory.
- Verification snippet hardened to take the path from `argv`; added the well-formedness
  check for touched XML.
- **Not vendored:** the upstream sibling skill `indd` (drives a live InDesign app via
  ExtendScript for render/export verification and structural edits). Every upstream
  cross-reference to it was rewritten to "do this in InDesign", so nothing here teaches
  a tool this repo does not ship. Import `indd` from the same repo if you need it.
- Added a gotcha the upstream docs did not state: `pack` writes file entries only, so an
  empty directory is dropped on round-trip (harmless to InDesign; explains a non-clean
  `diff -r` of build vs repacked extract).

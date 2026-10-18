# gog Gmail recipes (read-only)

Set once per shell:
```bash
G() { gog --account "$ACCT" --readonly --gmail-no-send --no-input --wrap-untrusted "$@"; }
```
**`--wrap-untrusted` wraps text fields** (`from`, `subject`, body) in multi-line `<<<EXTERNAL_UNTRUSTED_CONTENT ...>>>` markers. IDs, `threadId`, dates and `attachmentId` stay clean. Rule of thumb:
- Output goes into the model's context: keep `--wrap-untrusted`.
- Output only feeds a local script (counts, filenames, ids): use a no-wrap variant so `from`/`subject` parse cleanly, and never let the model read those raw fields.

```bash
G()  { gog --account "$ACCT" --readonly --gmail-no-send --no-input --wrap-untrusted "$@"; }   # for the model
GS() { gog --account "$ACCT" --readonly --gmail-no-send --no-input "$@"; }                     # for scripts
```

## Count before you fetch

```bash
# hits per year (threads), no downloads
for y in 2022 2023 2024 2025 2026; do
  n=$(G --json gmail search "after:$y/01/01 before:$((y+1))/01/01 has:attachment filename:pdf" --all | jq '.threads|length')
  echo "$y $n"
done
```

## Page through everything

```bash
GS --json gmail messages search 'after:2024/01/01 before:2025/01/01 has:attachment' --all \
  | jq -r '.messages[] | [.id,.threadId,.internalDateIso,.from,.subject] | @tsv'
```
Or loop manually: read `.nextPageToken`, pass `--page TOKEN` until `has_more` is false.

## Top senders (spot newsletters before downloading)

```bash
GS --json gmail messages search 'after:2022/01/01 has:attachment' --all \
 | jq -r '.messages[].from' | sed 's/.*<//;s/>.*//' | sort | uniq -c | sort -rn | head -40
```

## Attachments of one message

```bash
GS --json gmail get "$MID" | jq -r '.attachments[] | [.attachmentId,.filename,.mimeType,.sizeHuman] | @tsv'
G gmail attachment "$MID" "$ATT" --out "$DIR/2024-03-12_sender_ref.pdf"   # always pass --out; build the name from internalDateIso, not from wrapped subject
```
Filenames from `thread get --download` look like `<msgId>_<attId8>_<original>`; two mails can carry the same original name, so keep the prefix or rename with the message date.

## Whole thread with attachments

```bash
G gmail thread get "$TID" --download --out-dir "$DIR"
```

## Body-only mails (e-invoices without a PDF)

```bash
G gmail get "$MID" --format raw > "$DIR/$MID.json"      # lossless Gmail API payload
G --json gmail get "$MID" --sanitize-content | jq -r '.body' > "$DIR/$MID.txt"
```
Many shop, rail and SaaS receipts have **no attachment at all**. A search with `has:attachment` misses them: run a second pass with `-has:attachment (invoice OR rechnung OR receipt OR beleg OR quittung)` and keep the body.

## Idempotency under --readonly

Read-only tokens cannot mark or label mail, so keep your own ledger of message ids:
```bash
touch ledger.txt
grep -qx "$MID" ledger.txt || { download "$MID" && echo "$MID" >> ledger.txt; }
```

## Useful queries

| Intent | Query |
|---|---|
| Date window | `after:2023/01/01 before:2024/01/01` (also `newer_than:7d`, `older_than:1y`) |
| PDFs only | `has:attachment filename:pdf` |
| Big attachments | `larger:5M` |
| Receipts, DE+EN | `(rechnung OR invoice OR beleg OR receipt OR quittung OR zahlung OR order OR bestellung)` |
| Exclude noise | `-category:promotions -category:social` |
| Sender domain | `from:@amazon.de` |
| Starred / label | `is:starred`, `label:Finance` |

## Gotchas

- `gmail search` returns **threads**; `gmail messages search` returns **messages**. Use the second when you need per-mail dates.
- Trashed and Spam mail are excluded by default; add `in:anywhere` to include them.
- Gmail dates in queries use the account's timezone; `internalDateIso` in results is UTC.
- Large `--all` runs hit API quota (HTTP 429): batch by year and sleep between years.

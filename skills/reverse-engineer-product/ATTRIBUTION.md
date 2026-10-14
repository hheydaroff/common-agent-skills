# Attribution

The method behind `reverse-engineer-product` is adapted from **REA: Reverse Engineer Anything**
by [morluto](https://github.com/morluto/rea), MIT licensed
(`.agents/skills/reverse-engineer-anything/`, README "How REA works"; retrieved 2026-10-14).

## Ideas carried over (re-expressed for products, not copied)

| REA idea | Here |
|---|---|
| Distinguish observations, inferences and unknowns; never imply static analysis observed execution | Provenance tags [O]/[S]/[I]/[P]; never imply you inspected what you only recalled |
| Route the target first, use the cheapest evidence channel that answers the question | Evidence-channel ladder |
| Summary first, drill only on a concrete gap; never repeat an identical call | Step 1 sweep before Step 2 depth; no repeated queries |
| Turn the request into a checklist of questions and the evidence each needs; close it answered / partial / unresolved | Step 0 and Step 6 |
| Finding ledger with confidence, search boundary and remaining unknowns; `record_unknown` | Evidence ledger, unknowns register, bounded negatives |
| Reconcile static (shipped artifact) with runtime (observed behaviour); mismatch is reported | Step 3: claims vs observation |
| Compare complete, compatible sets before claiming equivalence or absence | Compare mode D; "not found" carries its bound |
| `verify_reconstruction`: a pass covers declared comparable claims only | Verification table in the replication blueprint |
| Separate observed behaviour from design choices when building | Two strictly separate blueprint sections |
| Decompose into independent questions for parallel workers | kept, with the caveat that web research stays in the main session |

## Intentionally not taken

- REA's MCP server, CLI and tool catalogue.
- Native, managed, firmware, Android, WASM and EVM analysis; Ghidra, Hopper, IDA, JADX and similar providers.
- Packet-capture, signal-decoding and crash-dump workflows.
- Any REA code, setup or configuration.

Binary-level reverse engineering stays out of scope for this skill.

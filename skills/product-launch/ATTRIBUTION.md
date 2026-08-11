# Attribution

Adapted from [pm-skills / pm-go-to-market](https://github.com/hheydaroff/pm-skills/tree/main/pm-go-to-market)
by Paweł Huryn ([The Product Compass Newsletter](https://www.productcompass.pm)).

## What was vendored

All 6 skills of the pm-go-to-market plugin, collapsed into one skill with
references:

| Upstream skill | Local reference |
|---|---|
| gtm-strategy | references/gtm-strategy.md (+ /plan-launch command workflow & template) |
| beachhead-segment | references/beachhead-segment.md |
| ideal-customer-profile | references/ideal-customer-profile.md |
| gtm-motions | references/gtm-motions.md |
| growth-loops | references/growth-loops.md (+ /growth-strategy command template) |
| competitive-battlecard | references/competitive-battlecard.md (+ /battlecard command template) |

## Local modifications

- Collapsed 6 skills + 3 commands (/plan-launch, /growth-strategy, /battlecard)
  into one `product-launch` skill with 3 modes.
- Removed Claude-plugin mechanics (`$ARGUMENTS`, "Apply the X skill" pointers).
- Output artifacts follow this repo's `docs/TYPE_descriptor.md` convention.

## Not vendored

The other 8 plugins in pm-skills (product-strategy, product-discovery,
market-research, marketing-growth, execution, data-analytics, ai-shipping,
toolkit).

## License (upstream, verbatim)

MIT License

Copyright (c) 2026 Pawel Huryn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

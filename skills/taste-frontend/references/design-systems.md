# Design System Selection

Load when picking a foundation for the build. Do not invent CSS for things that have an official package. Do not pretend an aesthetic trend is an official system.

## When to reach for a real design system (official packages)

| Brief reads as… | Reach for | Why |
|---|---|---|
| Microsoft / enterprise SaaS / dashboards | `@fluentui/react-components` or `@fluentui/web-components` | Official Fluent UI, Microsoft tokens, a11y done |
| Google-ish, Material-flavored product | `@material/web` + Material 3 tokens | Official, theme-able via Material Theming |
| IBM-style B2B / enterprise analytics | `@carbon/react` + `@carbon/styles` | Official Carbon, mature data-density |
| Shopify app surfaces | Polaris web components / Polaris React | Required for Shopify admin UI |
| Atlassian / Jira-style product | `@atlaskit/*` + `@atlaskit/tokens` | Official Atlassian DS |
| GitHub-style devtool / community page | `@primer/css` or `@primer/react-brand` | Official Primer; Brand variant for marketing |
| Public-sector UK service | `govuk-frontend` | Legally / regulatorily expected |
| US public-sector / trust-first | `uswds` | Same |
| Fast local-business / agency MVP | Bootstrap 5.3 | Boring, fast, works |
| Modern accessible React foundation | `@radix-ui/themes` | Primitives + polished theme |
| Modern SaaS where you own components | shadcn/ui (`npx shadcn@latest add ...`) | You own the code; never ship default state |
| Tailwind-based modern SaaS / AI marketing | Tailwind v4 utilities + `dark:` variant | Default for indie / small-team builds |

**Honesty rule:** if the brief reads as one of the above, install and use the **official** package. Do not recreate its CSS by hand. Do not import a system's tokens then override 90% of them.

**One system per project.** Do not mix Fluent React with Carbon. Do not import shadcn/ui into a Material 3 app.

## When the brief is an aesthetic, not a system

No single official package exists. Build with native CSS + Tailwind + a maintained component library. Be honest in comments about borrowed inspiration vs official material.

| Aesthetic | Honest implementation |
|---|---|
| Glassmorphism / frosted glass | `backdrop-filter`, layered borders, highlight overlays. Solid-fill fallback for `prefers-reduced-transparency`. |
| Bento (Apple-style tile grids) | CSS Grid with mixed cell sizes. No library owns this. |
| Brutalism | Native CSS, monospace, raw borders. No library. |
| Editorial / magazine | Serif type, asymmetric grid, generous whitespace. No library. |
| Dark tech / hacker | Mono + accent neon, terminal motifs. No library. |
| Aurora / mesh gradients | SVG or layered radial gradients. No library. |
| Kinetic typography | Native CSS animations, scroll-driven animations, GSAP for hijacks. No library. |
| Apple Liquid Glass | Apple documents this for Apple platforms only. **There is no official `liquid-glass.css`.** Web is an approximation — see references/liquid-glass.md. |

---

## Install commands per design system

```bash
# Material Web (Material 3)
npm install @material/web

# Fluent UI React (v9)
npm install @fluentui/react-components

# Fluent UI Web Components (framework-free)
npm install @fluentui/web-components @fluentui/tokens

# IBM Carbon
npm install @carbon/react @carbon/styles

# Radix Themes
npm install @radix-ui/themes

# shadcn/ui (open code, owned components)
npx shadcn@latest init
npx shadcn@latest add button card badge separator input

# Primer CSS (GitHub product/devtool UI)
npm install --save @primer/css

# Primer Brand (GitHub marketing UI)
npm install @primer/react-brand

# GOV.UK Frontend
npm install govuk-frontend

# USWDS (US Web Design System)
npm install uswds

# Atlassian Design System (Atlaskit)
yarn add @atlaskit/css-reset @atlaskit/tokens @atlaskit/button @atlaskit/badge @atlaskit/section-message @atlaskit/card

# Bootstrap 5.3
npm install bootstrap

# Shopify Polaris Web Components (Shopify apps only)
#   <meta name="shopify-api-key" content="%SHOPIFY_API_KEY%" />
#   <script src="https://cdn.shopify.com/shopifycloud/polaris.js"></script>
```

## Canonical sources (read before reinventing)

- **Material Web:** https://github.com/material-components/material-web · https://material-web.dev/theming/material-theming/ · https://m3.material.io/develop/web
- **Fluent UI:** https://fluent2.microsoft.design/get-started/develop · https://fluent2.microsoft.design/components/web/react/ · https://github.com/microsoft/fluentui
- **Carbon:** https://carbondesignsystem.com/ · https://github.com/carbon-design-system/carbon
- **Shopify Polaris:** https://shopify.dev/docs/api/app-home/web-components · https://github.com/Shopify/polaris-react · https://polaris-react.shopify.com/components
- **Atlassian:** https://atlassian.design/get-started/develop · https://atlassian.design/tokens/design-tokens
- **Primer:** https://primer.style/ · https://github.com/primer/css · https://github.com/primer/brand
- **GOV.UK:** https://design-system.service.gov.uk/ · https://github.com/alphagov/govuk-frontend
- **USWDS:** https://designsystem.digital.gov/documentation/developers/ · https://github.com/uswds/uswds
- **Bootstrap:** https://getbootstrap.com/docs/5.3/layout/grid/
- **Tailwind:** https://tailwindcss.com/docs/dark-mode · https://tailwindcss.com/blog/tailwindcss-v4
- **Radix:** https://www.radix-ui.com/themes/docs/components/theme · https://github.com/radix-ui/themes
- **shadcn/ui:** https://ui.shadcn.com/docs · https://github.com/shadcn-ui/ui
- **Native CSS / W3C:** MDN `backdrop-filter`, `prefers-color-scheme`, `prefers-reduced-motion`, CSS Grid, Scroll-driven animations · https://drafts.csswg.org/scroll-animations-1/
- **Apple Liquid Glass (Apple platforms only):** https://developer.apple.com/design/human-interface-guidelines/materials · https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass

Install commands above are reality anchors — ground decisions in production reality, not training-data fiction.

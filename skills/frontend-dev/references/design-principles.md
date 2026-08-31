# Design Principles

> Adapted from [HermeticOrmus/design-mastery-claude-code](https://github.com/HermeticOrmus/design-mastery-claude-code) (MIT). The visual fundamentals behind frontend-dev's design rules. Load when a layout "feels off" and you need the principled fix.

The fundamental laws governing visual perception and communication. These principles are not opinions—they're observations about how human vision and cognition work.

## When to Use This Skill

- Making visual design decisions
- Evaluating whether a design "works"
- Explaining why something feels off
- Teaching design fundamentals
- Debugging design problems

## Core Principles

### 1. Visual Hierarchy

**The Law**: Not all elements are equally important. Design must guide the eye.

**Establishing Hierarchy**:

| Tool | What It Does | Example |
|------|--------------|---------|
| Scale | Larger = more important | Hero headlines vs. body text |
| Weight | Heavier = more important | Bold headings vs. light body |
| Color | Saturated/contrasting = attention | Primary CTA vs. secondary |
| Position | Top-left (in LTR) = first seen | Logo placement |
| Space | More space = more importance | Generous padding around CTAs |
| Depth | Shadows/elevation = prominence | Floating action buttons |

**Testing Hierarchy**:
Blur the design at 50%. Can you still identify:
- The primary focal point?
- The secondary information?
- The action you should take?

### 2. Gestalt Principles

**The Law**: The brain organizes visual elements into meaningful groups.

#### Proximity
*Elements near each other are perceived as related.*

```
Good:  [Label]          [Label]
       [Input]          [Input]
       (8px gap)        (8px gap)

       (32px gap between groups)

       [Label]          [Label]
       [Input]          [Input]

Bad:   [Label]  [Label]  [Label]  [Label]
       [Input]  [Input]  [Input]  [Input]
       (equal spacing destroys grouping)
```

**In Tailwind**:
- Related items: `space-y-2` (8px)
- Unrelated groups: `space-y-8` (32px) or `divide-y`

#### Similarity
*Elements that look alike appear grouped.*

When multiple card types exist, make categories visually distinct:
- Same category: same border-radius, shadow, padding
- Different category: different color, icon style, or layout

#### Continuity
*The eye follows smooth paths.*

Applied to navigation:
```
[Home] → [Products] → [About] → [Contact]
         ↓
    [Category A]
    [Category B]
    [Category C]
```

Lines don't need to be visible—implied lines work.

#### Closure
*The mind completes incomplete shapes.*

Useful for:
- Logo design (WWF panda, FedEx arrow)
- Icon design (implied shapes)
- Cards that bleed off screen (implies more content)

#### Figure/Ground
*Clear separation between subject and background.*

Common failures:
- Text on busy image backgrounds
- Low contrast between layers
- Unclear what's clickable vs. static

### 3. The Rule of Thirds

**The Law**: Placing subjects at 1/3 intersections creates natural balance.

```
+-------+-------+-------+
|       |       |       |
|   ●   |       |       |  ← Focal point at intersection
+-------+-------+-------+
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

For web layouts:
- Hero text left-aligned, hitting left-third
- Key visuals placed at intersection points
- Whitespace fills remaining thirds

### 4. Golden Ratio (1:1.618)

**The Law**: Proportions found in nature feel inherently pleasing.

Applications:
- Content width to sidebar: `1:1.618`
- Heading to body size: `1.618:1`
- Spacing multipliers: `16px → 26px → 42px`

Tailwind approximation:
```
Base unit: 16px (text-base)
Medium:    24px (text-2xl ≈ 16 × 1.5)
Large:     40px (text-4xl ≈ 16 × 2.5)
```

### 5. Visual Balance

**The Law**: Compositions should feel stable, not falling.

**Symmetrical Balance**
- Equal weight on both sides
- Formal, stable, traditional
- Use for: corporate, luxury, authoritative

**Asymmetrical Balance**
- Unequal elements balanced by visual weight
- Dynamic, interesting, modern
- Use for: creative, startups, editorial

**Visual Weight Factors**:
| Element | Adds Weight |
|---------|-------------|
| Size | Larger = heavier |
| Color | Darker, saturated = heavier |
| Complexity | Detailed = heavier |
| Position | Lower = heavier |
| Isolation | Alone = heavier |

### 6. Alignment

**The Law**: Elements should share visual lines, even if not explicitly drawn.

**Strong Alignment**:
```
[Logo]
_________________________
[Navigation links          ]
_________________________

[Headline              ]
[Subhead               ]
[CTA Button]

(Everything shares left edge)
```

**Weak Alignment**:
```
    [Logo]
[Navigation links]
    [Headline]
   [Subhead   ]
    [CTA Button]

(No consistent edge)
```

### 7. Repetition

**The Law**: Consistent patterns create unity and learnability.

Elements to keep consistent:
- Border radius (all cards same)
- Shadow levels (same depth for same importance)
- Spacing units (multiples of 4px or 8px)
- Color application (primary always means action)
- Typography hierarchy (h2 always looks like h2)

### 8. Contrast

**The Law**: Difference creates interest and guides attention.

Types of contrast:
- Size contrast: Large headings, small captions
- Color contrast: Dark on light, warm accents
- Weight contrast: Bold headlines, regular body
- Style contrast: Serif headings, sans body
- Spacing contrast: Tight groups, generous separation

**Minimum contrast requirements**:
- Body text: 4.5:1 ratio (WCAG AA)
- Large text (18px+): 3:1 ratio
- UI components: 3:1 ratio

### 9. White Space (Negative Space)

**The Law**: What you leave empty is as important as what you fill.

**Functions of white space**:
1. **Breathing room**: Prevents cognitive overload
2. **Grouping**: Separates distinct content areas
3. **Emphasis**: Isolated elements command attention
4. **Luxury signal**: Generous space suggests premium

**Common failures**:
- Cramming elements to "fit more"
- Equal spacing everywhere (creates monotony)
- Fear of empty space

**Tailwind spacing guide**:
```
Tight (related):     gap-2 (8px)
Standard (siblings): gap-4 (16px)
Section (groups):    gap-8 (32px) or py-12
Page (major):        gap-16 (64px) or py-24
```

### 10. Unity

**The Law**: All elements should feel like they belong together.

**Achieving Unity**:
- Consistent color palette
- Unified typography system
- Repeated patterns and components
- Aligned grids
- Harmonious proportions

**Testing Unity**:
Take any element and place it elsewhere. Does it still feel like it belongs? If not, the system lacks unity.

## Quick Reference: Principles Applied

| Problem | Principle | Solution |
|---------|-----------|----------|
| "It feels cluttered" | White Space | Increase padding/margins |
| "I don't know where to look" | Hierarchy | Establish clear focal point |
| "It feels disconnected" | Unity/Repetition | Apply consistent patterns |
| "It feels boring" | Contrast | Add variation in size/color/weight |
| "Things seem randomly placed" | Alignment | Create shared edges |
| "The groups are confusing" | Proximity/Similarity | Cluster related items |
| "It feels off balance" | Balance | Redistribute visual weight |

## Related References

- **color-theory.md**: Color psychology and application
- **typography-fundamentals.md**: Type as design element
- **masters-applied.md**: Applied lessons from Bass, Vignelli, Rams, and others
- Evaluation checklist: folded in below

---

# Evaluation Checklist

Use this checklist as a self-check on your own output against fundamental principles.

## Quick Scan (30 seconds)

- [ ] **Clear focal point** - Eye knows where to go first
- [ ] **Readable hierarchy** - Importance is obvious
- [ ] **Sufficient contrast** - Text is legible
- [ ] **Breathing room** - Elements aren't cramped
- [ ] **Consistent patterns** - Similar things look similar

## Visual Hierarchy

- [ ] Primary element is unmistakably prominent
- [ ] Secondary elements support without competing
- [ ] Scale differences are meaningful (not random)
- [ ] Color usage guides attention appropriately
- [ ] Position reflects importance (top-left most important in LTR)

## Gestalt Principles

### Proximity
- [ ] Related items are grouped together
- [ ] Unrelated groups have clear separation
- [ ] Spacing is intentional, not arbitrary

### Similarity
- [ ] Same types of elements share visual treatment
- [ ] Differences between types are obvious
- [ ] No accidental visual confusion

### Continuity
- [ ] Eye can follow logical reading paths
- [ ] No unexpected breaks in visual flow
- [ ] Navigation feels natural

### Closure
- [ ] Incomplete shapes still read correctly
- [ ] Groupings are understood without explicit boxes
- [ ] Implied lines function as intended

### Figure/Ground
- [ ] Clear distinction between content and background
- [ ] No ambiguity about what's interactive
- [ ] Layers are understood at a glance

## Typography

- [ ] Maximum 2-3 typeface families
- [ ] Clear size hierarchy (title → heading → body → caption)
- [ ] Line length is comfortable (45-75 characters)
- [ ] Line height supports readability
- [ ] Font choices match brand personality

## Color

- [ ] Limited, intentional palette (not rainbow)
- [ ] 60-30-10 proportions (or deliberate variation)
- [ ] Same colors mean same things throughout
- [ ] All text passes WCAG AA contrast (4.5:1)
- [ ] UI elements have 3:1 contrast minimum
- [ ] Works for colorblind users (check with simulator)

## Spacing & Layout

- [ ] Consistent spacing scale (multiples of 4px or 8px)
- [ ] Generous white space around important elements
- [ ] Grid system creates predictable rhythm
- [ ] Responsive behavior is considered
- [ ] Touch targets are at least 44x44px

## Alignment

- [ ] Elements share common edges/axes
- [ ] No "almost aligned" situations
- [ ] Grid discipline is maintained
- [ ] Intentional breaks from grid are obvious

## Balance

- [ ] Visual weight is distributed appropriately
- [ ] Nothing feels like it's "falling off"
- [ ] Symmetry or asymmetry is intentional
- [ ] White space balances content density

## Contrast

- [ ] Size contrast creates hierarchy
- [ ] Color contrast guides attention
- [ ] Weight contrast (bold/light) is used purposefully
- [ ] Enough variety to prevent monotony

## Consistency

- [ ] Same components look the same everywhere
- [ ] Patterns are predictable
- [ ] Variations have clear purpose
- [ ] Nothing looks like a mistake

## Accessibility

- [ ] Color contrast passes WCAG AA
- [ ] Interactive elements have focus states
- [ ] No information conveyed by color alone
- [ ] Touch targets are large enough
- [ ] Motion can be reduced if needed
- [ ] Screen reader order makes sense

## Unity

- [ ] Everything feels like part of the same system
- [ ] No orphan elements that don't belong
- [ ] Brand personality is consistent
- [ ] Design tokens are applied systematically

---

## Scoring Guide

### How to Use
Rate each section 1-5:
- 1 = Major issues
- 2 = Significant problems
- 3 = Adequate
- 4 = Good
- 5 = Excellent

### Priority Matrix

| Score Range | Action |
|-------------|--------|
| 1-2 | Must fix before shipping |
| 3 | Should fix if time allows |
| 4-5 | Acceptable |

### Section Weights

| Section | Weight |
|---------|--------|
| Visual Hierarchy | High |
| Typography | High |
| Color | High |
| Accessibility | High |
| Gestalt | Medium |
| Spacing & Layout | Medium |
| Consistency | Medium |
| Alignment | Low |
| Balance | Low |
| Contrast | Low |
| Unity | Low |

---

## Common Failures & Fixes

| Issue | Principle Violated | Quick Fix |
|-------|-------------------|-----------|
| "It feels cluttered" | White Space | Increase padding by 50% |
| "I don't know where to look" | Hierarchy | Make one thing 2x larger |
| "It feels disconnected" | Unity | Apply consistent border-radius |
| "It's hard to read" | Contrast | Increase to 4.5:1 ratio |
| "Things seem random" | Alignment | Snap to 8-column grid |
| "Groups are confusing" | Proximity | Add 2x space between groups |
| "It feels amateur" | Consistency | Audit and unify similar elements |

---

Source: [HermeticOrmus/design-mastery-claude-code](https://github.com/HermeticOrmus/design-mastery-claude-code) (MIT, © 2024 Hermetic Ormus). Attribution and license: [design-mastery-ATTRIBUTION.md](design-mastery-ATTRIBUTION.md)

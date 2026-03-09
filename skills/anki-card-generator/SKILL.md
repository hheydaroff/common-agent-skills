---
name: anki-card-generator
description: Generate high-quality Anki flashcards following LessWrong best practices and cognitive science principles. Outputs simple-anki-sync compatible markdown. Use when user requests to create Anki cards, make flashcards, or learn material—phrases like "create flashcards", "make Anki cards", "help me memorize", "generate cards for", "study with cards".
---

# Anki Card Generator

Generate high-quality Anki cards based on LessWrong best practices and simple-anki-sync format.

## Pre-Generation Clarification

Before generating cards, clarify with user if unclear:

1. **Scope**: "Which aspects to focus on?" (for broad topics)
2. **Depth**: "Basic concepts only, or detailed Level 2/3 cards?"
3. **Quantity**: "How many cards? (Recommend 5-10 for core concepts)"
4. **Context**: "Any specific exam or application scenario?"

Proceed only after understanding requirements.

## Output Format

Use simple-anki-sync format:

```markdown
#anki/[domain]/[topic]

| [Question] |
| ---------- |
| [Core answer]<br><br><small>💡 [Supplementary info]</small> |
```

### Format Options

**Option A (Recommended)**: HTML tags

```markdown
| 唐朝建立时间 |
| ---------- |
| 618年，李渊建立<br><br><small>💡 隋末农民起义后起兵</small> |
```

**Option B**: Separator

```markdown
| 唐朝建立时间 |
| ---------- |
| 618年，李渊建立 ——— 💡 隋末农民起义后起兵 |
```

**Option C**: Parentheses

```markdown
| 唐朝建立时间 |
| ---------- |
| 618年，李渊建立（趣闻：其子李世民功劳最大） |
```

## Atomization Rules

### Word Limits

- **English**: Max 9 words, absolute limit 18 words
- **Chinese**: Recommended 15-20 characters, absolute limit 30-35 characters
- **Max items**: 3 bullet points per card

### Core Principle

If a card can be split into two shorter cards, split it.

## Question Design

### Standardized Templates

- **Time**: "X date/time" (not "When did X happen?")
- **Definition**: "X definition" (not "What is X?")
- **Person**: "who X" (not "Who did X?")
- **Pros/Cons**: "X pros and cons" (not "What are advantages of X?")

### Key Rules

- Match real-world recall scenarios
- Use plain, unremarkable wording
- Avoid words in question that appear in answer
- Keep all critical info in answer, not question

## Answer Construction

### Core Answer

- Strictly follow word limits
- Answer should be meaningful without the question
- All key information in answer

### Supplementary Info (Optional)

Format: `<br><br><small>💡 content</small>`

**Emoji Guide**:

- 💡 Fun fact / trivia
- 📝 Note / explanation
- 🔗 Related concept
- ⚡ Tip / key point
- 📊 Data / statistics
- 📅 Date / timeline

Keep supplementary info to 10-20 characters.

### Handle System

Use `>` to reference related cards:

```markdown
| Newton's contributions |
| ---------------------- |
| >laws of motion >universal gravitation >calculus development |
```

## Detail Levels

- **Level 1**: Basic concept (core answer)
- **Level 2**: Detailed info (supplementary section)
- **Level 3**: Advanced details (create separate cards)

## Tag Naming

Use English tags: `#anki/[domain]/[topic]`

Common domains: history, programming, language, science, mathematics, psychology, economics, philosophy, medicine, art, literature, biology

## Quality Checklist

### Per Card

- [ ] Core answer within word limit?
- [ ] Correct supplementary format?
- [ ] Can it be further split?
- [ ] Question matches real recall scenario?
- [ ] No memory shortcuts?
- [ ] All key info in answer?

### Card Set

- [ ] Appropriate cross-references?
- [ ] Proper detail levels?
- [ ] No redundancy?

## Domain Examples

See [references/examples.md](references/examples.md) for detailed examples:

- History (ancient China)
- Programming (Python)
- Language learning (English)
- Academic concepts (psychology)
- Complex topics (quantum mechanics)
- Error corrections
- Advanced techniques (reversible cards, redundancy design)

## Workflow

1. **Receive input**: Knowledge points, wiki links, study materials
2. **Clarify**: Ask questions if uncertain
3. **Generate**: Follow atomization and best practices
4. **Output**: simple-anki-sync markdown format

**Core Philosophy**: Prioritize sustainability and real recall scenarios over comprehensive coverage. Focus on preventing cognitive and motivational barriers.

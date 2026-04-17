# Source Document Intake

## Overview

Convert source materials to structured text before planning slides. This step ensures no content is lost and provides a clean reference for the Strategist phase.

---

## Conversion Methods

| Source Format | Command | Notes |
|--------------|---------|-------|
| **PDF** | `python -m markitdown document.pdf` | Best for text-heavy PDFs. For scanned PDFs, may need OCR |
| **DOCX / Word** | `python -m markitdown document.docx` | Preserves headings and structure |
| **PPTX** (existing deck) | `python -m markitdown presentation.pptx` | Extracts slide text; use for reference or remake |
| **XLSX / CSV** | `python -m markitdown data.xlsx` | Extracts table data |
| **HTML / URL** | `python -m markitdown https://example.com/article` | Fetches and converts web content |
| **Markdown** | Read directly | Already structured |
| **Plain text** | Read directly | User pastes content into chat |

### Installation

```bash
pip install "markitdown[all]"
```

The `[all]` extra includes PDF, DOCX, PPTX, XLSX, and other format support.

---

## Workflow

### Step 1: Convert to Markdown

```bash
# Convert and save to a reference file
python -m markitdown source.pdf > source_content.md
```

### Step 2: Review Extracted Content

Read `source_content.md` to understand:
- **Structure**: Headings, sections, lists
- **Key data**: Numbers, statistics, comparisons
- **Content volume**: Word count → page count estimation
- **Visuals needed**: References to charts, images, diagrams

### Step 3: Content Analysis

Before entering the Strategist phase, assess:

| Dimension | Question | Impact |
|-----------|----------|--------|
| **Volume** | How much content? | Page count, content density |
| **Structure** | Clear sections? | TOC design, section dividers |
| **Data** | Statistics, numbers, comparisons? | Chart/visualization needs |
| **Narrative** | Story arc? Argument flow? | Content strategy style |
| **Visuals** | Referenced images or diagrams? | Image handling approach |
| **Audience** | Who is this for? | Tone, complexity level |

### Step 4: Proceed to Strategist

With content analyzed, move to the [Strategist Phase](strategist.md) with informed recommendations.

---

## Multi-Source Handling

When the user provides multiple source files:

1. Convert each file separately
2. Read and identify overlap / complementary content
3. Create a unified content outline
4. Note which source each section comes from (for reference)

```bash
python -m markitdown report.pdf > sources/report.md
python -m markitdown data.xlsx > sources/data.md
python -m markitdown notes.docx > sources/notes.md
```

---

## Content from Conversation

When the user provides content directly in chat (no file):
- No conversion needed
- Capture the key points, structure, and data from the conversation
- Confirm with the user if anything is unclear before proceeding
- Proceed directly to [Strategist Phase](strategist.md)

---

## Output

After intake, you should have:
- Clear understanding of all source content
- Estimated content volume and structure
- Initial sense of audience, purpose, and tone
- Ready to make informed recommendations in the Strategist phase

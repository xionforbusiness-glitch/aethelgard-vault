---
name: llm-wiki-multimodal-ingest
description: Ingest images into LLM Wiki with OCR and asset organization.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [wiki, multimodal, image-ingest, obsidian, vision]
    category: research
    related_skills: [llm-wiki, obsidian]
---

# LLM Wiki Multimodal Ingest

Use this skill when the user sends an image, screenshot, diagram, or handwritten note to be ingested into their LLM Wiki.

## Workflow

### Step 1: Analyze the image with vision_analyze
Use `vision_analyze` to extract all visible text, UI elements, and context.

### Step 2: Save the image asset
Save the original image to `raw/assets/` with a descriptive filename.
**Naming:** `YYYYMMDD_description.png` or `YYYYMMDD_type_description.png`

### Step 3: Create the raw source note
Create `raw/articles/YYYYMMDD_description.md` with:
- YAML frontmatter (`source_url`, `ingested`, `image_file`)
- Full OCR transcription
- Structured metadata

### Step 4: Synthesize Knowledge & Create Wiki Pages
Based on the image content, generate the appropriate Layer 2 pages:
- **Concept Page (`concepts/`):** For technical architectures, algorithms, frameworks, or workflows.
- **Entity Page (`entities/`):** For organizations, labs, people, or foundation model releases.
- **Comparison Page (`comparisons/`):** Side-by-side matrices when an image introduces competing tools/models.
- **Implementation / Deployment Plan:** When the user requests installation or planning, include clear hardware prerequisites, Python/Node setup, test scripts, and integration architecture.
- **Existing Page Updates:** Cross-link and patch existing skill/knowledge base files to reflect newly acquired capabilities.

Each new page must include YAML frontmatter (`title`, `created`, `updated`, `type`, `tags`, `sources`), minimum 2 outbound `[[wikilinks]]`, and provenance references.

### Step 5: Update navigation
- Add concept to `index.md`
- Update "Total pages" count
- Append to `log.md`

## Pitfalls

- **Never modify raw/ after initial write** — raw sources are immutable.
- **Always save the original image** — don't rely on OCR alone.
- **Extract UI metadata** — for website screenshots, get URL, headline, inputs, results.
- **Tag with schema taxonomy** — only use tags defined in SCHEMA.md.
- **Cross-reference immediately** — add at least 2 outbound wikilinks.

## Cross-References
- [[llm-wiki]] — General LLM Wiki procedures
- [[obsidian]] — Obsidian vault operations
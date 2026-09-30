# Aethelgard Vault — LLM Wiki Schema

## Domain
Personal knowledge base and LLM Wiki (Karpathy pattern) for **Omar Elnemr** (Aethelgard Vault). Covers:
- Personal identity, bio, education, and career notes
- Technical skills: Computer Vision (YOLOv8, OpenCV), Embedded Systems & Robotics (Arduino, LEGO SPIKE Prime), Linux CLI/Bash, Networking & Tunneling (Wireshark, OpenVPN), Data Structures & Algorithms, AI Annotation & Evaluation
- Projects, architectural writeups, and software builds
- Hobbies, speedcubing (CFOP algorithms), gaming (We Happy Few, Rain World, Sea of Conquest), aviation (DCS), audio/hardware gear, and literature
- Incoming web research, technical papers, and articles ingested via Hermes Telegram bot

## Conventions
- **File names:** Lowercase, hyphens/underscores, no spaces for generated wiki pages (e.g., `yolov8-realtime-tracking.md`). Existing notes retain their clean filenames.
- **YAML Frontmatter:** Every page begins with YAML frontmatter (title, created, updated, type, tags, sources).
- **Wikilinks:** Use `[[wikilinks]]` to interlink notes (minimum 2 outbound links per new page).
- **Date Bump:** Always bump the `updated` date when modifying a note.
- **Cataloging:** Every new page must be registered in `index.md` (and cross-referenced in `vault_index_dashboard.md`).
- **Activity Logging:** Every ingest, query synthesis, and lint action is appended to `log.md`.
- **Provenance Markers:** On pages that synthesize multiple raw sources, append `^[raw/articles/source-file.md]` to key paragraphs.

## Frontmatter Standard
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary | reference
tags: [from taxonomy below]
sources: [raw/articles/source-name.md]
confidence: high | medium | low
contested: false
contradictions: []
---
```

## Tag Taxonomy
- **Identity & Career:** personal, bio, education, work, resume, experience
- **Technical & Software:** python, c-plus-plus, bash, linux, git, networking, openvpn, wireshark, dsa
- **AI & Data:** ai, ml, computer-vision, yolo, opencv, annotation, prompt-engineering, llm, llm-wiki
- **Hardware & Robotics:** arduino, embedded, robotics, lego-spike, hardware, sensors, actuators
- **Aviation & Sim:** aviation, dcs, ground-ops, flight-sim
- **Hobbies & Lifestyle:** speedcubing, cfop, gaming, media, audio, gear, reading
- **Hermes & Tools:** hermes-agent, obsidian, omniroute, telegram-bot, skill, tool

## Three Layers
1. **Raw Sources (`raw/`):** Immutable. Articles (`raw/articles/`), research papers (`raw/papers/`), transcripts (`raw/transcripts/`), and media/assets (`raw/assets/`). The AI reads but never alters these files.
2. **Wiki Pages (`entities/`, `concepts/`, `comparisons/`, `queries/`):** AI-generated and maintained markdown notes that synthesize and cross-link knowledge.
3. **Schema (`SCHEMA.md`):** Defines structure, rules, and taxonomies for consistent agent maintenance.

## Core Operations
- **Ingest (`/ingest <url|file|text>`):** Fetch content, store immutable raw source in `raw/`, extract key entities/concepts, generate/update wiki notes with `[[wikilinks]]`, update `index.md` and `log.md`.
- **Query (`/query <question>`):** Orient by reading `index.md`, search relevant vault notes, synthesize a direct answer with `[[wikilinks]]` citations, file deep analyses to `queries/`.
- **Lint (`/lint`):** Audit the vault for broken `[[wikilinks]]`, orphan pages, missing tags, stale claims, and format inconsistencies. Report findings to `log.md`.

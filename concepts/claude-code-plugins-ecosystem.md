---
title: Claude Code Plugins & Marketplaces Ecosystem
created: 2026-09-20
updated: 2026-09-20
type: concept
tags: [claude-code, plugins, skills, agents, marketplace, automation, extension]
sources: [raw/articles/aitmpl-claude-code-plugins-directory.md]
confidence: high
contested: false
contradictions: []
---

# Claude Code Plugins & Marketplaces Ecosystem

**AITMPL Directory:** 34 major plugin collections, 400K+ total skills across all platforms.

A comprehensive ecosystem of Claude Code extensions, including skills, agents, commands, hooks, and MCPs. Most collections work across Claude Code, Codex, Cursor, Hermes, and other AI coding agents.

## Architecture Overview

```
Claude Code Plugins Ecosystem
│
├── Tier 1: Foundational Systems (100K+ stars)
│   ├── ECC (229K) — Agent harness, memory, skills
│   └── Claude Mem (87K) — Cross-session context
│
├── Tier 2: Official & Community (10K-50K stars)
│   ├── Claude Plugins Official (32K) — Anthropic directory
│   ├── Claude HUD (26K) — Agent monitoring
│   └── Knowledge Work Plugins (23K) — Knowledge worker tools
│
├── Tier 3: Specialized (1K-5K stars)
│   ├── Claude Skills (22K) — 345 multi-domain skills
│   ├── Playwright Skill (2.9K) — Browser automation
│   └── Claude Code Plugins Plus Skills (2.5K) — 425 plugins
│
└── Tier 4: Emerging (< 1K stars)
    ├── Flow Next (657) — Agentic engineering workflows
    ├── Cartographer (604) — Codebase mapping
    └── Cohesivity Plugin (0) — Backend services
```

## Top Collections by Stars

| Collection | Stars | Specialization |
|------------|-------|----------------|
| ECC | 229K | Agent harness, skills, memory, security |
| Claude Mem | 87K | Cross-session persistent context |
| Claude Plugins Official | 32K | Official Anthropic-managed directory |
| Claude HUD | 26K | Agent monitoring, context usage display |
| Compound Engineering | 23K | Official Compound Engineering skills |
| Knowledge Work Plugins | 23K | Knowledge worker tools |
| Claude Skills | 22K | 345 skills across 9 domains |
| Claude Octopus | 3.8K | Multi-agent (up to 8 models per task) |
| Buildwithclaude | 3.2K | Hub for skills, agents, commands |
| Playwright Skill | 2.9K | Browser automation testing |
| Claude Code Plugins Plus | 2.5K | 425 plugins, 2,810 skills |
| Flow Next | 657 | Adversarial reviews, durable specs |
| Cartographer | 604 | Codebase mapping with subagents |
| ML Research | 2 | Hugging Face ML engineering (SFT/DPO/GRPO/LoRA) |

## Plugin Types

| Type | Use Case | Example Collections |
|------|----------|---------------------|
| **Skills** | Reusable capabilities | Claude Skills (345), ECC, Agent Skills |
| **Agents** | Autonomous workflows | Agentsys (49 agents), Cartographer, Claude Octopus |
| **Commands** | Slash commands | Claude HUD, Claude Notifications Go |
| **Hooks** | Lifecycle events | Claude Review Loop, Claude Forge |
| **MCPs** | External integrations | Pg Aiguide, Pinion OS, Cohesivity |

## Top Picks for Your Use Case

### Must-Have

**1. ECC (229K stars)** — [[ECC]] (already in your vault!)
- Skills, agents, memory system, security hooks
- Works with Hermes (your current environment)
- Perfect for expanding agent capabilities

**2. Claude Skills (22K stars)** — Massive skill library
- 345 skills across 9 domains (engineering, research, compliance, finance, marketing, product, C-level advisory, business operations, productivity)
- CLI package manager available
- Works with Claude Code, Codex, Gemini CLI, Cursor

**3. Claude Mem (87K stars)** — Cross-session persistence
- Captures everything your agent does during sessions
- Compresses with AI and injects relevant context into future sessions
- Works with Claude Code, OpenClaw, Codex, Gemini, Hermes, Copilot, OpenCode

### Useful for Specific Projects

| Project | Recommended Plugin | Why |
|---------|-------------------|-----|
| **Arabic Tracing Game** | Claude Skills (UI/UX), Playwright Skill | Testing automation, UI components |
| **Computer Vision Pipeline** | ML Research, Agent Skills (HashiCorp) | ML engineering, infrastructure automation |
| **Robotics/Arduino** | HashiCorp Agent Skills, Agentsys | Multi-agent coordination, infra management |
| **Documentation** | Cartographer | Codebase mapping with AI subagents |
| **Testing** | Playwright Skill | Model-invoked browser automation |
| **Workflow Automation** | Flow Next | Adversarial cross-model reviews, durable specs |

## Integration Recommendations

1. **Start with ECC** — You already have it; master its skills system
2. **Add Claude Mem** — Get persistent memory across your Hermes sessions
3. **Add Claude Skills** — 345 reusable skills for common tasks
4. **Explore specialized** based on active project:
   - ML Research for computer vision
   - Playwright Skill for test automation
   - Cartographer for project documentation

## Quick Install Pattern

Most collections follow the same pattern:
```bash
/plugin marketplace add <collection-name>
```

Then access skills, agents, and commands directly in Claude Code.

## Cross-References

- [[ECC]] — Already in your vault (agent harness)
- [[01 Technical Skills]] — Python, JavaScript, automation
- [[02 Projects]] — Apply plugins to your builds
- [[technical_skills_knowledge_base]] — System integration

---

*Updated: 2026-09-20*  
*Ecosystem size: 34 major collections, 400K+ combined skills*  
*Best for: Extending Claude Code, Hermes, Cursor, and other agents*  
*Your entry point: ECC (already integrated)*
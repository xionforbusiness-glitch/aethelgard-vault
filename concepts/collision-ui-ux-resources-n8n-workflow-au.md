Instant SDUI Stream]
        A11y -->|Git Workflow| GitNode[n8n Git / GitHub Node: Auto-PR to Design System]
        A11y -->|Fail| RuleEngine
    end
```

---

## Core System Components

### 1. Headless Design-Token Engine (UI UX Pro Max Adapter)
The UI UX Pro Max Skill repository provides 192 design reasoning rules (covering typography hierarchies, contrast bounds, micro-interaction states, and responsiveness paradigms) combined with 79 search-indexed UI archetypes. 

We wrap these heuristics within an **n8n Custom Function Node (Python/NodeJS runtime)**, enabling the workflow to pass standard operational payloads (e.g., "SaaS billing threshold reached, prompt upgrade") and automatically derive:
- Archetype selection (e.g., `modal-feature-gate-glassmorphic`)
- Color palette constraints (Tailwind-compatible variables mapped to system state)
- Spatial geometry matrix (margins, padding, touch-target scales)

### 2. The n8n Graph Execution Pipeline
The n8n visual engine manages end-to-end lifecycle orchestration:
- **Webhook Listener Node**: Receives event signals from backend systems or user activity.
- **Code Node (Style Extractor)**: Queries the Pro Max Rule Engine for appropriate component tokens based on accessibility profiles and screen constraints.
- **LangChain / AI Agent Node**: Runs Claude 3.7 / Claude Code locally to assemble declarative SDUI components conforming to the designated UI archetype.
- **Validation Sandbox Node**: Runs a headless CLI step (via `Execute Command` or Dockerized environment) validating the emitted component tree against Tailwind schemas and `@axe-core/puppeteer` accessibility audits.
- **Response / Webhook Target**: Either streams JSON-SDUI back to mobile/web clients in real-time or issues a commit directly to the repo.

---

## Implementation: n8n Workflow Configuration

### Step 1: Ingest Intent & Match Archetype (n8n Code Node)

```javascript
// n8n Code Node: Ingest & Archetype Matching
const input = $json.event_payload;

// Map inbound backend event to UI UX Pro Max rule heuristics
function resolveStylePattern(event) {
  if (event.type === 'CHECKOUT_BLOCKED') {
    return {
      archetypeId: 42, // 'urgent-action-modal'
      density: 'compact',
      contrastRatio: 'AAA',
      style: 'neo-brutalist-clean',
      maxTokens: 1200
    };
  }
  return {
    archetypeId: 11, // 'minimal-dashboard-card'
    density: 'standard',
    contrastRatio: 'AA',
    style: 'modern-glass',
    maxTokens: 800
  };
}

const archetype = resolveStylePattern(input);

return {
  json: {
    archetype,
    context: input,
    systemPrompt: `You are an automated SDUI compiler running with UI-UX-Pro-Max heuristics. 
Apply Rule-Set: ${archetype.archetypeId} (${archetype.style}). Contrast: ${archetype.contrastRatio}. 
Output valid JSON schema for Server-Driven UI.`
  }
};
```

### Step 2: Python Compiler Node for Axe-Core & Structural Validation

```python
# n8n Python Node: Validation & AST Verification
import json

sdui_payload = _input.first().json.get("generated_sdui")

def validate_schema(node):
    required_keys = {"type", "props", "children", "accessibility"}
    if not required_keys.issubset(node.keys()):
        return False
    
    # Assert minimum tap-target sizing according to Pro Max heuristics
    if node.get("type") in ["Button", "Input"]:
        size = node.get("props", {}).get("min_height", 0)
        if size < 44:  # Rule 88: Minimum 44px tap target
            return False

    for child in node.get("children", []):
        if not validate_schema(child):
            return False
            
    return True

is_valid = validate_schema(sdui_payload)

return [{"json": {"is_valid": is_valid, "validated_payload": sdui_payload}}]
```

---

## Edge Case Handling & Fallbacks
1. **Accessibility Non-Compliance**: If Axe-Core detects contrast violations ($CR < 4.5:1$), the n8n router rejects compilation and triggers an inner retry loop incrementing token luminances along the Tailwind color vector.
2. **Deterministic UI Fallback**: When LLM output fails schema validation twice, n8n invokes a pre-compiled static fallback AST corresponding to the requested UI style index, avoiding interface downtime.

## Cross-Domain Synergy Summary
- **UI/UX Pro Max Skill** eliminates aesthetic hallucinations and accessibility bugs by providing rigid, codified UI heuristics.
- **n8n Automation** supplies the zero-friction, scalable event pipe, turning static styling knowledge into a live, self-adjusting UI delivery middleware.
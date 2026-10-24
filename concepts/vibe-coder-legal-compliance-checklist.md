---
title: "The Vibe Coder's Legal & Compliance Checklist (Don't Get Sued Playbook)"
created: 2026-10-24
updated: 2026-10-24
type: concept
tags: [vibecoding, compliance, legal, gdpr, privacy-policy, webdev, terms-of-service, appsec, accessibility]
sources: [baroobi.inc Facebook Reel 1616035636923477]
confidence: high
contested: false
contradictions: []
---

# ⚖️ The Vibe Coder's Legal & Compliance Checklist (Don't Get Sued Playbook)

> **"Hey Claude / Cursor, I don't want to get sued, so add the following."**  
> Operational compliance checklist for AI-generated applications, SaaS projects, and vibe-coded MVPs to protect against regulatory fines (GDPR/CCPA), ADA accessibility lawsuits, and deceptive business practice penalties.

---

## ⚡ The Compliance Blindspot in AI Apps

When developers build apps rapidly with AI coding assistants (Claude Code, Cursor, Lovable, v0), the AI focuses exclusively on features and UI. It completely neglects legal disclosures, consent flows, asset licensing, and accessibility requirements.

If you deploy publicly without these protections, your application is exposed to immediate legal liability and automated crawler scans looking for non-compliance.

---

## 📋 The Master Compliance Audit Matrix

```
┌────────────────────────────────────────────────────────────────────────┐
│                   THE VIBE CODER LEGAL AUDIT MATRIX                    │
├───────────────────┬────────────────────────────────────────────────────┤
│ 1. Legal Policies │ Privacy Policy, Terms of Service, Refund, Cookies  │
│ 2. Data Minim     │ Don't collect data you don't need; prune SDKs      │
│ 3. User Rights    │ Automated data deletion requests & Unsubscribe     │
│ 4. No Deception   │ Drop dark patterns, hidden fees & fake testimonials│
│ 5. Accessibility  │ WCAG 2.1: Alt text, color contrast, keyboard nav   │
│ 6. Asset License  │ Audited commercial rights for fonts, icons & images│
└───────────────────┴────────────────────────────────────────────────────┘
```

---

### 1. Mandatory Legal Pages & Consent
* **Privacy Policy:** Must disclose what personal data is collected, how it is processed, third-party analytics/processors (Stripe, PostHog, Google Analytics), and storage duration.
* **Terms of Service (ToS):** Limitation of liability, dispute resolution, governing jurisdiction, and acceptable use rules.
* **Refund & Cancellation Policy:** Explicit terms for subscriptions, chargebacks, and refund eligibility.
* **Cookie Policy & Consent Banner:** Must provide explicit opt-in (especially for EU/UK traffic under GDPR/ePrivacy Directive) before firing marketing or tracking scripts.

### 2. Data Minimization & SDK Audits
* **Collect Only What You Need:** Stop storing full IP addresses, device fingerprints, or unnecessary user demographics unless essential to core functionality.
* **Third-Party SDK Auditing:** Inspect client bundles to ensure third-party analytics libraries aren't leaking sensitive form input or user tokens.

### 3. User Rights & Data Deletion
* **Right to be Forgotten (Data Deletion):** Provide a user-facing button or clear email endpoint (`support@...` or `privacy@...`) allowing users to request complete deletion of their account and database records.
* **CAN-SPAM / GDPR Email Compliance:** Every transactional and marketing email must include a single-click **Unsubscribe link** and a physical/registered business mailing address.

### 4. Consumer Protection (Zero Dark Patterns)
* **No Hidden Fees:** Pricing must clearly state subscription renewal cadence and taxes before checkout.
* **No Fake Social Proof:** Drop generated fake reviews, fictitious countdown timers ("Only 2 seats left!"), or misleading claims that violate FTC guidelines.

### 5. Accessibility & Inclusivity (ADA / WCAG Compliance)
* **Keyboard Navigation:** Full focus trap management and ability to navigate interactive elements via `Tab` and `Enter`.
* **Color Contrast:** Minimum 4.5:1 contrast ratio for normal text and 3:1 for large text.
* **Alt Text:** Descriptive `alt=""` attributes on all meaningful images, diagrams, and media.

### 6. Asset & Intellectual Property Licensing
* **Commercial Font Licenses:** Verify web fonts aren't using desktop-only or personal-use-only licenses (e.g., using verified Google Fonts or paid commercial web font licenses).
* **Licensed Media:** No ripped unsplash/stock images without proper commercial attribution or licensing.

---

## 👑 The Copy-Paste Prompt for AI Coding Assistants (Claude Code / Cursor)

When finalizing an AI-built application, prompt your agent with:

```text
Act as a Web Compliance and Legal Operations Auditor. Review our application to ensure it follows standard global compliance (GDPR, CCPA, FTC guidelines, and WCAG accessibility standards).

Implement or verify the following requirements:
1. Legal Policies: Generate boilerplate Privacy Policy, Terms of Service, Cookie Policy, and Refund Policy pages customized to our business name and domain.
2. Consent Banner: Add a lightweight, accessible cookie consent banner that only enables non-essential tracking upon user acceptance.
3. User Data Rights: Create a functional 'Delete My Account and Data' flow in settings that purges user rows from our database.
4. Email Compliance: Ensure all email templates include our registered business address and an unsubscribe link.
5. Accessibility Audit: Scan our components for missing image alt text, low color contrast, and ensure all buttons and dialogs are fully keyboard-navigable.
6. Transparency: Verify that checkout pricing displays recurring renewal terms clearly with zero dark patterns.

Flag any third-party SDKs or exposed tracking scripts that collect excessive user telemetry.
```

---

## 🔗 Related Notes & Vault Assets

* [[concepts/vibe-coder-security-fix-kit|The Vibe Coder's Security Fix Kit (AppSec Hardening)]]
* [[concepts/unlazy-anti-laziness-agent-skill|Unlazy: Completion Discipline Skill]]
* [[concepts/ai-red-teaming-and-llm-hacking-playbook|AI Red Teaming Playbook]]
* [[01 Technical Skills|Technical Skills Knowledge Base]]
* [[log|Operational Log]]

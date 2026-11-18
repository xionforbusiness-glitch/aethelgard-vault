---
title: "FinStek Interview Debrief & Technical Growth Plan"
aliases: [FinStek Interview Debrief, Misha Interview Review]
tags: [interview, career, finstek, retrospective, cpp, debugging, technical-support]
created: 2026-11-18
company: FinStek
interviewer: Misha (PhD in Computer Science, UK)
role: Technical Support & Front-End Developer
outcome: Rejected (Need stronger coding, algorithms, and debugging fundamentals)
---

# FinStek Interview Debrief — 2026-11-18

**Company:** [[finstek|FinStek]] (`finstek.com`)  
**Role:** Technical Support & Front-End Developer  
**Interviewer:** Misha (PhD in Computer Science, UK)  
**Outcome:** Not selected at this stage — candid, high-value feedback provided directly by Misha.

---

## 1. Interview Breakdown (Question by Question)

### Q1. Academics & Preferred Languages -> Live Coding Task
- **What happened:** After discussing degrees and CGPA, Misha asked for Omar's most comfortable programming languages. Omar answered **C++ and JavaScript**. Misha then asked for a simple live coding exercise: **parse a string (e.g., `"900"`) into an integer output**.
- **Result:** Froze and admitted inability to code it live because Omar hadn't written C++ in ~2 years and had focused on packet/network analysis and cybersecurity instead of hands-on coding.
- **Root Lesson:** Never claim a language as "most comfortable" unless you can write basic I/O, loops, and string/integer parsing in it cold without AI.
- **Reference Solution (C++):**
  ```cpp
  #include <iostream>
  #include <string>

  int main() {
      std::string s = "900";
      int num = std::stoi(s); // Built-in approach

      // Manual algorithmic approach (what interviewers love to see):
      int manual = 0;
      for (char c : s) {
          if (c >= '0' && c <= '9') {
              manual = manual * 10 + (c - '0');
          }
      }
      std::cout << manual << std::endl;
  }
  ```

### Q2. Technical Support — Site Works for You, Fails for Customer
- **Question:** A customer reports the website isn't working on their end, while it works fine on yours. What do you do?
- **Omar's Answer:** Suggested checking DevTools (overcomplicated it; missed basic client-side isolation first).
- **What Misha Expected (Start Simple -> Escalate):**
  1. Clear browser cache / cookies or test in **Incognito/Private mode**.
  2. Test another browser or device/network.
  3. Check local **firewall**, antivirus, ad-blockers, or **VPN / proxy** interference.
  4. *Then* inspect browser DevTools (Console/Network) or DNS/ISP routing if the simple checks fail.

### Q3. Technical Support — Invalid Credentials for One Specific User
- **Question:** One specific user gets "invalid credentials." What could be wrong, and what about the **backend**?
- **Omar's Answer:** Covered client-side well (incognito/cache, OAuth token glitch, typo or wrong keyboard language). Blanked when Misha asked **"What about the backend?"**
- **What to Check on the Backend Next Time:**
  1. **Database user record:** Does the account exist? Is it locked, suspended, unverified, or soft-deleted? Check trailing spaces or email case sensitivity.
  2. **Auth / Server Logs:** Inspect the exact auth failure code (wrong password hash vs. expired session vs. account lockout after too many failed attempts).
  3. **Rate limiting / IP block:** Did the user trigger brute-force protection?
  4. **Service sync / DB replication:** Did a recent password reset fail to propagate across auth/CRM/trading servers, or did a hashing/encoding mismatch occur?

### Q4. Security Verification — Password / Email Change Call
- **Question:** A customer calls asking to change their password or email. What do you do?
- **Omar's Answer:** Authenticate the caller first via **OTP**, identity document / SSN (if on file), or verified address details.
- **Result:** **Strong pass** — Misha accepted this cleanly.

### Q5. Portfolio Projects — Aethelgard & Iman Gadzhi Project
- **What happened:**
  - Misha dismissed Aethelgard as "basic stuff anyone can do" with AI.
  - On the Iman Gadzhi project, Misha asked if it was live (1–2 days before shutting down due to cost) and asked **"What language was it written in?"** Omar answered **"I don't know, my agent built it."**
- **Misha's Core Challenge:** *"You have AI to code, but what if it fails? How are you going to debug it?"*
- **Root Lesson:** Using AI agents is fine, **not knowing the language, architecture, or how to debug your own project is an instant disqualifier**. Never mention any project in an interview unless you can explain its exact tech stack, data flow, and manually read/debug its code.

---

## 2. Honest Assessment — Strengths vs. Real Gaps

### What Worked
- **Radical honesty & composure:** Did not fake or bluff when stuck.
- **Security instincts:** Immediately thought of OTP and multi-factor identity verification on account-change requests.
- **Networking / OS foundation:** Solid mental model of TCP/IP, packets, firewalls, and system infrastructure.

### Critical Gaps Exposed (No Sugarcoating)
1. **Live coding fluency:** Cannot yet write elementary string/integer algorithms without AI assistance.
2. **Backend support mental model:** Comfortable on the client/network side, but blanked on backend auth/DB failure checks.
3. **AI-dependency vs. Code Ownership:** Admitting *"I don't know what language my project used"* immediately tells a technical lead you cannot debug production failures when AI breaks.
4. **Overcomplicating L1 triage:** Jumped straight to DevTools instead of starting with cache/incognito/firewall/VPN basics.

---

## 3. Concrete 30-Day Remediation Plan (Misha's Exact Roadmap)

1. **C++ & Core Coding Fluency (30–45 min/day, NO AI):**
   - Practice writing from scratch: string parsing (`stoi`, manual digit loop, reversing strings, palindromes), arrays/vectors, hash maps (`std::unordered_map`), pointers/references, and basic file/stdin I/O.
   - Solve 25–30 Easy problems on LeetCode / HackerRank in **C++ or JavaScript** strictly by hand.
2. **Master Basic Algorithms & Data Structures:**
   - Time/space complexity (`O(1)`, `O(n)`, `O(n log n)`), arrays, hash maps, stacks/queues, binary search, and basic recursion. (See [[data_structures_asymptotic_complexity]]).
3. **Technical Support Triage Checklist (Client -> Network -> Backend -> DB):**
   - Drill the 4-layer troubleshooting ladder for every support scenario: **1) Client/Browser** (cache, incognito, keyboard/typo) -> **2) Network** (firewall, VPN, DNS, DevTools) -> **3) Backend/Auth** (logs, rate limits, tokens, sync) -> **4) Database** (user state, lock flags, data integrity).
4. **Full Ownership of Every Listed Project:**
   - Before any future interview, read through the core source files of every project on your CV (`antigravity_proxy.py`, `run.py`, etc.) and be able to explain the exact language, entry point, database schema, and how you personally debugged a real bug.

---

## Related Notes
- [[01 Technical Skills]]
- [[02 Projects]]
- [[03 Work Experience]]
- [[data_structures_asymptotic_complexity]]

# Take Home Assignment - Vendor Research Tool

# **SignalCore — Engineering Evaluation**

## **Overview**

Build a working prototype that compares technology vendors against a set of requirements using publicly available data.

**Time budget:** 2–3 hours
**Deliverable:** A working web application with source code, plus a brief write-up of your approach
**Follow-up:** 45-minute Zoom conversation to discuss your work

## **The Problem**

An AI engineering team is selecting an **LLM observability platform** to monitor, trace, and evaluate their production LLM applications. They're running a mix of RAG pipelines and multi-step agents, and need to compare vendors before committing.

**Vendors to evaluate:**

- **LangSmith** — LangChain's commercial observability platform
- **Langfuse** — Open-source (MIT) LLM observability platform
- **Braintrust** — Managed evaluation and observability platform
- **Posthog** — A broader platform that includes LLM observability

**Requirements to evaluate against:**

| # | Requirement | Priority |
| --- | --- | --- |
| 1 | Framework-agnostic tracing (not locked into LangChain or any single framework) | High |
| 2 | Self-hosting option with full data sovereignty | High |
| 3 | Built-in evaluation framework (LLM-as-judge, custom metrics, regression testing) | High |
| 4 | OpenTelemetry support for integration with existing observability stack | Medium |
| 5 | Prompt management and versioning with rollback capability | Medium |
| 6 | Transparent, predictable pricing at scale (100K+ traces/month) | Low |

## **What We're Looking For**

Build a web application that:

1. **Collects evidence** — The application should *do the research itself*, not just display a pre-filled comparison. Go beyond what an LLM already knows by programmatically pulling from vendor documentation, GitHub repos, comparison sites, community discussions, or any other public sources. This space moves fast and LLM training data goes stale quickly. We care about *where the information came from* and *how recent it is*.
2. **Scores vendors against requirements** — Design a scoring methodology. There's no single right answer here, but your approach should be transparent and defensible. How do you handle requirements where public evidence is strong for one vendor but sparse for another?
3. **Presents results through a usable UI** — A user should be able to understand not just *which* vendor scored highest, but *why*, and how confident they should be in that assessment.

## **Guidelines**

- **Use any tech stack** you're comfortable with.
- **Using AI tools is encouraged** — Claude Code, Cursor, Codex, whatever you prefer. We're interested in how you work with AI, not whether you avoid it. Please save notable prompts or a brief log of how you used AI during the exercise.
- **Scope aggressively.** Three hours isn't much. A focused prototype that does one thing well beats a sprawling app that does everything poorly. Tell us what you'd build next if you had more time.
- **Ship something that runs.** Include a README with setup instructions. We'll be running it locally.

## **What to Submit**

1. **Source code** in a Git repository (GitHub, GitLab, or zip)
2. **README** with setup/run instructions
3. **Brief write-up** (can be in the README) covering:
    - Your approach and key decisions
    - How you used AI tools — what worked, what didn't, where you intervened
    - What you'd improve with more time

## **What We'll Discuss on the Zoom**

Come prepared to talk about:

- **Architecture choices** — Why did you structure the system the way you did? What would change if this needed to scale to 50 vendors and 200 requirements?
- **Scoring methodology** — How did you handle varying evidence quality? What are the failure modes of your approach?
- **AI in your workflow** — Where did AI accelerate you? Where did it lead you astray or need correction? How did you validate AI-generated output?
- **Product thinking** — If this were a real product feature, what would the next iteration look like?

---

*We respect your time. If something in this assignment is unclear, make a reasonable assumption, document it, and move on. We'd rather see how you handle ambiguity than have you blocked waiting for a reply.*
# From Ideation to Scale: Building AI Products in the Real World

## Overview

This repository contains presentation slides used at **Imperial College London** to walk students through a real-world product development journey. The case study follows **Rufus**, Amazon's GenAI-powered shopping assistant — from an initial leadership bet on large language models, through launch, scaling challenges, and global expansion. The slides are built using the [WebSlides](https://webslides.tv/) framework and can be viewed by opening `index.html` in any modern browser.

---

## A narrative grounded in the development of Amazon Rufus

### THE VISION

Rufus did not begin with a customer complaint. It began with a leadership bet — a top-down conviction that large language models would fundamentally change how people shop. This is an unusual origin for a product, and it shaped everything that followed. The PM's first job was not to decide whether to build it, but to figure out what "it" actually was.

Amazon's PR/FAQ mechanism was the instrument that forced clarity. Before a single line of code was written, the team had to draft the customer press release: what would Rufus do, for whom, and how would we know it had worked? That discipline — working backwards from the customer experience rather than forwards from the technology — is what separates Amazon's approach to product development from most others. Even when leadership has already placed the bet, the PR/FAQ ensures the team earns the right to build by articulating the value first.

### THE BUILD

The product that launched was not the product that was designed at first. A/B testing rewrote Rufus's direction multiple times. This is not a failure of planning — it is the intended outcome of a culture that treats data as the final arbiter. The team's job was not to be right; it was to be wrong quickly and cheaply, then iterate towards something that actually worked.

Scope discipline was the hardest early decision. The instinct when building something new — especially something backed by an LLM with broad capability — is to solve everything at once. The strategic choice was to start narrow: one query type, one use case, done well. That constraint created the conditions for learning. Alexa launched with thirteen skills. Rufus launched with a deliberate focus. Breadth comes later, earned by demonstrating depth.

### THE LAUNCH FAILURE NOBODY EXPECTED

When Rufus launched in beta, the team anticipated debugging model quality — wrong answers, hallucinations, confidence miscalibration. What they did not anticipate was simpler and stranger: customers opened the chat interface and froze. They did not know what to type. The mental model for an AI shopping assistant did not yet exist in customers' heads.

The fix was not a model retrain. It was a UI redesign — suggested prompt chips that taught customers the language of the product. This is the lesson that defines AI product development: the interface and the model are one system. A brilliant model wrapped in a confusing interface is a failed product. You are not building a technology; you are building a conversation. Design it accordingly.

### WHAT SCALE ACTUALLY MEANS

Most people think scaling means more servers. It does not. Scaling means your product works brilliantly for ten million different people, in ten different countries, with ten different expectations — without you in the room. Rufus encountered five distinct scaling walls, each requiring a different kind of solution.

Technical scale was the baseline requirement — latency that held under real shopping traffic, because customers do not wait. Evaluation at scale demanded a north star metric: conversion lift after Rufus interactions became the measure that mattered. But at millions of queries per day, human review is impossible. Automated evaluation infrastructure — AI judging AI — is not optional; it is foundational, and it must be built before it is needed. Guardrails presented the hardest internal tension: how much to constrain what Rufus could say versus letting it be genuinely useful. Too constrained and the product is useless. Too open and the brand risk is unacceptable. This calibration never fully resolves — it is remade every sprint. The practical starting point is conservative: earn the right to expand. Rollback and resilience were tested in production when a model update caused a quality regression. The rollback mechanism worked. What the incident exposed was a gap in the evaluation pipeline — the regression reached users before it was caught. Rolling back code is straightforward; rolling back learned behaviour is not. The lesson the team took forward was this: your ability to detect problems matters as much as your ability to fix them. Finally, culture and compliance proved that retrofitting is harder than it sounds. Rufus launched US-first. Expanding to other markets was not a translation exercise — it was a product rebuild. Shopping behaviour, trust patterns, and communication norms differ fundamentally across markets. What reads as helpful in the US can read as presumptuous in Japan. GDPR means EU customer data cannot flow through the same pipelines as US data. These constraints are not obstacles to innovation; they are the shape of the problem.

### FIVE TRUTHS TO TAKE FORWARD

- **Keep it narrow.** Scope is a strategic choice, not a failure of ambition.
- **The interface is the product.** Design the conversation, not just the capability.
- **A/B tests will rewrite your product.** Build a culture that follows the data, not the plan.
- **Build evaluation infrastructure before you need it.** Detection is as important as the fix.
- **Constrain vs. utility is never resolved.** Start conservative. Earn the right to expand.

---

## FREQUENTLY ASKED QUESTIONS

**How do you know when an AI product is ready to ship?**
There is no perfect. You define minimum confidence thresholds across quality, latency, and safety — then the bar moves as you learn. Perfectionism at launch is a form of avoidance.

**Who owns quality — PM, engineer, or data scientist?**
All three, simultaneously. That ambiguity is not a process failure; it is the actual structure of the problem. The org design challenge is making that shared ownership productive rather than diffuse.

**What if A/B test results are noisy?**
Layer your signals. Rufus combined conversion data, human quality scores, and latency metrics. No single signal is sufficient. Confidence comes from convergence across multiple independent measures.

**How do you balance speed with safety?**
Constrain scope early and expand carefully. A narrow launch is not a failure of ambition — it is a strategy for earning the trust that makes broader expansion possible.

**What happens when the model gives wrong answers at scale?**
Triage, rollback, root cause, fix the evaluation gap, redeploy. The runbook matters as much as the fix. If you cannot execute a rollback in under thirty minutes, your deployment process needs work.

**Does GDPR actually stop innovation?**
It slows shortcuts, not innovation. Good data architecture handles compliance from the start. The cost of retrofitting data pipelines for GDPR compliance after the fact is far higher than designing for it upfront.

**How did Amazon decide to build Rufus rather than buy?**
The decision hinged on data moat and differentiation. Amazon's proprietary shopping behaviour data was the competitive advantage — a third-party model trained on generic data could not replicate it. Build vs. buy is always a bet on where your defensible advantage actually lives.

---

## APPENDIX

### A. The PR/FAQ Framework

Amazon's working-backwards mechanism requires teams to write the customer press release and an internal FAQ before any engineering begins. The press release describes the finished product from the customer's perspective — what it does, who it is for, and why it matters. The FAQ addresses the hard questions: what are the risks, what could go wrong, what does success look like? The discipline of answering these questions before building is what separates well-scoped products from those that drift. For Rufus, this mechanism was used even under a leadership mandate — translating top-down vision into bottom-up clarity.

### B. Evaluation Architecture

Rufus used three evaluation layers in combination: (1) Conversion lift — did customers who interacted with Rufus purchase more? This was the north star business metric. (2) Human quality raters — structured evaluation of model outputs against defined quality criteria, used to catch regressions that conversion data might miss or lag. (3) Latency and technical performance metrics — response time under production load, error rates, and infrastructure health. The critical lesson from the production regression incident was that automated evaluation infrastructure must be built before it is needed. Relying on manual review or lagging business signals is insufficient at scale.

### C. Guardrail Risk Tiers

Not all AI outputs carry equal risk. A practical tiering approach: Low-risk queries (product information, general comparisons) require minimal guardrails and can be processed with standard validation. Medium-risk outputs (subjective recommendations, category-level comparisons) require rule-based validators and ML classifiers, with responses held for validation before delivery. High-risk scenarios (health-adjacent products, financial implications, legally sensitive categories) require full multi-layer validation, no streaming, and in some cases human review before delivery. The guardrail tier applied to any given query should be determined programmatically by a risk classifier, not by manual curation — manual curation does not scale.

### D. Rollback Runbook

The production regression on Rufus established the template for subsequent incidents: (1) Alert — automated monitoring detects quality signal degradation. Threshold breach triggers immediate notification. (2) Triage — on-call engineer confirms the regression is model-related, not infrastructure-related. Traffic is not reduced at this stage unless user impact is severe. (3) Rollback — revert to the previous stable model version using the deployment mechanism. Target: under thirty minutes from alert to rollback. (4) Root cause — review the evaluation pipeline to identify why the regression was not caught pre-deployment. This is the most important step. (5) Communicate — internal stakeholder update within two hours; customer-facing communication if user impact was material. (6) Fix and redeploy — address both the model issue and the evaluation gap before re-attempting the update.

### E. Global Expansion Considerations

Rufus launched in the US and subsequently expanded to additional markets. The key learning from that process: localisation is not translation. The following dimensions each require market-specific work: (1) Query behaviour — customers in different markets have different search vocabularies, different levels of specificity, and different expectations of what an AI assistant should do. (2) Trust signals — what constitutes a credible recommendation varies significantly by market. (3) Communication tone — directness that feels helpful in the US can feel presumptuous in Japan; hedging that feels polite in the UK can feel evasive in Germany. (4) Data architecture — GDPR and equivalent regulations in other markets require data to be processed and stored within specific geographic boundaries. This is not a configuration change; it is a separate infrastructure build. Plan for it from the start, not as a retrofit.

### F. Suggested Discussion Questions for Students

1. If your CEO told you tomorrow to build an AI product in your domain, what is the first question you would ask — and why?
2. Think of an AI product you use regularly. Where do you think the guardrail line is drawn? Do you think it is in the right place?
3. What would a PR/FAQ for a product you want to build look like? What is the hardest question in the internal FAQ section?
4. If you had to choose between launching a product that is 80% quality in two months, or 95% quality in six months, which would you choose — and what conditions would change your answer?
5. Where does the data moat in your industry live? Who owns it, and what does that mean for build vs. buy decisions in AI?

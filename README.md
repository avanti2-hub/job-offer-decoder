---
title: Job Offer Decoder
emoji: 🛡️
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
tags:
  - openenv
  - reinforcement-learning
  - legal
  - india
---
# Job Offer Decoder
### *An RL Environment That Trains AI To Read What Freshers Can't*

[![OpenEnv](https://img.shields.io/badge/OpenEnv-Compatible-blue)](https://github.com/meta-pytorch/OpenEnv)
[![HuggingFace](https://img.shields.io/badge/🤗-Spaces-yellow)](https://huggingface.co)
[![Python](https://img.shields.io/badge/Python-3.11-green)](https://python.org)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-orange)](LICENSE)

---

## A fresher signed an offer letter last week.

She had two job offers. One paid ₹12 LPA, one paid ₹10 LPA. She picked the higher one — obviously.

Six months later she tried to quit. The company handed her a bill for ₹1,50,000.

She had signed a training bond. It was in paragraph 4, clause 3(b), buried between the leave policy and the medical insurance section. Written in eight lines of legal language she had never seen before. She didn't know what "liquidated damages" meant. Nobody told her.

She couldn't pay. She couldn't leave. She worked there for another 18 months — miserable, trapped, and underpaid — because she signed something she didn't understand.

**This happens to hundreds of thousands of Indian freshers every single year.**

---

## The Actual Problem

India produces **50+ lakh graduates annually.** Almost none of them have access to legal advice when signing their first job offer. A lawyer costs ₹5,000–15,000 per hour. Their parents don't understand modern CTC structures. Their college placement cells are incentivized to push acceptances, not protect students.

So freshers read the salary number, feel excited, and sign.

What they miss:

**The bond clause** — disguised as a "Human Capital Investment Covenant" or "Organizational Commitment Undertaking." Written in 150 words of dense legal prose. Means: pay us ₹75,000 to ₹2,00,000 if you leave before 18–36 months.

**The CTC inflation** — a ₹12 LPA offer that includes Employer PF (not your money), Gratuity (only after 5 years), Performance Bonus (only if 6 simultaneous conditions are met), and Medical Insurance (paid to insurer, not you). Real in-hand: ₹45,700/month. Not ₹1,00,000.

**The fake increment** — "30% hike after one year!" sounds like ₹2.4L raise on a ₹8L CTC. The offer letter says increment is calculated on Basic Salary only (₹3L). Real raise: ₹90,000. The candidate never reads that line.

**The IP trap** — "All work product created during employment, whether or not during working hours, whether or not using personal equipment, shall vest exclusively in the Company." The fresher who codes on weekends, who has a startup idea, who freelances on Sundays — just gave all of it away. Forever. Including for 12 months after they leave.

**The arbitration trap** — disputes must be resolved in Delhi. Arbitrator appointed by the company. Employee works in Pune. To fight for their rights, they must travel 1,400km, hire a Delhi lawyer, face an arbitrator the company chose. The clause is designed to make fighting back economically impossible.

**The garden leave** — 90-day notice period. Company can impose garden leave: candidate sits at home, receives salary, cannot join any new employer. Then a 24-month non-compete begins. Total time before the candidate is truly free after resigning: **27 months.**

Not one of these is illegal. Every single one is in real offer letters being signed by real freshers right now.

The tragedy is not that companies do this. The tragedy is that **a single reading by someone who knows what to look for would catch all of it in minutes.**

That reader doesn't exist for most freshers. Until now.

---

## What We Built

`job-offer-decoder` is a **multi-step Reinforcement Learning environment** built on the [OpenEnv](https://github.com/meta-pytorch/OpenEnv) framework by Meta PyTorch.

It trains AI agents to do exactly what that missing expert reader would do — systematically, accurately, and in seconds.

The environment presents an AI agent with realistic Indian job offer letters written in actual legal language. The agent must work through three cognitive stages that mirror how a real employment lawyer thinks:

**Stage 1 — See everything.**
Read the entire document. Find every clause that could harm the candidate. Not just the obvious ones — the ones buried in sub-clauses, disguised in neutral language, hidden inside definitions sections.

**Stage 2 — Quantify the damage.**
For every harmful clause found, calculate the exact rupee impact. How much is the bond penalty? What is the real monthly in-hand salary after removing non-cash and conditional components? How much money does the candidate lose during probation? What is the realistic variable pay after applying all conditions?

**Stage 3 — Tell them what to do.**
Give a verdict. Identify the three most dangerous clauses in priority order. Specify exactly what to demand from the company. Reference the Indian laws that protect the candidate. Tell them what to do if the company refuses.

An AI that scores well on this environment has learned to be that expert reader — the one that 50 lakh freshers need and cannot afford.

---

## The Environment Architecture
┌──────────────────────────────────────────────────────────────┐
│                     EPISODE FLOW                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   reset()                                                    │
│   └── Returns: Realistic legal offer letter                  │
│                Difficulty: Easy / Medium / Hard              │
│                Instructions: "List ALL suspicious clauses"   │
│                                                              │
│   step(analysis_1)                          Weight: 30%      │
│   └── Grades: Clause identification accuracy                 │
│       Returns: Score 1 + "Calculate financial impact"        │
│                                                              │
│   step(analysis_2)                          Weight: 35%      │
│   └── Grades: Accuracy of rupee calculations                 │
│       Returns: Score 2 + "Give recommendation"               │
│                                                              │
│   step(analysis_3)                          Weight: 35%      │
│   └── Grades: Quality of negotiation strategy                │
│       Returns: Final Score (weighted average) + done=True    │
│                                                              │
└──────────────────────────────────────────────────────────────┘

The three-stage design is deliberate. A one-shot classifier that labels offers as "risky" or "safe" has no real-world value. What a fresher needs is someone who can find the problem, explain the financial damage in rupees, and tell them specifically what to negotiate. That requires sequential reasoning — and sequential reasoning requires a multi-step environment.

---

## Difficulty Progression

### Easy — Single Trap, Dense Legal Language

The offer letter contains one harmful clause, but it is written in the kind of language that makes most people's eyes glaze over.

A real example from our environment:

> *"In consideration of and as a condition precedent to such investment, you hereby irrevocably covenant, warrant, and undertake that you shall remain in the uninterrupted, full-time, exclusive employment of the Company for a minimum continuous period of twenty-four (24) calendar months computed from your date of joining. In the event of your voluntary separation, abandonment of employment, or constructive resignation prior to the expiration of the aforesaid minimum service tenure, you shall, without any further notice or demand, become immediately liable to pay to the Company a sum of Rs. 1,50,000 as a genuine pre-estimate of the liquidated damages..."*

A student reads this and sees: employment terms.
The AI must read this and see: 24-month bond, ₹1,50,000 penalty, HIGH risk.

---

### Medium — Two to Three Combined Traps

Real offer letters don't have one problem. They have several. The medium tasks combine multiple traps that interact with each other.

For example: an offer with a probation salary cut (70% for 6 months = ₹1,44,000 lost) PLUS a clawback joining bonus (₹1,00,000 that must be returned with 18% interest if leaving within 12 months) PLUS a 90-day notice period the company is not obligated to waive.

The AI must find all three, calculate the combined financial exposure, and understand how they interact — the joining bonus clawback makes the probation period even more dangerous because the candidate is already earning less and cannot afford to leave.

---

### Hard — Four to Nine Traps, Full Legal Complexity

The hard tasks are the ones that would trouble even a smart reader with time to spare.

They combine financial traps (probation cuts, variable pay illusions, fake increments) with legal traps (IP ownership extending 12 months post-employment, arbitration clauses designed to make legal recourse impossible, garden leave combined with non-compete creating 27-month lock-in) and structural traps (6-day work weeks buried in working hours section, salary review clauses with "if any" language that legally permits zero increment forever).

The AI must identify every trap, calculate every rupee of exposure, understand the legal implications, and produce a prioritized negotiation strategy with specific reference to Indian employment law.

---

## The Nine Traps

| Trap | What It Looks Like | What It Actually Means |
|------|-------------------|----------------------|
| Training Bond | "Human Capital Investment Covenant" | Pay ₹75K–₹2L if you leave early |
| Probation Salary Cut | "70% of CTC during probation period" | ₹1.44L lost in first 6 months |
| Clawback Bonus | "Joining Bonus subject to recovery provision" | Return ₹1L + 18% interest if leaving within 12 months |
| Fake Increment | "30% increment on Basic Salary" | ₹90K raise, not ₹2.4L |
| Variable Pay Illusion | "PLI subject to KRA achievement" | 6 conditions all simultaneously — realistically 40% payout |
| IP Ownership Trap | "Work product vests in Company" | Your startup, your freelance, your weekend code — all theirs |
| Garden Leave | "Company may impose Garden Leave" | Paid to sit home, cannot join new employer for 90 days |
| Arbitration Trap | "Disputes resolved in New Delhi" | Company-appointed arbitrator, 1400km from your city |
| Salary Review Illusion | "Increment, if any, at discretion" | Legal zero increment every year, forever |

---

## Specifications

| Property | Details |
|----------|---------|
| Framework | OpenEnv (Meta PyTorch) |
| Interaction | Multi-step (3 steps per episode) |
| Difficulty Levels | Easy · Medium · Hard |
| Offer Letters | 18 realistic legal documents |
| Trap Types | 9 categories |
| Traps Per Letter | 1 (Easy) · 2–3 (Medium) · 4–9 (Hard) |
| Reward Range | 0.0 – 1.0 (weighted average of 3 steps) |
| Action Space | Natural language analysis |
| Observation Space | Legal offer letter text + step instructions |
| Inference Runtime | Under 5 minutes |
| Infrastructure | 2 vCPU · 8GB RAM (HF Spaces free tier) |

---

## API Reference
GET  /health   →  {"status": "healthy"}
POST /reset    →  Offer letter + Step 1 instructions
POST /step     →  Score + next step instructions (or final score)
GET  /state    →  Episode metadata
GET  /docs     →  Interactive API documentation

---

## Quick Start

**Install:**
```bash
pip install git+https://huggingface.co/spaces/YOUR_USERNAME/job-offer-decoder
```

**Use:**
```python
import asyncio
from job_offer_decoder import JobOfferDecoderEnv, JobOfferAction

async def run():
    async with JobOfferDecoderEnv(
        base_url="https://YOUR_USERNAME-job-offer-decoder.hf.space"
    ) as env:

        # Get offer letter
        result = await env.reset()
        print(result.observation.offer_text)

        # Step 1 — Identify clauses
        result = await env.step(JobOfferAction(
            analysis="I found a 24-month training bond with "
                     "Rs. 1,50,000 liquidated damages penalty...",
            task_type="step_1_identification"
        ))
        print(f"Step 1: {result.reward}")

        # Step 2 — Financial impact
        result = await env.step(JobOfferAction(
            analysis="Bond exposure: Rs. 1,50,000. Real monthly "
                     "inhand: Rs. 45,700 not Rs. 64,000...",
            task_type="step_2_financial_impact"
        ))
        print(f"Step 2: {result.reward}")

        # Step 3 — Recommendation
        result = await env.step(JobOfferAction(
            analysis="Do not sign. Negotiate bond removal first. "
                     "Non-compete unenforceable under Section 27 "
                     "Indian Contract Act 1872...",
            task_type="step_3_recommendation"
        ))
        print(f"Final Score: {result.reward}")

asyncio.run(run())
```

**Run inference:**
```bash
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4o-mini"
export HF_TOKEN="your_token_here"

python inference.py
```

---

## Scoring

### Step 1 — Clause Identification (30%)
Measures how completely the agent identifies all harmful clauses. Partial credit for each trap found. Bonus for finding all traps in a letter.

### Step 2 — Financial Impact (35%)
Measures accuracy of rupee calculations. Checks real monthly salary, probation loss, bond penalty, realistic variable pay, clawback amounts. Tolerance of ±15% on calculations. Bonus for calculating total cumulative exposure.

### Step 3 — Recommendation (35%)
Measures quality of negotiation strategy. Checks for clear verdict, specific negotiation demands, prioritization of clauses, actionable advice, and legal references. Bonus for citing Indian Contract Act non-compete enforceability.

---

## Project Structure
job_offer_decoder/
│
├── inference.py                          ← Baseline inference script
├── models.py                             ← Action / Observation / State
├── client.py                             ← HTTP client
├── openenv.yaml                          ← Environment manifest
├── pyproject.toml                        ← Package config
├── README.md                             ← This file
│
└── server/
├── job_offer_decoder_environment.py  ← Core logic
│                                        18 offer letters
│                                        9 trap graders
│                                        3-step episode manager
├── app.py                            ← FastAPI server
├── requirements.txt                  ← Dependencies
└── Dockerfile                        ← Container

---

## Legal Grounding

Every trap in this environment is grounded in actual Indian law:

**Training Bonds** — Enforceable under Indian Contract Act 1872 if the restraint is reasonable in duration and amount. Courts have upheld bonds of 1–2 years with proportionate penalties.

**Non-Compete Clauses** — Section 27, Indian Contract Act 1872 renders post-employment non-compete agreements largely void as restraint of trade. Companies use them regardless because most employees don't know this.

**Gratuity** — Payment of Gratuity Act 1972 requires minimum 5 years of continuous service. Including gratuity in CTC for a role most people leave in 2–3 years is deliberately misleading.

**Employer PF** — Employees' Provident Funds Act 1952. Employer contribution goes to EPFO, not the employee's salary account. Including it in CTC inflates the number without adding take-home value.

**Garden Leave** — No specific Indian statute governs garden leave. Enforceability depends entirely on contract terms, making it a powerful tool for companies and a largely invisible trap for employees.

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `API_BASE_URL` | LLM API endpoint URL |
| `MODEL_NAME` | Model identifier for inference |
| `HF_TOKEN` | Hugging Face / API authentication key |
| `SPACE_URL` | Deployed HF Space URL |

---

## Who This Is For

**Freshers** signing their first offer letter and wanting to understand what they're agreeing to.

**Placement cells** at colleges that want to systematically protect students during recruitment season.

**RL researchers** who want a real-world, high-stakes, multi-step environment where the quality of reasoning directly maps to real-world impact.

**Anyone** who believes that understanding a legal document you're about to sign should not require access to a ₹5,000/hour lawyer.

---

## The Bigger Picture

This environment exists because the gap between what offer letters say and what they mean is not a knowledge problem — it is an access problem.

The knowledge to decode these documents exists. Employment lawyers, senior HR professionals, and experienced employees read these clauses correctly every day.

What doesn't exist is accessible, free, instant access to that knowledge for the people who need it most: the 22-year-old accepting their first job, excited about the salary number, trusting that the rest is standard.

An AI trained on this environment closes that gap. It reads the legal language. It does the math. It tells you what to fight for.

That is what this environment trains. That is why it matters.

---

*Built on [OpenEnv](https://github.com/meta-pytorch/OpenEnv) · Powered by Meta PyTorch and Hugging Face*

*For Indian freshers who deserve to know what they're signing.*
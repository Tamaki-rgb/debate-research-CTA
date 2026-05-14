# Does Debate Training Develop Critical Thinking?

A research project I started after noticing something at my school: students who debated seemed to think differently — faster, sharper, more structured. But was that actually true, or just my impression?

This is my attempt to find out.

---

## What this is

An independent data-driven study examining whether participation in debate programs correlates with higher critical thinking scores among secondary school students in Shymkent, Kazakhstan.

I surveyed 100 students, split them into two groups (debate participants vs. non-participants), and measured their performance across four cognitive criteria using a structured scenario-based questionnaire.

The results were interesting — and not always what I expected.

---

## Research design

**Survey:** 16 questions across three blocks
- Block A — background (debate experience, duration, grade level)
- Block B — 9 scenario-based tasks measuring critical thinking objectively
- Block C — 3 self-assessment questions (used to detect overconfidence gap)

**Criteria measured:**
- Argumentation
- Source Evaluation
- Openness to Change
- Structured Thinking

Loosely based on the Watson-Glaser Critical Thinking framework, adapted for secondary school level.

---

## Key findings

| Criterion | Debate participants | Non-participants |
|---|---|---|
| Argumentation | 7.9% | 18.5% |
| Source Evaluation | 65.8% | 33.1% |
| Openness to Change | 63.2% | 33.9% |
| Structured Thinking | 72.8% | 43.0% |

The argumentation result flipped — non-participants scored higher. My interpretation: debate training may build rhetorical confidence over evidence-based reasoning, at least at the secondary school level. That's worth investigating further.

The self-assessment data also showed a consistent overconfidence gap among non-participants: they rated themselves highly, but their actual scores told a different story.

---

## Stack

- Data collection: Google Forms
- Analysis: Python (pandas, matplotlib, seaborn)
- Visualization: matplotlib with custom dark theme
- Website: vanilla HTML/CSS/JS, no frameworks

---

## Project structure

```
debate-research/
├── data/
│   └── Untitled_form.csv       # raw survey responses
├── analysis/
│   └── analysis.py             # scoring + chart generation
├── charts/                     # generated PNG charts
└── website/
    └── index.html              # research website
```

---

## About me

I'm Umid, a 10th grade student from Shymkent, Kazakhstan. I'm interested in data science and how numbers can reveal things that intuition gets wrong — which is kind of what happened here.

This project was built independently as part of my research portfolio.

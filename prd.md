
# Banker Helper — Developer PRD & Build Map (Solo Dev)

**Author:** Célian
**Created:** 2026-02-07
**Purpose:** This document is both a **Product Requirements Document** and a **development roadmap + engineering guide**. It is designed to be read daily while building the project, acting as a north star, guardrail, and technical compass.

This is not a startup product. This is a **serious financial engineering tool**, built with craftsmanship, correctness, and long-term extensibility in mind.

---

# 1. Core Vision

Build a **financial reasoning engine** with a clean Python core, a modern CLI interface, and optional tactical web UI.

The goal is to create a tool that:

* Feels fast, powerful, and elegant
* Is mathematically correct and well-tested
* Encourages exploration and scenario modeling
* Scales cleanly from personal finance → corporate finance → markets

This is a *thinking tool*, not a dashboard.

---

# 2. Design Principles (Non‑Negotiable)

1. **Core-first architecture**
   All financial logic lives in `banker_core`. Interfaces are thin wrappers.

2. **Pure functions & deterministic outputs**
   Same input → same output. No hidden state.

3. **Typed domain models**
   Financial concepts are represented by explicit Pydantic models.

4. **Separation of concerns**
   Core → Models → Renderers → CLI / Web

5. **Composable tooling**
   CLI commands should chain, script, and export cleanly.

6. **High test coverage**
   Math must be boringly correct.

---

# 3. System Architecture

```
                 ┌────────────┐
                 │  CLI (UX)  │
                 └─────▲──────┘
                       │
                       │
              ┌────────┴─────────┐
              │   banker_core    │   ← Financial Engine
              └────────▲─────────┘
                       │
                       │
                 ┌─────┴──────┐
                 │  Models    │   ← Domain Language
                 └─────▲──────┘
                       │
                       │
                 ┌─────┴──────┐
                 │ Renderers  │   ← Terminal Presentation
                 └────────────┘

(Optional Web UI: FastAPI → banker_core → JSON)
```

**Dependency Flow:**

```
banker_core  ←  CLI
banker_core  ←  Web
```

Never reverse this.

---

# 4. Repository Structure

```
banker/
├── pyproject.toml
├── README.md
├── banker_core/
│   ├── math/
│   ├── loans/
│   ├── investments/
│   ├── corporate/
│   ├── bonds/
│   ├── risk/
│   ├── models.py
│   └── exceptions.py
├── banker_cli/
│   ├── main.py
│   ├── renderers/
│   └── commands/
├── banker_web/
│   └── app.py
└── tests/
```

---

# 5. Core Modules & Responsibility Map

| Module      | Responsibility                                |
| ----------- | --------------------------------------------- |
| math        | Time value of money, compounding, discounting |
| loans       | Mortgages, amortization, affordability        |
| investments | Growth models, savings, retirement            |
| corporate   | WACC, DCF, IRR, NPV, valuation                |
| bonds       | Pricing, YTM, duration, convexity             |
| risk        | Scenarios, sensitivity, Monte Carlo           |

---

# 6. Domain Models (`models.py`)

**Purpose:** Create a shared financial language between math, CLI, and web.

Models define:

* financial inputs
* financial outputs
* structured business meaning

### Example

```python
class LoanInput(BaseModel):
    principal: float
    annual_rate: float
    years: int
    extra_payment: float = 0

class LoanResult(BaseModel):
    monthly_payment: float
    total_interest: float
    total_paid: float
    years: float
```

**Rules:**

* Core functions accept and return models
* CLI only builds models and renders results
* Web endpoints accept and return models

---

# 7. Rendering System (Rich-powered)

Renderers transform **models → visual clarity**.

Renderers never compute.

```
banker_cli/renderers/
├── loan.py
├── invest.py
├── corporate.py
└── bonds.py
```

### Example Pattern

```python
def render_loan(result: LoanResult):
    table = Table(...)
    ...
```

**Output Modes:**

* pretty (default): rich tables
* json: machine output

---

# 8. CLI Grammar

```
banker <command> [subcommand] [options]
```

Examples:

```
banker loan --amount 350000 --rate 5.4 --years 25
banker invest --initial 10000 --monthly 500 --rate 7 --years 20
banker wacc --equity 9 --debt 5.5 --tax 26 --ev 12e6 --debt-value 4.5e6
```

---

# 9. Feature Universe & Command Map

## Foundation Math

* pv, fv, rate, nper, annuity

## Loans & Mortgages

* loan
* mortgage
* amortization
* refinance
* compare

## Investments

* invest
* portfolio
* sharpe
* rebalance
* fire

## Corporate Finance

* wacc
* capm
* dcf
* npv
* irr
* comps

## Bonds & Fixed Income

* bond price
* bond ytm
* duration
* convexity
* ladder

## Risk & Scenario

* scenario
* sensitivity
* montecarlo
* stress-test

---

# 10. MVP Scope (v0.1)

Only these commands:

1. loan
2. invest
3. afford

Everything else is future-proofed, not implemented.

---

# 11. Mathematical Requirements

* Use double precision
* Stable formulas
* Unit-tested against spreadsheet references
* Edge-case handling: zero rates, high rates, long horizons

---

# 12. Tech Stack

* Python 3.11+
* uv
* typer (CLI)
* rich (terminal UX)
* pydantic (models)
* numpy (optional math)
* fastapi + uvicorn + uvloop (optional web)
* pytest + hypothesis (testing)

---

# 13. Development Roadmap

## Phase 0 — Scaffold (Day 1)

* Repo
* pyproject
* core package skeleton
* CLI skeleton
* CI pipeline

## Phase 1 — Loan Engine (Days 2–4)

* LoanInput / LoanResult
* monthly payment math
* amortization engine
* tests
* CLI + renderer

## Phase 2 — Investment Engine (Days 5–7)

* InvestmentInput / Result
* growth model
* renderer
* tests

## Phase 3 — Affordability Engine (Days 8–10)

* debt ratios
* stress-test logic
* renderer

## Phase 4 — Hardening (Days 11–14)

* full test coverage
* performance check
* documentation

---

# 14. Testing Strategy

* Unit tests for every formula
* Integration tests for CLI
* Property tests for math invariants
* Regression tests vs Excel

---

# 15. Engineering Guardrails

* No logic in CLI
* No printing in core
* No math in renderers
* No mutation of model inputs

---

# 16. Acceptance Criteria

A command is considered *complete* only if:

* Math validated
* Edge cases handled
* Unit tests written
* CLI output formatted
* JSON export works

---

# 17. Definition of Done

Feature is done when:

* Code passes CI
* Documentation exists
* Output is readable
* No technical debt added

---

# 18. Long-Term Vision

This architecture supports:

* Web dashboards
* Notebook integrations
* GUI apps
* Automated pipelines
* AI-assisted financial reasoning

Without rewriting core logic.

---

# 19. Mental Model

```
Math → Models → Engine → Renderer → CLI → Human
```

Every line of code must fit cleanly inside this pipeline.

---

# 20. Daily Development Loop

```
Design → Implement → Test → Render → Reflect
```

Repeat.

---

**This document is your engineering compass.**

Whenever you feel scope creep, confusion, or uncertainty — return here.

*End of document.*

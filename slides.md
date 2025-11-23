---

marp: true
theme: default
paginate: true

# Custom theme CSS for Marp slides

style: |
/* Use a modern system font stack */
section {
font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* Header area for contact */
.marp-header {
position: absolute;
top: 0.6rem;
left: 1rem;
font-size: 0.85rem;
opacity: 0.9;
}

/* Page number style (Marp's paginate creates .marp-pagination) */
.marp-pagination {
position: absolute;
right: 1rem;
bottom: 0.6rem;
font-size: 0.82rem;
color: rgba(0,0,0,0.6);
}

/* Make code blocks slightly larger and monospace */
pre, code {
font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", "Segoe UI Mono", monospace;
font-size: 0.9rem;
}

/* Accent color for important badges */
.badge { background: linear-gradient(90deg,#0ea5e9,#6366f1); color: white; padding: 0.25rem 0.5rem; border-radius: 6px; }
-------------------------------------------------------------------------------------------------------------------------

<!-- Title slide -->

# MyProduct — Product Documentation

**Contact:** [22f3001685@ds.study.iitm.ac.in](mailto:22f3001685@ds.study.iitm.ac.in)

---

## Purpose

* Maintainable slide-based docs in Git
* Easy conversion to PDF/HTML using Marp CLI
* Suitable for engineering and product audiences

---

---

backgroundImage: url('images/architecture-bg.png')
background-position: center
class: lead
-----------

# System Architecture

This slide demonstrates a slide with a background image. Put `architecture-bg.png` under `images/` in the repo.

Notes: Describe components and data flows.

---

## Quickstart

1. Clone the repository
2. Install Marp CLI: `npm i -g @marp-team/marp-cli` (or use `npx`)
3. Render:

```bash
# render HTML
npx @marp-team/marp-cli slides.md -o slides.html
# render PDF
npx @marp-team/marp-cli slides.md -o slides.pdf
```

---

## Algorithmic Complexity (math)

We analyze the sort used in indexing. The expected cost is:

* Average: $T(n)=O(n\log n)$
* Worst-case: $T(n)=O(n^2)$

Display form (expected growth):

$$\mathbb{E}[T(n)] = c,n\log n + o(n\log n)$$

Explain the constant $c$ depends on implementation details.

---

## Code Example

```python
# Compute time complexity estimate for doubling input
def estimate_growth(times):
    # times: list of (n, measured_seconds)
    from math import log2
    rates = []
    for (n1,t1),(n2,t2) in zip(times, times[1:]):
        rates.append((t2/t1) / (n2/n1))
    return sum(rates)/len(rates)
```

---

## Versioning & CI (example)

Keep `slides.md` in the repo and add a CI job to render artifacts.

```yaml
# .github/workflows/render-slides.yml
name: Render Slides
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Render Marp
        run: npx @marp-team/marp-cli slides.md -o slides.pdf
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: slides-pdf
          path: slides.pdf
```

---

# Assets & Structure

Recommended repository layout:

```
marp-product-docs/
├─ slides.md
├─ images/
│  └─ architecture-bg.png
├─ .github/workflows/render-slides.yml
└─ README.md
```

---

# Thank you

Contact: [22f3001685@ds.study.iitm.ac.in](mailto:22f3001685@ds.study.iitm.ac.in)

---

<!-- Build notes:
- To render locally: npx @marp-team/marp-cli slides.md -o slides.pdf
- Ensure images/architecture-bg.png exists, or replace the path in slide frontmatter.
-->

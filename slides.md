---

marp: true

theme: gaia 
paginate: true
style: |
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }

---

# Slide with Custom Columns

<div class="columns">
  <div>
    ### Left Column  
    * Item A
    * Item B
  </div>
  <div>
    ### Right Column
    Content goes here.
  </div>
</div>

---
<style>
/* Position the page number in the bottom right corner */
section::after {
  content: attr(data-marpit-pagination) '/' attr(data-marpit-pagination-total);
  position: absolute;
  bottom: 20px; /* Adjust as needed */
  right: 20px; /* Adjust as needed */
  font-size: 0.8em; /* Adjust font size */
  color: grey; /* Adjust color */
}
</style>

<!-- Title slide -->

# MyProduct — Product Documentation

**Contact:** [22f3001685@ds.study.iitm.ac.in](mailto:22f3001685@ds.study.iitm.ac.in)

---

## Purpose

* Maintainable slide-based docs in Git
* Easy conversion to PDF/HTML using Marp CLI
* Suitable for engineering and product audiences

---
![bg](\images\architecture-bg.png)

---

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

# Compute Commons: Access Rights in Embodied-AI Inference Auctions

**FP9 · Xinrong Sun · COMSCI/ECON 206 · Professor Luyao Zhang**

Review snapshot: `ps2-review-2026-09-27`. Solo team. This package contains an English proposal, synthetic computational demonstration, a self-contained executed notebook and a Hugging Face-ready static behavioral interaction. It extends the author's classroom second-price inference-auction proposal and the PS1 distinction between consultation and binding participation.

## Reproduce the actual results

Python 3.10 or later; standard library only:

```bash
cd code
python model.py
```

This writes `results.json` and `sweep.csv`. The fresh run passes **144,439 assertions**. Expected core results:

| Rule | Worker reserve | Entrant credit | Winners | Payments | Winner utilities | Firm value | Revenue |
|---|---:|---:|---|---|---|---:|---:|
| Standard | 0 | 0 | A, B | 6, 6 | 4, 3 | 19 | 12 |
| Credit only | 0 | 4 | A, E | 9, 5 | 1, 1 | 16 | 14 |
| Reservation only | 1 | 0 | A | 9 | 1 | 10 | 9 |
| Both | 1 | 5 | E | 5 | 1 | 6 | 5 |

All use values (10,9,6), eligibility (0,0,1), capacity 2 and fixed tie order A/B/E. Payments and values have synthetic normalized units. Utility for every loser is zero. The 39-setting sweep changes reserve from 0 through 2 and credit from 0 through 12.

`code/compute_commons_ps2.ipynb` embeds the exact Python source and captured local execution. Upload it to Colab or run in Jupyter; it does not fetch code remotely. Hosted execution is not asserted. Optional JavaScript parity check, from this package root:

```bash
node verify-js.cjs
```

The DOM-handler test uses a stub, not a full browser. The proof in Appendix A establishes continuous-domain value incentive compatibility; finite testing alone does not.

## Behavioral demonstration

Open `hf_space/index.html` with `model.js` beside it. It runs without an account, package installation or server. The Hugging Face metadata in `hf_space/README.md` declares a static Space. The participant predicts a payment, commits a bid, observes the outcome, and optionally exports a local reflection JSON. It labels synthetic opponents and manual peer entry separately. No response data are automatically transmitted. A facilitator must independently collect sealed bids for peer play; this static page cannot enforce multiplayer privacy.

## Compile the proposal

Upload the complete source to the supplied Overleaf project, select `main.tex` and pdfLaTeX, and recompile. The source retains the course-supplied `acmart.cls` and `ACM-Reference-Format.bst`.

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

Main Sections 1–5, metadata, teaser and artifact notices must fit in two pages. Author Notes, references and Appendices A–F follow. Inspect the rendered PDF after any change to links or text.

## Scope and evidence

The slot is a standardized inference admission window for a proposed supervised OpenVLA-based testbed. No robot, VLA or hardware benchmark was run. Private values, unit demand, public fixed eligibility, enforceable payments and a committed coordinator define the theorem. Arbitrary budgets, dynamic queues, complementary slots, common-value safety signals, collusion and false identities are outside it.

A separate eligibility stress test lets incumbent A acquire an undeserved entrant label. Under reserve 1 and credit 5, A then gains 4. An idealized additional fine 10 with independent perfect detection needs probability at least 0.4 to deter this one deviation. This is not a solved audit game or a legal enforcement recommendation.

## Publication and submission status

The local snapshot is executable. The designated course repository is https://github.com/dku-comsci-econ206-Autumn2026/-PS2-FP9-ComputeCommons and the designated Space is https://huggingface.co/spaces/dku-comsci-econ206-2026/Xinrong_Sun. The GitHub integration returned HTTP 403 on upload; the Hugging Face connector is read-only. PS2 files have not been published to either destination. A personal fork and pull request, exact release commit, and a hosted notebook URL remain pending. The prior PS1 repository at https://github.com/Sunnyxinrong/PS1-Xinrong-Sun was inspected at commit `50930c85a29265d24e603dc25d3968879ccc5ad6`; it is not a PS2 repository.

The author supplied a four-part classroom account, not recorded human bids. September 28 symposium reviews, two outgoing reviews, and the September 30 response cannot be represented as completed in this September 27 draft. Record genuine feedback and verification before the final revision.

## Attribution and responsibility

Original code: MIT (see LICENSE). Course/ACM templates and scholarly materials retain their own terms. The poster adapts the supplied course template. The model uses established Vickrey and critical-payment principles. ChatGPT/Codex assisted derivation, code, checks, primary-source retrieval, English writing and artifact preparation. Sun supplied the topic, prior work and classroom decision. Independent human review of new material is not certified; record it only after it occurs. No private classroom photographs are included in the public demo.

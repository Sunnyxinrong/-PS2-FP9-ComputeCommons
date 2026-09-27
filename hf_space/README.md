---
title: Compute Commons Inference Auction
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: static
pinned: false
license: mit
---

# Compute Commons: access rights in embodied-AI inference auctions

Xinrong Sun, FP9, COMSCI/ECON 206, instructor Professor Luyao Zhang.

Open `index.html` locally with `model.js` beside it. No installation, login or API key is needed. This directory is ready for a Hugging Face static Space. A local build does not establish that the Space has been deployed.

The interface uses the paper's private-value, unit-demand mechanism, with two slots, worker reservation `r`, verified entrant credit `c`, fixed tie order A/B/E and critical payments. It structures prediction, a sealed own bid, explanation and local reflection export. Synthetic opponents are the default; manual peer entry is explicitly labeled. A facilitator must collect bids privately before entering them: this static page is not a secure multiplayer server.

## Evidence and privacy

All example inputs are synthetic. No human data, actual robot performance or causal behavioral result is supplied. Responses remain in page memory until the participant chooses to export JSON. The app sends no telemetry or response uploads; the hosting service may keep its own normal access logs. Use aliases and fictional task values. Do not enter personal information or proprietary robot logs. Refreshing clears the in-memory round record.

The planned pilot distinguishes payment confusion from legitimacy concerns and ordinary payoff indifference. Tutorial and explanation comparisons remain planned; this demonstration is not a randomized study engine. Record signed bid error and utility regret separately. Truthfulness applies to values conditional on verified identity and a committed rule, not to unverifiable eligibility.

MIT applies to original code. Source concepts: Vickrey (1961), DOI 10.1111/j.1540-6261.1961.tb02789.x; Roughgarden, CS364A Lecture 3, https://timroughgarden.org/f13/l/l3.pdf. Application: https://openvla.github.io/. AI assistance is disclosed in the paper.

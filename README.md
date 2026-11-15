<div align="center">
  <img src="assets/hero.svg" alt="Shikhar Verma. I build agent guardrails, payment systems and evals." width="100%">
</div>

<p align="center">
  <a href="#about">About</a> &nbsp;|&nbsp;
  <a href="#featured-projects">Projects</a> &nbsp;|&nbsp;
  <a href="#open-source-contributions">Open source</a> &nbsp;|&nbsp;
  <a href="#tech-stack">Tech stack</a> &nbsp;|&nbsp;
  <a href="#github-activity">Activity</a>
</p>

## About

<img align="right" src="https://github.com/Shikhyy.png?size=360" width="150" alt="Shikhar Verma">

I'm a developer who builds AI agents, payment systems and the evaluations that test them. I focus on software where a wrong action costs real money, and on making that software show what it did and why.

I maintain about 60 public repositories. Many began as hackathon or challenge entries that I kept developing after the deadline. I also contribute upstream to Meshery, Hermes Agent and Kestra.

| | |
| :-- | :-- |
| **Focus** | AI agent security, resilient payments, model evaluation |
| **Main languages** | TypeScript, Python, Go, Rust |
| **Open source** | 8 merged pull requests across Meshery, Hermes Agent and Kestra |
| **Latest work** | OrderBook-DST, Lineage, WIF Tape, Sangam, Enfeoff |

<br clear="right">

## Featured projects

| Project | Area | Description |
| :-- | :-- | :-- |
| [**Lineage**](https://github.com/Shikhyy/lineage) ([demo](https://lineage-beryl.vercel.app)) | Agent security | A payment agent that cannot be phished. Every payment detail carries its provenance, and 0 of 12 simulated attacks succeed. |
| [**Sentinyx**](https://github.com/Shikhyy/sentinyx) ([demo](https://sentinyx.vercel.app)) | Agent security | Finds instructions hidden in onchain text that agents read, and stops the agent from obeying them. |
| [**Enfeoff**](https://github.com/Shikhyy/enfeoff) ([demo](https://enfeoff.vercel.app)) | Agent security | On-chain delegation for AI agents on Solana. A sub-agent never receives more authority than its parent holds. |
| [**Precedent**](https://github.com/Shikhyy/precedent) | Agent security | Solidity security advice treated like case law: every claim is dated and newer rulings supersede older ones. |
| [**ResilientPay**](https://github.com/Shikhyy/ResilientPay) | Payments | Research prototype for payments that survive poor connectivity: offline authorization, store-and-forward, later reconciliation. |
| [**WIF Tape**](https://github.com/Shikhyy/wiftape) ([demo](https://wiftape.vercel.app)) | Payments | A round-based stock-token prediction game on Robinhood Chain, settled by Chainlink. |
| [**OrderBook-DST**](https://github.com/Shikhyy/orderbook-dst) | Evaluation | An eval for exchange-core code that must stay correct across hundreds of events. 17 tasks and 329 real model trials. |
| [**RippleCI**](https://github.com/Shikhyy/RippleCI) ([demo](https://ripple-ci.vercel.app)) | Evaluation | Release intelligence that traces a change's blast radius through a code graph and selects which tests to run. |
| [**Cairnquill**](https://github.com/Shikhyy/cairnquill) ([demo](https://cairnquill.vercel.app)) | Evaluation | An AML report copilot on Snowflake. An LLM drafts claims and a SQL verifier blocks any number it cannot prove. |
| [**Sangam**](https://github.com/Shikhyy/sangam) ([demo](https://sangam-voice.vercel.app)) | Voice | A voice agent that talks like you, matching how you mix Hindi and English. |
| [**Scythe 3D**](https://github.com/Shikhyy/scythe) | Games | A browser multiplayer version of the board game Scythe for one to five players. |

## Open source contributions

<div align="center">
<table>
  <tr>
    <td align="center" width="33%">
      <a href="https://github.com/meshery/meshery/pulls?q=is%3Apr+author%3AShikhyy"><img src="https://github.com/meshery.png?size=160" width="64" height="64" alt="Meshery"></a><br>
      <b>Meshery</b><br>
      <sub>4 merged, 1 open</sub>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/NousResearch/hermes-agent/pulls?q=is%3Apr+author%3AShikhyy"><img src="https://github.com/NousResearch.png?size=160" width="64" height="64" alt="Nous Research"></a><br>
      <b>Hermes Agent</b><br>
      <sub>1 merged, 3 open</sub>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/kestra-io/blueprints/pulls?q=is%3Apr+author%3AShikhyy"><img src="https://github.com/kestra-io.png?size=160" width="64" height="64" alt="Kestra"></a><br>
      <b>Kestra</b><br>
      <sub>3 merged</sub>
    </td>
  </tr>
</table>
</div>

<details>
<summary>View the pull requests</summary>
<br>

**Meshery**
- [Make provider package installation robust: bounded download, atomic extraction, GitHub tarballs](https://github.com/meshery/meshery/pull/23574) (open)
- [Preserve the provider status when deleting a performance profile fails](https://github.com/meshery/meshery/pull/23549) (merged)
- [Fix typos in user-facing error and log messages](https://github.com/meshery/meshery/pull/23546) (merged)
- [Return 404 when deleting a performance profile that does not exist](https://github.com/meshery/meshery/pull/23544) (merged)

**Hermes Agent**
- [Add chronos speculative reasoning plugin to the catalog](https://github.com/NousResearch/hermes-agent/pull/150020) (merged)
- [Recover desktop sessions on canonical not_found](https://github.com/NousResearch/hermes-agent/pull/152829) (open)
- [Reject unverifiable Telegram media before an unbounded download](https://github.com/NousResearch/hermes-agent/pull/152811) (open)
- [Defer psutil import and guard conftest process reap](https://github.com/NousResearch/hermes-agent/pull/150315) (open)

**Kestra**
- [GoodData plugin: workspaces, dataSources, executions and layouts tasks, plus a trigger](https://github.com/kestra-io/plugin-gooddata/pull/5) (merged)
- [Automated data quality validator with DuckDB](https://github.com/kestra-io/blueprints/pull/1606) (merged)
- [Skip blueprint indexing when the doc-indexing webhook is unset](https://github.com/kestra-io/blueprints/pull/4619) (merged)

</details>

## Tech stack

<div align="center">

<p>
<img src="https://img.shields.io/badge/TypeScript-111111?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
<img src="https://img.shields.io/badge/JavaScript-111111?style=flat-square&logo=javascript&logoColor=white" alt="JavaScript">
<img src="https://img.shields.io/badge/Python-111111?style=flat-square&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Go-111111?style=flat-square&logo=go&logoColor=white" alt="Go">
<img src="https://img.shields.io/badge/Rust-111111?style=flat-square&logo=rust&logoColor=white" alt="Rust">
<img src="https://img.shields.io/badge/Kotlin-111111?style=flat-square&logo=kotlin&logoColor=white" alt="Kotlin">
<img src="https://img.shields.io/badge/Solidity-111111?style=flat-square&logo=solidity&logoColor=white" alt="Solidity">
<img src="https://img.shields.io/badge/Next.js-111111?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js">
<img src="https://img.shields.io/badge/Vercel-111111?style=flat-square&logo=vercel&logoColor=white" alt="Vercel">
<img src="https://img.shields.io/badge/Docker-111111?style=flat-square&logo=docker&logoColor=white" alt="Docker">
<img src="https://img.shields.io/badge/PostgreSQL-111111?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
<img src="https://img.shields.io/badge/Solana-111111?style=flat-square&logo=solana&logoColor=white" alt="Solana">
<img src="https://img.shields.io/badge/Chainlink-111111?style=flat-square&logo=chainlink&logoColor=white" alt="Chainlink">
<img src="https://img.shields.io/badge/Snowflake-111111?style=flat-square&logo=snowflake&logoColor=white" alt="Snowflake">
<img src="https://img.shields.io/badge/DuckDB-111111?style=flat-square&logo=duckdb&logoColor=white" alt="DuckDB">
<img src="https://img.shields.io/badge/FalkorDB-111111?style=flat-square&logoColor=white" alt="FalkorDB">
</p>

<img src="assets/stack.svg" alt="Primary language across 49 public repositories. TypeScript 33, Python 7, HTML 3, JavaScript 3, Kotlin 1, Rust 1, Solidity 1." width="100%">

</div>

**Built for and with**

<div align="center">
<p>
<a href="https://github.com/Shikhyy/cairnquill"><img src="https://img.shields.io/badge/Snowflake-Cairnquill-444444?style=flat-square&logo=snowflake&logoColor=white&labelColor=111111" alt="Snowflake, Cairnquill"></a>
<a href="https://github.com/Shikhyy/precedent"><img src="https://img.shields.io/badge/Sanity-Precedent-444444?style=flat-square&logo=sanity&logoColor=white&labelColor=111111" alt="Sanity, Precedent"></a>
<a href="https://github.com/Shikhyy/sangam"><img src="https://img.shields.io/badge/Gnani-Sangam-444444?style=flat-square&labelColor=111111" alt="Gnani, Sangam"></a>
<a href="https://github.com/Shikhyy/wiftape"><img src="https://img.shields.io/badge/Robinhood_Chain-WIF_Tape-444444?style=flat-square&labelColor=111111" alt="Robinhood Chain, WIF Tape"></a>
<a href="https://github.com/Shikhyy/enfeoff"><img src="https://img.shields.io/badge/Solana-Enfeoff-444444?style=flat-square&logo=solana&logoColor=white&labelColor=111111" alt="Solana, Enfeoff"></a>
</p>
</div>

## GitHub activity

<div align="center">
<img src="assets/tape.svg" alt="A cassette card for Shikhar Verma. The tracklist is my eight most recent repositories, and the equalizer is built from 53 weeks of contributions." width="100%">
<br><br>
<img src="assets/city.svg" alt="An isometric city built from a year of contributions on a bordered base. 3,605 contributions across 173 active days, busiest day 175." width="100%">
</div>

<details>
<summary>Contribution invaders</summary>
<br>
<div align="center">
<img src="assets/invaders.svg" alt="A year of daily contributions as a grid. A ship sweeps underneath and shoots the twelve busiest days." width="100%">
</div>
</details>

<br>

<p align="center">
  <sub>Graphics are generated from my GitHub contribution calendar by <code>scripts/generate.py</code>. All repositories are on the <a href="https://github.com/Shikhyy?tab=repositories">repositories tab</a>.</sub>
</p>

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <img src="assets/hero-light.svg" alt="Shikhar Verma, Shikhyy on GitHub. Building AI agent guardrails, secure payments and evals." width="100%">
</picture>
</div>

<p align="center">
  <a href="#about">About</a> &nbsp;|&nbsp;
  <a href="#flagship-projects">Flagship projects</a> &nbsp;|&nbsp;
  <a href="#more-builds">More builds</a> &nbsp;|&nbsp;
  <a href="#open-source-contributions">Open source</a> &nbsp;|&nbsp;
  <a href="#tech-stack">Stack</a> &nbsp;|&nbsp;
  <a href="#github-in-numbers">Stats</a> &nbsp;|&nbsp;
  <a href="#play">Play</a>
</p>

## About

I build software that handles money or untrusted input, and then I try to break it. Most of my repos started as hackathon or challenge entries. The ones I keep going back to ask the same question: what should a program be allowed to do when it can't be sure who told it to?

In the last year that has meant <!--AUTO:about_numbers:start-->over 3,500 commits and 51 original repositories<!--AUTO:about_numbers:end-->, from payment agents and prompt-injection scanners to a benchmark for exchange code. A few habits show up in all of them:

- **Measure instead of claiming.** OrderBook-DST has 329 real trials with confidence intervals. Lineage's attack lab runs *your* attack against the real engine.
- **Write the invariant down, then test it.** Enfeoff states six rules and the on-chain program checks every one of them on every spend.
- **Ship something you can click.** Many of the projects below have a live demo you can try.

**This week:** <!--AUTO:this_week:start-->131 commits across 10 repositories and 23 pull requests, mostly in **bell** (48), **Saans** (25) and **Joltide** (24).<!--AUTO:this_week:end-->

| | |
| :-- | :-- |
| **Focus** | AI evaluation, agent security, resilient payments |
| **Studying** | Production Engineering with a minor in Computer Science, NIT Tiruchirappalli |
| **Club** | Blockchain developer at SPIDER R&D, NIT Trichy |
| **Open source** | <!--AUTO:oss_row:start-->26 merged pull requests across Meshery, Blowhorn, keploy, Kestra, x402 and Hermes Agent<!--AUTO:oss_row:end--> |

<!--AUTO:spotlight:start-->
> **Project spotlight, changes daily:** [Sentinyx](https://github.com/Shikhyy/sentinyx)
> Every night it scans the newest tokens on Base and publishes the results as open data: a table, CSV, JSON and an Atom feed.

<!--AUTO:spotlight:end-->

## Flagship projects

### Lineage: a payment agent that can't be phished

<table>
<tr>
<td width="54%" valign="top">

Business email compromise is the biggest fraud against payables, and AI agents add a new route in: instructions hidden in invoices, chat and *persistent memory* can steer them. Most guardrails check amounts and allowlists. They don't ask where a value came from.

Lineage traces every payment-critical value (payee, account, amount) back to its source, either untrusted context such as email, chat, memory and tool output, or a trusted vendor record or the owner. A guard that sits **outside the LLM** answers `ALLOW`, `ASK_OWNER` or `BLOCK`. Only the executor holds credentials, and every decision lands in a SHA-256 hash-chained audit log. A Rust signer puts the same guard in front of NEAR Intents signing.

In a 17-scenario simulated benchmark it blocked **12 of 12 attacks** and completed all five benign payments. The live-LLM evaluation is still to do.

**Try it:** the attack lab runs a phishing message you write twice on the real engine, once with no guard and once behind Lineage.

`Go` `Rust` `TypeScript` `Next.js` &nbsp;|&nbsp; [Repo](https://github.com/Shikhyy/lineage) &nbsp;|&nbsp; [Live demo](https://lineage-beryl.vercel.app)

</td>
<td width="46%" valign="top">
<a href="https://lineage-beryl.vercel.app"><img src="https://raw.githubusercontent.com/Shikhyy/lineage/HEAD/assets/screens/03-attack-lab.jpeg" alt="Lineage attack lab: a phishing message sent with no guard loses 1,250 dollars, and behind Lineage it is held for the owner."></a>
</td>
</tr>
</table>

### Sentinyx: finding the instructions hidden in onchain text

<table>
<tr>
<td width="54%" valign="top">

AI agents now read the chain: a coin's name, an NFT's description, a Basename's text records, comments in verified source. All of it is free text that anyone can write, and some of it is written for the machine. An attacker doesn't need to hack anything. They put a sentence in a token description, or hide one in invisible Unicode.

Sentinyx has two jobs. It **finds** the text: a scanner reads every field an agent would read, decodes zero-width, bidirectional and Base64 payloads, and says which lines are aimed at machines. It **stops** the damage: a Go proxy for MCP and JSON-RPC marks tool output untrusted and denies or holds any transfer, install or shell command whose critical argument came from that text.

There is also a nightly **Night Ledger** that scans the newest tokens on Base and publishes the results as open data (CSV, JSON, Atom), plus an API, a README badge and a CLI. The guard is honest about its limits: it matches values, so a value the model retypes differently would slip past it. Tested against mock services, and detector precision and recall are not measured yet.

`TypeScript` `Go` `Next.js` `Base` `MCP` &nbsp;|&nbsp; [Repo](https://github.com/Shikhyy/sentinyx) &nbsp;|&nbsp; [Live demo](https://sentinyx.vercel.app)

</td>
<td width="46%" valign="top">
<a href="https://sentinyx.vercel.app"><img src="https://raw.githubusercontent.com/Shikhyy/sentinyx/HEAD/docs/images/lab.png" alt="Sentinyx Attack Lab: pick an attack, choose whether the guard is on, and launch it."></a>
</td>
</tr>
</table>

### Enfeoff: bounded delegation for AI agents, enforced on-chain

<table>
<tr>
<td width="54%" valign="top">

An agent that can spend money will sooner or later be talked into spending it badly. Enfeoff makes the limit part of the chain instead of part of a prompt. An owner funds a vault and creates a root **mandate**. Any holder can delegate a strictly smaller one, and every spend is checked against the whole chain of ancestors.

Six invariants hold on every call: a child always gets less than its parent has left, every ancestor is charged for every spend, revoking or expiring a node kills its subtree, funds only reach allowlisted wallets, receipts make an action single-use, and large spends sit in an owner **veto window** before release.

One detail I like: the recipient check runs *before* the budget check, so a prompt-injected "send everything to the attacker" fails with `RecipientNotAllowed` and not a confusing budget error. 32 Anchor tests, deployed on devnet with a test token. Unaudited.

`Rust` `Anchor` `Solana` `TypeScript` &nbsp;|&nbsp; [Repo](https://github.com/Shikhyy/enfeoff) &nbsp;|&nbsp; [Live demo](https://enfeoff.vercel.app)

</td>
<td width="46%" valign="top">
<a href="https://enfeoff.vercel.app"><img src="https://raw.githubusercontent.com/Shikhyy/enfeoff/HEAD/assets/web-invariants.jpg" alt="Enfeoff site: rules the program checks on every call. A child gets less, never more."></a>
</td>
</tr>
</table>

### ResilientPay: payments that survive losing the network

UPI-scale payments assume a live connection between payer, banks and the network. In a subway, a rural area or an outage, they simply fail. ResilientPay asks what can be done safely **offline**, and its answer is to bound the risk instead of pretending a disconnected system has consensus.

A payer's phone carries a pre-authorised **offline credential** with a finite budget, a short life and monotonic counters. Each payment is a 106-byte canonical CBOR envelope signed with Ed25519, handed over device to device by NFC, with SMS as the fallback. When either side reconnects, a deterministic reconciliation engine settles it and flags any conflict.

The repo is built spec-first: requirements, a threat model, a trust model, a double-spend model, protocol and state-machine specs, a deterministic simulator and a paper manuscript, all before the apps. It is a research prototype with test identities and simulated value, and it says plainly that it is not meant to replace UPI.

<div align="center">
<img src="assets/resilientpay.svg" alt="ResilientPay simulator results: 98.5% NFC success, 93.0% SMS fallback delivery, 62.3% smaller payloads, 0 false acceptances across 2,000 fault-injected transactions, 0 paise of undetected exposure across 900 double-spend trials, and a hash-chain audit log 3.2x faster on writes and 7.2x faster to verify." width="100%">
</div>

`Rust` `Go` `Kotlin` `TypeScript` &nbsp;|&nbsp; [Repo](https://github.com/Shikhyy/ResilientPay) &nbsp;|&nbsp; [Paper](https://github.com/Shikhyy/ResilientPay/blob/main/docs/01-research/23_PAPER.md) &nbsp;|&nbsp; [Android app](https://github.com/Shikhyy/resilientpay-android)

### OrderBook-DST: can a model write exchange code that stays correct?

Exchanges, brokers and crypto venues run matching and risk engines where a bug moves real money instantly. A reviewer reading one function will not see a rebate credited without debiting the fee vault. A conservation check over many events will. OrderBook-DST asks whether a model can write that code so it holds up over **hundreds of events**, not just the tests it can see. The tasks model failure classes behind real losses: Knight Capital in 2012, FTX and Alameda in 2022, and the LME nickel halt the same year.

A model writes one handler file, and it is graded **by code, never by an LLM judge**: 20% public tests, 30% on 87 hidden checkpoints, and 50% on 20 hidden seeds of 200 events each, with invariants checked after every event (money conserved, margin locks, order ids and priority, FIX replay). The benchmark has 17 tasks in 9 families and 81 hand-written bugs the grader must catch. Reproducing it costs $0 on free tiers.

<div align="center">
<img src="assets/results.svg" alt="OrderBook-DST pass rates on the 11 implementation tasks: nemotron_ultra 100%, mistral_large 93.9%, gemini_35_flash 87.5% incomplete, gemma_26b 81.8%, flash_lite 78.8%, nemotron_nano 36.4%, ministral_8b 36.4%." width="100%">
</div>

`Python` &nbsp;|&nbsp; [Repo, results and research report](https://github.com/Shikhyy/orderbook-dst)

### Cairnquill: an LLM drafts, SQL verifies

An AML suspicious-transaction report copilot built on Snowflake, aimed at the problem of LLM hallucination in regulatory filings. An XGBoost detector flags accounts, immutable evidence snapshots ("cairns") are collected, and Snowflake Cortex drafts numeric claims. A deterministic SQL verifier then checks **every claim against the snapshot**. If the model invents a number, the draft is blocked. Approved filings get a SHA-256 seal. On its planted-error harness it reports a 98.5% catch rate, a 0.5% false-block rate and 420 ms average verification. Synthetic data only. 253 commits.

`Snowflake` `Cortex` `FastAPI` `React` &nbsp;|&nbsp; [Repo](https://github.com/Shikhyy/cairnquill) &nbsp;|&nbsp; [Live demo](https://cairnquill.vercel.app)

## More builds

| Project | What it is | Built with |
| :-- | :-- | :-- |
| [**Nexus**](https://github.com/Shikhyy/Nexus) ([demo](https://nexus-delta-lemon.vercel.app)) | A human and AI co-evolution engine. It tracks market signals, finds an organisation's capability gaps in real time and deploys a fleet of agents against them, with a 3D live view. My largest repo at 363 commits. | FastAPI, WebSockets, Three.js, Groq, Supabase |
| [**wyrmline**](https://github.com/Shikhyy/wyrmline) | An echo-sounder for open-source supply-chain risk. Every core function is a raw OpenCypher query on a graph database: multi-hop blast radius of a compromised package, CI/CD risk scoring, incident correlation, and a GitHub Actions agent that blocks risky PRs. | Python, HydraDB, React, D3 |
| [**VitaSync**](https://github.com/Shikhyy/VitaSync) | Private, on-premise health intelligence. Patients upload records, extraction and retrieval produce grounded answers from a self-hosted Qwen model, and clinicians can query only with active patient consent, optionally pay-per-query over x402. | Qwen, vLLM, AMD GPU, Docker |
| [**RippleCI**](https://github.com/Shikhyy/RippleCI) ([demo](https://ripple-ci.vercel.app)) | Release intelligence that parses Python into an AST graph, traces a change's blast radius with Cypher, picks tests under a runtime budget, and checks the plan against synthetic mutants. | Python, FalkorDB |
| [**GOSSIP**](https://github.com/Shikhyy/GOSSIP) ([demo](https://gossip-brown.vercel.app)) | A continuous prediction market. Instead of yes or no, you bet on an exact value on a Gaussian curve, priced by an on-chain Gaussian AMM, with AI agents trading through an MCP server. | Rust, Anchor, Solana, Next.js |
| [**Sangam**](https://github.com/Shikhyy/sangam) ([demo](https://sangam-voice.vercel.app)) | A voice agent that talks like you. It measures how you mix Hindi and English and keeps its replies in the same mix. 96.7% token accuracy on a 398-token held-out set with synthetic labels. | TypeScript, Next.js, speech APIs |
| [**cobot-arm**](https://github.com/Shikhyy/cobot-arm) | A PCB soldering fixture on a six-axis, seven-servo 3D-printed arm. The site renders the project's own CAD export as a working 3D model, and a browser joystick drives the real arm over Web Serial, with 38 automated checks on the wire format and control maths. | TypeScript, React Three Fiber, Arduino, Web Serial |
| [**squadrune**](https://github.com/Shikhyy/squadrune) | Four specialist agents (security, architecture, spec compliance, test coverage) review a pull request concurrently, and a synthesis agent ranks the verdict. Work in progress. | Python, asyncio |
| [**WIF Tape**](https://github.com/Shikhyy/wiftape) ([demo](https://wiftape.vercel.app)) | A round-based stock-token prediction game on Robinhood Chain. Chainlink settles each round, winners split the losing pool and 10% of it is burned. | Solidity, Next.js |

Also on the profile: [Apex](https://github.com/Shikhyy/Apex), a four-agent DeFi yield pipeline with a risk-gating Guardian, [Pantheon](https://github.com/Shikhyy/Pantheon), an agent-vs-agent marketplace on 0G, [AEOspy](https://github.com/Shikhyy/AEOspy), a radar for how AI answer engines cite your brand, and [Precedent](https://github.com/Shikhyy/precedent), Solidity security advice treated like case law.

## Open source contributions

<!--AUTO:oss_logos:start-->
<div align="center">
<table>
  <tr>
    <td align="center" width="16%">
      <a href="https://github.com/blowhorn-ai/tells/pulls?q=is%3Apr+author%3AShikhyy"><img src="https://github.com/blowhorn-ai.png?size=160" width="56" height="56" alt="Blowhorn"></a><br>
      <b>Blowhorn</b><br>
      <sub>4 merged</sub>
    </td>
    <td align="center" width="16%">
      <a href="https://github.com/meshery/meshkit/pulls?q=is%3Apr+author%3AShikhyy"><img src="https://github.com/meshery.png?size=160" width="56" height="56" alt="Meshery"></a><br>
      <b>Meshery</b><br>
      <sub>12 merged, 2 open</sub>
    </td>
    <td align="center" width="16%">
      <a href="https://github.com/karmada-io/karmada/pulls?q=is%3Apr+author%3AShikhyy"><img src="https://github.com/karmada-io.png?size=160" width="56" height="56" alt="karmada-io"></a><br>
      <b>karmada-io</b><br>
      <sub>1 open</sub>
    </td>
    <td align="center" width="16%">
      <a href="https://github.com/jaegertracing/jaeger/pulls?q=is%3Apr+author%3AShikhyy"><img src="https://github.com/jaegertracing.png?size=160" width="56" height="56" alt="jaegertracing"></a><br>
      <b>jaegertracing</b><br>
      <sub>1 open</sub>
    </td>
    <td align="center" width="16%">
      <a href="https://github.com/keploy/keploy/pulls?q=is%3Apr+author%3AShikhyy"><img src="https://github.com/keploy.png?size=160" width="56" height="56" alt="keploy"></a><br>
      <b>keploy</b><br>
      <sub>4 merged, 5 open</sub>
    </td>
    <td align="center" width="16%">
      <a href="https://github.com/x402-foundation/x402/pulls?q=is%3Apr+author%3AShikhyy"><img src="https://github.com/x402-foundation.png?size=160" width="56" height="56" alt="x402"></a><br>
      <b>x402</b><br>
      <sub>2 merged, 2 open</sub>
    </td>
  </tr>
</table>
</div>
<!--AUTO:oss_logos:end-->

<div align="center">
<img src="assets/oss.svg" alt="Open source timeline: pull requests to open source projects in recent weeks, one row per project, filled dots for merged and outlined dots for open, refreshed automatically." width="100%">
</div>

<p align="center">
<sub>Meshery is a <a href="https://layer5.io">Layer5</a> project.</sub><br>
<img src="https://img.shields.io/badge/Layer5-Meshery_contributor-00B39F?style=flat-square&labelColor=111111" alt="Layer5, Meshery contributor" align="middle">
&nbsp;
<img src="https://badges.layer5.io/assets/badges/first-design/first-design.png" width="44" alt="Layer5 Design Pioneer badge" align="middle">
</p>

<!--AUTO:oss_prs:start-->
**Latest activity**

- **Merged** Nov 24: [ci: update GitHub Actions to their latest versions](https://github.com/blowhorn-ai/tells/pull/95) (Blowhorn)
- **Merged** Nov 24: [ci(site): guard the Enlist control and a Coming soon split on the home page](https://github.com/blowhorn-ai/blowhorn-site/pull/737) (Blowhorn)
- **Open** since Nov 23: [fix(registry): reject SourceURL without version instead of panicking](https://github.com/meshery/meshkit/pull/1187) (Meshery)
- **Merged** Nov 23: [fix(server): harden provider package download and atomic extraction](https://github.com/meshery/meshery/pull/23574) (Meshery)
- **Open** since Nov 23: [Fix panic in RetainServiceAccountFields for secret entries without a name](https://github.com/karmada-io/karmada/pull/8114) (karmada-io)
- **Open** since Nov 23: [test(elasticsearch): cover monthly and yearly periodic index layouts](https://github.com/jaegertracing/jaeger/pull/10262) (jaegertracing)

<details>
<summary>All pull requests by project (40)</summary>
<br>

**Blowhorn**
- [ci: update GitHub Actions to their latest versions](https://github.com/blowhorn-ai/tells/pull/95) (tells, merged Nov 24)
- [ci(site): guard the Enlist control and a Coming soon split on the home page](https://github.com/blowhorn-ai/blowhorn-site/pull/737) (blowhorn-site, merged Nov 24)
- [ci(security): pin remaining floating action tags to commit SHAs](https://github.com/blowhorn-ai/blowhorn-site/pull/624) (blowhorn-site, merged Nov 23)
- [fix(verdict): treat timezone aliases as the same zone](https://github.com/blowhorn-ai/tells/pull/87) (tells, merged Nov 19)

**Meshery**
- [fix(registry): reject SourceURL without version instead of panicking](https://github.com/meshery/meshkit/pull/1187) (meshkit, open since Nov 23)
- [fix(server): harden provider package download and atomic extraction](https://github.com/meshery/meshery/pull/23574) (meshery, merged Nov 23)
- [fix(server): contain panics in HTTP handlers and auto-registration](https://github.com/meshery/meshery/pull/23988) (meshery, merged Nov 20)
- [docs: condense AGENTS.md and relocate detail to documentation](https://github.com/meshery/meshery/pull/23923) (meshery, open since Nov 18)
- [\[Kubernetes\] Do not return a nil kubeconfig for an empty file](https://github.com/meshery/meshkit/pull/1176) (meshkit, merged Nov 17)
- [\[mesheryctl\] Show N/A for a component with no model in component list](https://github.com/meshery/meshery/pull/23818) (meshery, merged Nov 17)
- [\[mesheryctl\] Report a null server version in system check instead of panicking](https://github.com/meshery/meshery/pull/23817) (meshery, merged Nov 17)
- [\[mesheryctl\] Treat a null design lookup as not found in design apply](https://github.com/meshery/meshery/pull/23816) (meshery, merged Nov 17)
- [\[mesheryctl\] Treat a null response as no filters in filter list](https://github.com/meshery/meshery/pull/23815) (meshery, merged Nov 17)
- [\[mesheryctl\] Treat a null response as an empty page in perf profile and perf result](https://github.com/meshery/meshery/pull/23814) (meshery, merged Nov 17)
- [\[Server\] Preserve the provider status when deleting a performance profile fails](https://github.com/meshery/meshery/pull/23549) (meshery, merged Nov 14)
- [\[Server\]\[mesheryctl\] Fix typos in user-facing error and log messages](https://github.com/meshery/meshery/pull/23546) (meshery, merged Nov 14)
- [\[Server\] Return 404 when deleting a performance profile that does not exist](https://github.com/meshery/meshery/pull/23544) (meshery, merged Nov 14)
- [Introduction - Shikhar Verma](https://github.com/meshery/meshery/pull/23495) (meshery, merged Nov 13)

**karmada-io**
- [Fix panic in RetainServiceAccountFields for secret entries without a name](https://github.com/karmada-io/karmada/pull/8114) (open since Nov 23)

**jaegertracing**
- [test(elasticsearch): cover monthly and yearly periodic index layouts](https://github.com/jaegertracing/jaeger/pull/10262) (open since Nov 23)

**keploy**
- [fix(templates): find an encoded placeholder after text of another width](https://github.com/keploy/keploy/pull/5390) (keploy, open since Nov 22)
- [fix(report): keep the whole body diff when a value is over 64 KiB](https://github.com/keploy/keploy/pull/5389) (keploy, open since Nov 22)
- [fix(sanitize): keep a JSON body's numbers and text when it holds a secret](https://github.com/keploy/keploy/pull/5384) (keploy, open since Nov 22)
- [fix(import): accept a folder variable that is not all strings](https://github.com/keploy/keploy/pull/5382) (keploy, open since Nov 22)
- [fix(export): list a folder's requests in a fixed order, and drop a null item](https://github.com/keploy/keploy/pull/5326) (keploy, merged Nov 22)
- [fix: pick the diff's context key in a fixed order](https://github.com/keploy/jsondiff/pull/26) (jsondiff, open since Nov 22)
- [fix(import): keep the tests of Postman folders that share a name](https://github.com/keploy/keploy/pull/5327) (keploy, merged Nov 21)
- [fix(normalize): sanitize a set again when normalizing it fails](https://github.com/keploy/keploy/pull/5325) (keploy, merged Nov 21)
- [test(learn): skip the mount-table zone tests off Linux](https://github.com/keploy/keploy/pull/5321) (keploy, merged Nov 21)

**x402**
- [docs(siwx): define origin canonicalization for domain and uri checks](https://github.com/x402-foundation/x402/pull/4348) (open since Nov 20)
- [feat(evm): add Circle USDC as the default stablecoin on eight networks](https://github.com/x402-foundation/x402/pull/4337) (merged Nov 20)
- [fix(python): give back the FacilitatorWeb3Signer nonce when a send fails](https://github.com/x402-foundation/x402/pull/4313) (merged Nov 19)
- [docs(specs): state the minimum remaining validity for exact EVM validBefore](https://github.com/x402-foundation/x402/pull/4307) (open since Nov 17)

**Hermes Agent**
- [fix(desktop): recover sessions on canonical not_found](https://github.com/NousResearch/hermes-agent/pull/152829) (open since Nov 10)
- [fix(telegram): reject unverifiable media before unbounded download](https://github.com/NousResearch/hermes-agent/pull/152811) (open since Nov 10)
- [feat(catalog): add chronos speculative reasoning plugin](https://github.com/NousResearch/hermes-agent/pull/150020) (merged Nov 10)
- [fix(local_runtime): defer psutil import and guard conftest process reap](https://github.com/NousResearch/hermes-agent/pull/150315) (open since Nov 6)

**Kestra**
- [fix(ci): skip blueprint indexing when DOC_INDEXING_WEBHOOK is unset](https://github.com/kestra-io/blueprints/pull/4619) (blueprints, merged Nov 4)
- [feat(gooddata): add workspaces, dataSources, executions, layouts tasks and trigger (closes #4)](https://github.com/kestra-io/plugin-gooddata/pull/5) (plugin-gooddata, merged Oct 21)
- [feat(blueprints): add automated data quality validator with DuckDB](https://github.com/kestra-io/blueprints/pull/1606) (blueprints, merged Oct 15)

</details>
<!--AUTO:oss_prs:end-->

## Tech stack

<div align="center">

<p>
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white" alt="Go">
<img src="https://img.shields.io/badge/Rust-DEA584?style=flat-square&logo=rust&logoColor=black" alt="Rust">
<img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JavaScript">
<img src="https://img.shields.io/badge/Kotlin-7F52FF?style=flat-square&logo=kotlin&logoColor=white" alt="Kotlin">
<img src="https://img.shields.io/badge/Solidity-363636?style=flat-square&logo=solidity&logoColor=white" alt="Solidity">
</p>

<p>
<img src="https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js">
<img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
<img src="https://img.shields.io/badge/Three.js-000000?style=flat-square&logo=threedotjs&logoColor=white" alt="Three.js">
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
<img src="https://img.shields.io/badge/Supabase-3FCF8E?style=flat-square&logo=supabase&logoColor=white" alt="Supabase">
<img src="https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white" alt="Redis">
<img src="https://img.shields.io/badge/DuckDB-FFF000?style=flat-square&logo=duckdb&logoColor=black" alt="DuckDB">
<img src="https://img.shields.io/badge/Snowflake-29B5E8?style=flat-square&logo=snowflake&logoColor=white" alt="Snowflake">
<img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker">
<img src="https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white" alt="Vercel">
</p>

<p>
<img src="https://img.shields.io/badge/Solana-9945FF?style=flat-square&logo=solana&logoColor=white" alt="Solana">
<img src="https://img.shields.io/badge/Chainlink-375BD2?style=flat-square&logo=chainlink&logoColor=white" alt="Chainlink">
<img src="https://img.shields.io/badge/MCP-3A3A3A?style=flat-square" alt="MCP">
<img src="https://img.shields.io/badge/FalkorDB-3A3A3A?style=flat-square" alt="FalkorDB">
<img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" alt="LangChain">
</p>

<img src="assets/stack.svg" alt="Primary language across my public repositories, refreshed automatically." width="100%">

</div>

**Built for and with**

<div align="center">
<p>
<a href="https://github.com/Shikhyy/cairnquill"><img src="https://img.shields.io/badge/Snowflake-Cairnquill-2A2A2A?style=flat-square&logo=snowflake&logoColor=white&labelColor=29B5E8" alt="Snowflake, Cairnquill"></a>
<a href="https://github.com/Shikhyy/precedent"><img src="https://img.shields.io/badge/Sanity-Precedent-2A2A2A?style=flat-square&logo=sanity&logoColor=white&labelColor=F03E2F" alt="Sanity, Precedent"></a>
<a href="https://github.com/Shikhyy/sangam"><img src="https://img.shields.io/badge/Gnani-Sangam-444444?style=flat-square&labelColor=111111" alt="Gnani, Sangam"></a>
<a href="https://github.com/Shikhyy/wiftape"><img src="https://img.shields.io/badge/Robinhood_Chain-WIF_Tape-444444?style=flat-square&labelColor=111111" alt="Robinhood Chain, WIF Tape"></a>
<a href="https://github.com/Shikhyy/enfeoff"><img src="https://img.shields.io/badge/Solana-Enfeoff-2A2A2A?style=flat-square&logo=solana&logoColor=white&labelColor=9945FF" alt="Solana, Enfeoff"></a>
<a href="https://github.com/Shikhyy/wyrmline"><img src="https://img.shields.io/badge/HydraDB-wyrmline-444444?style=flat-square&labelColor=111111" alt="HydraDB, wyrmline"></a>
<a href="https://github.com/Shikhyy/AEOspy"><img src="https://img.shields.io/badge/Bright_Data-AEOspy-2A2A2A?style=flat-square&labelColor=3D7FFC" alt="Bright Data, AEOspy"></a>
<a href="https://github.com/Shikhyy/Pantheon"><img src="https://img.shields.io/badge/0G-Pantheon-444444?style=flat-square&labelColor=111111" alt="0G, Pantheon"></a>
</p>
</div>

## GitHub in numbers

<div align="center">
<img src="assets/stats.svg" alt="GitHub in numbers: commits, pull requests, outside projects, original repositories and contribution streaks, refreshed automatically." width="100%">
<br><br>
<img src="assets/tape.svg" alt="A cassette card for Shikhar Verma. The tracklist is my eight most recent repositories, and the equalizer is built from 53 weeks of contributions." width="100%">
<br><br>
<img src="assets/city.svg" alt="An isometric city built from the last year of contributions on a bordered base. Taller buildings are busier days." width="100%">
<br><br>
<img src="https://komarev.com/ghpvc/?username=Shikhyy&label=Profile%20views&color=111111&style=flat-square" alt="Profile views">
</div>

## Play

<div align="center">
<a href="https://shikhyy.github.io/Shikhyy/web/invaders/"><img src="assets/invaders.svg" alt="Contribution Invaders. A year of daily contributions as a grid of invaders, with a ship sweeping underneath. Click to play." width="100%"></a>
<br>
<a href="https://shikhyy.github.io/Shikhyy/web/invaders/"><b>Play Contribution Invaders</b></a>
<br>
<sub>Every invader is a real day from my last year on GitHub, and the ringed ones are my busiest days. Arrow keys or drag to move, space or tap to fire.</sub>
</div>

<br>

<p align="center">
  <sub>The numbers, open source activity, recent repositories, language chart and contribution graphics refresh automatically every six hours through a GitHub Action running <code>scripts/update.py</code>. <!--AUTO:updated:start-->Last updated 2026-11-25 UTC<!--AUTO:updated:end--> All repositories are on the <a href="https://github.com/Shikhyy?tab=repositories">repositories tab</a>.</sub>
</p>

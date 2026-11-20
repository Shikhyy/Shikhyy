"""Project metadata shared by update.py and generate.py."""

# friendly names for organisations whose login is not how I'd write them
LABELS = {
    "meshery": "Meshery",
    "NousResearch": "Hermes Agent",
    "kestra-io": "Kestra",
    "x402-foundation": "x402",
    "blowhorn-ai": "Blowhorn",
}

# One genuinely interesting fact per project, each taken from that project's own README.
# update.py shows one per day, rotating through the list.
SPOTLIGHT = [
    ("Lineage", "lineage",
     "Its attack lab runs the phishing message you write twice on the real engine, once with no guard and once behind Lineage, "
     "and shows the difference computed from real data."),
    ("Sentinyx", "sentinyx",
     "Every night it scans the newest tokens on Base and publishes the results as open data: a table, CSV, JSON and an Atom feed."),
    ("Enfeoff", "enfeoff",
     "A prompt-injected \"send everything to the attacker\" fails with `RecipientNotAllowed`, because the recipient check "
     "runs before the budget check."),
    ("ResilientPay", "ResilientPay",
     "A whole payment fits in a 106-byte envelope, which is why sending it over SMS takes two segments instead of four."),
    ("OrderBook-DST", "orderbook-dst",
     "Its tasks are modelled on real failures: Knight Capital's roughly $440M loss in 2012, FTX and Alameda in 2022, "
     "and the LME nickel halt the same year."),
    ("Cairnquill", "cairnquill",
     "It doesn't trust its own model. Every number the LLM drafts is re-checked by deterministic SQL against the evidence, "
     "and one invented figure blocks the whole draft."),
    ("wyrmline", "wyrmline",
     "Every core function is a single raw OpenCypher query, because supply-chain risk is fundamentally a graph problem."),
    ("Nexus", "Nexus",
     "It is my biggest repo by commit count: a 3D human and AI co-evolution engine with a fleet of agents behind it."),
    ("GOSSIP", "GOSSIP",
     "You bet on an exact value on a Gaussian curve instead of yes or no, so a four-sigma surprise can pay around 1,000x."),
    ("cobot-arm", "cobot-arm",
     "The 3D arm on its website is not an illustration. It is the project's own CAD export, assembled into six working axes."),
    ("Sangam", "sangam",
     "It measures how you mix Hindi and English, then keeps the agent's replies in the same mix."),
    ("VitaSync", "VitaSync",
     "A doctor cannot query a patient's records unless the patient has granted active consent."),
]

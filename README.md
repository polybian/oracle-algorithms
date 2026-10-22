# oracle-algorithms

Implementations of the **Deutsch-Jozsa algorithm family** — the oracle
algorithms that proved quantum computers can beat classical ones —
built from scratch with Qiskit: **Bernstein-Vazirani** (hidden string
in one query) and **Simon** (hidden period with O(n) queries).

This is the fifth implementation in my quantum series (#19 in my portfolio), continuing the
oracle-algorithm thread from `quantum-circuits-implementation` (Deutsch-Jozsa).
I love molecular engineering, and above all QUANTUM.

## The three implementations

| # | Script | What it demonstrates |
|---|--------|----------------------|
| 1 | `01_bernstein_vazirani.py` | **Hidden string in 1 query** — s = '101', '011', '110' all recovered via phase kickback |
| 2 | `02_simon.py` | **Hidden period** — s = '101' found via Simon's circuit + classical GF(2) elimination |
| 3 | `03_query_advantage.py` | **Query-complexity table** — textbook DJ / BV / Simon: quantum vs classical |

## Architecture

```
|0>n -- H -- [oracle: CNOT(i -> ancilla) where s_i = 1] -- H -- measure = s   (BV)
|1>  -- X -- H ---------------------------------------------------------------

|0>n -- H -- [oracle f(x) = min(x, x XOR s), 3 CNOTs] -- H -- measure = y     (Simon)
|0>n -----------------------------------------------   with y·s = 0 mod 2
```

BV learns the string through phase kickback; Simon collects linear
equations y·s = 0 and solves them classically. See
[docs/architecture.md](docs/architecture.md) for the full design,
including the hand-derived Simon oracle (truth table → three CNOTs).

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

bash run_all.sh
```

## Validation

Measured on Qiskit Aer 2.6.0 (seeded simulator), 2026-10-21:

| Implementation | Prediction | Measured |
|------------|-----------|----------|
| Bernstein-Vazirani (3 hidden strings, 8 shots each) | each s recovered in 1 query | '101'→'101', '011'→'011', '110'→'110' — all match, assertion passed |
| Simon (n=3, s='101', 64 shots) | outcomes satisfy y·s=0; period recovered | outcomes 000×23, 010×15, 101×15, 111×11; 3 equations collected; recovered '101' == hidden — assertion passed |
| Query advantage | textbook table | DJ: 1 vs up to 2^(n-1)+1; BV: 1 vs n; Simon: O(n) vs O(2^(n/2)) — labeled as textbook facts, assertion passed |

Simon's measured outcomes are exactly the theory's set {000, 010, 101,
111} — every y satisfies y·s = 0 mod 2 for s = '101'.

## Why this matters (the one-paragraph version)

These three algorithms are the same trick asked three ways: put the
input in superposition, let the oracle act on everything at once via
phase kickback, and interfere the results so a global property becomes
measurable. Deutsch-Jozsa was the first proven quantum speedup,
Bernstein-Vazirani shows it on the natural problem of learning a
hidden string, and Simon's *exponential* separation is the direct
prototype of Shor's factoring algorithm. This project makes that
progression concrete — you watch the hidden string and the hidden
period come out of real circuits.

## Plain-language guide

[simplified-explanation.md](simplified-explanation.md) —
the oracle game, the secret code, and the hidden rhythm, in plain
language (Spanish).

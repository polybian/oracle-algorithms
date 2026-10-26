# Architecture

## What this project is

Implementations of the **Deutsch-Jozsa algorithm family** (the oracle
algorithms that proved quantum computers can beat classical ones)
built from scratch with Qiskit: **Bernstein-Vazirani** (1993) and
**Simon** (1994). This is the third implementation in my quantum
series, continuing where `quantum-circuits-implementation` (Deutsch-Jozsa) and
`bb84-qkd-implementation` left off.

## Layout

```
oracle-algorithms/
├── README.md
├── requirements.txt           # qiskit + qiskit-aer + numpy
├── run_all.sh
├── scripts/
│   ├── 01_bernstein_vazirani.py  # hidden string s recovered in 1 query
│   ├── 02_simon.py               # hidden period via Simon + GF(2) solve
│   └── 03_query_advantage.py     # textbook query-complexity table
├── docs/
│   └── architecture.md        # this file
└── simplified-explanation.md  # plain-language guide (Spanish)
```

## 01. Bernstein-Vazirani: how one query learns n bits

The oracle hides s and computes f(x) = s·x mod 2. The circuit:

```
|0>^n -- H -- [oracle: CNOT(i -> ancilla) where s_i = 1] -- H -- measure = s
|1>    -- X -- H ----------------------------------------------- (|->)
```

With the ancilla in |->, the oracle's action becomes a *phase*:
|x>|-> -> (-1)^(s·x) |x>|->. The input register now holds a phase
pattern encoding s, and the final Hadamards convert phase into
computational-basis information: the measurement reads out s
directly. One query, n bits, deterministic on an ideal machine.
Classically each query reveals at most one bit of s, hence n queries.

## 02. Simon: the oracle derivation

Hidden period s = '101' (n = 3), oracle f(x) = min(x, x XOR s) as
3-bit integers. This is 2-to-1 with exactly the right period:
f(x XOR s) = min(x XOR s, x) = f(x), and x != x XOR s for nonzero s.

Truth table (x -> f), bits listed MSB-first:

```
000 -> 000    100 -> 001
001 -> 001    101 -> 000
010 -> 010    110 -> 011
011 -> 011    111 -> 010
```

Reading the output bits: f2 = 0 always; f1 = 1 iff x in
{010,011,110,111}, i.e. f1 = x1; f0 = 1 iff x in {001,011,100,110},
i.e. f0 = x0 XOR x2. So the oracle is three CNOTs:

```
q3 (f0) <--- CNOT(q0), CNOT(q2)
q4 (f1) <--- CNOT(q1)
q5 (f2) <--- (nothing)
```

Simon's circuit (H on inputs, oracle, H on inputs, measure inputs)
yields y with y·s = 0 mod 2. For s = '101', valid outcomes are
{000, 010, 101, 111}; any two nonzero independent ones determine s
uniquely over GF(2). The script collects outcomes on a seeded
simulator and solves the linear system by brute-force nullspace
search (exact for n = 3), asserting the recovered period.

## Design choices

- **Hand-derived oracles, verified by truth table**: no black-box
  synthesis. Every gate is justified above, so the implementation
  is inspectable and the derivation is checkable.
- **Seeded simulator**: both scripts reproduce their results
  bit-for-bit; the README's numbers are regenerated, not remembered.
- **Classical post-processing kept explicit**: Simon's quantum part
  ends at the measurement; the GF(2) solve is plainly classical
  code, which is the clearest way to present the algorithm.
- **Assertions as the verdict**: BV asserts all three hidden strings
  recovered; Simon asserts the recovered period equals the hidden
  one. The algorithmic claims are passing checks, not commentary.

## What this is not

Not a complexity proof and not new research: these are textbook
algorithms implemented cleanly. The value is operational: real
circuits, real measured outcomes, and the query advantage made
concrete instead of notional.

"""
02 — Simon's algorithm: find a hidden period with O(n) queries.

Problem: an oracle hides a nonzero n-bit period s. The function f is
guaranteed 2-to-1 with f(x) = f(x XOR s) for all x. Classically,
finding s needs O(2^(n/2)) queries (birthday bound). Simon's circuit
produces, per query, a random y with y·s = 0 (mod 2); collecting n-1
linearly independent equations reveals s by classical elimination.

This script uses n = 3, hidden period s = '101', with the oracle
f(x) = min(x, x XOR s) built from CNOTs (derived in
docs/architecture.md). Outcomes are gathered on a seeded simulator,
the linear system is solved over GF(2), and the recovered period is
asserted equal to the hidden one.

Run:
    python3 scripts/02_simon.py [--shots 64] [--seed 5]
"""

import argparse

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

N = 3
HIDDEN_S = "101"  # s[0] <-> qubit 0


def build_simon_circuit() -> QuantumCircuit:
    """Simon's circuit for n=3, s='101', f(x) = min(x, x XOR s).

    Oracle (input q0..q2, output q3..q5):
      f2 = 0, f1 = x1, f0 = x0 XOR x2   (see docs/architecture.md)
    """
    qc = QuantumCircuit(2 * N, N)
    qc.h(range(N))
    # Oracle.
    qc.cx(1, 4)        # f1 = x1
    qc.cx(0, 3)        # f0 = x0 XOR x2
    qc.cx(2, 3)
    qc.h(range(N))
    qc.measure(range(N), range(N))
    return qc


def bits_to_int(key: str) -> int:
    """Qiskit outcome key -> int with bit i <-> qubit i."""
    return int(key[::-1], 2)


def int_to_bits(v: int, n: int) -> str:
    """Int -> bitstring with s[0] <-> qubit 0."""
    return "".join(str((v >> i) & 1) for i in range(n))


def dot_gf2(a: int, b: int) -> int:
    return bin(a & b).count("1") % 2


def recover_period(rows: list[int], n: int) -> int | None:
    """Brute-force GF(2) nullspace: the unique nonzero v with rows·v = 0."""
    candidates = [
        c for c in range(1, 2 ** n)
        if all(dot_gf2(r, c) == 0 for r in rows)
    ]
    return candidates[0] if len(candidates) == 1 else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", type=int, default=64)
    parser.add_argument("--seed", type=int, default=5)
    args = parser.parse_args()

    hidden = bits_to_int(HIDDEN_S)
    qc = build_simon_circuit()
    sim = AerSimulator(seed_simulator=args.seed)
    counts = sim.run(qc, shots=args.shots).result().get_counts()

    rows: list[int] = []
    print(f"Hidden period s = '{HIDDEN_S}' (kept secret from the solver)")
    print(f"\nMeasurement outcomes ({args.shots} shots):")
    for key in sorted(counts):
        y = bits_to_int(key)
        tag = ""
        if y != 0 and y not in rows:
            rows.append(y)
            tag = "  <- new equation"
        print(f"  y = {int_to_bits(y, N)}   ({counts[key]:>3} shots){tag}")

    print(f"\nLinear equations collected (y·s = 0 mod 2):")
    for r in rows:
        print(f"  {int_to_bits(r, N)} · s = 0")

    recovered = recover_period(rows, N)
    assert recovered is not None, "Equations under-constrained; no unique period."
    recovered_s = int_to_bits(recovered, N)
    print(f"\nRecovered period: '{recovered_s}'")
    assert recovered == hidden, (
        f"Wrong period: recovered '{recovered_s}', hidden '{HIDDEN_S}'"
    )
    print("OK — Simon's circuit found the hidden period; classical "
          "elimination confirmed it.")


if __name__ == "__main__":
    main()

"""
01 — Bernstein-Vazirani: recover a hidden bitstring in ONE query.

Problem: an oracle hides an n-bit string s. The oracle computes
f(x) = s·x (mod 2), the dot product of s with the input x.
Classically you need n queries (one per bit). Bernstein-Vazirani
recovers the entire string with a single oracle call, using phase
kickback: the ancilla prepared in |-> imprints (-1)^(s·x) onto the
input register, and the final Hadamards turn that phase pattern
directly into the bitstring s.

This script tests three different hidden strings (3 bits each),
seeded for reproducibility, and asserts the recovered string matches
the hidden one every time.

Run:
    python3 scripts/01_bernstein_vazirani.py [--shots 8]
"""

import argparse

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

HIDDEN_STRINGS = ["101", "011", "110"]


def build_bv_circuit(s: str) -> QuantumCircuit:
    """BV circuit for hidden string s (s[0] <-> qubit 0)."""
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    # Ancilla in |-> for phase kickback.
    qc.x(n)
    qc.h(range(n + 1))
    # Oracle: CNOT from input i to ancilla wherever s has a 1.
    for i, bit in enumerate(s):
        if bit == "1":
            qc.cx(i, n)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc


def recover_s(counts: dict, n: int) -> str:
    """Most frequent outcome, un-reversed (qiskit is little-endian)."""
    key = max(counts, key=counts.get)
    return key[::-1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", type=int, default=8)
    args = parser.parse_args()

    sim = AerSimulator(seed_simulator=21)
    print(f"{'hidden s':>10}  {'recovered':>10}  {'match'}")
    print("-" * 34)
    for s in HIDDEN_STRINGS:
        n = len(s)
        qc = build_bv_circuit(s)
        counts = sim.run(qc, shots=args.shots).result().get_counts()
        recovered = recover_s(counts, n)
        match = recovered == s
        print(f"{s:>10}  {recovered:>10}  {'YES' if match else 'NO'}")
        assert match, f"Failed to recover hidden string {s}: got {recovered}"

    print(f"\nOK — all {len(HIDDEN_STRINGS)} hidden strings recovered "
          f"in a single oracle query each.")


if __name__ == "__main__":
    main()

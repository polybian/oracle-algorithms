"""
03 - Query advantage: the Deutsch-Jozsa family at a glance.

Prints the query-complexity comparison for the three oracle
algorithms in this series. These are textbook results (not measured
here - the implementations that demonstrate them live in scripts
01 and 02 of this project, and in 04_deutsch_jozsa.py of
quantum-circuits-implementation):

  Deutsch-Jozsa:     1 quantum query vs up to 2^(n-1) + 1 classical
  Bernstein-Vazirani: 1 quantum query vs n classical
  Simon:             O(n) quantum queries vs O(2^(n/2)) classical

Why it matters: Deutsch-Jozsa was the first proven quantum speedup,
Bernstein-Vazirani shows the speedup on a more natural problem
(learning a hidden string), and Simon's exponential separation is
the direct ancestor of Shor's factoring algorithm.

Run:
    python3 scripts/03_query_advantage.py
"""


def main() -> None:
    print("Query complexity - textbook results for the oracle family:\n")
    print(f"  {'Algorithm':<20} {'Quantum queries':<16} {'Classical queries'}")
    print("  " + "-" * 58)
    print(f"  {'Deutsch-Jozsa':<20} {'1':<16} {'up to 2^(n-1) + 1'}")
    print(f"  {'Bernstein-Vazirani':<20} {'1':<16} {'n'}")
    print(f"  {'Simon':<20} {'O(n)':<16} {'O(2^(n/2))'}")
    print()
    print("  n = 10:  DJ needs 1 vs up to 513;  BV needs 1 vs 10;")
    print("           Simon needs ~10 vs ~32.")
    print("  n = 50:  DJ needs 1 vs up to 2^49; BV needs 1 vs 50;")
    print("           Simon needs ~50 vs ~2^25 (33 million).")
    print()
    print("OK - table printed. (Textbook facts; see scripts 01/02 for the")
    print("implementations that realize the quantum column.)")


if __name__ == "__main__":
    main()

# Phase 40 reproducibility and validation

Environment: Python 3 with numpy, C++17 compiler. The exact finite fields are 998244353 (generator 3) and 2013265921 (generator 31).

Run the 16 current Phase 40 unit tests:

```sh
g++ -O3 -std=c++17 phase40_exact_audit.cpp -o phase40_exact_audit
python -m unittest -v tests_phase40
```

Regenerate the C++ inputs without relying on any previous mounted source (standalone source copies are included here):

```sh
python - <<'PY'
import phase40_four_green as p
for prime,gen in p.PRIMES:
    for n in (8,16,32,64,128):
        p.export_instance(p.build(n,prime,gen),f'N{n}_p{prime}.txt')
PY
```

Run complete N=8 mapping enumeration (dual fields):

```sh
./phase40_exact_audit N8_p998244353.txt 0 0 rescue
./phase40_exact_audit N8_p2013265921.txt 0 0 rescue
```

The second and fourth positional command-line fields are a maximum sequential count and number of pseudorandom trials; zero means full enumeration for the second count, except when the third parameter sets a number of trials. `rescue` uses an alternative 5-cycle only if the first rank is insufficient. **A deficient certificate never proves a factorization exists.**

Further checks:

```sh
python phase40_holonomy.py
python phase40_local_synthesis.py
python phase40_weyl_control.py
```

`phase40_jacobian_certificates.json` provides exact nonzero modular determinant residues for the same underlying integer-weighted graphs. `phase40_mapping_audit.json` records the checked mapping counts. N>8 are pseudorandom samples only. Check `VALIDATION.md` for the fresh-reproduction report.

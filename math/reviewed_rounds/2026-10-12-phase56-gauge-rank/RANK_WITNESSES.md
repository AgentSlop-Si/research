# Phase 56 finite rank and minor witnesses

All cases use seed 560123, depth two and the same recorded integer sample at both primes. B=T(N+1)-N-1 is the gauge ceiling; Q=(N-1)^2 is the target dimension. Ranks refer equally to the source-compatible raw logarithmic chart and the gauge-fixed direct cross-ratio chart on the verified nonzero domain.

## Exact image dimensions

| N | q1+q2 | Rank, both primes | B | Q | Characteristic-zero conclusion |
|---:|:---:|---:|---:|---:|:---|
| 5 | 2+2 | 16 | 18 | 16 | Target dominance |
| 7 | 3+3 | 36 | 40 | 36 | Target dominance |
| 8 | 3+4 | 49 | 54 | 49 | Target dominance |
| 11 | 3+3 | 60 | 60 | 100 | Exact image dimension 60; not target-dominant |
| 11 | 4+4 | 84 | 84 | 100 | Exact image dimension 84; not target-dominant |
| 11 | 4+5 | 96 | 96 | 100 | Exact image dimension 96; not target-dominant |
| 11 | 5+5 | 100 | 108 | 100 | Target dominance |
| 13 | 5+5 | 126 | 126 | 144 | Exact image dimension 126; not target-dominant |
| 13 | 6+6 | 144 | 154 | 144 | Target dominance |
| 17 | 8+8 | 256 | 270 | 256 | Target dominance |
| 19 | 9+9 | 324 | 340 | 324 | Target dominance |
| 23 | 11+11 | 484 | 504 | 484 | Target dominance |
| 31 | 15+15 | 900 | 928 | 900 | Target dominance |

The nine dominant configurations attain T=N-1 at the listed sizes in the unrestricted complex-gain family. The four smaller dimensions are 60, 84, 96 and 126. These are existential statements for the recorded cycle orders, not for every order choice, every parameter point, every target, or any untested size. They do not establish Fourier membership or a Fourier-specific minimum.

## Nonzero minors at both primes

One raw and one direct minor are recorded in each case. Every listed determinant is a residue in its stated field and is nonzero. The two exact determinant methods agree on all 52 minors.

| N | q1+q2 | Prime p | Rank r | Raw logarithmic minor det mod p | Direct cross-ratio minor det mod p | Guards |
|---:|:---:|---:|---:|---:|---:|:---:|
| 5 | 2+2 | 65521 | 16 | 28073 | 47865 | All pass |
| 5 | 2+2 | 1000003 | 16 | 444735 | 135578 | All pass |
| 7 | 3+3 | 65521 | 36 | 38437 | 55405 | All pass |
| 7 | 3+3 | 1000003 | 36 | 664550 | 601576 | All pass |
| 8 | 3+4 | 65521 | 49 | 48719 | 53029 | All pass |
| 8 | 3+4 | 1000003 | 49 | 411864 | 231748 | All pass |
| 11 | 3+3 | 65521 | 60 | 50299 | 42599 | All pass |
| 11 | 3+3 | 1000003 | 60 | 460136 | 355263 | All pass |
| 11 | 4+4 | 65521 | 84 | 11294 | 22582 | All pass |
| 11 | 4+4 | 1000003 | 84 | 489603 | 776908 | All pass |
| 11 | 4+5 | 65521 | 96 | 22520 | 21501 | All pass |
| 11 | 4+5 | 1000003 | 96 | 674935 | 257836 | All pass |
| 11 | 5+5 | 65521 | 100 | 20350 | 13963 | All pass |
| 11 | 5+5 | 1000003 | 100 | 181447 | 381824 | All pass |
| 13 | 5+5 | 65521 | 126 | 14174 | 40721 | All pass |
| 13 | 5+5 | 1000003 | 126 | 717755 | 648984 | All pass |
| 13 | 6+6 | 65521 | 144 | 23645 | 16443 | All pass |
| 13 | 6+6 | 1000003 | 144 | 341430 | 614854 | All pass |
| 17 | 8+8 | 65521 | 256 | 24041 | 35586 | All pass |
| 17 | 8+8 | 1000003 | 256 | 166828 | 692870 | All pass |
| 19 | 9+9 | 65521 | 324 | 34209 | 14468 | All pass |
| 19 | 9+9 | 1000003 | 324 | 729389 | 509483 | All pass |
| 23 | 11+11 | 65521 | 484 | 26031 | 29056 | All pass |
| 23 | 11+11 | 1000003 | 484 | 667292 | 145785 | All pass |
| 31 | 15+15 | 65521 | 900 | 50838 | 36600 | All pass |
| 31 | 15+15 | 1000003 | 900 | 3138 | 896811 | All pass |

### Guard meaning

“All pass” means all sampled logarithmic coordinates and rational denominators are nonzero, every matrix entry is nonzero, normalization preserves every cross ratio, the independently propagated exact dual direction agrees, and zeroing a row of the reduced minor is rejected. The raw gauge subspace has 2N+1 independently checked kernel directions; it need not exhaust the whole kernel. Prime testing, exact inverse checks and fixed-width product bounds also pass.

The admissibility rejection controls are zero gain, h=1, h=0, zero coefficient and zero mask. No floating-point rank or determinant computation is used. The conservative largest product bound is 991003964003964 < 9223372036854775807. These bounded checks do not validate unrestricted larger dimensions or primes.

## Exact ordered minor indices and matrix identities

Indices are zero-based. Each a..b token expands to every integer a,a+1,...,b, inclusive. Tokens and indices must remain in the displayed order; do not sort the selected columns, since this could change the determinant sign. Each selected row list and column list has exactly r entries.

Rows enumerate Y_ij in row-major order, with i=1,...,N-1 and then j=1,...,N-1. Raw columns enumerate stage 1 and then stage 2; within each term, gain Euler directions at vertices 0,...,N-2 (last gain held as reference), then h and a Euler directions; all N mask Euler directions follow. Direct columns enumerate the same stages and terms; a first term contributes h only, while each nonfirst term contributes gain coordinates at vertices 1,...,N-1, h and a; mask coordinates at vertices 1,...,N-1 follow.

Matrix SHA-256 values hash the complete Jacobian serialized in row-major order as little-endian signed 64-bit reduced residues. They do not hash JSON formatting. The original integer samples and full replay inputs are retained in the separately sealed evidence package. The tables below preserve exact witness selection and matrix identity; they are not a standalone executable reproduction dataset.

### N=5, q1+q2=2+2, p=65521

- Raw shape: 16 by 29; direct shape: 16 by 18.
- Raw logarithmic rows: 0..15.
- Raw logarithmic columns: 0..10, 12..16.
- Raw logarithmic determinant modulo p: 28073.
- Direct cross-ratio rows: 0..15.
- Direct cross-ratio columns: 0..15.
- Direct cross-ratio determinant modulo p: 47865.
- Raw matrix SHA-256: `0e0f705e05a1d1b1106d082d396cdf1d1cf9364a83f19b6419cdc89fcc014d6b`.
- Direct matrix SHA-256: `f2cece16058a4ba72cb828da20b70db54b65679ca5b2aee155282d44fd2728ec`.

### N=5, q1+q2=2+2, p=1000003

- Raw shape: 16 by 29; direct shape: 16 by 18.
- Raw logarithmic rows: 0..15.
- Raw logarithmic columns: 0..10, 12..16.
- Raw logarithmic determinant modulo p: 444735.
- Direct cross-ratio rows: 0..15.
- Direct cross-ratio columns: 0..15.
- Direct cross-ratio determinant modulo p: 135578.
- Raw matrix SHA-256: `62f0bd9db8a14db84a5509a98547bc145047645b810243bb92e49b829754c9d3`.
- Direct matrix SHA-256: `520ae99c7d3bd7f26da7a4e9a8199d78b2055e2f6b1dbeb0681af30a68300b47`.

### N=7, q1+q2=3+3, p=65521

- Raw shape: 36 by 55; direct shape: 36 by 40.
- Raw logarithmic rows: 0..35.
- Raw logarithmic columns: 0..22, 24..36.
- Raw logarithmic determinant modulo p: 38437.
- Direct cross-ratio rows: 0..35.
- Direct cross-ratio columns: 0..35.
- Direct cross-ratio determinant modulo p: 55405.
- Raw matrix SHA-256: `fb48f409e86e629f010435619b0a9043151d9b1070b4824b1a71319b348661f6`.
- Direct matrix SHA-256: `2099585e4fc6fc6f4dbed17180ae4d5895308735cbcf99f9d81e66440abfb858`.

### N=7, q1+q2=3+3, p=1000003

- Raw shape: 36 by 55; direct shape: 36 by 40.
- Raw logarithmic rows: 0..35.
- Raw logarithmic columns: 0..22, 24..36.
- Raw logarithmic determinant modulo p: 664550.
- Direct cross-ratio rows: 0..35.
- Direct cross-ratio columns: 0..35.
- Direct cross-ratio determinant modulo p: 601576.
- Raw matrix SHA-256: `1ec7bd1b52b748463834b87a2f03798c9749d8e1812658f15c4b0cbfc9b81266`.
- Direct matrix SHA-256: `3abe8dbfa1a25423a3c81c2ed81f75fa50646b221f8893f1efb0a51260ed27e5`.

### N=8, q1+q2=3+4, p=65521

- Raw shape: 49 by 71; direct shape: 49 by 54.
- Raw logarithmic rows: 0..48.
- Raw logarithmic columns: 0..25, 27..49.
- Raw logarithmic determinant modulo p: 48719.
- Direct cross-ratio rows: 0..48.
- Direct cross-ratio columns: 0..48.
- Direct cross-ratio determinant modulo p: 53029.
- Raw matrix SHA-256: `a36ec0d1dd50ddaa38ed818375c32d84622c195093dd5efd747bbfc262b56ce2`.
- Direct matrix SHA-256: `a222201f4d6b7fb64d92c5f4edfe313a54b579eb195e9ed7b9f0b7ca87a71d74`.

### N=8, q1+q2=3+4, p=1000003

- Raw shape: 49 by 71; direct shape: 49 by 54.
- Raw logarithmic rows: 0..48.
- Raw logarithmic columns: 0..25, 27..49.
- Raw logarithmic determinant modulo p: 411864.
- Direct cross-ratio rows: 0..48.
- Direct cross-ratio columns: 0..48.
- Direct cross-ratio determinant modulo p: 231748.
- Raw matrix SHA-256: `c3dbff9d78ad37e2cc3ed20f6bf16c1937f349d7387cac58eb7af56e899a7122`.
- Direct matrix SHA-256: `59f1a69d88f381ca5fde6bb1e3d1aee61d1badea58f3a927e30b84104e00a436`.

### N=11, q1+q2=3+3, p=65521

- Raw shape: 100 by 83; direct shape: 100 by 60.
- Raw logarithmic rows: 0..59.
- Raw logarithmic columns: 0..34, 36..59, 70.
- Raw logarithmic determinant modulo p: 50299.
- Direct cross-ratio rows: 0..59.
- Direct cross-ratio columns: 0..59.
- Direct cross-ratio determinant modulo p: 42599.
- Raw matrix SHA-256: `effcaec8b2a62525521d8614e69b348034faeddfeafdef0acb6e72564db1b942`.
- Direct matrix SHA-256: `94b86b472f40487d4d959f904a19d9321151a9822305aae8a363cada621dd547`.

### N=11, q1+q2=3+3, p=1000003

- Raw shape: 100 by 83; direct shape: 100 by 60.
- Raw logarithmic rows: 0..59.
- Raw logarithmic columns: 0..34, 36..59, 70.
- Raw logarithmic determinant modulo p: 460136.
- Direct cross-ratio rows: 0..59.
- Direct cross-ratio columns: 0..59.
- Direct cross-ratio determinant modulo p: 355263.
- Raw matrix SHA-256: `a9c6cbe53ae8570293392b4e6fb86a3462f3c1fc09ea16f488ed23a362ff6b3c`.
- Direct matrix SHA-256: `9e51654e70a7bc629c0b70cf8eb7ff253e3cec8967a3d342aa1a453723f7bae7`.

### N=11, q1+q2=4+4, p=65521

- Raw shape: 100 by 107; direct shape: 100 by 84.
- Raw logarithmic rows: 0..83.
- Raw logarithmic columns: 0..46, 48..83, 94.
- Raw logarithmic determinant modulo p: 11294.
- Direct cross-ratio rows: 0..83.
- Direct cross-ratio columns: 0..83.
- Direct cross-ratio determinant modulo p: 22582.
- Raw matrix SHA-256: `2ab0613973ab2a18130e1053df633b927cc3d194a2aaaeeb7dbe00e541f22eb8`.
- Direct matrix SHA-256: `4c80b47fe679fba749c2656c18132eacfa819d47c6f5093efe9f086bed825004`.

### N=11, q1+q2=4+4, p=1000003

- Raw shape: 100 by 107; direct shape: 100 by 84.
- Raw logarithmic rows: 0..83.
- Raw logarithmic columns: 0..46, 48..83, 94.
- Raw logarithmic determinant modulo p: 489603.
- Direct cross-ratio rows: 0..83.
- Direct cross-ratio columns: 0..83.
- Direct cross-ratio determinant modulo p: 776908.
- Raw matrix SHA-256: `f25498579e814a77cdb7a9e33f565e39821252efd56a8e382fe94940ffdd2aa7`.
- Direct matrix SHA-256: `712a2d47f49de1470df5323af2dfd24c3e3002b0941e9700a7b25e086fb10ddf`.

### N=11, q1+q2=4+5, p=65521

- Raw shape: 100 by 119; direct shape: 100 by 96.
- Raw logarithmic rows: 0..95.
- Raw logarithmic columns: 0..46, 48..95, 106.
- Raw logarithmic determinant modulo p: 22520.
- Direct cross-ratio rows: 0..95.
- Direct cross-ratio columns: 0..95.
- Direct cross-ratio determinant modulo p: 21501.
- Raw matrix SHA-256: `8444f9b9dc9878bc7f4419f392512a32fadb6721ffd8d075839197db1a1fb33f`.
- Direct matrix SHA-256: `67e2331f59b3eff5212fa63268d0d65ef1a1a03b9d130ff0b11ec261bd892003`.

### N=11, q1+q2=4+5, p=1000003

- Raw shape: 100 by 119; direct shape: 100 by 96.
- Raw logarithmic rows: 0..95.
- Raw logarithmic columns: 0..46, 48..95, 106.
- Raw logarithmic determinant modulo p: 674935.
- Direct cross-ratio rows: 0..95.
- Direct cross-ratio columns: 0..95.
- Direct cross-ratio determinant modulo p: 257836.
- Raw matrix SHA-256: `0cf56a126b7b0a75aef9dafeb8d801d55d238386f3a72484fe22a90a6e3b0b86`.
- Direct matrix SHA-256: `9d090aeb89146658775a3985e509d9df75cbe1f34fb4edc7b0261a44e39711b9`.

### N=11, q1+q2=5+5, p=65521

- Raw shape: 100 by 131; direct shape: 100 by 108.
- Raw logarithmic rows: 0..99.
- Raw logarithmic columns: 0..58, 60..100.
- Raw logarithmic determinant modulo p: 20350.
- Direct cross-ratio rows: 0..99.
- Direct cross-ratio columns: 0..99.
- Direct cross-ratio determinant modulo p: 13963.
- Raw matrix SHA-256: `7f9d24437922c251e4dea99ffe2a0074b886d7acc11d57750cc0484a99863add`.
- Direct matrix SHA-256: `af54122fb340f81067836c0e7ea6e7e37e8eaf030158a1ae62b26fc54c0a9744`.

### N=11, q1+q2=5+5, p=1000003

- Raw shape: 100 by 131; direct shape: 100 by 108.
- Raw logarithmic rows: 0..99.
- Raw logarithmic columns: 0..58, 60..100.
- Raw logarithmic determinant modulo p: 181447.
- Direct cross-ratio rows: 0..99.
- Direct cross-ratio columns: 0..99.
- Direct cross-ratio determinant modulo p: 381824.
- Raw matrix SHA-256: `4d994f12f3271336662e173ef73e22cd946fff735ee73840c18008e3e03f5320`.
- Direct matrix SHA-256: `163a48a17f7968ddd39755fb7c161161b49de5f19500b47e785ea4e28d925a7e`.

### N=13, q1+q2=5+5, p=65521

- Raw shape: 144 by 153; direct shape: 144 by 126.
- Raw logarithmic rows: 0..125.
- Raw logarithmic columns: 0..68, 70..125, 138.
- Raw logarithmic determinant modulo p: 14174.
- Direct cross-ratio rows: 0..125.
- Direct cross-ratio columns: 0..125.
- Direct cross-ratio determinant modulo p: 40721.
- Raw matrix SHA-256: `465cd03e75eae8ab389883ded7514d7fa6b63191dafacdf8400e4d071aee8e17`.
- Direct matrix SHA-256: `e69ef9125f2aa0d4f2d17ed6bcb17ff63df2453acf81cc8fb6503c7649236b27`.

### N=13, q1+q2=5+5, p=1000003

- Raw shape: 144 by 153; direct shape: 144 by 126.
- Raw logarithmic rows: 0..125.
- Raw logarithmic columns: 0..68, 70..125, 138.
- Raw logarithmic determinant modulo p: 717755.
- Direct cross-ratio rows: 0..125.
- Direct cross-ratio columns: 0..125.
- Direct cross-ratio determinant modulo p: 648984.
- Raw matrix SHA-256: `9a7c5cd92206b0581d099cff40e78c2d1ad471dc4dbfab7aeec754879fd15cdd`.
- Direct matrix SHA-256: `de66a785d50650eecae26270e2d497909866dccfe92df8981cc20ae89167c1f1`.

### N=13, q1+q2=6+6, p=65521

- Raw shape: 144 by 181; direct shape: 144 by 154.
- Raw logarithmic rows: 0..143.
- Raw logarithmic columns: 0..82, 84..144.
- Raw logarithmic determinant modulo p: 23645.
- Direct cross-ratio rows: 0..143.
- Direct cross-ratio columns: 0..143.
- Direct cross-ratio determinant modulo p: 16443.
- Raw matrix SHA-256: `7f052fd802f1ad88c487997709f87e50cd52333c6103e7cff61e7f403b58f1da`.
- Direct matrix SHA-256: `75711ae7067887e6bbaf1c1f458944fbedceb51c785b35c473a34276403b78c4`.

### N=13, q1+q2=6+6, p=1000003

- Raw shape: 144 by 181; direct shape: 144 by 154.
- Raw logarithmic rows: 0..143.
- Raw logarithmic columns: 0..82, 84..144.
- Raw logarithmic determinant modulo p: 341430.
- Direct cross-ratio rows: 0..143.
- Direct cross-ratio columns: 0..143.
- Direct cross-ratio determinant modulo p: 614854.
- Raw matrix SHA-256: `08d6fc7fe6907dd34aab6326fe2a1c220714ca33e17104a22788801a9c327c38`.
- Direct matrix SHA-256: `02685e362d268b28e2577ea73c8e20496395a3b352d3ce19b890dc06b4470fe8`.

### N=17, q1+q2=8+8, p=65521

- Raw shape: 256 by 305; direct shape: 256 by 270.
- Raw logarithmic rows: 0..255.
- Raw logarithmic columns: 0..142, 144..256.
- Raw logarithmic determinant modulo p: 24041.
- Direct cross-ratio rows: 0..255.
- Direct cross-ratio columns: 0..255.
- Direct cross-ratio determinant modulo p: 35586.
- Raw matrix SHA-256: `878cb08edc18304704f11e8e5f82559a52c2be9c068e4c9e3c06d8ac5b12ffa6`.
- Direct matrix SHA-256: `d78e8167b3c380a448d359fe71a73d25617a404bca4a546b4e301f451c91e669`.

### N=17, q1+q2=8+8, p=1000003

- Raw shape: 256 by 305; direct shape: 256 by 270.
- Raw logarithmic rows: 0..255.
- Raw logarithmic columns: 0..142, 144..256.
- Raw logarithmic determinant modulo p: 166828.
- Direct cross-ratio rows: 0..255.
- Direct cross-ratio columns: 0..255.
- Direct cross-ratio determinant modulo p: 692870.
- Raw matrix SHA-256: `27a68ed0360668aa398a785a0ee325941c5677daf1a6e258a5ae091bc52af0d3`.
- Direct matrix SHA-256: `dfa2e00236b4526bf931d6e3e4d141426276c02ad4dddc165b28f95fa8d93039`.

### N=19, q1+q2=9+9, p=65521

- Raw shape: 324 by 379; direct shape: 324 by 340.
- Raw logarithmic rows: 0..323.
- Raw logarithmic columns: 0..178, 180..324.
- Raw logarithmic determinant modulo p: 34209.
- Direct cross-ratio rows: 0..323.
- Direct cross-ratio columns: 0..323.
- Direct cross-ratio determinant modulo p: 14468.
- Raw matrix SHA-256: `5c49bfb03c3cb634303bd98664ff74420b5d4479e9ee1aaeae1dcd71c0682f4e`.
- Direct matrix SHA-256: `ffcf65e6d1b7824ec02d822c31230eeb77da9f08bfd17e1c7c8595b966178739`.

### N=19, q1+q2=9+9, p=1000003

- Raw shape: 324 by 379; direct shape: 324 by 340.
- Raw logarithmic rows: 0..323.
- Raw logarithmic columns: 0..178, 180..324.
- Raw logarithmic determinant modulo p: 729389.
- Direct cross-ratio rows: 0..323.
- Direct cross-ratio columns: 0..323.
- Direct cross-ratio determinant modulo p: 509483.
- Raw matrix SHA-256: `6313f58f8d05190fd0fe8efbca587fef2bba0cffdad09f85e129d690af811c7a`.
- Direct matrix SHA-256: `fe07b94a3cc005742391fd73c451eb8b62ea88ae1ae3f9f884017324d46ef2d7`.

### N=23, q1+q2=11+11, p=65521

- Raw shape: 484 by 551; direct shape: 484 by 504.
- Raw logarithmic rows: 0..483.
- Raw logarithmic columns: 0..262, 264..484.
- Raw logarithmic determinant modulo p: 26031.
- Direct cross-ratio rows: 0..483.
- Direct cross-ratio columns: 0..483.
- Direct cross-ratio determinant modulo p: 29056.
- Raw matrix SHA-256: `dff9085f2626fd72dd944a999210717fd3faa38009e5a59a5b1c3b7a789190fb`.
- Direct matrix SHA-256: `5981754d07ebafb90ab17ec059905d88ba9fea5d57a506d0eda03ff90ee9f66e`.

### N=23, q1+q2=11+11, p=1000003

- Raw shape: 484 by 551; direct shape: 484 by 504.
- Raw logarithmic rows: 0..483.
- Raw logarithmic columns: 0..262, 264..484.
- Raw logarithmic determinant modulo p: 667292.
- Direct cross-ratio rows: 0..483.
- Direct cross-ratio columns: 0..483.
- Direct cross-ratio determinant modulo p: 145785.
- Raw matrix SHA-256: `fd9c6dff130a229febc412919f3d4e320141259f040d657166d0187a09fab2ef`.
- Direct matrix SHA-256: `8f04924e3ca76b2bc2fc2eab9d220e029f0116cd57669032f629e06665ca4632`.

### N=31, q1+q2=15+15, p=65521

- Raw shape: 900 by 991; direct shape: 900 by 928.
- Raw logarithmic rows: 0..899.
- Raw logarithmic columns: 0..478, 480..900.
- Raw logarithmic determinant modulo p: 50838.
- Direct cross-ratio rows: 0..899.
- Direct cross-ratio columns: 0..899.
- Direct cross-ratio determinant modulo p: 36600.
- Raw matrix SHA-256: `7fbf9675abe49ac8b795ab4f52a927862aec02436f773e95bcb39645847446a3`.
- Direct matrix SHA-256: `2f28939af62b3d1aa0ce2b5e834f6cf908479185cc2cca72cb7f53bf64ffe19a`.

### N=31, q1+q2=15+15, p=1000003

- Raw shape: 900 by 991; direct shape: 900 by 928.
- Raw logarithmic rows: 0..899.
- Raw logarithmic columns: 0..478, 480..900.
- Raw logarithmic determinant modulo p: 3138.
- Direct cross-ratio rows: 0..899.
- Direct cross-ratio columns: 0..899.
- Direct cross-ratio determinant modulo p: 896811.
- Raw matrix SHA-256: `96a3afc35a19204565008815a7512cc4d20bcfbb218757aab559a6dfe31d5155`.
- Direct matrix SHA-256: `2df535f0b0b301cf0301c0a927963a32a524424f72308c36094106ef7a4e5238`.

## Independent whole-matrix check

A second implementation uses pure-Python multivariate dual arithmetic, independent of the inverse-resolvent differentiation. All ten complete direct matrices for (N,q1,q2)=(5,2,2),(7,3,3),(8,3,4),(11,3,3),(13,5,5), each at both primes, match the corresponding matrix identities above. The second review also reconciles all 26 receipts, but does not independently execute all 26 cases.

For the mathematical inference from a guarded nonzero modular minor to the exact characteristic-zero image dimension, see [the complete proof review](PROOF_REVIEW.md).

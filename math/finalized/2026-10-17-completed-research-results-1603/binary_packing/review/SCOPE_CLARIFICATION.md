# Centering scope clarification

The accepted binary Newton packing result proves:

1. A legal binary-input family forces simultaneous row heights and actual packed argument lengths before centering.
2. Common per-node centering cannot substantially reduce the row-height or slot-width lower bounds.
3. The defined uniformly padded independent-node recursion has complexity n exp(Theta(log n / log log n)).

Statement 2 alone must not be described as an unconditional actual-packed-length lower bound after centering. An allowed family with its zero/singleton blocks early and a long trailing sequence of constant P−1 blocks loses that entire trailing sequence when centered by P−1. The independent control gives a native-rank-16 example with actual original length 97,678 bits: at node −1, its centered packing has 1,234 actual bits against 16,560 allocated bits.

A sufficient explicit strengthening is to place a zero block immediately before the terminal constant P−1 block in each operand. Under any common integer center c, the final two coefficients become −c and P−1−c, and cannot both vanish. With the strict packing separation Q>2L A B applied to the centered maxima, the remaining lower coefficients cannot cancel the last nonzero leading coefficient. Each packed argument then retains at least (L−2)w bits up to an absolute additive constant. Consequently the actual-length deficit is at most two slots per node, and the leading volume lower bound persists. For a size-minimizing center, w=Theta(r), so the total deficit is O(r^2).

The strengthening changes only the allowed placement of an already required zero block. The original uncentered actual-size witness, optimum-translation calculation, and fixed-padded-schedule theorem remain valid without it. Neither version proves an unrestricted or genuinely input-adaptive recursive lower bound. Prime-Mersenne compatibility remains open.

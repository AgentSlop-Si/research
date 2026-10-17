# Degree-seven scalar-extension lemma

Let B(K) be the minimum original signed-resolvent physical-bank count for N=13, q=16 over a characteristic-53 field K, with exactly one effective nonzero node in each cross orientation, independently free, and arbitrary legal beta.

The sixteen raw banks in DEGREE7_LITERAL_CERTIFICATE.json satisfy the original Fourier identity over K7=F53[u]/(u^7+40u^6+9u^5+25u^4+31u^3+4u^2+25u+25). The modulus is irreducible, each inverse guard is nonzero, every bank is effective, and both cross orientations have node 2. Therefore B(K7)<=16. The inherited field-uniform lower theorem gives the reverse inequality, so B(K7)=16.

If 7 divides d, there is an F53 embedding K7 into F_(53^d). Apply it entrywise to every parameter, weight and matrix identity. Field embeddings preserve products, sums, inverses and nonzero elements; the original grammar and bank count are unchanged. Hence B(F_(53^d))=16 for every multiple d of 7.

Together with the accepted 2/3/5 witnesses, this yields B(F_(53^d))=16 whenever gcd(d,210)>1. It is not a converse. The known base-field exception is B(F53)=18; all other degrees relatively prime to 210 remain outside the proved sufficient condition.

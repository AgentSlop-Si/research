"""Reviewer-authored exact mathematical controls. No uploaded imports or execution.

These controls evaluate elementary finite-field identities and witnesses. They
are not an alternative execution path for any source program or source test.
"""
import json
from math import gcd, prod
from pathlib import Path


def require(condition, description):
    if not condition:
        raise RuntimeError(description)


def fourier(vector, root, prime):
    return [sum(value * pow(root, j*k, prime) for j, value in enumerate(vector)) % prime
            for k in range(len(vector))]


def multiply_polynomials(left, right, prime):
    coefficients = [0] * (len(left)+len(right)-1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            coefficients[i+j] = (coefficients[i+j]+a*b) % prime
    return coefficients


def main():
    checks = 0
    resonance_checks = 0
    prime = 97
    graph_cases = []
    for n in [2,3,4,6,8,12,16]:
        root = pow(5, 96//n, prime)
        require(len({pow(root,k,prime) for k in range(n)}) == n, 'primitive root')
        for delay in range(1,n):
            filters = [[1], [1,-1], [1,-2]]
            if n >= 3:
                filters.extend([[1,-3,2], [1,0,-1]])
            for q in filters:
                zero_count = sum(sum(c*pow(root,k*delay*i,prime) for i,c in enumerate(q)) % prime == 0
                                 for k in range(n))
                require(zero_count <= min(n,(len(q)-1)*gcd(n,delay)), 'resonance bound')
                resonance_checks += 1
                for j in range(n):
                    # Evaluate the two matrix-entry formulas independently.
                    for k in range(n):
                        left = sum(c*pow(root, k*((j+i*delay)%n), prime) for i,c in enumerate(q)) % prime
                        right = (pow(root,j*k,prime) * sum(c*pow(root,k*delay*i,prime) for i,c in enumerate(q))) % prime
                        require(left == right, 'graph Fourier identity')
                        checks += 1
                graph_cases.append({'N':n,'delay':delay,'q':q,'resonances':zero_count})

    # Rational numerator/denominator identity, checked by direct geometric sums.
    rational_cases = 0
    for n in [3,4,6,8,12,16]:
        root = pow(5,96//n,prime)
        for count in range(min(4,n)+1):
            locations = list(range(count))
            weights = [j+2 for j in locations]
            denominator = [1]
            for j in locations:
                denominator = multiply_polynomials(denominator,[1,-pow(root,j,prime)],prime)
            numerator = [0] * max(1,count)
            for index,j in enumerate(locations):
                polynomial = [weights[index]]
                for other in locations:
                    if other != j:
                        polynomial = multiply_polynomials(polynomial,[1,-pow(root,other,prime)],prime)
                for degree,value in enumerate(polynomial):
                    numerator[degree] = (numerator[degree]+value) % prime
            series = [sum(v*pow(root,j*k,prime) for j,v in zip(locations,weights)) % prime for k in range(n)]
            for k in range(n):
                coefficient = sum(denominator[t]*series[k-t] for t in range(min(k,len(denominator)-1)+1)) % prime
                require(coefficient == (numerator[k] if k < len(numerator) else 0), 'rational coefficient identity')
            rational_cases += 1

    # Independent explicit matrix witness for the source's N=2 control-flow bug.
    p = 2013265921
    inverse = pow(44,-1,p)
    x = [-inverse % p,9*inverse % p]
    residual = [(9*x[0]+x[1])%p,(x[0]+5*x[1])%p]
    require(residual == [0,1], 'N=2 matrix witness')
    tiny = {'N':2,'p':p,'x':x,'P_matrix':[[9,1],[1,5]],'P_x':residual,
            'expected_DFT':fourier(x,p-1,p),
            'source_trace_not_executed':['majority_long_shift returns None because the residual contains zero',
                'bm_prefix_candidate sees discrepancy 0 then 1, returning [1,0,-1]',
                'graph_polynomial_apply rejects length 3 > N=2 before fallback'],
            'proposed_q_mod_p':[1,0,p-1]}

    # A shorter cyclic residual is incompatible with the engine's N-point roots.
    root = 22
    actual_formula = (root-2)*pow((1-2*root)%97,-1,97)%97
    require(actual_formula == 83 and actual_formula != root, 'length mismatch witness')
    wrong_length = {'N_engine':4,'N_residual':2,'p':97,'omega':root,'r':[0,1],
                    'delay':1,'q':[1,-2],'short_cycle_defect_mod_p':[95,1],
                    'frequency_1_formula':actual_formula,'zero_padded_DFT_frequency_1':root,
                    'source_execution':False}

    field_cases=[]
    for p,n,g in [(17,16,3),(31,15,3)]:
        w=pow(g,(p-1)//n,p)
        require(len({pow(w,j,p) for j in range(n)}) == n,'field witness root')
        diagonal_l=[(7+pow(w,j,p))%p for j in range(n)]
        diagonal_p=[(7+2*pow(w,-j,p))%p for j in range(n)]
        field_cases.append({'p':p,'N':n,'generator':g,'omega':w,
          'L_zero_diagonals':[j for j,v in enumerate(diagonal_l) if v==0],
          'P_zero_diagonals':[j for j,v in enumerate(diagonal_p) if v==0],
          'det_L':(prod(diagonal_l)-(-2)**n)%p,
          'det_P':(prod(diagonal_p)-(-1)**n)%p,
          'has_2N_roots':(p-1)%(2*n)==0,
          'required_Bluestein_convolution_length':1<<(2*n-2).bit_length(),
          'has_convolution_roots':(p-1)%(1<<(2*n-2).bit_length())==0})
    require(field_cases[0]['det_L']==field_cases[0]['det_P']==16,'zero diagonal determinant')
    require(field_cases[1]['det_L']==field_cases[1]['det_P']==3 and not field_cases[1]['has_convolution_roots'], 'fallback roots witness')
    return {'status':'PASS','source_execution':False,'source_imports':False,'source_compilation':False,
            'graph_matrix_entry_checks':checks,'graph_cases':graph_cases,
            'resonance_bound_checks':resonance_checks,'rational_identity_cases':rational_cases,
            'valid_small_length_exception_witness':tiny,'low_level_length_mismatch_witness':wrong_length,
            'field_boundary_witnesses':field_cases,
            'boundary':'Math identities and statically derived path witnesses only. No uploaded test or benchmark was run.'}


if __name__ == '__main__':
    result = main()
    target = Path(__file__).resolve().parent/'INDEPENDENT_MATH_RESULTS.json'
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'graph_cases'},indent=2))

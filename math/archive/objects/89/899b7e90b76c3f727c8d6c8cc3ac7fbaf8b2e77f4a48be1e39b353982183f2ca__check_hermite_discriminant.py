"""Fresh exploratory control, not an uploaded-source execution or a proof."""
import json
import sympy as s
x,t=s.symbols('x t')
rows=[]
for A in range(1,9):
    J=s.hermite_prob(A+1,x)+A*(1-t)*s.hermite_prob(A-1,x)
    D=s.Poly(s.discriminant(J,x),t).sqf_part()
    roots=s.nroots(D,maxsteps=500)
    rows.append({'A':A,'squarefree_discriminant':str(D.as_expr()),'roots':[{'approx':str(r.evalf(16)),'distance_from_1':abs(complex(r)-1)} for r in roots]})
print(json.dumps({'status':'finite numerical exploration only; not disk theorem proof','rows':rows},indent=2))

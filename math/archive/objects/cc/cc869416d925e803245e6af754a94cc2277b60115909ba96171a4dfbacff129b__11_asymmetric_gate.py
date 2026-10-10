"""A Fourier-specific obstruction for an asymmetric, variable-generator class.

Stage 1: S[i,j]=a[i]*right_envelope[j] below diagonal,
                 =c[i]*right_envelope[j] above diagonal, arbitrary diag.
Stage 2: S[i,j]=left_envelope[i]*b[j] below diagonal,
                 =left_envelope[i]*e[j] above diagonal, arbitrary diag.

Exact matrix-free cut-and-difference witnesses; any interior permutation.
"""
from dataclasses import dataclass
from scan_resolvent import apply_dft, permute

@dataclass
class ColumnEnvelope:
    lower_rows: list[int]
    upper_rows: list[int]
    right: list[int]
    diagonal: list[int]
    def apply(self,x,p):
        n=len(x)
        prefix=0;total=sum((self.right[j]*x[j])%p for j in range(n))%p
        y=[]
        for i in range(n):
            here=self.right[i]*x[i]%p
            suffix=(total-prefix-here)%p
            y.append((self.lower_rows[i]*prefix+self.upper_rows[i]*suffix+self.diagonal[i]*x[i])%p)
            prefix=(prefix+here)%p
        return y
    def adjacent_annihilator(self,j,p):
        # j is starting coordinate of pair: e_j/r_j - e_(j+1)/r_(j+1)
        n=len(self.right);x=[0]*n
        x[j]=pow(self.right[j],-1,p)
        x[j+1]=-pow(self.right[j+1],-1,p)%p
        return x

@dataclass
class RowEnvelope:
    left: list[int]
    lower_cols: list[int]
    upper_cols: list[int]
    diagonal: list[int]
    def apply(self,x,p):
        n=len(x)
        prefix=0;total=sum((self.lower_cols[j]*x[j])%p for j in range(n))%p
        # Upper uses an independent column envelope, so use separate suffix.
        suffix=sum((self.upper_cols[j]*x[j])%p for j in range(n))%p
        y=[]
        for i in range(n):
            suffix=(suffix-self.upper_cols[i]*x[i])%p
            y.append((self.left[i]*(prefix+suffix)+self.diagonal[i]*x[i])%p)
            prefix=(prefix+self.lower_cols[i]*x[i])%p
        return y
    def local_difference(self,x,p):
        # Divides by nonzero left envelope, cancels all columns except i,i+1
        return [(x[i+1]*pow(self.left[i+1],-1,p)-x[i]*pow(self.left[i],-1,p))%p
                for i in range(len(x)-1)]


def asymmetric_two_col_certificate(s1,s2,perm,n,p,w,output_gauge=None,input_gauge=None):
    x0=s1.adjacent_annihilator(0,p)
    x1=s1.adjacent_annihilator(1,p)
    if output_gauge is None: output_gauge=[1]*n
    if input_gauge is None: input_gauge=[1]*n
    lhs=[];rhs=[]
    for x in (x0,x1):
        # If target is diag(output)*F*diag(input), preserve all supports.
        u=[xj*gj%p for xj,gj in zip(x,input_gauge)]
        Fourier=apply_dft(u,w,p)
        Fourier=[yy*gg%p for yy,gg in zip(Fourier,output_gauge)]
        lhs.append(s2.local_difference(Fourier,p))
        rhs.append(s2.local_difference(s2.apply(permute(s1.apply(x,p),perm),p),p))
    return {
        'source_union':sum(bool(s1.apply(x0,p)[i] or s1.apply(x1,p)[i]) for i in range(n)),
        'rhs_union':sum(bool(rhs[0][i] or rhs[1][i]) for i in range(n-1)),
        'lhs_joint_zeros':sum(lhs[0][i]==0 and lhs[1][i]==0 for i in range(n-1)),
        'rhs_joint_zeros':sum(rhs[0][i]==0 and rhs[1][i]==0 for i in range(n-1)),
    }

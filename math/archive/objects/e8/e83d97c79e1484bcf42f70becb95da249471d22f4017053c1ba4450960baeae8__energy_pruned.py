"""Deterministic full-output, globally l2-scaled approximate Fourier transform.

The error/work theorem is for ideal arithmetic and exact norm comparisons.
This NumPy complex128 prototype is not a certified floating-point algorithm.
It does not compute an exact FFT except when it falls back or prunes only zeros.
"""
from collections import Counter
import math
import numpy as np


def _component_scale(x,stats,label):
    m=len(x)
    stats[label+'_component_reads']+=2*m
    stats[label+'_absolute_values']+=2*m
    stats[label+'_comparisons']+=max(0,2*m-1)
    return float(max(np.max(np.abs(x.real),initial=0.0),
                     np.max(np.abs(x.imag),initial=0.0)))


def _scaled_norm(x,stats):
    """Scaled sum of squares avoids squaring very large/small components."""
    m=len(x)
    stats['norm_calls']+=1
    stats['norm_value_volume']+=m
    scale=_component_scale(x,stats,'norm_scale')
    stats['norm_zero_comparisons']+=1
    if scale==0.0:
        return 0.0
    re=x.real/scale
    im=x.imag/scale
    stats['norm_scaling_component_reads']+=2*m
    stats['norm_temporary_component_writes']+=2*m
    stats['norm_dot_component_reads']+=4*m
    stats['norm_real_divisions']+=2*m
    stats['norm_real_multiplications']+=2*m+1
    stats['norm_real_additions']+=max(0,2*m-1)
    stats['norm_square_roots']+=1
    return scale*math.sqrt(float(np.dot(re,re)+np.dot(im,im)))


def _rescale(out,scale,stats):
    stats['rescaling_real_multiplications']+=2*len(out)
    stats['rescaling_complex_writes']+=len(out)
    with np.errstate(over='ignore',invalid='ignore',under='ignore'):
        out*=scale
    stats['finite_output_component_checks']+=2*len(out)
    if not np.all(np.isfinite(out)):
        raise OverflowError('The complex128 output is not finite after rescaling')
    return out


def energy_pruned_fft(values,epsilon,*,return_trace=False):
    """Approximate numpy.fft.fft(values,norm='ortho'), returning output/stats.

For ideal arithmetic, every output error is at most epsilon*||values||_2.
N must be a positive power of two, epsilon finite and >=0, all inputs finite.
The initial input scan, normalization, norm scans, coefficients and complete
output materialization are included in the stated work. Counts are logical
array/arithmetic counts, not Python instruction counts or exact native flops.
"""
    x=np.asarray(values,dtype=np.complex128)
    if x.ndim!=1:
        raise ValueError('input must be one-dimensional')
    n=len(x)
    if n<1 or n&(n-1):
        raise ValueError('length must be a positive power of two')
    if not math.isfinite(float(epsilon)) or epsilon<0:
        raise ValueError('epsilon must be finite and nonnegative')
    if not np.all(np.isfinite(x)):
        raise ValueError('input values must be finite')
    stats=Counter(n=n,finite_input_component_checks=2*n)
    scale=_component_scale(x,stats,'input_scale')
    out=np.zeros(n,dtype=np.complex128)
    stats['initial_output_zero_writes']=n
    if scale==0.0:
        stats['all_zero_input']=1
        stats['pruned_output_count']=n
        stats['returned_output_count']=n
        return out,dict(stats)
    # Scale components separately to avoid complex-division overflow paths.
    work=np.empty(n,dtype=np.complex128)
    work.real=x.real/scale
    work.imag=x.imag/scale
    stats['input_normalization_component_reads']=2*n
    stats['input_normalization_temporary_component_writes']=2*n
    stats['input_normalization_real_divisions']=2*n
    stats['input_normalization_complex_writes']=n
    root_norm=_scaled_norm(work,stats)
    if epsilon==0:
        # Only this branch uses an ordinary library FFT on the entire input.
        out=np.fft.fft(work,norm='ortho')
        stats['full_fft_fallback']=1
        stats['fallback_fft_length']=n
        stats['fallback_radix2_butterfly_count']=n*(n.bit_length()-1)//2
        stats['fallback_output_writes']=n
        stats['computed_output_count']=n
        stats['returned_output_count']=n
        return _rescale(out,scale,stats),dict(stats)
    if epsilon>=1:
        stats['pruned_output_count']=n
        stats['pruned_node_count']=1
        stats['returned_output_count']=n
        return out,dict(stats)
    threshold=float(epsilon)*root_norm
    stats['threshold_real_multiplications']=1
    roots=None
    inverse_sqrt_two=1/math.sqrt(2.0)
    stats['constant_square_roots']=1
    stats['constant_real_divisions']=1
    # The depth-d node owns frequencies offset (mod stride=2**d).
    stack=[(work,0,1,0,root_norm)]
    trace=[]
    active_per_depth=Counter()
    norm_per_depth=Counter()
    while stack:
        v,offset,stride,depth,known_norm=stack.pop()
        m=len(v)
        stats['visited_nodes']+=1
        stats['logical_node_index_operations']+=5
        if known_norm is None:
            node_norm=_scaled_norm(v,stats)
        else:
            node_norm=known_norm
        norm_per_depth[depth]+=m
        stats['prune_norm_comparisons']+=1
        if node_norm<=threshold:
            stats['pruned_node_count']+=1
            stats['pruned_output_count']+=m
            if return_trace:
                trace.append(dict(depth=depth,length=m,offset=offset,stride=stride,
                                  norm=node_norm,threshold=threshold,pruned=True))
            continue
        active_per_depth[depth]+=1
        if m==1:
            out[offset]=v[0]
            stats['computed_output_count']+=1
            stats['computed_output_writes']+=1
            continue
        if roots is None:
            roots=np.exp((-2j*np.pi/n)*np.arange(n//2,dtype=np.float64))
            stats['root_exponential_evaluations']=n//2
            stats['root_phase_scalar_products']=n//2
            stats['root_phase_scalar_setup']=2
            stats['root_coefficient_writes']=n//2
            stats['root_index_initializations']=n//2
        half=m//2
        even=(v[:half]+v[half:])*inverse_sqrt_two
        odd=(v[:half]-v[half:])*inverse_sqrt_two
        odd*=roots[::n//m]
        stats['split_nodes']+=1
        stats['split_complex_values_read']+=2*m+half
        stats['split_complex_values_written']+=m+half
        stats['split_complex_temporary_writes']+=m
        stats['split_value_volume']+=m
        stats['butterflies']+=half
        stats['complex_additions_or_subtractions']+=m
        stats['complex_multiplications']+=half
        stats['real_scalings_of_complex_values']+=m
        stats['twiddle_coefficient_reads']+=half
        stats['logical_split_index_operations']+=half+8
        stack.append((odd,offset+stride,stride*2,depth+1,None))
        stack.append((even,offset,stride*2,depth+1,None))
        stats['max_pending_nodes']=max(stats['max_pending_nodes'],len(stack))
        if return_trace:
            trace.append(dict(depth=depth,length=m,offset=offset,stride=stride,
                              norm=node_norm,threshold=threshold,pruned=False))
    stats['returned_output_count']=n
    stats['active_nodes_by_depth']=dict(sorted(active_per_depth.items()))
    stats['norm_value_volume_by_depth']=dict(sorted(norm_per_depth.items()))
    stats['scaled_input_norm']=root_norm
    stats['input_component_scale']=scale
    stats['scaled_prune_threshold']=threshold
    if return_trace:
        stats['trace']=trace
    return _rescale(out,scale,stats),dict(stats)


def ideal_split_volume_bound(n,epsilon):
    """Conservative real-valued bound on sum of lengths of split nodes."""
    if n<1 or n&(n-1):
        raise ValueError('length must be a positive power of two')
    if not math.isfinite(float(epsilon)) or epsilon<0:
        raise ValueError('epsilon must be finite and nonnegative')
    if epsilon<=0:
        return n*(n.bit_length()-1)
    if epsilon>=1:
        return 0.0
    if epsilon<=1/math.sqrt(n):
        return n*(n.bit_length()-1)
    return sum(min(2**d,epsilon**-2)*n/(2**d)
               for d in range(n.bit_length()-1))

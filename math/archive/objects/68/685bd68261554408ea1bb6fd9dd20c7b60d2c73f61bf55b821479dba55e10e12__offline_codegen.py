"""Build an AOT C++ kernel from *symbolic degrees only*, never input values.

RUN ONLY DURING BUILD/DEPLOYMENT. Runtime code never invokes a compiler.
The distributed sample shape comes from F=A*A*B+A*B+B*B+C*D.
"""
from pathlib import Path
import json
import subprocess
import time

ROOT=Path(__file__).resolve().parent
MANIFEST=ROOT/'shape_manifest.json'

DEFAULT_SHAPE={
  'name':'a2b_ab_b2_cd',
  'dense': [[0,1],[1,0],[1,1],[2,0]],
  'sparse': [[0,2],[2,1]],
}

def safe_degree_pairs(pairs):
    if type(pairs)!=list or len(pairs)>16:
        raise ValueError('invalid shape')
    out=[]
    for pair in pairs:
        if type(pair)!=list or len(pair)!=2 or any(type(x)!=int or x<0 or x>8 for x in pair):
            raise ValueError('invalid degree pair')
        out.append(tuple(pair))
    if len(out)!=len(set(out)):
        raise ValueError('duplicate degree pair')
    return out


def coefficient_expr(a,b):
    parts=['alpha']*a+['beta']*b
    return '*'.join(parts) if parts else '1.0'


def generate_source(shape):
    ds=safe_degree_pairs(shape['dense'])
    ss=safe_degree_pairs(shape['sparse'])
    result=['// Auto-generated OFFLINE from validated degree lists; no input values are embedded.',
            '#include <cstdint>', '#include <cmath>',
            'extern "C" int fft10_shape_eval(',
            '  int64_t n, const double* base, const double* dense,',
            '  const int64_t* sparse_positions, const double* sparse_weights,',
            '  int64_t pa, double alpha, int64_t pb, double beta,',
            '  const int64_t* indices, int64_t q_count, double* out) {',
            '  if(n<2 || q_count<0 || !base || !out || pa<0 || pa>=n || pb<0 || pb>=n)',
            '    return 1;',
            '  if(!std::isfinite(alpha) || !std::isfinite(beta)) return 2;',
            '  if(!indices && q_count!=n) return 3;']
    if ds:result+=['  if(!dense) return 4;']
    if ss:result+=['  if(!sparse_positions || !sparse_weights) return 5;']
    for j,(a,b) in enumerate(ds):
        result += [f'  const int64_t shift{j}=static_cast<int64_t>((static_cast<__int128>({a})*pa+static_cast<__int128>({b})*pb)%n);',
                   f'  const double scale{j}={coefficient_expr(a,b)};']
    result += ['  for(int64_t r=0;r<q_count;++r) {',
               '    const int64_t q=indices?indices[r]:r;',
               '    if(q<0||q>=n)return 6;']
    for j,_ in enumerate(ds):
        result += [f'    int64_t j{j}=q-shift{j}; if(j{j}<0)j{j}+=n;']
    expression='base[q]'+''.join(f'+scale{j}*dense[{j}*n+j{j}]' for j in range(len(ds)))
    result += [f'    out[r]={expression};','  }']
    for j,(a,b) in enumerate(ss):
        result += [f'  const int64_t sp{j}=static_cast<int64_t>((static_cast<__int128>(sparse_positions[{j}])+static_cast<__int128>({a})*pa+static_cast<__int128>({b})*pb)%n);',
                   f'  const double sv{j}=sparse_weights[{j}]*({coefficient_expr(a,b)});']
        result += ([f'  if(!indices)out[sp{j}]+=sv{j};',
                    f'  else for(int64_t r=0;r<q_count;++r)if(indices[r]==sp{j})out[r]+=sv{j};'])
    result += ['  return 0;','}']
    return '\n'.join(result)+'\n'


def build(shape=DEFAULT_SHAPE):
    ds=safe_degree_pairs(shape['dense']);ss=safe_degree_pairs(shape['sparse'])
    if type(shape.get('name'))!=str or not shape['name'].replace('_','').isalnum():
        raise ValueError('invalid name')
    src=ROOT/'native_shape_a2b.cpp'
    lib=ROOT/'libfft_phase10_shape.so'
    src.write_text(generate_source(shape))
    t=time.perf_counter()
    command=['g++','-O3','-std=c++17','-fPIC','-shared','-fno-fast-math','-o',str(lib),str(src)]
    subprocess.run(command,check=True)
    elapsed=time.perf_counter()-t
    manifest={'shape':shape,'native_library':lib.name,'native_source':src.name,
              'build_command':' '.join(command),'offline_compile_seconds':elapsed,
              'runtime_compilation':False}
    MANIFEST.write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Specialized AOT library: {lib.name}, {lib.stat().st_size} bytes, built in {elapsed:.3f}s')
    return lib

if __name__=='__main__':build()

import numpy as np
import mpmath
import matplotlib.pyplot as plt

mpmath.mp.dps = 20

a_values = [mpmath.mpf(0.5), mpmath.mpf(0.7), mpmath.mpf(0.875), mpmath.mpf(0.9)]
b_values = [mpmath.mpf(b) for b in np.linspace(0, 1, 50)] 

def f(z, k, p):
    z = mpmath.mpc(z)
    return mpmath.sqrt(z - p) / (mpmath.sqrt(z + k) * mpmath.sqrt(1 - z * z))

def fm(z, k, p):
    z = mpmath.mpc(z)
    return mpmath.sqrt(p - z) / (mpmath.sqrt(z + k) * mpmath.sqrt(1 - z * z))

def g(k, p):
    ep = mpmath.mpf(1e-10)
    if k.real <= 1 or p.real >= 1 or p.real <= -1:
        return mpmath.nan

    sln = mpmath.quad(lambda z: f(z, k, p), [-k + ep, mpmath.mpf(-1.) - ep]).real
    return sln

def gm(k, p):
    ep = mpmath.mpf(1e-10)
    if k.real <= 1 or p.real >= 1 or p.real <= -1:
        return mpmath.nan
    
    sln = mpmath.quad(lambda z: fm(z, k, p), [mpmath.mpf(-1.) + ep, p]).real
    return sln

def Fn(k, p):
    one_over_pi = mpmath.mpf(1.0) / mpmath.pi
    c = mpmath.matrix([a, b])
    d = mpmath.matrix([mpmath.mpf(-1.) * one_over_pi * g(k, p), mpmath.mpf(-1.) * one_over_pi * gm(k, p)])
    return c + d


def T(z,k,p):
    z = mpmath.mpc(z)
    return (mpmath.mpf(1.0)/mpmath.sqrt(mpmath.mpf(1.0) - z*z))*((mpmath.sqrt(z -p)/mpmath.sqrt(z+k)) - mpmath.mpf(1.0))

def Tn(k,p):
    ep = mpmath.mpf(1e-10)
    one_over_pi = mpmath.mpf(1.0) / mpmath.pi
    sln = mpmath.quad(lambda z: T(z, k, p), [mpmath.mpf(1.0) + ep, mpmath.mpf(1000000.)])
    return one_over_pi*sln


def solution(a, b, m=20):
    k = mpmath.mpf(1.1)
    p = mpmath.mpf(-0.5)

    for i in range (m, 0, -1):
        n = mpmath.findroot(Fn, (k, p), solver='muller', tol=i)
        k = n[0]
        p = n[1]
        #print(n)

    n = mpmath.findroot(Fn, (k, p), solver='bisect', tol=1)
    #print(n)
    return n

results = []
for a in a_values:
    row = []
    for b in b_values:
        n = solution(a, b)
        k, p = n[0], n[1]
        m = Tn(k, p)
        row.append(float(m.imag))
    results.append(row) 


output = [[0 for _ in range(len(a_values)+1)] for _ in range(len(b_values))]
for i in range(len(b_values)):
    output[i][0] = float(b_values[i])

for i in range(len(b_values)):
    for j in range(1,len(a_values)+1):
        output[i][j] = results[j-1][i]


for row in output:
    print(" ".join(map(str, row)))

for j in range(1, len(a_values) + 1):
    a_label = f'a/L = {a_values[j - 1]}'
    y_values = [row[j] for row in output]
    plt.plot(b_values, y_values, label=a_label)

plt.xlabel('b/L')
plt.ylabel('Ls/L')
plt.title('Solution of Crowdys equations')
plt.legend()
plt.grid(True)
plt.show()

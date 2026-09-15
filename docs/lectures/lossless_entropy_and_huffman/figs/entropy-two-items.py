import matplotlib.pyplot as plt
import numpy as np
import math


def h1(t):
    if t < 1/3:
        return 1/4
    elif t < 2/3:
        return 3*(2/3 - t)*(1/4) + 3*(t - 1/3)*(3/4)
    else:
        return 3/4


hilbert_lists = dict()

# Return a list of pairs
def recursive_hilbert():
    global hilbert_lists
    NN = 3
    for k in range(1,NN+1):
        if k == 1:
            hilbert_lists[1] = [(0,0), (0,1), (1,1), (1,0)]
        else:
            L1 = list([(y,x) for (x,y) in hilbert_lists[k-1]])
            L2 = list([(x,y+2**(k-1)) for (x,y) in hilbert_lists[k-1]])
            L3 = list([(x+2**(k-1),y+2**(k-1)) for (x,y) in hilbert_lists[k-1]])
            L4 = list([(2**(k-1) - 1 - y + 2**(k-1), 2**(k-1) - 1 - x) for (x,y) in hilbert_lists[k-1]])
            hilbert_lists[k] = (L1+L2+L3+L4)



# Discrete Hilbert coordinates
def dh(j,k):
    global hilbert_lists
    if j < 0:
        j == 0
    if j >= 2**(2*k):
        j = 2**(2*k) - 1
    if k < 1:
        return (0,0)
    else:
        #results = [(0,0), (0,1), (1,1), (1,0)]
        #results = [(0,0), (1,0), (1,1), (0,1), (0,2), (0,3), (1,3), (1,2), (2,2), (2,3),(3,3),(3,2), (3,1), (2,1),(2,0), (3,0)]
        results = hilbert_lists[k]
        return results[j]


# L4 beigas
#[(3,1), (2,1),(2,0), (3,0)]
# atnem 2**(k-1) no x koordinaates
#[(1,1), (0,1), (0,0), (1,0)]
# spogu'lojam ar t -> (2**(k-1)-1)-t
#[(0,0), (1,0), (1,1), (0,1)]
# apmaina x <-> y
#[(0,0), (0,1), (1,1), (1,0)]



def hh(k,t):
    delta = 1/(2**(2*k) - 1)
    j_t = math.floor(t/delta)
    # discrete square coordinates
    (x0,y0) = dh(j_t, k)
    (x1,y1) = dh(j_t + 1, k)
    xx0 = (2*x0 + 1)/2**(k+1)
    xx1 = (2*x1 + 1)/2**(k+1)

    x = (2**(2*k) - 1)*((j_t*delta + delta - t)*xx0 + (t - j_t*delta)*xx1)
    #print('xx0 = {}, xx1 = {}, x = {}'.format(xx0, xx1, x))
    return x

def square(t):
    return t*t


def main():
    # Build Hilbert lists
    recursive_hilbert()
    step = 0.001 # how often we sample the points to draw the graph.
    t = np.arange(0,1+step,step)  # generate numpy array [0, step, 2*step, ...]
    #x = h1(t)
    x1 = np.array([hh(1,t_i) for t_i in t])
    x2 = np.array([hh(2,t_i) for t_i in t])
    x3 = np.array([hh(3,t_i) for t_i in t])
    plt.plot(t,x1,t,x2,t,x3)

    axes = plt.gca()
    axes.set_xlim([-0.05, 1.05])
    axes.set_ylim([0, 1])

    plt.grid(color='lightgray', linestyle='dashed', linewidth=0.5)
    plt.xlabel('Curve parameter t in [0,1]')  # string must be enclosed with quotes '  '
    plt.ylabel('The value of hk_x(t)')
    plt.title('Plotting hk_x(t): Horizontal Projections of H1, H2, H3')
    plt.legend(['h1_x(t)', 'h2_x(t)', 'h3_x(t)'])      # legend entries as seperate strings in a list

    #print('hilbertlist = {}'.format(recursive_hilbert[2]))

    plt.show()

if __name__ == '__main__':
    main()

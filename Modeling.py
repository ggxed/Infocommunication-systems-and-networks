from os import times

import numpy as np
from queue import Queue
import math
import matplotlib.pyplot as plt
import random

def lineplot2(x_data, y1_data, y2_data, x_label="", y_label="", title="",y1_legend="",y2_legend=""):
    _, ax = plt.subplots()


    ax.plot(x_data, y1_data,'b',lw = 2)
    ax.plot(x_data, y2_data,'m',lw = 2)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend([y1_legend, y2_legend])


def get_M_N(timeline):
    M_N = 0
    cur_mes = 0
    q = Queue()
    number_windows = int(np.ceil(timeline[len(timeline) - 1]))
    for i in range(0, number_windows):
        if not q.empty():
            q.get()
        while  timeline[cur_mes] < i:
            q.put(cur_mes )
            cur_mes  += 1
        M_N += q.qsize()
    return  M_N/number_windows


def synchronous_modeling (l):
    size = 100000
    times_send = [0]
    delay = 0
    tau = [(-1/l)*math.log(random.random()) for i in range(size)]
    timeline = np.cumsum(tau)
    j = 1
    t = math.ceil(timeline[0]) + 1
    delay += (t - timeline[0])
    times_send.append(t)
    for i in range(1, len(timeline)):
        t = math.ceil(timeline[i])
        if t >= times_send[j]:
            t += 1
            delay += (t - timeline[i])
            times_send.append(t)
        else:
            while t < times_send[j] + 1:
                t += 1
            delay += (t - timeline[i])
            times_send.append(t)
        j += 1
    return delay/size, get_M_N(timeline)


def asynchronous_modeling (l):
    size = 100000
    times_send = [0]
    delay = 0
    tau = [(-1/l)*math.log(random.random()) for i in range(size)]
    timeline = np.cumsum(tau)
    j = 1
    t = math.ceil(timeline[0]) + 1
    delay += (t - timeline[0])
    times_send.append(t)
    for i in range(1, len(timeline)):
        t = timeline[i]
        if t >= times_send[j]:
            t += 1
            delay += (t - timeline[i])
            times_send.append(t)
        else:
            t = times_send[j] + 1
            delay += (t - timeline[i])
            times_send.append(t)
        j += 1
    return delay/size, get_M_N(timeline)



def synchronous_theor_d(L):
    return ((2-L)/(2*(1-L))) + 0.5


def asynchronous_theor_d(L):
    return (2-L)/(2*(1-L))

def theor_n(L):
    return (L*(2-L))/(2*(1-L))





def main():
    lambdes = np.arange(0.1, 1.0, 0.1)
    M_D_s = []
    M_D_as = []
    M_N_s = []
    M_N_as = []
    M_D_s_theor = []
    M_D_as_theor = []
    M_N_s_theor = []
    M_N_as_theor = []
    print("Synchronous modeling:")
    for L in lambdes:
        print ("lambda = ", L, " Consequently: ")
        d, n = synchronous_modeling(L)
        M_D_s.append(d)
        M_N_s.append(n)
        d_theor = synchronous_theor_d(L)
        n_theor = theor_n(L)
        M_D_s_theor.append(d_theor)
        M_N_s_theor.append(n_theor)
        print("modeling M[D] = ", d)
        print("theoretical M[D] = ", d_theor)
        print("modeling M[N] = ", n)
        print("theoretical M[N] = ", n_theor)
        print("----------------------------------------")

    print("******************************************************")
    print("Asynchronous modeling:")

    for L in lambdes:
        print ("lambda = ", L, " Consequently: ")
        d, n = asynchronous_modeling(L)
        M_D_as.append(d)
        M_N_as.append(n)
        d_theor = asynchronous_theor_d(L)
        n_theor = theor_n(L)
        M_D_as_theor.append(d_theor)
        M_N_as_theor.append(n_theor)
        print("modeling M[D] = ", d)
        print("theoretical M[D] = ", d_theor)
        print("modeling M[N] = ", n)
        print("theoretical M[N] = ", n_theor)
        print("----------------------------------------")

    lineplot2(lambdes, M_D_s, M_D_s_theor, "input flow rate (lambda)", "average message wait time", "M(D) synchronous", "M(D) modelling", "M(D) theoretical")
    lineplot2(lambdes, M_D_as, M_D_as_theor, "input flow rate (lambda)", "average message wait time", "M(D) asynchronous", "M(D) modelling", "M(D) theoretical")
    lineplot2(lambdes, M_N_s, M_N_s_theor, "input flow rate (lambda)", "average number of messages", "M(N) synchronous", "M(N) modelling", "M(N) theoretical")
    lineplot2(lambdes, M_N_as, M_N_as_theor, "input flow rate (lambda)", "average number of messages", "M(N) asynchronous", "M(N) modelling", "M(N) theoretical")
    plt.show()
if __name__ == '__main__':
    main()



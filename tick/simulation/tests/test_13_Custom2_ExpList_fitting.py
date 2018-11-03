# License: BSD 3 clause

import numpy as np
from tick.simulation import HawkesKernel0, HawkesKernelExp, HawkesKernelPowerLaw, \
    HawkesKernelSumExp
from tick.simulation import SimuHawkes

timestamps_list = []
global_n_list = []

n_nodes = 3
dim = n_nodes
MaxN = 5
mu_i = [np.array([0.5, 0.7, 0.8, 0.6, 0.5]), np.array([0.5, 0.6, 0.8, 0.8, 0.6]), np.array([0.5, 0.6, 0.9, 0.2, 0.7])]

end_time = 1.0
end_times = []

beta = 3
kernels = np.array([
            [HawkesKernelExp(0.3, beta), HawkesKernelExp(0.1, beta), HawkesKernelExp(0.4, beta)],
            [HawkesKernelExp(0.2, beta), HawkesKernelExp(0.3, beta), HawkesKernelExp(0.5, beta)],
            [HawkesKernelExp(0.3, beta), HawkesKernelExp(0.4, beta), HawkesKernelExp(0.3, beta)]
])

for num_simu in range(100000):
    seed = num_simu * 10086 + 3007
    simu_model = SimuHawkes(kernels=kernels, end_time=end_time, custom='Type2', seed=seed, MaxN_of_f=MaxN, f_i=mu_i)

    for i in range(n_nodes):
        simu_model.set_baseline(i, 0.0)
        for j in range(n_nodes):
            simu_model.set_kernel(i, j, kernels[i, j])
    simu_model.track_intensity(0.1)
    simu_model.simulate()

    timestamps = simu_model.timestamps

    # print(len(timestamps[0]) + len(timestamps[1])+len(timestamps[2]))
    # exit(0)

    timestamps.append(np.array([]))
    timestamps_list.append(timestamps)

    global_n = np.array(simu_model._pp.get_global_n())
    global_n = np.insert(global_n, 0, 0).astype(int)
    global_n_list.append(global_n)

    end_times.append(end_time)

end_times = np.array(end_times)
##################################################################################################################
from tick.optim.model.hawkes_fixed_expkern_loglik_custom2_list import ModelHawkesFixedExpKernCustomType2LogLikList

model_list = ModelHawkesFixedExpKernCustomType2LogLikList(beta, MaxN, n_threads=4)
model_list.fit(timestamps_list, global_n_list, end_times=end_times)



##################################################################################################################
from tick.optim.solver import GD, AGD, SGD, SVRG, SDCA
from tick.optim.prox import ProxElasticNet, ProxL2Sq, ProxZero, ProxL1
prox = ProxL1(0.0, positive=True)
prox = ProxZero()

solver = AGD(step=1e0, linesearch=False, max_iter=1000, print_every=50)
solver.set_model(model_list).set_prox(prox)

x_real = np.array(
    [0.5, 0.7, 0.8, 0.6, 0.5,    0.5, 0.6, 0.8, 0.8, 0.6,    0.5, 0.6, 0.9, 0.2, 0.7,  0.3, 0.1, 0.4, 0.2, 0.3, 0.5, 0.3, 0.4, 0.3])
x0 = np.array(
    [0.2, 0.2, 0.2, 0.9, 0.9,    0.2, 0.2, 0.2, 0.9, 0.9,    0.2, 0.2, 0.2, 0.9, 0.9,  0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6])
solver.solve(x0)

print(model_list.loss(x_real))
print(model_list.loss(solver.solution))
print(solver.solution)
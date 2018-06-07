"""
Citrine Informatics Technical Challenge
Scientific Software Engineer
Arash Nemati Hayati - 06/01/2018
Efficient sampling of high-dimensional spaces with complex non-linear constraints
"""

import sys
import numpy as np
from numdifftools import Jacobian
from scipy.optimize import basinhopping as min
from scipy import stats
sys.path.insert(0, 'citrine-challenge/citrine/Source/')
from Source.constraints import Constraint
from Source.test_gen import Test_gen

# Sanity check for the global optimization to be bounded
class MyBounds(object):
    def __init__(self, xmin, xmax):
        self.xmax = np.array(xmax)
        self.xmin = np.array(xmin)
    def __call__(self, **kwargs):
        x = kwargs["x_new"]
        tmax = bool(np.all(x <= self.xmax))
        tmin = bool(np.all(x >= self.xmin))
        return tmax and tmin

# generate random purturbation for the global stochastic search
class RandomDisplacementBounds():
    #random displacement with bounds
    def __init__(self, xmin, xmax, step_size):
        self.xmin = xmin
        self.xmax = xmax
        self.stepsize = step_size
        self.xmin = xmin
        self.xmax = xmax
    def __call__(self, x):
        xnew = stats.cauchy.rvs(loc=0.0, scale=0.002, size=np.shape(x))
        np.clip(xnew, self.xmin, self.xmax, out = xnew)
        return xnew

# Optimization method
class Optimization():
    def __init__(self, input_file, output_file):
        self.input = Constraint(input_file)
        self.output = output_file
        self.test_gen = Test_gen()
    
    # calculate the derivative of n-dimensional volume objective
    def fun_der(self, x, n):
        return Jacobian(lambda x: self.test_gen.objective(x, n))(x).ravel()
    
    # sampling high-dimnesional space
    def sample(self, N):
        # Set the output file
        self.test_gen.init_output(self.output)
        # Get the dimensions of the problem
        dim = self.input.get_ndim()
        # Set the constraints
        cons = self.test_gen.gen_const(self.input)
        # Set SLSQP constraints
        cons_sl = cons
        # set COBYLA constraints
        cons_co = self.test_gen.gen_bound_const(dim - 1, cons)
        # get the initial points
        initial_point = self.input.get_example()
        # define the bounds of the problem
        xmin = self.test_gen.gen_bound(dim)[0]
        xmax = self.test_gen.gen_bound(dim)[1]
        bounds = [(low, high) for low, high in zip(xmin, xmax)]
        mybounds = MyBounds(xmin, xmax)
        # initialize counters, set step_size, threshold
        count = 0
        count_f = 0
        thres = 1e-5
        step_size = 0.5
        take_step = None
        # Start the search for candidates
        print("Searching for solutions...")
        while (count < N):
            minimizer_kwargs = dict(method="COBYLA", constraints = cons_co)
            if count_f > 0 and count_f % 5 == 0:
                minimizer_kwargs = dict(method="SLSQP", constraints = cons_sl, bounds = bounds, jac = lambda x: self.fun_der(x, dim-1))
            try:
                res = min(lambda x: self.test_gen.objective(x, dim-1), initial_point, minimizer_kwargs=minimizer_kwargs,\
                  niter_success = 3, niter = 5, take_step = take_step, accept_test = mybounds, stepsize = step_size)
            except IndexError:
                print("Maximum number of candidates reached")
                return
                
            if self.test_gen.check_bounds(res.x) and self.input.apply(res.x) and -res.fun > 0:
                initial_point = res.x + np.random.uniform(-thres, thres, np.shape(res.x))
                if count == 0:
                    cons.extend([{'type': 'ineq', 'fun': lambda x: -res.fun - thres - self.test_gen.f(x, dim-1)}])
                else:
                    cons[len(cons) - 1] = {'type': 'ineq', 'fun': lambda x: -res.fun - thres - self.test_gen.f(x, dim-1)}
                count = count + 1
                print(count, " ", end='', flush=True)
                for i in res.x:
                    print("%1.6f" % i, " ", end="", flush=True)
                print("")
                self.test_gen.write_output(self.output, res.x)
            else:
                count_f = count_f + 1
            """
        if count % 20 == 0:
            take_step = RandomDisplacementBounds(xmin[0], xmax[0], step_size)
            """
            if -res.fun < 0:
                print("Maximum number of candidates reached")
                return 
        self.test_gen.close_output(self.output)
        return

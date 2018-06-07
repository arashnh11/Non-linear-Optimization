"""
Citrine Informatics Technical Challenge
Scientific Software Engineer
Arash Nemati Hayati - 06/01/2018
Efficient sampling of high-dimensional spaces with complex non-linear constraints
"""
import os
import sys
sys.path.insert(0, 'citrine-challenge/citrine/Source/')

# Class to generate the testcase and output configurations required to run the optimization 
class Test_gen():
    def __init__(self):
        print("Testcase created...")

    # n-dimensional volume function
    def f(self, x, n):
        if (n < 0): return 1
        return x[n] * self.f(x, n-1)
     
    # objective function * -1 since the default algorithm find the minimum candidates. With this
    # transformation it will find the maximum conditions of the objective function   
    def objective(self, x, n):
        return -self.f(x, n)

    # generate unit hypercube boundary conditions
    def gen_bound(self, n):
        xmin = [1e-15 for j in range(n)]
        xmax = [1.0 for j in range(n)]
        return [xmin, xmax]
    
    # generates boundary constraints required by COBYLA optimization scheme
    def gen_bound_const(self, n, cons):
        for i in range(0, n+1):
            fun_min = 'x[' + str(i) + ']'
            fun_max = '1.0 - x[' + str(i) + ']'  
            cons.extend([{'type': 'ineq', 'fun': lambda x: eval(fun_min)}])
            cons.extend([{'type': 'ineq', 'fun': lambda x: eval(fun_max)}])
            return cons
    
    # Check if the solution satisfies the boundary conditions
    def check_bounds(self, x):
        for ijk in x:
            if ijk < 0.0 or ijk > 1.0:
                return False
        return True
    
    # Generate the constraints defined in the input file
    def gen_const(self, input_file):
        List = input_file.get_constr()
        cons = []
        for jk in List:
            eqq = lambda x, jk = jk: eval(jk)
            cons.extend([{'type': 'ineq', 'fun': eqq}])
        return cons
    
    # Generate the output file
    def init_output(self, filename):
        os.chmod(filename, 0o644)
        File = open(filename, "w+")
        File.write('')
        File.close()
    
    # Write to the output file
    def write_output(self, filename, x): 
        File = open(filename, "a+", encoding='utf-8')
        for i in x:
            File.write("%1.6f\t" % i)
        File.write("\n")
        File.close()
    
    # Close the output file
    def close_output(self, filename):
        File = open(filename, "a+")
        File.close()
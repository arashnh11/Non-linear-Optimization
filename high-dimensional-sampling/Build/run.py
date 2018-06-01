"""
Citrine Informatics Technical Challenge
Scientific Software Engineer
Arash Nemati Hayati - 06/01/2018
Efficient sampling of high-dimensional spaces with complex non-linear constraints
"""
from cgitb import reset
reset
import time
import sys
sys.path.insert(0, 'citrine-challenge/citrine/Source/')
from Source.optimization import Optimization

def main(input_file, output_file, N):
    # start the timer
    start = time.time()  
    # Run the sampling on the input_file and save the candidate solutions to the output file
    opt = Optimization(input_file, output_file)
    opt.sample(N)
    # stop the timer
    end = time.time()
    print("Elapsed time = ", "%1.3f" % (end - start), "seconds")
    return 
if __name__ == "__main__":
    #args given by user including input file, output file, and desired number of candidates
    main(str(sys.argv[1]), str(sys.argv[2]), int(sys.argv[3])) 
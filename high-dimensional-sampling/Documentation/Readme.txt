===================================================================================
Citrine Informatics Technical Challenge
Scientific Software Engineer

Efficient sampling of high dimensional spaces with complex, non-linear constraints
By Arash Nemati Hayati - 06/01/2018
===================================================================================

To use this software:
------------------------------------
1. Go to the Build directory.
2. Run the following command:
python <input_file> <output_file> <N_results>

Example:
python "../Testing/Examples/example.txt" "../Output/output.txt" 1000

A demo of the following testcase can be found inside the Testing directory:
1. Go to the Testing directory
2. Run the following command:
python demo.py

Sample input file:
2 # Number of dimensions
0.0 0.0 # initial values
# Simple 3-component mixture - constraint
1.0 - x[0] - x[1] >= 0.0

Installation
--------------------------
The following standard python libraries must be installed (if not already exist):
1. pathlib
2. numdifftools
3. scipy
4. numpy

To compile the code:
Linux
1. cd Build
2. python <input_file> <output_file> <N_results>

Windows
1. Go to the Build directory.
2. Open run.py with Eclipse, Visual Studio or other compatible environment 
3. Go to Run, the Run configurations from the menu-bar (for Eclipse)
4. Go to the Arguments tab and paste the following:
5. 		<input_file> <output_file> <N_results>
6. Click to Run the testcase

Bugs, issues, questions
-------------------------------
All inquiries should be submitted on github or by email to a.nematihayati@gmail.com
Comments are greatly appreciated.

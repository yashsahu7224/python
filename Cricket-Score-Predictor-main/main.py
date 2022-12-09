### Imports ###
# add imports - classes and defs
import sys
sys.path.append('/predictor')
from predictor import predictRuns


"""
sys.argv[1] is the input test file name given as command line arguments

"""
runs = predictRuns('inputFile.csv')
print("Predicted Runs: ", runs)
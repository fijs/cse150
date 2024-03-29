"""For each input in in/input*.txt, you can invoke this file as:

    python test_p6.py submitted_file.py <inputfile >out.txt

"""
import os
import sys
import time
####While testing individual files you may need to add these lines###
sys.path.append('../../src')
sys.path.append('../../solutions')
###########
from assignment3 import *

def run_code_from(python_file, input_text):
    # Load the class from the specified .py file
    sys.path.append(os.path.abspath(os.path.dirname(python_file)))
    module = __import__(os.path.splitext(os.path.basename(python_file))[0])
    solve_method = getattr(module, 'backtracking_search')
    game = XSudoku(input_text)
    start = time.time()
    game.solve_with(solve_method)
    end = time.time()
    print "Time taken: {}".format(end - start)
    return str(game)


if __name__ == '__main__':
    print(run_code_from(sys.argv[1], sys.stdin.read().strip()))

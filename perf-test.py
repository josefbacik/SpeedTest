import sys
import argparse
from Environment import Environment

# ADD YOUR TESTS TO THIS LIST
tests = [ "SequentialIO" ]

"""
Start main program area
"""

parser = argparse.ArgumentParser(description="Run a suite of tests")
parser.add_argument('profile', help="Profile to use for the tests")
parser.add_argument('--verbose', dest='verbose', default=False, action='store_true', help="Enable verbose mode")

args = parser.parse_args()

env = Environment()
env.verbose = args.verbose
env.load_config(args.profile)

env.setup_environment()

for test in tests:
    test_class = __import__(test)
    test_class = getattr(test_class, test)
    t = test_class()
    t.run(env)
    env.next_test()

# vim: set expandtab tabstop=4 shiftwidth=4

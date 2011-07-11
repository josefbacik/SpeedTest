from time import time
from Environment import Environment

class ExampleTest:
    def __init__(self):
        # This space intentially left blank
        pass
    def run(self, env):
        env.test_start("ExampleTest")

        # Load the last result set
        result = env.load_last_result("ExampleTest").split(' ')

        start = time()
        # do some stuff
        end = time()
        time_diff = end - start

        """
        For this example we'll just save how long the test took so the format
        will be

        Name: <version> <seconds>

        We include a version here in case we have to change the results format
        so we can just discard the old results, or maybe keep code to recognize
        the old format, either way.
        """
        if len(result) == 3 and result[1] == 1:
            diff = env.percent_difference_time(float(result[2]), time_diff)
            env.test_complete("ExampleTest", diff)
        else:
            env.test_complete("ExampleTest", 0)
        env.test_result("ExampleTest: 1 " + str(time_diff) + "\n")
        if env.verbose:
            print("\tTime: %.2f s" % (time_diff))

# vim: set expandtab tabstop=4 shiftwidth=4

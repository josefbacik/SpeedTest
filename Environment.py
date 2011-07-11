import ConfigParser
import sys
import subprocess
import os
import re

class Environment:
    def __init__(self):
        self.name = ""
        self.fs = ""
        self.device = ""
        self.dir = "./"
        self.umount = True
        self.mkfs = False
        self.logfile = open("log.txt", 'w')
        self.results = None
        self.mkfs_opts = ""
        self.verbose = False
        self.total_memory = 0

    def percent_difference_time(self, old, new):
        """Calculate the percent difference between 2 time values

        old -- the old value
        new -- the new value
        """
        diff = new - old
        avg = (old + new) / 2
        perc = (diff / avg) * 100
        return perc

    def system_memory(self):
        """Return the system memory in megabytes"""
        if self.total_memory != 0:
            return self.total_memory
        meminfo = open("/proc/meminfo", 'r')
        mem_str = meminfo.readline()
        match = re.search("MemTotal:\s+(\d+).*", mem_str)
        self.total_memory = int(match.group(1))
        self.total_memory = self.total_memory / 1024
        return self.total_memory

    def test_complete(self, testname, diff):
        """Called when a test completes

        testname -- the name of the test that completed
        diff -- the percentage of difference between 2 runs
        """
        if diff < 5:
            output = "%.2f%%: PASS" % diff
        else:
            output = "%.2f%%: FAIL" % diff
        self.log(output + "\n")
        print output

    def test_start(self, testname):
        """Called when starting a test

        testname -- the name of the test
        """
        output = testname + "..."
        self.log(output)
        sys.stdout.write(output)
        sys.stdout.flush()

    def load_last_result(self, testname):
        """Load the string of the last result for this test

        testname -- the test to look for in the results file.
        """
        if self.results == None:
            return ""
        self.results.seek(0, os.SEEK_SET)
        for line in self.results:
            if re.search(testname, line):
                return line
        return ""

    def run_command(self, command):
        """Run a command and redirect it's output to the logfile

        command -- the command and it's arguments in a list
        """
        self.log("Running " + str(command) + "\n")
        p = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=self.logfile)
        err = p.wait()
        return err

    def load_config(self, file):
        """Load an environment config"""
        config = ConfigParser.ConfigParser()
        config.read(file)
        self.name = config.sections()[0]
        self.results = open(self.name + ".results", 'a+')

        # All of this ugliness because python < 2.7 doesn't support
        # allow_no_value for ConfigParser
        if config.has_option(self.name, "fs"):
            self.fs = config.get(self.name, "fs")
        if config.has_option(self.name, "device"):
            self.device = config.get(self.name, "device")
        if config.has_option(self.name, "directory"):
            self.dir = config.get(self.name, "directory")
        if config.has_option(self.name, "umount"):
            self.umount = config.getboolean(self.name, "umount")
        if config.has_option(self.name, "mkfs"):
            self.mkfs = config.getboolean(self.name, "mkfs")
        if config.has_option(self.name, "mkfs_opts"):
            self.mkfs_opts = config.get(self.name, "mkfs_opts")

    def setup_environment(self):
        if self.mkfs:
            self.run_command(["umount", self.dir])

            mkfs = ["mkfs." + self.fs]
            if not self.mkfs_opts == "":
                mkfs.extend(self.mkfs_opts.split(' '))
            mkfs.append(self.device)
            err = self.run_command(mkfs)
            if err:
                print "Error mkfs'ing %s" % self.device
                sys.exit()

            err = self.run_command(["mount", self.device, self.dir])
            if err:
                print "Error mounting %s" % self.device
                sys.exit()

    def test_result(self, testname, version, units, time):
        if self.results == None:
            return
        output = testname + ": " + str(version) + " " + str(units) + " " + str(time)
        output = output + "\n"
        self.results.write(output)

    def next_test(self):
        if self.umount:
            err = self.run_command(["umount", self.dir])

            err = self.run_command(["mount", self.device, self.dir])
            if err:
                print "Error mounting %s" % self.device
                sys.exit()

    def log(self, str):
        if self.logfile == None:
            return
        self.logfile.write(str)
        self.logfile.flush()
# vim: set expandtab tabstop=4 shiftwidth=4

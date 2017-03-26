import os
import re
import subprocess



## \defgroup DetectingBlock Detecting system related classes
#
# The Detecting system is a class that analyzes system
# in search of some key variables for the parallel system initialization
# @{
#

## Detecting system
class DetectSystem:

    ## The constructor
    def __init__(self):
        return

    ## CPU count
    # Number of available virtual or physical CPUs on this system
    # If can't be determined, it will rise an exception
    # @retval Integer. Number CPUs
    def cpu_count(self):
        # Trying with cpuset
        # cpuset may restrict the number of *available* processors
        try:
            m = re.search(r'(?m)^Cpus_allowed:\s*(.*)$',
                          open('/proc/self/status').read())
            if m:
                res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
                if res > 0:
                    return res
        except IOError:
            pass

        # Python 2.6+
        try:
            import multiprocessing
            return multiprocessing.cpu_count()
        except (ImportError, NotImplementedError):
            pass

        # Trying with psutil -- http://code.google.com/p/psutil/
        try:
            import psutil
            return psutil.cpu_count()   # psutil.NUM_CPUS on old versions
        except (ImportError, AttributeError):
            pass

        # Trying with POSIX
        try:
            res = int(os.sysconf('SC_NPROCESSORS_ONLN'))

            if res > 0:
                return res
        except (AttributeError, ValueError):
            pass

        # Trying within Windows OS
        try:
            res = int(os.environ['NUMBER_OF_PROCESSORS'])

            if res > 0:
                return res
        except (KeyError, ValueError):
            pass

        # Trying with jython
        try:
            from java.lang import Runtime
            runtime = Runtime.getRuntime()
            res = runtime.availableProcessors()
            if res > 0:
                return res
        except ImportError:
            pass

        # Trying within BSD OS
        try:
            sysctl = subprocess.Popen(['sysctl', '-n', 'hw.ncpu'],
                                      stdout=subprocess.PIPE)
            scStdout = sysctl.communicate()[0]
            res = int(scStdout)

            if res > 0:
                return res
        except (OSError, ValueError):
            pass

        # Trying within Linux OS
        try:
            res = open('/proc/cpuinfo').read().count('processor\t:')

            if res > 0:
                return res
        except IOError:
            pass

        # Trying within Solaris
        try:
            pseudoDevices = os.listdir('/devices/pseudo/')
            res = 0
            for pd in pseudoDevices:
                if re.match(r'^cpuid@[0-9]+$', pd):
                    res += 1

            if res > 0:
                return res
        except OSError:
            pass

        # Trying on other UNIXes OS (heuristic)
        try:
            try:
                dmesg = open('/var/run/dmesg.boot').read()
            except IOError:
                dmesgProcess = subprocess.Popen(['dmesg'], stdout=subprocess.PIPE)
                dmesg = dmesgProcess.communicate()[0]

            res = 0
            while '\ncpu' + str(res) + ':' in dmesg:
                res += 1

            if res > 0:
                return res
        except OSError:
            pass

        raise Exception('Can not determine number of CPUs on this system')

## @}
#

    ## Thread number
    # Determine the number of virtual threads to be used, specially for IO blocking operation
    # such as Input/Output disk's operation.
    # @param io_number: number of I/O operation to execute in parallel
    # @retval Integer. Number of virtual threads
    def thread_number(self, io_number):
        cpus = self.cpu_count()
        if io_number < cpus:
            return cpus
        else:
            if io_number > 70:
                return 70
            else:
                return io_number

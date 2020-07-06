import os
import sys


class IOManager(object):
    repositoryRoot = None
    outputRoot = None
    sourceRoot = None
    files = None

    def __init__(self):
        # Set up paths
        self.repositoryRoot = os.path.realpath('%s/../../' % os.path.dirname(os.path.abspath(__file__)))
        self.outputRoot = os.path.join(self.repositoryRoot, 'output')
        self.sourceRoot = os.path.join(self.repositoryRoot, 'sources')

        if not os.path.exists(self.outputRoot):
            msg = "The output directory '%s' does not exist" % self.outputRoot
            raise RuntimeError(msg)

        if not os.path.exists(self.sourceRoot):
            msg = "The source directory '%s' does not exist" % self.sourceRoot
            raise RuntimeError(msg)

        self.files = os.listdir(self.sourceRoot)

        # Bail out if no files
        if not self.files:
            print "No files in '%s'." % self.sourceRoot
            print 'Nothing to do.'
            sys.exit(0)

    def writeConfigToFile(self, filePath, config):
        with open(filePath, 'w') as handle:
            for key, value in config.items():
                if key in ('MY_DATA', 'COUNTER', 'ROOT_DIR'):
                    continue

                handle.write("%s: %s\n" % (key, value))

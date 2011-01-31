# -*- python -*-
#
#
import os, sys
import lsst.SConsUtils as scons

env = scons.makeEnv("devenv_doc", r"$HeadURL: $", [ ])


# farm out the SConscripts
for d in ["latex", "doxygen"]:
    try:
        SConscript(os.path.join(d, "SConscript"))
    except Exception, e:
        print >> sys.stderr, "Error processing file %s:" % (os.path.join(d, "SConscript"))
        print e
        
# cleaning
rootClean  = r"*~ config.log"
#latexClean = r"*.aux *.log *.out *.pdf"

scons.CleanTree(rootClean)
#scons.CleanTree(latexClean, dir="latex")

env.Declare()
env.Help("""
Documentation Package
""")

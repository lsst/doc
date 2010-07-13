# -*- python -*-
#
#
import os
import lsst.SConsUtils as scons

env = scons.makeEnv("devenv_doc", r"$HeadURL: $", [])

targ = "AppsForSci"
pdfOutput = env.PDF(target=targ+'.pdf',source=targ+'.tex')
Depends(pdfOutput, Split('AppsForSci.tex'))

cleanFiles = ["*~", "config.log"]
texSuffixes = [".aux", ".log", ".out", ".pdf"]
cleanFiles += map(lambda x: targ+x, texSuffixes)
scons.CleanTree(cleanFiles)

env.Declare()
env.Help("""
Documentation Package
""")

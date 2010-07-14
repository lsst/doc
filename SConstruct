# -*- python -*-
#
#
import os
import lsst.SConsUtils as scons

env = scons.makeEnv("devenv_doc", r"$HeadURL: $", [])


# farm out the SCoscripts
for d in (
    ".",
    "latex",
    ):
    if d != ".":
        try:
            SConscript(os.path.join(d, "SConscript"))
        except Exception, e:
            print >> sys.stderr, "In processing file %s:" % (os.path.join(d, "SConscript"))
            print >> sys.stderr, traceback.format_exc()


# root-level cleaning
cleanFiles = ["*~", "config.log"]

# files to clean in the latex/ directory
latexSuffixes = [".aux", ".log", ".out", ".pdf"]
cleanFiles += map(lambda x: os.path.join("latex","*"+x), latexSuffixes)

# Clean
scons.CleanTree(cleanFiles)



##################
# make the html
#
Latex2HtmlAction = Action('latex2html -html_version "4.0" -local_icons -mkdir -dir $TARGET $SOURCE')
Latex2HtmlBuilder = Builder(action = Latex2HtmlAction)
env.Append(BUILDERS = {'Latex2Html' : Latex2HtmlBuilder})

env.Latex2Html(source = 'latex/lsstManual.tex', target = Dir('html')) 


env.Declare()
env.Help("""
Documentation Package
""")

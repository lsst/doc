#!/usr/bin/env python
#
import os, re, sys
import eups
import optparse


def loadConfigFile(configFile):
    lines = []

    fp = open(configFile, 'r')
    for line in fp.readlines():
        # it's tempting to skip blank lines here, but don't!
        #  ... a line continuation '\' followed by a
        #    blank line (removed) will append the wrong line
        if re.search("^\s*#", line):
            continue
        lines.append(line)
    fp.close()

    out = re.sub(r"\\\n+", " ", "".join(lines)) # join contined '/' lines
    out = out.strip("\n")                       # remove leading and trailing \n

    # now we can remove blank lines
    lines = []
    for line in out.split("\n"):
        if re.search("^\s*$", line):
            continue
        lines.append(line)
    
    return lines


class Doxyfile(object):
    """Represent a doxygen configuration file"""

    def __init__(self, productName, baseDir=None, docDir="doc", configFile="doxygen.conf"):
        """Read and parse productName's config file.

        We'll look for it in eups, and (failing that) in baseDir/productName/docDir"""

        self.productName = productName
        self.entries = {}  # the key/values from the doxygen.conf file for this package
        
        ################
        # get baseDir for this package
        pdir = eups.productDir(productName) # Look in the eups productDir
        if pdir and os.path.exists(os.path.join(pdir, docDir, configFile)):
            self.baseDir = pdir
        else:                           # look in baseDir
            if not baseDir:
                return

            productName = re.sub(r"_", "/", productName)
            self.baseDir = os.path.join(baseDir, productName)

            
        ################
        # load the doxygen.conf file
        self.docDir = os.path.join(self.baseDir, docDir)
        lines = loadConfigFile(os.path.join(self.docDir, configFile))

        for line in lines:

            mat = re.search(r"^\s*(\S+)\s*=\s*(.*)$", line)
            assert mat

            values = []
            name = mat.group(1)

            # Deal with specific paths for some settings
            for entry in mat.group(2).split():
                if name in ("EXAMPLE_PATH", "EXCLUDE", "INPUT"):
                    entry = os.path.normpath(os.path.join(self.docDir, entry))

                values.append(entry)

            # override some of the settings
            if name == "SEARCHENGINE":
                value = "YES"
            elif name == "DETAILS_AT_TOP":
                continue
            else:
                value = " ".join(values)

            # stash this setting
            self.entries[name] = value


    #############
    # print ourself as a list of entries
    def __str__(self):
        return ("# %s\n" % self.productName) + \
               "\n".join(["%-30s = %s" % item for item in self.entries.items()])

    ############
    # provide a shortcut to entries' k,v pairs
    def items(self):
        return self.entries.items()


    
###################################################################
#
# 
#
###################################################################
def main(products, baseDir=None, htmlDir="htmlDir", verbose=False):

    configs = {}
    productList = []

    for p in products:
        if verbose:
            print "Loading product: " + str(p)
        try:
            configs[p] = Doxyfile(p, baseDir)
            productList.append(p)
        except IOError:
            pass

    config = Doxyfile(" ".join(productList))
    for p in productList:
        for doxySetting, value in configs[p].items():
            # append if we already have this setting
            if config.entries.has_key(doxySetting):
                # if it's a quoted string, don't split it
                if re.search("\"[^\"]+\"", value.strip()):
                    values = [value, config.entries[doxySetting]]
                else:
                    values = value.split() + config.entries[doxySetting].split()
                config.entries[doxySetting] = " ".join(set(values))
            else:
                config.entries[doxySetting] = value

    # override the output directory
    config.entries["HTML_OUTPUT"] = htmlDir
    config.entries["GENERATE_TAGFILE"] = os.path.join(htmlDir, "doxygen.tag")
    
    return str(config)




#########################################
# If we're run from the command line
#########################################
if __name__ == '__main__':

    parser = optparse.OptionParser(usage=__doc__)
    opts, args = parser.parse_args()

    if len(args) > 0:
        parser.print_help()
        sys.exit(1)

        
    baseDir = os.path.join(os.environ["HOME"], "LSST")
    products = args
    if not products:
        products = "utils afw ip_isr ip_diffim ip_utils ip_pipeline meas_astrom meas_algorithms meas_pipeline meas_utils pex_exceptions pex_logging pex_policy pex_harness daf_base daf_data daf_persistence coadd_utils".split()
    
    print main(products, baseDir)

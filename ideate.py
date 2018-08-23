import traceback, os, sys, logging, argparse, glob
import pandas as pd

class Project:
    def __init__(self, prjdf, prtdf, pjrdf, pid):
        self.proj = prjdf
        self.tags = prtdf
        self.reqs = pjrdf
        self.pid  = pid
        self.name = self.proj.iloc[[pid]]["name"]
        self.stage = self.proj.iloc[[pid]]["stage"]
        self.active = self.proj.iloc[[pid]]["active"]

    def setName(self, name):
        self.name = name
        self.proj[[pid]]["name"] = name

    def setStage(self, stage):
        self.stage = stage
        self.proj[[pid]]["stage"]

    def setActive(self, active):
        self.active = active
        self.proj[[pid]]["active"] = active

    def create(cls, prjdf, prtdf, pjrdf, name):
        prjdf.append( {"name" : name, "stage" : "formation", "active" : False } )
        return cls(prjdf, prtdf, pjrdf, prjdf.index[-1])

def initialize(log, args):
    log.debug("Starting initializer")
    cwd = os.getcwd()

    if(not os.path.isdir(cwd + "/frame")):
        log.debug("'{}/frame' does not exist; creating".format(cwd))
        os.mkdir(cwd + "/frame")
    else:
        log.debug("'{}/frame' already exists; emptying".format(cwd))
        [ os.remove(f) for f in glob.glob(cwd + "/frame/*") ]

    if(not os.path.isdir(cwd + "/docs")):
        log.debug("'{}/docs' does not exist; creating".format(cwd))
        os.mkdir(cwd + "/docs")
    else:
        log.debug("'{}/docs' already exists; emptying".format(cwd))
        [ os.remove(f) for f in glob.glob(cwd + "/docs/*") ]

    prjdf = pd.DataFrame(columns=[ "active", "stage", "name" ]) #projects
    prtdf = pd.DataFrame(columns=[ "pid", "tid"]) #project tags
    tagdf = pd.DataFrame(columns=[ "tag", "desc" ]) #tags
    rcrdf = pd.DataFrame(columns=[ "pid", "stage", "timestamp", "note" ]) #records
    pjrdf = pd.DataFrame(columns=[ "pid", "rid", "value", "low", "high" ]) #project requires
    reqdf = pd.DataFrame(columns=[ "type", "reid" ]) #requirements; type can be money (no reference), skill (refs other), resource (refs resource), or project (refs project)
    resdf = pd.DataFrame(columns=[ "name", "reid" ]) #resource
    othdf = pd.DataFrame(columns=[ "name" ]) #other
    log.debug("Databases created")

    testp = Project.create(Project, prjdf, prtdf, pjrdf, "testing")

    log.debug("Testing data entered")

    fdir = cwd + "/frame/"
    prjdf.to_csv(fdir + "projects.csv")
    prtdf.to_csv(fdir + "project_tags.csv")
    tagdf.to_csv(fdir + "tags.csv")
    rcrdf.to_csv(fdir + "records.csv")
    reqdf.to_csv(fdir + "project_requires.csv")
    resdf.to_csv(fdir + "resources.csv")
    othdf.to_csv(fdir + "other.csv")
    log.debug("Databases written")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help = "display debugging information", action = "store_true")
    parser.add_argument("-s", "--silent", help = "only display critical errors", action = "store_true")
    parser.add_argument("-n", "--init", help = "initialize pandas dataframes and directory structure", action = "store_true")

    args = parser.parse_args()

    level = 0
    if(args.verbose):
        level = logging.DEBUG
    elif(args.silent):
        level = logging.CRITICAL
    else:
        level = logging.INFO

    logging.basicConfig(level=level, format="%(name)s) %(message)s")

    log = logging.getLogger("ideate")

    if(args.init):
        log.info("Initializing...")
        initialize(logging.getLogger("ideate.init"), args)
        log.info("Initialization Complete")

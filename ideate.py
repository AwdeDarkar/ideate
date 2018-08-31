import traceback, os, sys, logging, argparse, glob, time
import pandas as pd

class Project:
    def __init__(self, dbs, pid):
        self.dbs = dbs
        self.pid  = pid
        self.name = self.dbs["projects"].iloc[[pid]]["name"]
        self.stage = self.dbs["projects"].iloc[[pid]]["stage"]
        self.active = self.dbs["projects"].iloc[[pid]]["active"]
        self.requirements = []

        for req in dbs["project requires"].loc[dbs["project requires"]["pid"] == self.pid]:
            self.requirements.append(Requirement(dbs, req["rid"]))

        self.tags = []

    def setName(self, name):
        self.name = name
        self.dbs["projects"][[self.pid]]["name"] = name

    def setStage(self, stage):
        self.stage = stage
        self.dbs["projects"][[self.pid]]["stage"] = stage
        pd_a(self.dbs["records"], { "pid" : self.pid, "stage" : stage, "timestamp" : time.time() })

    def setActive(self, active):
        self.active = active
        self.dbs["projects"][[self.pid]]["active"] = active

    def create(dbs, name):
        pd_a(prjdf, {"name" : name, "stage" : "formation", "active" : False })
        return Project(dbs, prjdf.index[-1])

def pd_a(df, row):
    df.loc[df.shape[0]] = row

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

    dbs = {}
    dbs["projects"] = pd.DataFrame(columns=[ "active", "stage", "name" ]) #projects
    dbs["project tags"] = pd.DataFrame(columns=[ "pid", "tid"]) #project tags
    dbs["tags"] = pd.DataFrame(columns=[ "tag", "desc" ]) #tags
    dbs["records"] = pd.DataFrame(columns=[ "pid", "stage", "timestamp", "note" ]) #records
    dbs["project requires"] = pd.DataFrame(columns=[ "pid", "rid", "value", "low", "high" ]) #project requires
    dbs["requirements"] = pd.DataFrame(columns=[ "type", "reid" ]) #requirements; type can be money (no reference), skill (refs other), resource (refs resource), or project (refs project)
    dbs["resource"] = pd.DataFrame(columns=[ "name", "reid" ]) #resource
    dbs["other"] = pd.DataFrame(columns=[ "name" ]) #other
    log.debug("Databases created")

    log.debug(str(prjdf.shape))
    testp = Project.create(Project, dbs, "testing")
    log.debug(str(prjdf.shape))

    log.debug("Testing data entered")

    fdir = cwd + "/frame/"
    dbs["projects"].to_csv(fdir + "projects.csv")
    dbs["project tags"].to_csv(fdir + "project_tags.csv")
    dbs["tags"].to_csv(fdir + "tags.csv")
    dbs["records"].to_csv(fdir + "records.csv")
    dbs["project requires"].to_csv(fdir + "project_requires.csv")
    dbs["resources"].to_csv(fdir + "resources.csv")
    dbs["other"].to_csv(fdir + "other.csv")
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

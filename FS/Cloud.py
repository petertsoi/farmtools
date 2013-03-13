from os import chdir, listdir, path, system
import tarfile

from farmtools.Farm.Env import *
from farmtools.FS.Sandbox import *

class Cloud:
  __clouduser__ = "farm"
  __dnsname__ = "cloud.cs.berkeley.edu"
  @classmethod
  def UploadDir(cls, outputdir):
    mybox = Sandbox()
    if outputdir:
      outputdir = path.join(mybox.path, outputdir)
      if path.exists(outputdir) and path.isdir(outputdir):
        tarfilename = ".farmout.tgz"
        tarfilepath = path.join(mybox.path, tarfilename)
        tar = tarfile.open(tarfilepath, "w:gz")
        chdir(outputdir)
        for file in listdir(outputdir):
          tar.add(file)
        tar.close()
        clouduser = cls.__clouduser__
        dnsname = cls.__dnsname__
        owner = mybox.env.Get("FARM_JOBOWNER")
        jid = mybox.env.Get("FARM_JOBID")
        tid = mybox.env.Get("FARM_TASKID")
        remotepath = path.join("/var/spool/tractor/farm-output", owner, jid, tid)
        system("ssh -o StrictHostKeyChecking=no %(clouduser)s@%(dnsname)s 'source cnm_settings; cnm_dfmkdir -u %(owner)s -j %(jid)s -t %(tid)s'" % locals())
        system("scp -o StrictHostKeyChecking=no %(tarfilepath)s %(clouduser)s@%(dnsname)s:%(remotepath)s/." % locals())
        system("ssh -o StrictHostKeyChecking=no %(clouduser)s@%(dnsname)s 'cd %(remotepath)s; tar -zxf %(tarfilename)s; rm -f %(tarfilename)s; chmod -R 775 .'" % locals())
      else:
        raise Exception("UploadDir requires a directory path")
    else:
      raise Exception("UploadDir requires a directory path")


#!/usr/bin/python3
import os
import sys
import wget
import time
import subprocess


class NxFilter(object):
    NXF_DIR = "NXF-IMAGE"
    NXF_PATH = "./{}".format(NXF_DIR)

    def __init__(self, url_nxf):
        self.url_nxf = url_nxf
        self.url_list = self.url_nxf.split("/")
        self.old_nxf = self.url_list[-1]
        self.nxfstate = None
          
    def download(self):
        try:
          os.chdir(self.NXF_DIR)
          self.nxfstate = subprocess.call(["wget", self.url_nxf])

        except Exception as e:
           return "Something happen with the download link\n{}".format(e)

    def install(self):
         subprocess.call(["dpkg", "-i", self.old_nxf])

    def stop(self):
         subprocess.call(["systemctl", "stop", "nxfilter"])

    def start(self):
         subprocess.call(["systemctl", "start", "nxfilter"])

    def status(self):
         subprocess.call(["systemctl", "status", "nxfilter"])

class Prep_NXF(object):
   def __init__(self, folder):
       self.folder = folder

   def folderExist(self):
       return os.path.isdir(self.folder) 

   def packageExist(self, package):
       for file in os.listdir(self.folder):
            if file == package:
               return True
       return False


def get_status(value):
   status = None
   if value:
       status = "success"
   else:
       status = "failed"
   return status 

if __name__ == "__main__":
    print("-"*5+"NXFILTER UPGRADE SCRIPT"+"-"*5) 
    running = True
    print("Enter Nxfilter URL")
    geturl = input(">: ")
    nxf = NxFilter(geturl)
    prep_nxf = Prep_NXF(nxf.NXF_DIR)
    test_folder = "-> Check if Folder Exist [{}]"
    test_package = "-> Check if Package Already Exist [{}]"
    while running:
         #CHECK NXFILTER CONDITION
         print("PRE DOWNLOAD CHECKING....")
         print(test_folder.format(prep_nxf.folderExist()))
         print(test_package.format(prep_nxf.packageExist(nxf.old_nxf)))
         if prep_nxf.folderExist() and not prep_nxf.packageExist(nxf.old_nxf):
            #HERE GOES THE CODE FOR DOWNLOAD
            nxf.download()
            running = False
        
         else:
             print("One of the Condition Failed, Check PRE DOWNLOAD status")
             break
             sys.exit(1)

    if nxf.nxfstate == 0:
	     print("Download was successfull !!!")
	     print("Action => Stop Current Nxfilter Process ....")
	     nxf.stop()
	     time.sleep(.5)
	     print("Action => Installing Nxfilter Package....")
	     nxf.install()
	     time.sleep(1)
	     print("Action => Start New Nxfilter Process ....")
	     nxf.start()
	     time.sleep(.5)
	     print("NXFILTER {} HAVE BEEN SUCCESSFULY DOWNLOADED & INSTALLED".format(nxf.old_nxf))
	     nxf.status()
	     sys.exit()

    else:
       print("Download Have Failed...Check the Correct URL")
       sys.exit()

    
 

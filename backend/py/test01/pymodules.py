import pathlib, os,sys
## To have the parent folder of this file
path_thisfile = pathlib.Path(__file__).parent.resolve().__str__() #  pathlib.Path(__file__).parent.resolve() returns a WindowsPath Object, and __str__() is to convert the object to a string
segs_ls =  path_thisfile.split('\\')
currentprojectname = segs_ls[len(segs_ls)-1]
# loading modules from modules_spacy 
# exec ("from " + currentprojectname + ".pymodules.spacy.modules_spacy import *") # load all modules (*)

## load common modules ... not used in this simple example
# cwd = os.getcwd() # cwd is where the python command starts. In this case, it is at projectroot/backend/py
# # add the location of the py common module file 
# location_commonmodules = cwd + '/common_pymodules'
# sys.path.insert(1, location_commonmodules) # add the location at the top of the sys.path, thus, by default, the py script file spacy_modules will be loaded from there
# from modules_testing import * # it works as spacy_modules is in the same folder of this py file
# from modules_spacy import * # do not name the py file like spacy.py (it'll be confused with the package spacy)
# from modules_common import *
# from modules_classification import * # it works as spacy_modules is in the same folder of this py file

def get_spacy_sentences(text):
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentences_ls =[]
    for sent in doc.sents:
        sentences_ls.append(sent.text)
    return sentences_ls


def get_spacytest_data(requestdatafromfrontend_json):
    import os, json

    # do not use cwd
    # # get the currentworking path, i.e., in this case, C:\Users\syao2\AppData\Local\MyWorks\js\herokutest\backend\py
    # cwd = os.getcwd() # cwd is a string
    # from pathlib import Path
    # cwd_pathobj = Path(cwd) # convert to a path object
    # # need to go back to the project path C:\Users\syao2\AppData\Local\MyWorks\js\herokutest\
    # projectrootstr = str(cwd_pathobj.parent.parent.absolute()).replace('\\', '/') 
    # print('projectroot', projectrootstr)

    # use file parent folder instead
    import pathlib
    parentfolder_thisfile = pathlib.Path(__file__).parent.parent.parent.parent.resolve().__str__() # the parent folder of this file (a diff way to get the parent folder, diff from the above)
    projectrootstr = parentfolder_thisfile.replace('\\', '/') 
    print ( 'projectrootstr', projectrootstr  )

    jsonfile=projectrootstr + requestdatafromfrontend_json['requestdatafromfrontend']['location']['somedata_filelocation']
    try:
        openedfile = open(jsonfile, encoding="UTF-8")
        somedata_dict = json.load(openedfile)
    except:
        somedata_dict={}

    text = requestdatafromfrontend_json['requestdatafromfrontend']['data']

    sentences_ls = get_spacy_sentences(text)

    responsedatafrombackend_json = {'responsedatafrombackend':sentences_ls}
    return responsedatafrombackend_json



def get_some_data(requestdatafromfrontend_json):
    import os, json

    # # get the currentworking path, i.e., in this case, C:\Users\syao2\AppData\Local\MyWorks\js\herokutest\backend\py
    # cwd = os.getcwd() # cwd is a string
    # from pathlib import Path
    # cwd_pathobj = Path(cwd) # convert to a path object
    # # need to go back to the project path C:\Users\syao2\AppData\Local\MyWorks\js\herokutest\
    # projectrootstr = str(cwd_pathobj.parent.parent.absolute()).replace('\\', '/') 
    # print('65, projectroot', projectrootstr)

    # use file parent folder instead
    import pathlib
    parentfolder_thisfile = pathlib.Path(__file__).parent.parent.parent.parent.resolve().__str__() # the parent folder of this file (a diff way to get the parent folder, diff from the above)
    projectrootstr = parentfolder_thisfile.replace('\\', '/') 
    print ( 'projectrootstr', projectrootstr  )

    jsonfile=projectrootstr + requestdatafromfrontend_json['requestdatafromfrontend']['location']['somedata_filelocation']
    try:
        openedfile = open(jsonfile, encoding="UTF-8")
        somedata_dict = json.load(openedfile)
    except:
        somedata_dict={}
    responsedatafrombackend_json = {'responsedatafrombackend':somedata_dict}
    return responsedatafrombackend_json


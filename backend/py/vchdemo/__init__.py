# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
# this is for VCH demo

# IMPORT MODULES
# import the Flask member from the flask package
from flask import Flask, render_template, request

#make an instance of Flask, __name__ representing a set of pre-defined variable names
# define the path to the html template 
# https://stackoverflow.com/questions/31002890/how-to-reference-a-html-template-from-a-different-directory-in-python-flask

## Without specifying the path to the folder containing html templates, the line is:
appFlask = Flask(__name__)

#### solve the CORS problem #######################
# https://flask-cors.readthedocs.io/en/latest/
from flask_cors import CORS
CORS(appFlask)
#### solve the CORS problem #######################

rootpathstr = appFlask.root_path # string of path to this example (e.g., test01)
from pathlib import Path
rootpath = Path(rootpathstr) # convert the path string to a path object
projectrootstr = str(rootpath.parent.parent.parent.absolute()).replace('\\', '/')  # projectroot is the root of the whole project, like C:\Users\syao2\AppData\Local\MyWorks\js\herokutest
# print ('projectrootstr', projectrootstr)

# use the indexhtml and the frontend js apps in the project root, not the example root
appFlask.template_folder = projectrootstr + '/frontend'
appFlask.static_folder = projectrootstr + '/frontend/js' 

# debate: using the index in projectroot/frontend/index.html is neat.
# however, it is not flexible if there are multiple py applications (test01, test2, ...) and each requires a different index
# that said, ususally a project only contains contents that should be controlled by a single index.html 

## following are to use the the frontend html template and js applications with the project. It is not available for this test01 example though. 
# # print('====', appFlask.root_path)
# # define the virtual folders for html templates and javascript files
# appFlask.template_folder = appFlask.root_path.replace('\\', '/') + '/frontend/webpagetemplates'
# appFlask.static_folder = appFlask.root_path.replace('\\', '/') + '/frontend/js' 
# # print('==temp==', appFlask.template_folder)
# # print('==static==', appFlask.static_folder)
#################################################################################

# determine the example folder name (in this case it is tes1), which is the last part after the backslash in appFlask.root_path
# split the rootpath by backslash
# segs_ls =  appFlask.root_path.split('\\')
# currentexamplename = segs_ls[len(segs_ls)-1]
# # print('===length of segs_ls', len(segs_ls), currentexamplename)
# # Note: must after setting appFlask (eval() does not work)
# exec ("from " + currentexamplename + " import master") # import modules in test01/master.py
#########################################################################################################
# the above does not work when deployin to heroku. The following is a work-around solution:
# 1. add the current path to sys.path
import os, sys
parentfolder_thisfile = str(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/') # the parent folder of this file (a diff way to get the parent folder, diff from the above)
sys.path.insert(1, parentfolder_thisfile)
print ('path_thisfile', parentfolder_thisfile) 
from pymodules import *
#########################################################

# DECORATION
# define what to be rendered to the index page (index page is enabled to send request to backend)
@appFlask.route('/')
@appFlask.route('/index') # not using flask to send request so no need to specify methods=['POST'] here
# RENDERING OR DO SOMETHING
def doSomethingInHomepage():
    return render_template('index.html')

# define the backend with gets request and post response 
@appFlask.route('/backend', methods=['POST'])  # ust specify methods= ['POST']
# render / do something
def doSomethingAtBackend():
    # datafromfrontend_str = request.form['datafromfrontend'] # Note: this line works if the data sent from frontend is from a submit form, in which there is an input field with id='datafromfrontend'
    requestdatafromfrontend_json=request.get_json(force=True)
    # print(39, 'the data json from frontend ======', requestdatafromfrontend_json)

    # check the request category
    requesttask = requestdatafromfrontend_json['requesttask']
    # print ('-'+requesttask+'-')
    # if requesttask is to get a selected sentence
    if requesttask == 'get_tokenized_data':
        responsedatafrombackend_json= get_tokenized_data(requestdatafromfrontend_json)
    elif requesttask == 'get_ent_nc':
        responsedatafrombackend_json= get_ent_nc(requestdatafromfrontend_json)
    elif requesttask == 'get_matched_phrases':
        responsedatafrombackend_json= get_matched_phrases(requestdatafromfrontend_json)
    elif requesttask == 'get_cleaned_text':
        responsedatafrombackend_json= get_cleaned_text(requestdatafromfrontend_json)
    



    else:
        responsedatafrombackend_json = {'responsedatafrombackend': requesttask + " is an unknown request cateogory." } 

    networkpaths_dict = {
        "appname": 'The value of __name__ is {}'.format(__name__),
        "appfilepath": 'The path of the current file {}'.format(rootpathstr),
        "projectrootpath" :'The root of the current project {}'.format(projectrootstr)
    }
    responsedatafrombackend_json['networkinfo']=networkpaths_dict


    # print ('=====response data json:', responsedatafrombackend_json)
    import json
    stringified_responsedatafrombackend_str = json.dumps(responsedatafrombackend_json)
    # print('is it a string', isinstance(stringified_responsedatafrombackend_str, str))
    return stringified_responsedatafrombackend_str

if __name__ == '__main__':
    appFlask.run()













# import webbrowser
# url = 'http://localhost:1234'
# webbrowser.open_new_tab(url)

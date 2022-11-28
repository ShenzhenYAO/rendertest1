# 962c remove the section titles

section_titles='''
ABSENT
ADJOURN
ADJOURNMENT
ADMINISTRATION REPORTS
ADOPTION OF AGENDA
ADOPTION OF MINUTES
ADOPTION OF PREVIOUS MINUTES OF COUNCIL
ADOPTION OF THE AGENDA
AGENDA ADDITIONS & DELETION
APPOINTMENTS AND DELEGATIONS
APPROVAL OF AGENDA
APPROVAL OF MINUTES
APPROVAL OF THE AGENDA
BACKGROUND INFORMATION
BUSINESS ARISING
BUSINESS ARISING FROM MINUTES
BUSINESS ARISING FROM THE MINUTES
BUSINESS ITEMS
BYLAWS
CALL TO ORDER
CLOSED COUNCIL MEETING
COMMITTEE
COMMITTEE / COMMISSION MINUTES AND REPORTS
COMMITTEE MINUTES
COMMITTEE RECOMMENDATION
COMMITTEE REPORTS
COMMITTEES
COMMUNICATIONS
CONDOLENCES
CONSENT AGENDA
CONSENT AGENDA ITEMS
CORPORATE OFFICER
CORRESPONDENCE
CORRESPONDENCES
COUNCIL - STAFF IN CAMERA
COUNCIL AGENDA
COUNCIL COMMITTEES
COUNCIL IN ATTENDANCE
COUNCIL MEETING MINUTES
COUNCIL MEMBERS STAFF MEMBERS
COUNCIL OR STAFF ANNOUNCEMENTS
COUNCIL REPORTS
COUNCIL WORKSHOP REPORT
COUNCILLORS
DELEGATION
DELEGATIONS
END OF CONSENT AGENDA
ENQUIRIES AND OTHER MATTERS
FILEHEAD
FINAL MOTIONS AS APPROVED
FINANCE COMMITTEE MEETING
IN CAMERA
IN CAMERA MEETING
INFORMATION ITEMS
INQUIRIES
ITEMS FOR INFORMATION/RELEASE OF CLOSED MEETING ITEMS
ITEMS REMOVED FROM THE CONSENT AGENDA
LATE AGENDA ITEMS
LATE BUSINESS
MATTERS ADOPTED ON CONSENT
MAYOR'S
MAYOR'S YEAR-END MESSAGE
MOTION TO CLOSE
MOTION TO GO
MOTIONS
MUNICIPAL HALL COUNCIL CHAMBER
NEW BUSINESS
NEXT MEETING
NOTICE OF COUNCIL MEMBER'S MOTIONS
NOTICE OF MOTION
NOTICES OF MOTION
NOTICES OF MOTIONS
OPEN THE REGULAR MEETING
OPENING OF COUNCIL MEETING
OTHER BUSINESS
OTHER ITEMS / NOTICES OF MOTION
OTHER MEETINGS AND REVIEWS
OTHER REPORTS
OTHERS IN ATTENDANCE
PANEL MEETING
PERMITS
PRESENTATION
PRESENTATIONS
PROCLAMATIONS
PUBLIC
PUBLIC ANNOUNCEMENT
PUBLIC COMMENTS
PUBLIC DELEGATION
PUBLIC INPUT
PUBLIC PARTICIPATION
QUESTION PERIOD
QUESTIONS
RECEIVING OF INFORMATION
RECESS
RECOGNITIONS
RECOMMENDATIONS
RECONVENE REGULAR MEETING
REGRETS
RELEASE OF CLOSED MEETING DECISIONS
REOPEN TO THE PUBLIC
REPORT FROM IN CAMERA
REPORTS
RESOLUTIONS
REVIEW & APPROVAL OF MINUTES OF PRIOR MEETINGS
RISE AND REPORT
RISE WITH REPORT
SCHEDULED (TIMED) ITEMS
SERVICES DIVISION
STAFF IN ATTENDANCE
STAFF REPORT
STAFF REPORTS
START OF CONSENT AGENDA
TERMINATION
UNFINISHED BUSINESS
WELCOME
'''

import sys, os, json, gzip , re

# nlp = spacy.load("en_core_web_sm")
cwd = os.getcwd().replace('\\', '/') # the cwd is the location where python starts, in this case, it is C:\Personal\Virtual_Server\PHPWeb\ml_text\python
# add the location of the py common module file 
# location_commonmodules = cwd + '/pyflaskapps/common_pymodules'
# sys.path.insert(1, location_commonmodules) # add the location at the top of the sys.path, thus, by default, the py script file spacy_modules will be loaded from there
# from modules_common import * 
# from modules_spacy import * 

section_titles_ls = section_titles.split('\n')
section_titles_ls = list( [ x for x in section_titles_ls  if len(x)>0 ])
# print(section_titles_ls)

tmpdir= '/additional_96x/data/history/'
tmpoutdir  = '/additional_96x/data/history/out/' 

# read the bigtext gz
def clean3_get_ents_ncs():

    for nn in ["1", "2"]:
        gzlocation = cwd + tmpoutdir+ '/entities_cleaned2_nounchunks_bigtext_{}.json.gz'.format(nn)
        # print(corpusfilepath)
        with gzip.open(gzlocation, 'r') as fin:        
            json_bytes = fin.read()      
        # convert bytes to string
        json_str = json_bytes.decode('utf-8')  
        # convert string to json  
        srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
        ents_ncs_ls = srcjson['data']
        # get all labels
        
        new_ents_ncs_ls =[]

        for x in ents_ncs_ls:
            text = x['text']
            text = re.sub(r'\d+', '', text).strip() # remove digits
            text_like_title=0
            for y in section_titles_ls:
                if text[:len(y)] == y:
                    text_like_title =1
                    break
            if (text_like_title == 0):
                new_ents_ncs_ls.append(x)

        print(len(ents_ncs_ls), len(new_ents_ncs_ls))

        # save ents_ncs 
        jsonobj = {
            'sources': [
                cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_cleaned2_nounchunks_bigtext_{}.json.gz'.format(nn),
            ],
            "description": "cleaned by excluding entities that are like a section title (begins with a section title like string",
            'program': r'C:\Users\syao2\AppData\Local\MyWorks\js\ml_text\python\pyflaskapps\example15_spacytests\pymodules\spacy\tests\test962c.py',
            'data': new_ents_ncs_ls
        }

        # save all entites and noun chunks
        targetjsonfile = cwd + tmpoutdir + '/entities_cleaned3_nounchunks_bigtext_{}.json.gz'.format(nn)
        json_str = json.dumps(jsonobj) # convert to string
        json_bytes = json_str.encode('utf-8') # convert to bytes
        with gzip.open(targetjsonfile, 'w') as f:
            f.write(json_bytes)
        
clean3_get_ents_ncs()





# test962a3, based on the ents and ncs by 962
# exclude pure number, name, place, url, and like a section title ...

import sys, os, json, gzip 

# nlp = spacy.load("en_core_web_sm")
cwd = os.getcwd().replace('\\', '/') # the cwd is the location where python starts, in this case, it is C:\Personal\Virtual_Server\PHPWeb\ml_text\python
# # add the location of the py common module file 
# location_commonmodules = cwd + '/pyflaskapps/common_pymodules'
# sys.path.insert(1, location_commonmodules) # add the location at the top of the sys.path, thus, by default, the py script file spacy_modules will be loaded from there
# from modules_common import * 
# from modules_spacy import *
# 
# # load the json
tmpdir= '/additional_96x/data/history/'
tmpoutdir  = '/additional_96x/data/history/out/' 

# read the bigtext gz
def clean1_get_ents_ncs():

    # 1. MAKE a text dict with all entity text
    ent_text_dict={}
    for nn in ["1", "2"]:
        gzlocation = cwd + tmpoutdir + '/entities_cleaned0_nounchunks_bigtext_{}.json.gz'.format(nn)
        # print(corpusfilepath)
        with gzip.open(gzlocation, 'r') as fin:        
            json_bytes = fin.read()      
        # convert bytes to string
        json_str = json_bytes.decode('utf-8')  
        # convert string to json  
        srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
        ents_ncs_ls = srcjson['data']
        # print (ents_ncs_ls[0])

        for x in ents_ncs_ls:
            if x['label'] != 'noun_chunk':
                try: 
                    ent_text_dict[x['text']]
                except:
                    ent_text_dict[x['text']] = 1
    print(len(ent_text_dict.keys()))

    for nn in ["1", "2"]:
        gzlocation = cwd +  tmpoutdir +  '/entities_cleaned0_nounchunks_bigtext_{}.json.gz'.format(nn)
        # print(corpusfilepath)
        with gzip.open(gzlocation, 'r') as fin:        
            json_bytes = fin.read()      
        # convert bytes to string
        json_str = json_bytes.decode('utf-8')  
        # convert string to json  
        srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
        ents_ncs_ls = srcjson['data']
        # get all labels

        labels_ls =[]
        labels_exclude_ls =['ORG', 'DATE', 'TIME', 'GPE', 'PERSON',  'EVENT',  'CARDINAL', 'LAW', 'LOC', 'WORK_OF_ART', 'ORDINAL', 'PERCENT', 'MONEY', 'NORP', 'QUANTITY', 'LANGUAGE']
        ents_to_include_ls=[]
        ncs_ls=[]
        for x in ents_ncs_ls:
            if x['label'] not in labels_ls:
                labels_ls.append(x['label'])
            if x['label'] in labels_exclude_ls:
                pass
            elif x['label'] != 'noun_chunk':
                ents_to_include_ls.append(x)
            else: 
                ncs_ls.append(x)

        print(len(ents_ncs_ls),  len(ents_to_include_ls), len(ncs_ls) )

        ncs_to_keep_ls = []
        for x in ncs_ls:
            try:
                ent_text_dict[x['text']]
            except:
                ncs_to_keep_ls.append(x)
        print(len(ncs_ls), len(ncs_to_keep_ls))

        new_ents_ncs_ls = ents_to_include_ls + ncs_to_keep_ls

        # save ents_ncs 
        jsonobj = {
            'sources': [
                cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_cleaned0_nounchunks_bigtext_{}.json.gz'.format(nn),
            ],
            "description": "cleaned by excluding entities like ORG, PERSON, etc, and noun chunks that are the same as entities",
            'program': r'C:\Users\syao2\AppData\Local\MyWorks\js\ml_text\python\pyflaskapps\example15_spacytests\pymodules\spacy\tests\test962a3.py',
            'data': new_ents_ncs_ls
        }

        # save all entites and noun chunks
        targetjsonfile = cwd + tmpoutdir + 'entities_cleaned1_nounchunks_bigtext_{}.json.gz'.format(nn)
        json_str = json.dumps(jsonobj) # convert to string
        json_bytes = json_str.encode('utf-8') # convert to bytes
        with gzip.open(targetjsonfile, 'w') as f:
            f.write(json_bytes)
        
clean1_get_ents_ncs()
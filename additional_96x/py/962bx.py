# exclude if the phrase only have numbers or punctuations

import sys, os, json, gzip , re

# nlp = spacy.load("en_core_web_sm")
cwd = os.getcwd().replace('\\', '/') # the cwd is the location where python starts, in this case, it is C:\Personal\Virtual_Server\PHPWeb\ml_text\python
# add the location of the py common module file 
# location_commonmodules = cwd + '/pyflaskapps/common_pymodules'
# sys.path.insert(1, location_commonmodules) # add the location at the top of the sys.path, thus, by default, the py script file spacy_modules will be loaded from there
# from modules_common import * 
# from modules_spacy import * 

tmpdir= '/additional_96x/data/history/'
tmpoutdir  = '/additional_96x/data/history/out/' 


# read the bigtext gz
def clean2_get_ents_ncs():

    for nn in ["1", "2"]:
        gzlocation = cwd + tmpoutdir + '/entities_cleaned1_nounchunks_bigtext_{}.json.gz'.format(nn)
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
            text = re.sub(r"[+~`%^*()_-{}\[\]\|\\:\'\"\<\>#,.;@?!&$/]+", '', text).strip() # remove digits  ?!&$/
            # text = re.sub(r'[~`%^*()_-+={}\[\]\|\\:\'\"\<\>,.;@#?!&$/]+', '', text).strip() # remove digits
            # text = re.sub(r'[^\w]', '', text).strip() # remove digits
            if(len(text)>0) & (len(x['text']) > 1) & ( x['text'] !=x['text'].upper() ) & ('council' not in x['text'].lower()) &  ('bylaw' not in x['text'].lower()) & ('carr' not in x['text'].lower()):
                # print(x['text'])
                new_ents_ncs_ls.append(x)

        # print(len(ents_ncs_ls), len(new_ents_ncs_ls))

        # save ents_ncs 
        jsonobj = {
            'sources': [
                cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_cleaned1_nounchunks_bigtext_{}.json.gz'.format(nn),
            ],
            "description": "cleaned by excluding entities that only contas digits or punctuations",
            'program': r'C:\Users\syao2\AppData\Local\MyWorks\js\ml_text\python\pyflaskapps\example15_spacytests\pymodules\spacy\tests\test962b.py',
            'data': new_ents_ncs_ls
        }

        # save all entites and noun chunks
        targetjsonfile = cwd + tmpoutdir + '/entities_cleaned2_nounchunks_bigtext_{}.json.gz'.format(nn)
        json_str = json.dumps(jsonobj) # convert to string
        json_bytes = json_str.encode('utf-8') # convert to bytes
        with gzip.open(targetjsonfile, 'w') as f:
            f.write(json_bytes)
        
clean2_get_ents_ncs()
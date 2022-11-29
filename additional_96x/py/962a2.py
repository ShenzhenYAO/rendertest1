## merge ents ncs and phrases of other themes

import sys, os, json, gzip 

cwd = os.getcwd().replace('\\', '/')

# load the json
tmpdir= '/additional_96x/data/history/'
tmpoutdir  = '/additional_96x/data/history/out/'

# load the ents ncs gz

def bigtext_get_ents_ncs():

    for nn in ["1", "2"]:
        gzlocation = cwd + tmpdir + '/entities_uncleaned_nounchunks_bigtext_{}.json.gz'.format(nn)
        # print(corpusfilepath)
        with gzip.open(gzlocation, 'r') as fin:        
            json_bytes = fin.read()      
        # convert bytes to string
        json_str = json_bytes.decode('utf-8')  
        # convert string to json  
        srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}

        ents_ncs_ls = srcjson['data']

        # print(len(ents_ncs_ls), ents_ncs_ls[0])

        gzlocation2 = cwd + tmpoutdir + '/phrases_otherthemes_uncleaned_bigtext_{}.json.gz'.format(nn)
        # print(corpusfilepath)
        with gzip.open(gzlocation2, 'r') as fin:        
            json_bytes = fin.read()      
        # convert bytes to string
        json_str = json_bytes.decode('utf-8')  
        # convert string to json  
        srcjson2 = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}

        phrases_otherthemes_ls = srcjson2['data']

        # the end position in phrases_otherthemes_ls is WRONG!!!
        gzlocation = cwd + tmpoutdir + 'bigtext_and_sents_pos_in_bigtext_{}.json.gz'.format(nn)
        # print(corpusfilepath)
        with gzip.open(gzlocation, 'r') as fin:        
            json_bytes = fin.read()      
        # convert bytes to string
        json_str = json_bytes.decode('utf-8')  
        # convert string to json  
        srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
        bigtext = srcjson['data']['bigtext']
        # print(len(bigtext))
        for x in phrases_otherthemes_ls:
            start = x['start']
            end2= start + len(x['text']) -1
            x['end']=end2
            # x['text2'] = bigtext[start:end2+1]


        print(len(phrases_otherthemes_ls), phrases_otherthemes_ls[0])

        # merge the two

        all_ls = ents_ncs_ls + phrases_otherthemes_ls

        # save, ...
        jsonobj = {
            'sources': [
                cwd + tmpdir + '/entities_uncleaned_nounchunks_bigtext_{}.json.gz'.format(nn), 
                cwd + tmpoutdir + '/phrases_otherthemes_uncleaned_bigtext_{}.json.gz'.format(nn)
            ],
            'program': r'C:\Users\syao2\AppData\Local\MyWorks\js\ml_text\python\pyflaskapps\example15_spacytests\pymodules\spacy\tests\test962a2.py',
            'data': all_ls
        }

        # save all entites and noun chunks
        targetjsonfile = cwd + tmpoutdir + '/entities_cleaned0_nounchunks_bigtext_{}.json.gz'.format(nn)
        json_str = json.dumps(jsonobj) # convert to string
        json_bytes = json_str.encode('utf-8') # convert to bytes
        with gzip.open(targetjsonfile, 'w') as f:
            f.write(json_bytes)

bigtext_get_ents_ncs()
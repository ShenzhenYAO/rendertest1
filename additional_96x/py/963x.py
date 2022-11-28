# based on bigtext 1 and 2 made by 961
# split by the delimiter, indicate the start and end position of each sent

import sys, os, json, gzip 

# nlp = spacy.load("en_core_web_sm")
cwd = os.getcwd().replace('\\', '/') # the cwd is the location where python starts, in this case, it is C:\Personal\Virtual_Server\PHPWeb\ml_text\python
# add the location of the py common module file 
# location_commonmodules = cwd + '/pyflaskapps/common_pymodules'
# sys.path.insert(1, location_commonmodules) # add the location at the top of the sys.path, thus, by default, the py script file spacy_modules will be loaded from there
# from modules_common import * 
# from modules_spacy import * 

tmpdir= '/additional_96x/data/history/'
tmpoutdir  = '/additional_96x/data/history/out/' 


# testtext = '012 196808240800123456 345 196808240800123456 678'
# delimiter = ' 196808240800123456 '

def get_sent_start_end(text, delimiter):
    results_ls =[]
    len_dlmt = len(delimiter)
    sents_ls = text.split(delimiter)
    # print(sents_ls)
    start=0
    i=-1
    for sent in sents_ls:
        i +=1
        end = start + len(sent)
        # print(25, start, end)
        # print(27, text[start:end+1])
        results_ls.append({
            "start":start,
            "end":end,
            "sent_id_allsubsections": i
            # "text": text[start:end+1]
        }) 
        start = end + len_dlmt
    return results_ls

# results_ls = get_sent_start_end(testtext, delimiter)
# print (results_ls)
# the above shows that the algorithm is very simple

for nn in ["1","2"]:
    bigtextgzlocation = cwd + tmpdir + '/bigtext_sents_of_all_sections_{}.json.gz'.format(nn)
    # print(corpusfilepath)
    with gzip.open(bigtextgzlocation, 'r') as fin:        
        json_bytes = fin.read()      
    # convert bytes to string
    json_str = json_bytes.decode('utf-8')  
    # convert string to json  
    srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}

    bigtext = srcjson['data']
    delimiter = srcjson['delimiter']

    sents_pos_ls = get_sent_start_end(bigtext, delimiter)

    jsonobj = {
        'sources': [
            cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/bigtext_sents_of_all_sections_{}.json.gz'.format(nn), 
        ],
        'program': r'C:\Users\syao2\AppData\Local\MyWorks\js\ml_text\python\pyflaskapps\example15_spacytests\pymodules\spacy\tests\test963.py',
        'data': {"bigtext": bigtext, "sents_pos": sents_pos_ls}
    }

    # save
    targetjsonfile = cwd + tmpoutdir+  '/bigtext_and_sents_pos_in_bigtext_{}.json.gz'.format(nn)
    json_str = json.dumps(jsonobj) # convert to string
    json_bytes = json_str.encode('utf-8') # convert to bytes
    with gzip.open(targetjsonfile, 'w') as f:
        f.write(json_bytes)


    

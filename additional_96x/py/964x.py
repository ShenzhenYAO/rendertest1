

'''
    based on 961 and  963

    

    entities_nounchunks_bigtext_1 or 2.json is made by 962d, each like 
        {
            "start": ...,
            "end": ,
            "label":  
        }
        start/end for char pos in bigtext 1 or 2

    bigtext_and_sents_pos_in_bigtext_1 or 2.json is made by 963, like
    {"bigtext": bigtext, "sents_pos": sents_pos_ls}
    sents_pos_ls is like {start, end, sent_id_allsubsections}

    so, according to start and end position of ent/nc, we can locate which sent_id_allsubsections it has in bigtext_and_sents_pos_in_bigtext_1
        (as long as start between sents_pos_ls[start:end], or end sents_pos_ls[start:end] )
    
    then in 965,  with the sent_id_allsubsections, we can link to the sents_of_all_sections_1


is it possible to inject something here?
To exclude ents_ncs ..

''' 

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

for nn in ["1", "2"]:

    sents_index_phrases_ls =[]

    # load the ent nc list, like {start: end: label}
    location = cwd + tmpoutdir+ '/entities_cleaned4_nounchunks_bigtext_{}.json.gz'.format(nn)
    # print(corpusfilepath)
    with gzip.open(location, 'r') as fin:        
        json_bytes = fin.read()      
    # convert bytes to string
    json_str = json_bytes.decode('utf-8')  
    # convert string to json  
    srcjson = json.loads(json_str)   
    ents_ncs_ls = srcjson['data']

    ents_ncs_ls = sorted(ents_ncs_ls, key=lambda d: (d['start'], d['end'])) 
    # print(len(ents_ncs_ls))
    # print(ents_ncs_ls[0])


    # load the bigtext_and_sents_pos_in_bigtext
    location = cwd +tmpoutdir +  '/bigtext_and_sents_pos_in_bigtext_{}.json.gz'.format(nn)
    # print(corpusfilepath)
    with gzip.open(location, 'r') as fin:        
        json_bytes = fin.read()      
    # convert bytes to string
    json_str = json_bytes.decode('utf-8')  
    # convert string to json  
    srcjson = json.loads(json_str) 

    sents_pos_ls = srcjson['data']['sents_pos']
    bigtext = srcjson['data']['bigtext']
    # print(len(sents_pos_ls)) # like {start, end, sent_id_allsubsections}
    # print(sents_pos_ls[-1])

    # print(sents_pos_ls[0])

    # split sents_pos_ls into 46 
    kk =-1
    step = 100000
    sents_dict = {}
    this_seg_ls =[]
    for sent in sents_pos_ls:
        kk +=1 
        if kk==0:
            print (sent)       
        sent_start=sent['start']
        if sent_start <= step:
            this_seg_ls.append(sent)
        else:
            sents_dict[str(step)] = this_seg_ls
            this_seg_ls=[]
            this_seg_ls.append(sent)
            step +=100000
        if kk == len(sents_pos_ls)-1:
            sents_dict[str(step)] = this_seg_ls

    # print(len(list(sents_dict.keys())))
    # print(88, sents_dict[list(sents_dict.keys())[0]])


    # split the ents_ncs into 46
    kk =-1
    step = 100000
    en_dict = {}
    this_seg_ls =[]
    for en in ents_ncs_ls:
        kk +=1        
        en_start=en['start']
        if en_start <= step:
            this_seg_ls.append(en)
        else:
            en_dict[str(step)] = this_seg_ls
            this_seg_ls=[]
            this_seg_ls.append(en)
            step +=100000
        if kk == len(ents_ncs_ls)-1:
            en_dict[str(step)] = this_seg_ls
    print(110, len(list(en_dict.keys())))
    # print(len(en_dict[list(en_dict.keys())[0]]))
    # print(en_dict[list(en_dict.keys())[0]])


    new_sents_pos_ls = []
    step_keys_ls = list(sents_dict.keys())
    mm =-1
    for step in  step_keys_ls:
        mm +=1
        # if mm > 0:
        #     break
        print ('116, running ', mm, 'of', len(step_keys_ls))
        thisseg_sents_pos_ls = sents_dict[step]
        i =-1
        for sent in thisseg_sents_pos_ls:
            i+=1
            print(78, mm, 'sent', i, 'of', len(thisseg_sents_pos_ls))
            sent['sent_text'] = bigtext[sent['start']: sent['end']+1]
            sent['ents_ncs'] =[]

            j=-1
            thisseg_ents_ncs_ls = en_dict[step]
            # tmpdict = {"sent_text": sent_text, 'sent_id_allsubsections': sent['sent_id_allsubsections']}
            for phrase in thisseg_ents_ncs_ls:
                j +=1
                if ((phrase['start'] >= sent['start'] ) & (phrase['start'] <= sent['end']) ) | ((phrase['end'] >= sent['start'] ) & (phrase['end'] <= sent['end'])):
                    if ('warm' in phrase['text']):
                        print(phrase)
                        # x = z+1
                    phrasetext = bigtext[phrase['start']: phrase['end']+1]
                    sent['ents_ncs'].append(phrasetext)
            new_sents_pos_ls.append(sent)
        # now that sent has a new fileds: ['sent_text] and ['ents_ncs']
    # print(132, len(sents_pos_ls))
    # print(138, len(new_sents_pos_ls))
    


    jsonobj = {
        'sources': [
            cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/bigtext_and_sents_pos_in_bigtext_{}.json.gz'.format(nn), 
            cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_cleaned4_nounchunks_bigtext_{}.json.gz'.format(nn)
        ],
        'program': r'C:\Users\syao2\AppData\Local\MyWorks\js\ml_text\python\pyflaskapps\example15_spacytests\pymodules\spacy\tests\test964.py',
        'data': {"bigtext": bigtext, "sents_pos": new_sents_pos_ls}
    }


    targetjsonfile = cwd + tmpoutdir + '/bigtext_and_sents_pos_in_bigtext_and_entsncs_{}.json.gz'.format(nn)
    json_str = json.dumps(jsonobj) # convert to string
    json_bytes = json_str.encode('utf-8') # convert to bytes
    with gzip.open(targetjsonfile, 'w') as f:
        f.write(json_bytes)


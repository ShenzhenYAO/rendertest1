'''
    bigtext_and_sents_pos_in_bigtext_and_entsncs_1 or 2 .json.gz by 964 is like:

    {
        "start": 4588066,
        "end": 4588206,
        "sent_id_allsubsections": 35421,
        "sent_text": "\"Financial Plan for the Years 2022 to 2026 Bylaw, 2022, No. 8918\" Moved by Councillor Bell, seconded by Councillor McIlroyCouncillor Bell, . ",
        "ents_ncs": [
            "Bylaw",
            "2022",
            "8918",
            "Councillor Bell",
            "Councillor",
            "the Years 2022 to 2026 Bylaw",
            "Councillor Bell",
            "Councillor McIlroyCouncillor Bell"
        ]
    }

    sents_of_all_sections_1 or 2.json is made by 961, each sent like like 
        {sent_id_allsubsections: , sent_text:,  mega: {file, date, sectionid, subsectionid...}}

    make bigtext_and_sents_pos_in_bigtext_and_entsncs_1 into a dict like

    35421 (sent_id_allsubsections): { "ents_ncs": [...]}

    then loop for each in sents_of_all_sections_1, look up sent_id_allsubsections, and insert a key  'ents_ncs' ...


'''

import sys, os, json, gzip 

# nlp = spacy.load("en_core_web_sm")
cwd = os.getcwd().replace('\\', '/') # the cwd is the location where python starts, in this case, it is C:\Personal\Virtual_Server\PHPWeb\ml_text\python
# # add the location of the py common module file 
# location_commonmodules = cwd + '/pyflaskapps/common_pymodules'
# sys.path.insert(1, location_commonmodules) # add the location at the top of the sys.path, thus, by default, the py script file spacy_modules will be loaded from there
# from modules_common import * 
# from modules_spacy import * 

tmpdir= '/additional_96x/data/history/'
tmpoutdir  = '/additional_96x/data/history/out/' 


for nn in ["1", "2"]:

    # load the bigtext_and_sents_pos_in_bigtext_and_entsncs_
    location = cwd + tmpoutdir + '/bigtext_and_sents_pos_in_bigtext_and_entsncs_{}.json.gz'.format(nn)
    # print(corpusfilepath)
    with gzip.open(location, 'r') as fin:        
        json_bytes = fin.read()      
    # convert bytes to string
    json_str = json_bytes.decode('utf-8')  
    # convert string to json  
    srcjson = json.loads(json_str)   
    sents_entsncs_ls = srcjson['data']['sents_pos']

    # make a dict like "<sent_id_allsubsections>": [ent1, nc1, ...]
    sents_entsncs_dict ={}
    for x in sents_entsncs_ls:
        sent_id_allsubsections = x['sent_id_allsubsections'] 
        sents_entsncs_dict[str(sent_id_allsubsections)] = x['ents_ncs']  


    # # load the sents_of_all_sections_1 or 2
    location = cwd + tmpdir +  '/sents_of_all_sections_{}.json.gz'.format(nn) #!!!04a
    with gzip.open(location, 'r') as fin:        
        json_bytes = fin.read()      
    # convert bytes to string
    json_str = json_bytes.decode('utf-8')  
    # convert string to json  
    srcjson = json.loads(json_str)   

    sents_of_all_sections_ls = srcjson['data'] # like "sent_text", meta:{}
    print (73, 'number of sents', len(sents_of_all_sections_ls) )
    for x in   sents_of_all_sections_ls:
        sent_id_allsubsections = str(x['sent_id_allsubsections'])
        thissent_ents_ncs_ls = sents_entsncs_dict[sent_id_allsubsections] 
        x['ents_ncs'] = thissent_ents_ncs_ls


    # save it !
    jsonobj = {
        'sources': [
            cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/bigtext_and_sents_pos_in_bigtext_and_entsncs_{}.json.gz'.format(nn), 
            cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/sents_of_all_sections_{}.json.gz'.format(nn)
        ],
        'program': r'C:\Users\syao2\AppData\Local\MyWorks\js\ml_text\python\pyflaskapps\example15_spacytests\pymodules\spacy\tests\test965.py',
        'data': sents_of_all_sections_ls
    }


    targetjsonfile = cwd + tmpoutdir + '/sents_of_all_sections_entsncs_{}.json.gz'.format(nn)
    json_str = json.dumps(jsonobj) # convert to string
    json_bytes = json_str.encode('utf-8') # convert to bytes
    with gzip.open(targetjsonfile, 'w') as f:
        f.write(json_bytes)


    if (nn == "1"):
        sents_of_all_sections_ls_1 = sents_of_all_sections_ls
    elif (nn == "2"):
        sents_of_all_sections_ls_2 = sents_of_all_sections_ls
        sents_of_all_sections_ls_all = sents_of_all_sections_ls_1 + sents_of_all_sections_ls_2
        print(len(sents_of_all_sections_ls_all))

        jsonobj = {
            'sources': [
                cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/bigtext_and_sents_pos_in_bigtext_and_entsncs_1_2.json.gz', 
                cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/sents_of_all_sections_1_2.json.gz'
            ],
            'program': r'C:\Users\syao2\AppData\Local\MyWorks\js\ml_text\python\pyflaskapps\example15_spacytests\pymodules\spacy\tests\test965.py',
            'data': sents_of_all_sections_ls_all
        }


        targetjsonfile = cwd + tmpoutdir + '/sents_of_all_sections_entsncs_all.json.gz'
        json_str = json.dumps(jsonobj) # convert to string
        json_bytes = json_str.encode('utf-8') # convert to bytes
        with gzip.open(targetjsonfile, 'w') as f:
            f.write(json_bytes)


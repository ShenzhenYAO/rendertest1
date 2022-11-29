'''
    sents_of_all_sections_entsncs_all.json.gz from 965 has all ents and ncs from all sentences of all subsections of all text

    sents_with_matched_phrases_of_selected_sections from 954 has theme matched ...

    make a new theme "others", add phrases from ents and ncs if not in phrases matching a lemma

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

# load the sentences with matched phrases
srcfilepath = cwd + tmpdir + '/sents_with_matched_phrases_of_selected_sections.json.gz' # !!!! hisotry of 04a 
# srcfilepath = cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/sents_with_matched_phrases.json.json.gz'
with gzip.open(srcfilepath, 'r') as fin:        # 4. gzip
    json_bytes = fin.read()                     # 3. bytes (i.e. UTF-8)
# convert bytes to string
json_str = json_bytes.decode('utf-8')  
# convert string to json          # 2. string (i.e. JSON)
jsonobj = json.loads(json_str) # like {sent_text:..., meta:{...}, matched_phrases_themes:[phrase:..., themes:p[]]}
sents_match_termphrase_ls = jsonobj['data']

# print (jsonobj['sources'])
# print(31, 'length', len(sents_match_termphrase_ls), sents_match_termphrase_ls[0])


# load all sentences may have ents ncs ...
srcfilepath = cwd + tmpoutdir + '/sents_of_all_sections_entsncs_all.json.gz'
# srcfilepath = cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/sents_with_matched_phrases.json.json.gz'
with gzip.open(srcfilepath, 'r') as fin:        # 4. gzip
    json_bytes = fin.read()                     # 3. bytes (i.e. UTF-8)
# convert bytes to string
json_str = json_bytes.decode('utf-8')  
# convert string to json          # 2. string (i.e. JSON)
jsonobj = json.loads(json_str) # like {sent_text:..., meta:{...}, matched_phrases_themes:[phrase:..., themes:p[]]}
sents_all_with_entsncs_ls = jsonobj['data']

# print(45, 'length ', len(sents_all_with_entsncs_ls), sents_all_with_entsncs_ls[0])

# test: for each sent in sents_match_termphrase_ls (it does not have a sent id!), can it be found in sents_all_with_entsncs_ls?

# make sents_all_with_entsncs_ls into a dict
sents_all_with_entsncs_dict={}

subsections_dict= {}
for x in sents_all_with_entsncs_ls:
    keystr = x['meta']['city']+ '|' +x['meta']['date']+ '|' +x['meta']['file']+ '|' + str(x['meta']['sectionid'])+ '|' + str(x['meta']['subsectionid'])
    try:
        subsections_dict[keystr].append(x)
    except:
        subsections_dict[keystr] = [x]
# print (subsections_dict[keystr])

# check if each sent in sents_match_termphrase_ls can be found in sents_all_with_entsncs_ls,if so add the sent_id_allsubsections to the sent in sents_match_termphrase_ls
i=-1
for x in sents_match_termphrase_ls:
    i +=1
    keystr = x['meta']['city']+ '|' +x['meta']['date']+ '|' +x['meta']['file']+ '|' + str(x['meta']['sectionid'])+ '|' + str(x['meta']['subsectionid'])
    senttext_matched  = x['sent_text']
    try:
        dict_thissubsection_ls = subsections_dict[keystr]
        sents_thissubsection_ls=[]
        for y in dict_thissubsection_ls:
            sents_thissubsection_ls.append(y['sent_text'])
        # if (i==0):
        #     print('72, senttext_matched', senttext_matched)
        #     print('73, sents_thissubsection', sents_thissubsection_ls)
        #     print (senttext_matched in sents_thissubsection_ls)
        for z in sents_thissubsection_ls:
            if senttext_matched == z:
                x['sent_id_allsubsections'] = y['sent_id_allsubsections']
    except:
        print('subsection not found')
    
# make a dict of sents_match_termphrase_ls, sent_id_allsubsections as key
sents_match_termphrase_dict ={}
for x in  sents_match_termphrase_ls:
    key = str(x['sent_id_allsubsections'])
    sents_match_termphrase_dict[key] = x

# print(87, sents_match_termphrase_dict[key])

# now, for each sent in sents_all_with_entsncs_ls, add a field 
for x in sents_all_with_entsncs_ls:
    key2 = str(x['sent_id_allsubsections'])
    # if (key2 == key):
        # print (x)
    try:
        matched_phrases_themes = sents_match_termphrase_dict[key2]['matched_phrases_themes']
        x['matched_phrases_themes'] = matched_phrases_themes
    except:
        x['matched_phrases_themes'] =[]

    '''
    "matched_phrases_themes": [
        {
            "phrase": "childcare",
            "themes": [
                "economy",
                "employment",
                "healthcare",
                "poverty",
                "vulnerability",
                "youth_children"
            ]
        }
    ],
    '''
    # for each in matched_phrases_themes, move it to a new property: new_phrase_themes
    x['new_phrase_themes'] = []
    matched_phrases_ls =[]
    for y in x['matched_phrases_themes']:
        # print(118, y)
        tmpdict={}
        tmpdict['phrase'] = y['phrase']
        matched_phrases_ls.append(y['phrase'])
        tmpdict['themes'] =[]
        for z in y['themes']:
            if z in ['harm_reduction', 'youth_children', 'mental_health', 'housing']:
                tmpdict['themes'].append(z)
        if len(tmpdict['themes']) == 0:
            tmpdict['themes'] = ['others']
            # print(131, tmpdict)
        x['new_phrase_themes'].append(tmpdict)

    for y in x['ents_ncs']: # y is a phrase string
        thistext = y.replace("196808240800123456", "")
        thistext = thistext.strip()
        if (thistext not in matched_phrases_ls) & (len(thistext) > 1):
            matched_phrases_ls.append(thistext)
            x['new_phrase_themes'].append({"phrase":thistext, "themes":['others']})

    # if key2 == "37712":
    #     print (x)

# now sents_all_with_entsncs_ls includes matched_phrases_themes
jsonobj = {
    'sources': [
        cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/sents_with_matched_phrases_of_selected_sections.json.gz', 
        cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/sents_of_all_sections_entsncs_all.json.gz'
    ],
    'program': r'C:\Users\syao2\AppData\Local\MyWorks\js\ml_text\python\pyflaskapps\example15_spacytests\pymodules\spacy\tests\test966.py',
    'data': sents_all_with_entsncs_ls
}


targetjsonfile = cwd + tmpoutdir +  '/allsents_same_structure_as_with_matched_phrases_of_selected_sections.json.gz'
json_str = json.dumps(jsonobj) # convert to string
json_bytes = json_str.encode('utf-8') # convert to bytes
with gzip.open(targetjsonfile, 'w') as f:
    f.write(json_bytes)


# 962d remove those having a lemma in selected themes... 
#  Note: it takes about 20 mins to get the results

import sys, os, json, gzip , re, spacy

import spacy
nlp = spacy.load("en_core_web_sm")


cwd = os.getcwd().replace('\\', '/') # the cwd is the location where python starts, in this case, it is C:\Personal\Virtual_Server\PHPWeb\ml_text\python
# add the location of the py common module file 
# location_commonmodules = cwd + '/pyflaskapps/common_pymodules'
# sys.path.insert(1, location_commonmodules) # add the location at the top of the sys.path, thus, by default, the py script file spacy_modules will be loaded from there
# from modules_common import * 
# from modules_spacy import * 

tmpdir= '/additional_96x/data/history/'
tmpoutdir  = '/additional_96x/data/history/out/' 


import spacy
nlp = spacy.load("en_core_web_sm")

# load the themes and the themes_dict
# selected_themes_file = cwd + tmpoutdir + "/selected_themes.json"
# openedfile0 = open(selected_themes_file, encoding="UTF-8")
# selected_themes_dict = json.load(openedfile0) 
# selected_themes_ls = selected_themes_dict['data']['selected_themes']
selected_themes_ls = ["harm_reduction",            "housing",            "mental_health",            "youth_children"]

# load theme-specific phrases, and selected themes
themes_phrasesfile = cwd + tmpdir + "/themes_linked_lemmas_phrases.json"  # 09
openedfile0 = open(themes_phrasesfile, encoding="UTF-8")
matched_phrases_by_themes_dict = json.load(openedfile0) 
phrases_themes_dict = matched_phrases_by_themes_dict['data']['themes_lemmas_phrases']
# like theme1: {lemmas:[...], phrases:[...]}

# make a list of lemmas of the selected theme
lemmas_selected_themes_dict ={}
lemmas_selected_themes_ls=[]
for x in selected_themes_ls:
    lemmas_selected_themes_dict[x] = phrases_themes_dict[x]['lemmas']
    for y in phrases_themes_dict[x]['lemmas']:
        if y not in lemmas_selected_themes_ls:
            lemmas_selected_themes_ls.append(y)
# print(lemmas_selected_themes_dict)
# print(lemmas_selected_themes_ls)

# read the bigtext gz
def clean4_get_ents_ncs():
    labels_exclude_ls =['ORG', 'DATE', 'TIME', 'GPE', 'PERSON',  'EVENT',  'CARDINAL', 'LAW', 'LOC', 'WORK_OF_ART', 'ORDINAL', 'PERCENT', 'MONEY', 'NORP', 'QUANTITY', 'LANGUAGE']
    general_words_ls = []

    for nn in ["1", "2"]:
        gzlocation = cwd  + tmpoutdir + '/entities_cleaned3_nounchunks_bigtext_{}.json.gz'.format(nn)
        # print(corpusfilepath)
        with gzip.open(gzlocation, 'r') as fin:        
            json_bytes = fin.read()      
        # convert bytes to string
        json_str = json_bytes.decode('utf-8')  
        # convert string to json  
        srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
        ents_ncs_ls = srcjson['data']
        # get all labels
        
# ent include place address
# ent like person name
# token is number url
# text include number
# text like road avenue street mayor

        new_ents_ncs_ls =[]
        i=-1
        for x in ents_ncs_ls:
            i+=1
            print (55, i, 'of', len(ents_ncs_ls), len(new_ents_ncs_ls))
            text = x['text']
            doc = nlp(text)
            has_lemma_of_selected_theme=0
            # # exclude if having general words
            # for s in general_words_ls:
            #     if s in text.lower():
            #         has_lemma_of_selected_theme=1
            #         break
            for s in ['(', ')', 'p.o.box', 'https://', 're:', 
                    'april', 'file', 
                    'amend', 'appoint', 
                    'authentication', 
                    'certified',  'creek', 
                    'foundation', 'further', 'garden', 
                    'inc.', 'boulevard', 'breif', 'manager', 'census'

                 ]:
                if s in text.lower():
                    has_lemma_of_selected_theme=1
                    break
            if has_lemma_of_selected_theme == 1:
                continue
            # exclude if having road, street, avenue
            for s in ['road', 'street', 'avenue',  'drive', 'highway', 'facilities', 'creek', 'foundation', 'further', 'garden', 'inc.', 'crossing', 'a city', 'lake', 'canal', 'cheakamus', 'ava neve', 'quay', 'bay']:
                if s in text.lower():
                    has_lemma_of_selected_theme=1
                    break
            if has_lemma_of_selected_theme == 1:
                continue
            # exclude if having meeting related strings
            for s in ['council', 'plan', 'bylaw', 'zoning', 'report', 'file', 'chief', 'hall',  'session','section', 'policy', 'appropriation', 'procedure', 'lane', 'pave', 'lot', 'follow-up', 'motion', 'offering', 'notice', 'hearing', 'meeting', 'act', 'director', 'officer', 'agenda', 'supervisor', 'appendi', 'mayor', 'moved', 'unanimously', 'carried', 'opposed']:
                if s in text.lower():
                    has_lemma_of_selected_theme=1
                    break
            if has_lemma_of_selected_theme == 1:
                continue
            # exclude if having a number
            has_numbers = re.findall(r'\d', text.lower())
            if len(has_numbers) >0:
                has_lemma_of_selected_theme=1
                continue
            for y in lemmas_selected_themes_ls:
                if y in text.lower():
                    has_lemma_of_selected_theme =1
                    break
            if has_lemma_of_selected_theme == 1:
                continue
            for token in doc:
                lemma = token.lemma_.lower()
                if lemma in lemmas_selected_themes_ls:
                    has_lemma_of_selected_theme =1
                    break
                if ('hous' in text.lower()):
                    has_lemma_of_selected_theme =1
                    break
                if ('mental' in text.lower()):
                    has_lemma_of_selected_theme =1
                    break
                if ('youth' in text.lower()):
                    has_lemma_of_selected_theme =1
                    break
                if ('overdose' in text.lower()):
                    has_lemma_of_selected_theme =1
                    break
            for ent in doc.ents:
                if ent.label_ in labels_exclude_ls:
                    has_lemma_of_selected_theme =1
                    break 
            if has_lemma_of_selected_theme == 0:
                new_ents_ncs_ls.append(x)

        print(len(ents_ncs_ls), len(new_ents_ncs_ls))

        # save ents_ncs 
        jsonobj = {
            'sources': [
                cwd + "/pyflaskapps/data/output/new_policyanalysis/07_themes/selected_themes.json",
                cwd + "/pyflaskapps/data/output/new_policyanalysis/09_evaluate_phrases/themes_linked_lemmas_phrases.json",
                cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_cleaned3_nounchunks_bigtext_{}.json.gz'.format(nn),
            ],
            "description": "cleaned by excluding entities that has a lemma matching the selecte theme (these are identified phrases)",
            'program': r'C:\Users\syao2\AppData\Local\MyWorks\js\ml_text\python\pyflaskapps\example15_spacytests\pymodules\spacy\tests\test962d.py',
            'data': new_ents_ncs_ls
        }

        # save all entites and noun chunks
        targetjsonfile = cwd +  tmpoutdir + '/entities_cleaned4_nounchunks_bigtext_{}.json.gz'.format(nn)
        json_str = json.dumps(jsonobj) # convert to string
        json_bytes = json_str.encode('utf-8') # convert to bytes
        with gzip.open(targetjsonfile, 'w') as f:
            f.write(json_bytes)
        
clean4_get_ents_ncs()





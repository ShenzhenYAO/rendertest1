# read and combine subsection_text json files
def makerootlemmas01_combine_subsection_text_jsonfiles(files_ls):
    import json
    subsectiontext_ls =[]
    for thisfile in files_ls:
        openedfile = open(thisfile, encoding="UTF-8")
        subsectiontext_ls += json.load(openedfile)
    return subsectiontext_ls
######################################################################

def makerootlemmas02_combine_text_from_subsections(subsectiontext_ls):
    text=""
    for dict in subsectiontext_ls:
        text +=dict['text']
    return text
#######################################################################

def clean_text_rendertest1(text):
    import textacy.preprocessing 
    preproc = textacy.preprocessing.make_pipeline(
        textacy.preprocessing.normalize.unicode, # does not seem to work, cannot remove é \t \u2022 \u0027 ...
        textacy.preprocessing.normalize.quotation_marks, # convert ʼ to '
        textacy.preprocessing.normalize.whitespace, # replace non-break spaces/zero with spaces with a normal space, strip leading/trailing spaces
        textacy.preprocessing.normalize.bullet_points, # replace special bullet points like \u2022(•) with '-'
        textacy.preprocessing.normalize.hyphenated_words, # remove hyphens split the word into segments different lines like Shakes- peare without affecting the hyphens in a normal setting like semi_conductor
    )
    cleanedtext = preproc(text)
    cleanedtext = textacy.preprocessing.normalize.repeating_chars(cleanedtext, chars="*", maxn=0)
    cleanedtext = textacy.preprocessing.normalize.repeating_chars(cleanedtext, chars=",")
    cleanedtext = textacy.preprocessing.normalize.repeating_chars(cleanedtext, chars=".")
    cleanedtext = textacy.preprocessing.normalize.repeating_chars(cleanedtext, chars="\n")
    cleanedtext = textacy.preprocessing.replace.emails(cleanedtext, repl="")
    cleanedtext = textacy.preprocessing.replace.urls(cleanedtext, repl="")
    cleanedtext = textacy.preprocessing.replace.phone_numbers(cleanedtext, repl="")
    cleanedtext = textacy.preprocessing.replace.user_handles(cleanedtext, repl="")
    cleanedtext = textacy.preprocessing.remove.accents(cleanedtext)
    # self defined modules (in modules_common)
    cleanedtext = remove_unicode_chars(cleanedtext)
    cleanedtext = replace_multi_space_by_one(cleanedtext)
    cleanedtext= cleanedtext.replace("\"", "")
    return cleanedtext
###############################################################

def get_ents_ncs(text):
    import spacy
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
    ents_ls=[]
    ncs_ls=[]
    for ent in doc.ents:
        x=ent.text.replace('\n', ' ').strip()
        x=replace_multi_space_by_one(x)
        ents_ls.append(x)
    for nc in doc.noun_chunks:
        x=nc.text.replace('\n', ' ').strip()
        x=replace_multi_space_by_one(x)
        ncs_ls.append(x)
    # print(48, len(ncs_ls))
    return [ents_ls, ncs_ls]
###############################################################

# make rootlemmas from phrases 
# 1. # remove non-ASCII characters
# 2. skip phrases with & and % (these are like percentage or url)
# 3. remove phrases if only with digits, punctuations, or < 2 chars 
# 4. remove digits and punctuations and strip
# 5. exclude the entities from the phrase if the entity label is person, date, time, cardinal, ordinal, percent, money, quantity
# 6. skip agian if the phrase is only digits and punctuations (after removing the above),or only a single letter is left
# 7. only keep tokes of noun or propn
# 8 only keep root tokens with length > 1 after removing digits and punctuations  
# 9. exclude if it is like URL, or a number, or not ascii...
#   "is_space", "is_bracket", "is_quote", "is_currentcy", "like_url", "like_num", "like_email", 'is_stop',  "is_ascii", "is_digit", "is_punct",                         
def makerootlemmas03_rootlemmas_from_phrases(phrases_ls): # it is similar to what is in test12.py
    
    import re, spacy
    # nlp = spacy.load("en_core_web_sm") # load the nlp class
    nlp = spacy.load("en_core_web_lg") # although bigger, it contains many features (like token.vector) that are not provided (or of a wrong verion) by the _sm lib

    # for each phrase, find the root and append its lemma into the rootlemmas list
    rootlemmas_ls =[]
    labels_ls =[]
    ent_labels_ls= []
    exclude_labels_ls = ["PERSON", "DATE", "TIME", "CARDINAL", "ORDINAL","PERCENT","MONEY", "QUANTITY"]

    for phrase in phrases_ls:

        # 1. remove non-ASCII characters
        string_encode = phrase.encode("ascii", "ignore")
        phrase= string_encode.decode()
        # print('phrase after removing non ASCII ===', phrase)

        # 2. skip phrases with & and % (these are like percentage or url)
        if ("&" in phrase) | ("%" in phrase) :
            continue # skip the phrase, these are like part of a url

        # 3. remove phrases if only with digits, punctuations, or < 2 chars
        # skip if the phrase is only digits and punctuations,or only a single letter is left
        phrase1 = re.sub(r'[^\w\s]', '', phrase) # remove chars if not a word or a whitespace
        phrase1 = re.sub(r'\d+', '', phrase1).strip() # remove digits
        phrase1 = re.sub(r'|', '', phrase1).strip() # remove |
        # print('phrase after removing non ASCII ===', phrase1)
        if len(phrase1) < 2:
            # print('===', phrase, phrase1)
            continue # skip the phrase
        else:
            # 4. remove digits and punctuations and strip
            phrase2 = re.sub(r'\d+', '', phrase).strip() # remove digits
            phrase2 = re.sub(r'[,.;@#?!&$/]+', ' ', phrase2).strip() # remove digits
            doc = nlp(phrase2)
            try:
                for ent in doc.ents:
                    # print('ent ===', ent.text, ent.label_)
                    # make a list of unique ent lables
                    if ent.label_ not in labels_ls: # labels_ls is a tmp list for checking whether the ent.label_ has encountered previously
                        # print(ent.label_)
                        # print(spacy.explain(ent.label_))
                        labels_ls.append(ent.label_)
                        str = doc.text + "||" + ent.text + "||" + ent.label_ + "||" + spacy.explain(ent.label_)
                        # print(str)
                        ent_labels_ls.append(str)
                    # 5. exclude the entities from the phrase if the entity label is person, date, time, cardinal, ordinal, percent, money, quantity
                    if ent.label_ in exclude_labels_ls:
                        phrase=phrase.replace(ent.text, "")
                        if len(phrase.strip()) == 0:
                            doc = nlp(phrase)
                            break # stop the loop of ent in doc.ents, move to the next phrase
                        else:
                            # 6. skip if the phrase is only digits and punctuations,or only a single letter is left
                            # note check again after removing entities like dates, etc.
                            phrase1 = re.sub(r'[^\w\s]', '', phrase) # remove chars if not a word or a whitespace
                            phrase1 = re.sub(r'\d+', '', phrase1).strip() # remove digits
                            if len(phrase1) < 2:
                                phrase=""
                                doc = nlp(phrase)
                                break
                            doc=nlp(phrase.strip())
                    else:
                        pass
            except:
                pass            
            
            # print('phrase is ===', phrase)
            for token in nlp(phrase):
                try:
                    pos = token.pos_
                    # 7. only keep tokes of noun or propn
                    if pos not in ['NOUN', 'PROPN', 'X']:
                        continue #('skip the current token')
                    # elif pos not in pos_ls:
                    #     pos_ls.append(pos)
                except:
                    pass
                try:
                    lemma=token.lemma_.lower()
                    lemma2 =  re.sub(r'\d+', '', lemma).strip() # remove digits
                    lemma2 = re.sub(r'[-,.;@#?!&$/]+', '', lemma2).strip() # remove punctuations
                    # print('token.lemma ===', lemma)
                    # 8. only keep root tokens with length > 1 after removing digits and punctuations       
                    if (token.dep_ == 'ROOT') and (lemma2 not in rootlemmas_ls) and (len(lemma2) > 1):
                        # print('root lemma ===', lemma)                
                        # 9. exclude if it is like URL, or a number, or not ascii...
                        # "is_space", "is_bracket", "is_quote", "is_currentcy", "like_url", "like_num", "like_email", 'is_stop',  "is_ascii", "is_digit", "is_punct",
                        try:
                            if (token.is_space == True):
                                break
                        except:
                            pass
                        try:
                            if (token.is_bracket == True):
                                break
                        except:
                            pass
                        try:
                            if (token.is_quote == True):
                                break
                        except:
                            pass
                        try:
                            if (token.is_currentcy == True):
                                break
                        except:
                            pass
                        try:
                            if (token.like_url == True):
                                break
                        except:
                            pass
                        try:
                            if (token.like_num == True):
                                break
                        except:
                            pass
                        try:
                            if (token.like_email == True):
                                break
                        except:
                            pass
                        try:
                            if (token.is_stop == True):
                                break
                        except:
                            pass
                        try:
                            if (token.is_ascii == False):
                                break
                        except:
                            pass
                        try:
                            if (token.is_digit == True):
                                break
                        except:
                            pass
                        try:
                            if (token.is_punct == True):
                                break
                        except:
                            pass
                        rootlemmas_ls.append(lemma2)
                        break
                except:
                    pass
    rootlemmas_ls.sort()  # not  rootlemmas_ls= rootlemmas_ls.sort()
    return rootlemmas_ls
#####################################################################################

# this is to create themes for the first time, according to the file /pyflaskapps/data/output/lemma_classification/classified_lemmas.json
# which was created by test301.py from C:\Personal\Virtual_Server\PHPWeb\ml_text\python\pyflaskapps\data\output\lemma_classification\labelled_lemmas.txt
# which was manually copied from the file C:\Personal\Virtual_Server\PHPWeb\ml_text\python\pyflaskapps\data\output\lemma_classification\labelled_lemmas.xlsm
# which manually consolidates the themes_dict sheets (linking themes and rootlemmas by Josh Amina and Shenzhen) 
def init_themes(srcfile):
    import json
    openedfile = open(srcfile, encoding="UTF-8")
    lemmas_themes_ls = json.load(openedfile)
    themes_ls =[]
    for x in lemmas_themes_ls:
        if x['theme'] not in themes_ls:
            themes_ls.append(x['theme'])
    themes_ls.sort()
    return themes_ls
#################################

# initiate selected themes
def init_selected_themes(srcfile):
    import json
    openedfile = open(srcfile, encoding="UTF-8")
    selected_themes_ls = json.load(openedfile)
    selected_themes_ls.sort()
    return selected_themes_ls
#########################################

# to create the reviewed rootlemmas for the first time
def init_evaluated_rootlemmas(srcrootlemmasfile, srcthemesfile):
    evaluated_rootlemmas_ls=[]
    import json
    openedfile = open(srcrootlemmasfile, encoding="UTF-8")
    rootlemms_ls = json.load(openedfile)['data']['rootlemmas']
    openedfile = open(srcthemesfile, encoding="UTF-8")
    themes_ls = json.load(openedfile)['data']['themes']
    for x in rootlemms_ls:
        evaluated_rootlemmas_ls.append({'rootlemma':x, "evaluated_themes":themes_ls})
    return evaluated_rootlemmas_ls
###############################################################

# init unevaluated rootlemmas
def init_unevaluated_rootlemmas(newrootlemmasfile, evaluated_rootlemmasfile):
    import json
    unevaluated_rootlemmas_ls=[]
    openedfile = open(newrootlemmasfile, encoding="UTF-8")
    newrootlemms_ls = json.load(openedfile)['data']['rootlemmas']

    openedfile = open(evaluated_rootlemmasfile, encoding="UTF-8")
    evaluated_ls = json.load(openedfile)['data']['evaluated_rootlemmas']
    # make a list of evaluated lemmas
    evaluated_rootlemmas_ls = []
    for x in evaluated_ls:
        rootlemma= x['rootlemma']
        if (rootlemma not in evaluated_rootlemmas_ls ):
            evaluated_rootlemmas_ls.append(rootlemma)

    # append new rootlemma to unevaluated_rootlemmas_ls
    for newrootlemma in newrootlemms_ls:
        if (newrootlemma not in evaluated_rootlemmas_ls) & (newrootlemma not in unevaluated_rootlemmas_ls):
            unevaluated_rootlemmas_ls.append(newrootlemma)
    
    unevaluated_rootlemmas_ls.sort()
    return unevaluated_rootlemmas_ls
##################################################################

# copy the themes_linked_rootlemmas.json
def copy_themes_linked_rootlemmas(srcfile):
    import json
    openedfile = open(srcfile, encoding="UTF-8")
    themes_linked_rootlemmas_ls = json.load(openedfile)
    return themes_linked_rootlemmas_ls
###########################################################

# update rootlemmas that have been evaluted, but not linked to a specific theme
def update_evaluated_nolink_rootlemmas(evaluated_rootlemmasfiles, themes_linked_rootlemmasfile):
    import json
    openedfile = open(evaluated_rootlemmasfiles, encoding="UTF-8")
    evaluated_rootlemmas_ls = json.load(openedfile)['data']['evaluated_rootlemmas']

    openedfile = open(themes_linked_rootlemmasfile, encoding="UTF-8")
    themes_linked_rootlemmas_dict = json.load(openedfile)['data']['themes_linked_rootlemmas']

    linke_rootlemmas_ls = list(themes_linked_rootlemmas_dict.keys()) # have a list of rootlemmas (keys) that have at least one linked theme
    
    evaluated_nolink_rootlemmas_ls=[]
    for x in evaluated_rootlemmas_ls: # x like rootlemma:[theme1, theme2...]
        if x['rootlemma'] not in linke_rootlemmas_ls:
            evaluated_nolink_rootlemmas_ls.append(x) 
    return evaluated_nolink_rootlemmas_ls
#########################################################################

# update '/pyflaskapps/data/output/policyanalysis/labels/01_lemma_themes_dict.json'
# the idea is to make changes in the 01_lemma_themes_dict.json, and the following change are according to 01_lemma_themes_dict.json
# such to be consistent with the existing flow
def update_01_lemma_themes_dict(requestedchange_dict, lemma_themes_dictfile):
    import json
    openedfile = open(lemma_themes_dictfile, encoding="UTF-8")
    lemmas_themes_dict = json.load(openedfile) # like {'house': ['housing', '...']}

    themes_ls = list(requestedchange_dict.keys())
    for theme in themes_ls:
        #get the words indeed are lemmas
        try:
            toadd_lemmas_ls = requestedchange_dict[theme]['words']['add']
        except:
            toadd_lemmas_ls = []
        for lemma in toadd_lemmas_ls:
            try: 
                if theme not in lemmas_themes_dict[lemma]:
                    lemmas_themes_dict[lemma].append(theme) # add the current theme into the linked themes
            except:
                lemmas_themes_dict[lemma]= [theme] # if the lemma is not in lemmas_themes_dict, add as a new key, and add the current linked theme as a new

        try:
            toremove_lemmas_ls = requestedchange_dict[theme]['words']['remove']
        except:
            toremove_lemmas_ls = []
        for lemma in toremove_lemmas_ls:
            try:
                if theme in lemmas_themes_dict[lemma]:
                    lemmas_themes_dict[lemma].remove(theme) # remove, or delete, or pop
            except:
                print(272, 'the lemma "'+ lemma + '" cannot be found in the lemmas_themes_dict' )
                pass
        
    # save  lemma_themes_dictfile:
    with open(lemma_themes_dictfile, 'w') as f:
        json.dump(lemmas_themes_dict, f)  
########################################################################################################

# for rootlemmas in the themes_linked_rootlemmas.json, add them into the evaluated_rootlemmas.json (consider all themes are evaluated, thus also need to read the existing themes)
def update_evaluated_rootlemmas(themes_linked_rootlemmasfile, evaluated_rootlemmasfile, themesfile):
    import json
    openedfile = open(themes_linked_rootlemmasfile, encoding="UTF-8")
    themes_linked_rootlemmas_dict = json.load(openedfile)['data']['themes_linked_rootlemmas']
    themes_linked_rootlemmas_ls = list(themes_linked_rootlemmas_dict.keys()) # get a list of rootlemmas that has been linked to themes (in which some are newly added in the above step)

    # open the existing evaluated_rootlemmas.json
    openedfile = open(evaluated_rootlemmasfile, encoding="UTF-8")
    evaluated_rootlemmas_json = json.load(openedfile)
    evaluated_rootlemmas_ls = evaluated_rootlemmas_json['data']['evaluated_rootlemmas'] # like [{"rootlemma":.., "evaluated_themes":[]}, {...}]
    description_old = evaluated_rootlemmas_json['meta']['description']
    description_new = """
    This is based on changes in '/pyflaskapps/data/output/new_policyanalysis/08_evaluate_rootlemmas_themes/themes_linked_rootlemmas.json' (after defining new theme-rootlemma links).
    This file is updated by update_evaluated_rootlemmas() in 'python/pyflaskapps/common_pymodules/modules_common.py'. 
    """
    if description_new not in description_old:
        evaluated_rootlemmas_json['meta']['description'] = description_old + description_new
    evaluated_lemmas_ls =[] # a list of revaluated lemmas (evaluated_rootlemmas_ls is a list of dicts, each like {"rootlemma":.., "evaluated_themes":[]})
    for x in evaluated_rootlemmas_ls:
        evaluated_lemmas_ls.append(x['rootlemma'])

    openedfile = open(themesfile, encoding="UTF-8")
    evaluated_themes_ls = json.load(openedfile)['data']['themes']
    
    # add the new linked rootlemmas into evaluated_rootlemmas_ls
    for linked_rootlemma in themes_linked_rootlemmas_ls:
        if linked_rootlemma not in evaluated_lemmas_ls:
            evaluated_rootlemmas_ls.append({'rootlemma':linked_rootlemma, "evaluated_themes": evaluated_themes_ls }) # consider all existing themes are evaluated
    
    evaluated_rootlemmas_json['data']['evaluated_rootlemmas'] = evaluated_rootlemmas_ls

    with open(evaluated_rootlemmasfile, 'w') as f:
        json.dump(evaluated_rootlemmas_json, f)
#############################################################################

# to remove the rootlemmas in the requested data from the unevaluated_rootlemmas.json
def update_unevaluated_rootlemmas(unevaluated_rootlemmasfile, evaluated_rootlemmasfile):
    import json
    openedfile = open(unevaluated_rootlemmasfile, encoding="UTF-8")
    unevaluated_rootlemmas_json = json.load(openedfile)
    unevaluated_rootlemmas_ls = unevaluated_rootlemmas_json['data']['unevaluated_rootlemmas']
    
    openedfile = open(evaluated_rootlemmasfile, encoding="UTF-8")
    evaluated_rootlemmas_ls = json.load(openedfile)['data']['evaluated_rootlemmas']

    for x in evaluated_rootlemmas_ls:
        if x['rootlemma'] in unevaluated_rootlemmas_ls:
            unevaluated_rootlemmas_ls.remove(x['rootlemma'])
    
    description_old = unevaluated_rootlemmas_json['meta']['description']
    description_new = """
    update based on changes in '/pyflaskapps/data/output/new_policyanalysis/08_evaluate_rootlemmas_themes/evaluated_rootlemmas.json',
    in which new rootlemmas have been added. 
    Consequently, the newly evaluated rootlemmas are removed from this file by update_unevaluated_rootlemmas() in 'python/pyflaskapps/common_pymodules/modules_common.py'.
    """
    if description_new not in description_old:
        unevaluated_rootlemmas_json['meta']['description'] = description_old + description_new
    unevaluated_rootlemmas_json['data']['rootlemmas'] = unevaluated_rootlemmas_ls

    with open(unevaluated_rootlemmasfile, 'w') as f:
        json.dump(unevaluated_rootlemmas_json, f)
########################################################################

# add the newly added rootlemmas to existing_02_themes_lemmas_phrases_changingfile = cwd + '/pyflaskapps/data/output/policyanalysis/labels/02_themes_lemmas_phrases_changing.json'
# according to lemmas in themes_linked_rootlemmas.json 
def update_lemmas_in_02_themes_lemmas_phrases_changing(existing_02_themes_lemmas_phrases_changingfile, themes_linked_rootlemmasfile):
    import json
    openedfile = open(existing_02_themes_lemmas_phrases_changingfile, encoding="UTF-8")
    themes_lemmas_phrases_dict = json.load(openedfile)

    openedfile = open(themes_linked_rootlemmasfile, encoding="UTF-8")
    themes_linked_rootlemmas_dict = json.load(openedfile)['data']['themes_linked_rootlemmas']
    lemmas_ls = list(themes_linked_rootlemmas_dict.keys())
    for lemma in lemmas_ls:
        themes_ls = themes_linked_rootlemmas_dict[lemma]
        for theme in themes_ls:
            themes_lemmas_ls = themes_lemmas_phrases_dict[theme]['lemmas']
            if lemma not in themes_lemmas_ls:
                themes_lemmas_phrases_dict[theme]['lemmas'].append(lemma)

    with open(existing_02_themes_lemmas_phrases_changingfile, 'w') as f:
        json.dump(themes_lemmas_phrases_dict, f)  
################################################################################

# copy and make themes_linked_lemmas_phrases.json from the existing themes_lemmas_phrases '/pyflaskapps/data/output/policyanalysis/labels/02_themes_lemmas_phrases_changing.json'
def copy_original_themes_lemmas_phrases(original_themes_lemmas_phrasesfile, target_themes_lemmas_phrases):
    import json
    openedfile = open(original_themes_lemmas_phrasesfile, encoding="UTF-8")
    themes_lemmas_phrases_dict = json.load(openedfile)
    return themes_lemmas_phrases_dict
##########################################################################################

# get matched phrases ( those of the same verbatim_pattern, lemma_pattern, or pos_pattern and containing at least one theme-linned lemma)
def get_theme_related_phrases_from_newtext(text, existing_themes_lemmas_phrasesfile):
    import os,sys, json
    cwd = os.getcwd().replace('\\', '/')
    # add the location of the py common module file 
    location_commonmodules = cwd + '/pyflaskapps/common_pymodules'
    sys.path.insert(1, location_commonmodules)
    from modules_spacy import get_matched_spans

    openedfile = open(existing_themes_lemmas_phrasesfile, encoding="UTF-8")
    existing_themes_lemmas_dict = json.load(openedfile)['data']['themes_lemmas_phrases']
    
    # get all phrases in existing_themes_lemmas_dict regardless of theme category
    interested_phrases_ls =[]
    themes_ls = list(existing_themes_lemmas_dict.keys())
    for theme in themes_ls:
        phrases_ls = existing_themes_lemmas_dict[theme]['phrases']
        for phrase in phrases_ls:
            if phrase.strip() not in interested_phrases_ls:
                interested_phrases_ls.append(phrase.strip())
        lemmas_ls = existing_themes_lemmas_dict[theme]['lemmas']
        for lemma in lemmas_ls:
            if lemma not in interested_phrases_ls:
                interested_phrases_ls.append(lemma)

    phrasespans_ls = get_matched_spans(text, interested_phrases_ls, include_pos_pattern=True) # get_matched_spans in modules_spacy. Note: phrasesspan in that list are spacy spans (i.e., has token, and lemma info)
    print(76, 'number of phrasespans', len(phrasespans_ls))

    # assign phrases by theme (at least one of the phrase lemma is a theme-linked lemma)
    new_theme_phrases_dict = {} # like {theme1:{phrases:[]}, theme2:{...}}
    for theme in themes_ls:
        new_theme_phrases_dict[theme]={}
        new_theme_phrases_dict[theme]['phrases'] =[]
        lemmas_thistheme_ls = existing_themes_lemmas_dict[theme]['lemmas']
        for phrasespan in phrasespans_ls:
            phrasetext = phrasespan.text.strip()
            for token in phrasespan:
                if token.lemma_ in lemmas_thistheme_ls:
                    if phrasetext not in new_theme_phrases_dict[theme]['phrases']:
                        new_theme_phrases_dict[theme]['phrases'].append(phrasetext)
                        break # skip the rest tokens and go to the next phrasespan
        print(80, 'new phrases of the theme "'+ theme + '":', len(new_theme_phrases_dict[theme]['phrases']) )
    return new_theme_phrases_dict
##########################################################################################


## it is from both '/pyflaskapps/data/output/new_policyanalysis/09_evaluate_phrases/unevaluated_phrases.json', and '/pyflaskapps/data/output/new_policyanalysis/09_evaluate_phrases/themes_linked_lemmas_phrases.json'
def merge_phrases_to_evaluate(unevaluated_phrasesfile, existing_themes_lemmas_phrasesfile):
    import json

    openedfile = open(existing_themes_lemmas_phrasesfile, encoding="UTF-8")
    existing_themes_lemmas_dict = json.load(openedfile)['data']['themes_lemmas_phrases']

    openedfile = open(unevaluated_phrasesfile, encoding="UTF-8")
    unevaluated_phrases_dict = json.load(openedfile)['data']['unevaluated_phrases']

    merged_themes_phrases_dict ={}

    themes_ls = list(existing_themes_lemmas_dict.keys())

    for theme in themes_ls:
        merged_themes_phrases_dict[theme] ={}
        merged_themes_phrases_dict[theme]['phrases'] = existing_themes_lemmas_dict[theme]['phrases']
        try:
            newphrases_ls = unevaluated_phrases_dict[theme]['phrases']
        except:
            newphrases_ls =[]
        for phrase in newphrases_ls:
            if phrase not in merged_themes_phrases_dict[theme]['phrases']:
                merged_themes_phrases_dict[theme]['phrases'].append(phrase)
    
    return merged_themes_phrases_dict
########################################################################################

# according to '/pyflaskapps/data/output/new_policyanalysis/09_evaluate_phrases/evaluated_phrases_tmp.json'
# update the existing 02_themes_lemmas_phrases_changing '/pyflaskapps/data/output/policyanalysis/labels/02_themes_lemmas_phrases_changing.json'
def update_02_themes_lemmas_phrases_changing(existing_02_themes_lemmas_phrases_changingfile, evaluated_phrases_tmpfile):
    import json

    openedfile = open(existing_02_themes_lemmas_phrases_changingfile, encoding="UTF-8")
    themes_lemmas_phrases_dict = json.load(openedfile)

    openedfile = open(evaluated_phrases_tmpfile, encoding="UTF-8")
    evaluated_phrases_tmp_dict = json.load(openedfile)['data']['phrases_to_evaluate']

    themes_ls = list(evaluated_phrases_tmp_dict.keys())
    for theme in themes_ls:
        themes_lemmas_phrases_dict[theme]['phrases'] = evaluated_phrases_tmp_dict[theme]['phrases'] # completely overwrite the existing phrases with the newly evaluated phrases

    with open(existing_02_themes_lemmas_phrases_changingfile, 'w') as f:
        json.dump(themes_lemmas_phrases_dict, f)
################################################################################################

# update unevaluated_phrasesfile by removing phrases that are already evaluated in themes_linked_lemmas_phrases.json'
def update_unevaluated_phrases(unevaluated_phrasesfile, themes_linked_lemmas_phrasesfile):
    import json
    openedfile = open(unevaluated_phrasesfile, encoding="UTF-8")
    unevaluated_phrases_json = json.load(openedfile)
    unevaluated_phrases_dict = unevaluated_phrases_json['data']['unevaluated_phrases']
    openedfile = open(themes_linked_lemmas_phrasesfile, encoding="UTF-8")
    themes_lemmas_phrases_dict = json.load(openedfile)['data']['themes_lemmas_phrases']

    themes_ls = list(themes_lemmas_phrases_dict.keys())
    for theme in themes_ls:
        try:
            unevaluated_phrases_ls = unevaluated_phrases_dict[theme]['phrases']
        except:
            unevaluated_phrases_ls =[]
        phrases_ls = themes_lemmas_phrases_dict[theme]['phrases']
        for phrase in phrases_ls:
            if phrase in unevaluated_phrases_ls:
                unevaluated_phrases_dict[theme]['phrases'].remove(phrase)
    
    unevaluated_phrases_json['data']['unevaluated_phrases'] = unevaluated_phrases_dict

    description_old = unevaluated_phrases_json['meta']['description']
    description_new = """
    update by removing phrases that are already evaluated in themes_linked_lemmas_phrases.json.
    This file is made by update_unevaluated_phrases() in modules_common.py
    """
    if description_new not in description_old:
        unevaluated_phrases_json['meta']['description'] = description_old + description_new
    
    with open(unevaluated_phrasesfile, 'w') as f:
        json.dump(unevaluated_phrases_json, f) 

#######################################################################################












# init python\pyflaskapps\data\output\policyanalysis\labelled\labelled_meetingsents.json
# the following is to create the .json FOR THE FIRST TIME
# (what if new sents are added?)

def make_init_sent_themes_bymachine(sents_ls):
    for sent_dict in sents_ls:
        init_machine_themes_ls =[]
        for token_dict in sent_dict['tokens']:
            try:
                matched_themes_ls = token_dict['matched_themes']
                for theme in matched_themes_ls:
                    if theme not in init_machine_themes_ls:
                        init_machine_themes_ls.append(theme)
            except:
                pass
        sent_dict['labels']={}
        sent_dict['labels']['machine']=[]
        sent_dict['labels']['machine'].append({"version":0, "themes":init_machine_themes_ls})
    return sents_ls

def create_labelled_meetingsents():
    import sys, os, json
    cwd = os.getcwd().replace('\\', '/') # the cwd is
    src_jsonfile = cwd + '/pyflaskapps/data/output/policyanalysis/04_sents_minutes_lemmathemes_matched.json'
    openedfile = open(src_jsonfile, encoding="UTF-8")
    src_sents_ls = json.load(openedfile)

    # also need to open the target file (if it exists)
    targetfile = cwd + '/pyflaskapps/data/output/policyanalysis/labelled/labelled_meetingsents.json' #labelled_meetingsents
    try:
        openedfile = open(targetfile, encoding="UTF-8")
        target_sents_ls = json.load(openedfile)
    except:
        target_sents_ls=[]

    # thus to compare the target_sents and only update the parts (sents, labels) that are not in the target_sent_ls
    # print(len(target_sents_ls))

    # elements from both lists are considerred the same if identical for sent, file[basename], section[title], and subsection[title]
    # Note: uuid are not reliable as they might be changed when the src json is created again. 
    src_dict = {}
    for x in src_sents_ls:
        # print('src ===', x['sent'])
        t={}
        t['sent'] = x['sent']
        t['filebasename'] = x['file']['basename']
        t['title'] = x['section']['title']
        t['subtitle'] = x['subsection']['title']
        # t is a dict cannot be used as a key of another dictionary. it has to be stringified
        t_str = json.dumps(t)
        src_dict[t_str] = x

    print('length of src ls', len(src_sents_ls))

    target_dict = {}
    for x in target_sents_ls:
        # print('target ===', x['sent'])
        t={}
        t['sent'] = x['sent']
        t['filebasename'] = x['file']['basename']
        t['title'] = x['section']['title']
        t['subtitle'] = x['subsection']['title']
        # t is a dict cannot be used as a key of another dictionary. it has to be stringified
        t_str = json.dumps(t)
        target_dict[t_str]= x
    print('length of target_sents_ls', len(target_sents_ls))


    # use the data from the target_dict to overwrite data in the src_dict, thus to update the src_dict (which is like a blank slate) with the data from the previous labelling works
    src_keys = list(src_dict.keys())
    for src_key in src_keys:
        try:
            src_dict[src_key] = target_dict[src_key] # look up the same key in the target dict. If matched, use the target_dict data to overwrite the src data (this includes labelling, themes/token/matched phrases lemmas in the target json file)
        except:
            # if the src key is not found in the target dic, do nothing
            pass
    print('length of src_keys', len(src_keys))

    # but what if there are data in target_dict, but not in src_dict
    target_keys = list(target_dict.keys())        
    for target_key in target_keys:
        try: 
            x= src_dict[target_key]
        except:
            src_dict[target_key] = target_dict[target_key] # if the target key is not found in the src dict, add the data from the target dict to the src. 

    # now that the src_dict is very complete! It contains all its existing data (also updated with new data from target dict), as well as data from target dict that was not in src dict
    print('length of target_keys', len(target_keys))


    # convert the updated src_dict back to a list
    new_src_ls = []
    src_keys = list(src_dict.keys())
    for src_key in src_keys:
        # print('new ===', src_dict[src_key]['sent'])
        new_src_ls.append(src_dict[src_key])
    print('length of new_src_ls', len(new_src_ls))

    # next, for those in new_src_ls and have not be labelled by machine, make the intial label (v0)
    # it reads data from python\pyflaskapps\data\output\policyanalysis\labels\02_themes_lemmas_phrases_changing.json
    # for a sentence in new_src_ls, if any of the token matches a theme, append the matched theme to {label:{machine:{[{version:0, themes:[...]}]}}
    new_src_ls = make_init_sent_themes_bymachine(new_src_ls)

    # note: the existing target file is saved as a gzip (to save space)
    # the update file is saved as a json (easier to view) 
    # backup the existing data as a gzip 
    if (len(target_sents_ls) > 0):
        import datetime
        now = datetime.datetime.now()
        date_time = now.strftime("%Y%m%d_%H%M%S")
        # print("date and time:",date_time)
        backup = cwd + '/pyflaskapps/data/output/policyanalysis/labelled/history/labelled_meetingsents_' + date_time + '.json.gz'
        import gzip
        json_str = json.dumps(target_sents_ls) # convert to string
        json_bytes = json_str.encode('utf-8') # convert to bytes
        with gzip.open(backup, 'w') as f:
            f.write(json_bytes)

    # save the updated src_dict and overwrite the existing labelled
    with open(targetfile, 'w') as f:
        json.dump(new_src_ls, f)


# get all files and make a list with file path, base, and ext names
def get_files(d): # d is the ancestor folder in which the files and subfolders are to be searched 
    import os
    files_ls =[]
    for x in os.listdir(d):
        # print(x)
        f = os.path.join(d, x)
        # print(f)
        if os.path.isfile(f):
            name = os.path.basename(f) # like file.txt
            base, ext1 = os.path.splitext(name) # like file, .txt
            ext = ext1.replace('.', '') #.txt => txt
            tmp_dict = {"path":d, "base":base, "ext":ext}
            files_ls.append(tmp_dict)
        else:
            if os.path.isdir(f):
                f= f + '/'
                f2_ls = get_files(f)
                files_ls = files_ls + f2_ls
    return files_ls
    

# make a list of [{theme:..., phrases:[], lemmas:[]}, {}]
# get the 04.json
# import the classified lemmas
def make_themes_lemmes_phrases_dict():
    import sys, os, json
    cwd = os.getcwd().replace('\\', '/') # the cwd is
    sent_jsonfile = cwd + '/pyflaskapps/data/output/policyanalysis/04_sents_minutes_lemmathemes_matched.json'
    openedfile = open(sent_jsonfile, encoding="UTF-8")
    sents_ls = json.load(openedfile)
    # print('len sent ======', len(sents_ls))

    themes_ls =[]
    themeskeys_dict={} # this is the one to hold all themes {theme1:{lemmas:[], phrases:[]}
    i = -1
    for sent_dict in sents_ls:
        i +=1
        # if i > 0:
        #     continue
        for token in sent_dict['tokens']:
            # print(token['index'])
            # try if the token has a key matched_themes
            try:
                matched_theme_ls = token['matched_themes']
                # matched_lemma = token.lemma
                # print('matched_theme_ls ===', len(matched_theme_ls))
                matched_lemma = token['lemma']
                # print('matched_lemma === ', matched_lemma)

                for matched_theme in matched_theme_ls:
                    # print ('matched_theme === ', matched_theme)
                    # if matched_theme not in themes_ls:
                    #     themes_ls.append(matched_theme)
                    # print('len themes_ls ====', len(themes_ls))
                    #try if this matched_theme is already a key in themeskeys_dict
                    try:
                        matched_theme_dict =  themeskeys_dict[matched_theme]
                    except:
                        # if the key was not found, add it as a new key
                        themeskeys_dict[matched_theme] = {}
                        matched_theme_dict = themeskeys_dict[matched_theme]
                        matched_theme_dict['lemmas'] =[]
                        matched_theme_dict['phrases'] =[]

                    # add the lemma into matched_theme_dict['lemmas']
                    if matched_lemma not in matched_theme_dict['lemmas']:
                        matched_theme_dict['lemmas'].append(matched_lemma)

                    # add the phrases into  matched_theme_dict['phrase']
                    # identify the matched_phrase_ls
                    matched_phrase_ls=[]
                    for phrase_indices_dict in token['in_matched_phrases']:
                        # print('phrase_indices_dict ===', phrase_indices_dict)
                        start_tokenindex = phrase_indices_dict['start_tokenindex']
                        # get the toke of the phrase_indices_dict
                        start_token = sent_dict['tokens'][start_tokenindex]
                        # get the start char pos of the start_token
                        start_token_start_pos = start_token['start']

                        end_tokenindex = phrase_indices_dict['end_tokenindex']
                        # get the toke of the phrase_indices_dict
                        end_token = sent_dict['tokens'][end_tokenindex]
                        # get the start char pos of the start_token
                        end_token_end_pos = end_token['end']

                        # print('start and end position ===',start_token_start_pos, end_token_end_pos)
                        # print ('sentence ===', sent_dict['sent'])
                        matched_phrase = sent_dict['sent'][start_token_start_pos:end_token_end_pos+1]
                        # print ('matched_phrase ===', matched_phrase)
                        if (matched_phrase not in matched_phrase_ls):
                            matched_phrase_ls.append(matched_phrase)
                    for matched_phrase in matched_phrase_ls:
                        if matched_phrase not in matched_theme_dict['phrases']:
                            matched_theme_dict['phrases'].append(matched_phrase)
                    # to this step, matched_theme_dict is updated for the new/exist theme, lemma, and phrases
                    themeskeys_dict[matched_theme] = matched_theme_dict
            except:
                pass


    # write the target data list to disk
    targetfile = cwd + '/pyflaskapps/data/output/policyanalysis/05_themes_lemmas_phrases.json'
    with open(targetfile, 'w') as f:
        json.dump(themeskeys_dict, f)


#make a lemma_themes dict like {'house': ['housing', '...']}, i.e., use the lemma to lookup its associated themes
def make_lemma_themes_dict():
    lemma_themes_dict ={}
    import sys, os, json
    cwd = os.getcwd().replace('\\', '/') # the cwd is

    # import the classified lemmas
    lemmas_jsonfile = cwd + '/pyflaskapps/data/output/lemma_classification/classified_lemmas.json'
    openedfile = open(lemmas_jsonfile, encoding="UTF-8")
    lemma_theme_ls = json.load(openedfile)

    lemmas_ls = []
    for dict in lemma_theme_ls:
        lemma = dict['lemma']
        theme = dict['theme']
        if lemma not in lemmas_ls: # for a new lemma
            lemmas_ls.append(lemma) # append it to the lemma_ls to indicate that it is no longer a new lemma
            lemma_themes_dict[lemma] = [theme] # in the result lemma_themes_dict, add the lemma as a key, the theme is the first of a list of lookup values of the lemma
        else: # if the lemma is not new
            lemma_themes_dict[lemma].append(theme) # lemma_themes_dict[lemma] is a collection of themes that are associated with the lemma
    
    # write to disk
    targetfile = cwd + '/pyflaskapps/data/output/policyanalysis/labels/01_lemma_themes_dict.json'
    with open(targetfile, 'w') as f:
        json.dump(lemma_themes_dict, f)
#######################################################################



def remove_unicode_chars(str):
    result = ''.join([i if ord(i) < 128 else '' for i in str])
    return result


def remove_line_breaks(str):
    result = str.replace('-\n', '')
    result = result.replace('\n', ' ')
    return result

def replace_multi_space_by_one(str):
    import re
    return re.sub(' +', ' ', str)



# adapted based on python\pyflaskapps\example15_spacytests\pymodules\spacy\tests\test202.py 
# use reg express to correct the wrong sentence split because of the strange punctuations in the memos
# the idea is to 
# 1. convert ';\n1. ' to '.\n1_ '
# 2. convert '\n1. ' to '\n1_ '
# 3. convert 'WHEREAS' to 'WHEREAS.'
# 4. convert 'BE IT SOLVED' to 'BE IT SOLVED.'
def clean_all_vanmeeting_text_sentenceEnding():

    # read original json
    import sys, os, json
    cwd = os.getcwd().replace('\\', '/') # the cwd is the location where python starts, in this case, it is C:\Personal\Virtual_Server\PHPWeb\ml_text\python
    src_jsonfile = cwd + '/pyflaskapps/data/output/policyanalysis/01_text_minutes.json'
    openedfile = open(src_jsonfile, encoding="UTF-8")
    srcdata_ls = json.load(openedfile)
    # print('lengthe of original data ========', len(srcdata_ls))
    # print(srcdata_ls[0])

    i=-1
    for text_dict in srcdata_ls:
        i +=1
        if i < len(srcdata_ls): # for debug, set like i< 1
            text = text_dict["text"]
            # print ('original ================')
            # print (text)
            cleaned_text = clean_vanmeeting_sent_end(text)
            cleaned_text = remove_unicode_chars(cleaned_text) # note: sent is a spacy obj
            cleaned_text = remove_line_breaks(cleaned_text)
            cleaned_text = replace_multi_space_by_one(cleaned_text)

            # print('cleaned=====================')
            # print(cleaned_text)
            text_dict["text"] = cleaned_text

    targetdata_ls = srcdata_ls
    # write the target data list to disk
    targetfile = cwd + '/pyflaskapps/data/output/policyanalysis/02_text_minutes_cleaned1.json'
    with open(targetfile, 'w') as f:
        json.dump(targetdata_ls, f)  
########################################################
        
def clean_vanmeeting_sent_end(t):

    # get the part between two chars
    import re
    # t = "V;\n3. On June 23;\n31. whatever."

    while re.search(r';(\s)\d*\. ', t) != None:
        # search for the pattern: a semicolon, followed by a whitespace, digits, a dot, and a space
        x =re.search(r';(\s)\d*\. ', t) # a semicolon, followed by a whitespace, digits, a dot, and a space
        # print(x)

        #get the span of the matched segment (re.search only match for the first instance)
        span=x.span()
        # print(span[0], span[1])
        before = t[:span[0]] # get the substr before the matched seg
        # print(before)
        after = t[span[1]:] # get the substr after the matched seg
        # print(after)

        matchedseg = t[span[0]:span[1]] # get the matched seg
        # print(matchedseg)

        # print(t2)
        newseg=matchedseg.replace('.', '-').replace(';', '.') # from ';\n1. ' to '.\n1, '
        # print(newseg)

        t = before + newseg + after
        # print(t)

    while re.search(r'\s\d*\. ', t) != None:
        # search for the pattern:  a whitespace, digits, a dot, and a space
        x =re.search(r'\s\d*\. ', t) #  a whitespace, digits, a dot, and a space
        # print(x)

        #get the span of the matched segment (re.search only match for the first instance)
        span=x.span()
        # print(span[0], span[1])
        before = t[:span[0]] # get the substr before the matched seg
        # print(before)
        after = t[span[1]:] # get the substr after the matched seg
        # print(after)

        matchedseg = t[span[0]:span[1]] # get the matched seg
        # print(matchedseg)

        # print(t2)
        newseg=matchedseg.replace('.', '-') # from '\n1. ' to '\n1- ' # do not use like 1_, it'll cause error in splitting sentences
        # print(newseg)

        t = before + newseg + after
        # print(t)    
        
    # next, replace '\n7. ' as '\n7, '    
    t = t.replace('WHEREAS', 'WHEREAS.')
    t = t.replace('BE IT RESOLVED', 'BE IT RESOLVED.')

    return t

    ##############################################################################



'''
to arrange text of meeting into new layout like
To rearrange data from:
[
            {
                "file": "regu20210119min.html",
                "path": "data/input/vanmeetings/html",
                "sections": [
                    {
                        "title": "PRESENTATIONS",
                        "startEleIndex": 50,
                        "stopEleIndex": 75,
                        "elementsInSection": [\<element1 html\>, \<element2 html\>, etc],
                        "subsections": [
                            {
                                "subtitle": "1. Approval of Form of Development 5027 Boundary Road",
                                "startEleIndex": 174,
                                "motiontype": "Administrative Motion",
                                "stopEleIndex": 178,
                                "elementsInSubsection": [\<element1 html\>, \<element2 html\>, etc],
                                "text": \<text in of the subsection \>
                            }, // subsection1
                            {...} // subsection2
                        ] // subsection
                    },
                    {...}
                ] // section
            }, // file 1
            {...} // file 2
        ]

to: 

[
            {
                "text": \<subsection text\>,
                "subsection": {"title":} // each of the following is a dict so as to be flexible in adding new keys in the future
                "section":{"title":},
                "file":{"basename": }...
            } // subsection text1,
            {...} // subsection text2
        ]
'''
def rearrange_vanmeeting_text():
    # read original json
    # pip install uuid
    import sys, os, json, uuid
    cwd = os.getcwd().replace('\\', '/') # the cwd is the location where python starts, in this case, it is C:\Personal\Virtual_Server\PHPWeb\ml_text\python
    src_jsonfile = cwd + '/pyflaskapps/data/output/vanmeetingsample.json'
    openedfile = open(src_jsonfile, encoding="UTF-8")
    srcdata_ls = json.load(openedfile)
    print('lengthe of original data ========', len(srcdata_ls))

    # loop for each each file
    targetdata_ls = []
    for file_dict in srcdata_ls:
        # get file name
        filename = file_dict['file']
        # remove the extention name like .html
        # print(filename[-5:])
        if filename[-5:] == ".html":
            filename = filename[:-5]
        # print(filename)
        new_file_dict = {"basename":filename}
        # loop for sections
        for section_dict in file_dict["sections"]:
            section_title = section_dict["title"]
            new_section_dict = {"title": section_title}
            # loop for each subsection
            try:
                for subsection_dict in section_dict['subsections']:
                    subsection_title = subsection_dict["subtitle"]
                    new_subsection_dict = {"title": subsection_title}
                    text = subsection_dict["text"]
                    tmp_dict = {
                        "text": text,
                        "uuid":str(uuid.uuid4()),
                        "file": new_file_dict,
                        "section": new_section_dict,
                        "subsection": new_subsection_dict
                    }
                    targetdata_ls.append(tmp_dict)
            except:
                pass

    print('lengthe of target data ========', len(targetdata_ls))
    # write the target data list to disk
    targetfile = cwd + '/pyflaskapps/data/output/policyanalysis/01_text_minutes.json'
    with open(targetfile, 'w') as f:
        json.dump(targetdata_ls, f)
        
 ##############################################################################


def get_matched_phrasepos(text_dict, phrase): # text_dict must have ['text'], and ['tokens'], tokens like {start, end}
    import re

    text = text_dict['text']
    # make matched_phrases_backend_dict as in step 1 at frontend (adding _backend to indicate that the matched phrase dict is made at backend, so as to be compared with matched_phrase_dict property created at frontend )
    matched_allphrases_backend_dict={} # indicate that the matched phrase dict is made at backend, so as to be compared with matched_phrase_dict property created at frontend
    matched_dictinctphrases_backend_dict ={} # diff from above in that 'steriod, steriods' counted as once although these are two phrases
    distinct_startpos_theme_ls =[] # the match repeatedly counts the same phrase (like steriod, steriods counting for two times). matched with the same startpos and theme should only be counted for once when calculating matched themes! 
    # loop for each phrase of a theme

    # if i == 0:
    # if matched_phrase == 'cost':
        # print(407, matched_phrase)
    # https://sites.pitt.edu/~naraehan/python2/re.html
    pattern = re.compile(r"{}".format(phrase)) # use parameter in string, same as r"overdose" if the matched phrase is overdose, use word boundry
    matched_pos_ls=[]
    for matched in re.finditer(pattern, text):
        startpos = matched.start()
        endpos = startpos + len(phrase) -1 # same as matched.end()-1
        # if (uuid == "12685056") & (matched_phrase == 'cost'):
        #     print(414, startpos, endpos)
        # the above matches all substrings like "cost" in "corticosteroid"
        # adding word boundry (/b) into the matched_phrase does not work, as matched_phrase may contain multiple words
        # The idea is that for a phrase like 'cost-effectiveness', the matched.start(),i.e., the startpos of cost should be the same start position of the token 'cost' in the text
        # likewise, the matched.end() should be the same as the end position of the token 'effectiveness'
        # Thus, for each matched, if loop for each token, we can pick up the start token which has the same start position as the matched startpos
        #   as well as the end token which has the same end position as the matched endpos
        # those only having a matched startpos (like cost in costeroid) or a matched endpos (like corticost) are ignored 
        startmatched=0
        endmatched=0
        for x in text_dict['tokens']:
            # token text end position is not simply x['end'] (consider the token 'cost ' in which the end is the position of the space)!
            tokentext = text[x['start']:x['end']+1].strip() # get the stripped tokentext
            token_endpos = x['start'] + len(tokentext) -1 # calculate the token endpos without the ending white space
            # if (uuid == "12685056") & (x['lemma'] == 'cost'):
            #     print(429, 'tokentext', tokentext, x['start'], token_endpos)                        

            # if ((startpos >= x['start']) & (startpos <= x['end'])) :
            if startpos == x['start']:
                startmatched=1
                # if uuid == "12685056":
                #     print(430, '\\\\\\ a startpos is found', startpos, endpos, x['end'], x['lemma'])
            # if (startmatched == 1) & ((endpos >= x['start']) & (endpos <= x['end'])) :
            if (startmatched == 1) &  (endpos == token_endpos): # instead of x['end']  -- sometimes x['end'] referes to a white space
                endmatched=1
                # if uuid == "12685056":
                #     print(435, '/// an endpos is found', endpos)
                #     print(436, startpos, endpos)
            if (startmatched == 1) & ( endmatched == 1):
                # if uuid == "12685056":
                #     print (439, text[startpos:endpos+1])
                startmatched=0
                endmatched=0

                matched_pos_dict = {'phrase': phrase, 'start': startpos}
                matched_pos_ls.append(matched_pos_dict)
    return matched_pos_ls 
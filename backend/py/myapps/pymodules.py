import pathlib, os,sys
## To have the parent folder of this file
# path_thisfile = pathlib.Path(__file__).parent.resolve().__str__() #  pathlib.Path(__file__).parent.resolve() returns a WindowsPath Object, and __str__() is to convert the object to a string
# segs_ls =  path_thisfile.split('\\')
# currentprojectname = segs_ls[len(segs_ls)-1]
# loading modules from modules_spacy 
# exec ("from " + currentprojectname + ".pymodules.spacy.modules_spacy import *") # load all modules (*)

## load common modules ... not used in this simple example
# cwd = os.getcwd() # cwd is where the python command starts. In this case, it is at projectroot/backend/py
# cwd is not a good idea as it changes depending on where the current folder is. Use the project root path as the anchor instead
# add the location of the py common module file 
# location_commonmodules = cwd + '/common_pymodules'

# Note: the .parent.parent.parent.parent depends on the where thisfile locates in the project, i.e., it veries for different projects.
def get_project_root_path():
    import pathlib
    path_thisfile_obj = pathlib.Path(__file__) # it is a path object, not a string. it refers to backend/py/__init__.py (including the file name)
    path_projectroot_obj = path_thisfile_obj.parent.parent.parent.parent.absolute() # it is the parent (root) of parent (backend) of parent (py) of the file __init__.py 
    path_projectroot_str = str(path_projectroot_obj).replace('\\', '/') # convert to a string, replace backslash with slash
    print ('20, path_projectroot_str', path_projectroot_str)
    return path_projectroot_str
path_projectroot_str = get_project_root_path()
print(path_projectroot_str)
location_commonmodules = path_projectroot_str + '/backend/py/common_pymodules'
sys.path.insert(1, location_commonmodules) # add the location at the top of the sys.path, thus, by default, the py script file spacy_modules will be loaded from there

# from modules_testing import * # it works as spacy_modules is in the same folder of this py file
# from modules_spacy import * # do not name the py file like spacy.py (it'll be confused with the package spacy)
from modules_common import *
# from modules_classification import * # it works as spacy_modules is in the same folder of this py file



# based on test_a02.py in the ml_text project
def get_processed_textjson(requestdatafromfrontend_json):
    import json, spacy, math
    from collections import OrderedDict # for ordering dictionary by key
    from spacy.matcher import Matcher
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)

    entity_delimiter = " 196808240800 " # note: do not use numbers of length of 10 (10-digit numbers are like phone numbers and are removed by clean_text!)
    max_length_per_cut= 100 # if the big text is bigger then 100, force to split into several texts, each either <= 100 of length or is at least the length of an entity text (whichever is larger)

    requestjson=requestdatafromfrontend_json # like {requesttask: ..., requestdatafromfrontend:{article..., entities:[{entity1:..., text:...}]}}}
    data_frontend = requestjson['requestdatafromfrontend']
    article = data_frontend['article']
    entities_ls= data_frontend['entities'] # like [{entity1:..., text:...}]

    # concat texts from each entity into one textbody called alltext
    alltext = ""
    for x in entities_ls:
        alltext += x['text']
    # print(110, len(alltext))

    n_cuts = math.ceil(len(alltext) / max_length_per_cut) # e.g., if alltext length = 100, max_length_cut = 40, n_cuts = 2.5 round up to 3
    # divide textjson into n_cuts
    n_eles_per_selected = math.floor(len(entities_ls) / n_cuts) # e.g., if textjson has 16 elements, n_cuts =3, n_eles_per_selected = 16/3 round down to 5 -- each textjson cut is to have max of 6 elemets (0:5, 5:10, 10:15, 15:16)
    if n_eles_per_selected == 0:
        n_eles_per_selected =1 # at least one elements per selection
    n_selects = math.ceil(len(entities_ls) / n_eles_per_selected) # if selecting 5 elements per time in a selection, it takes 4 times to complete all 16 elements in a textjson
    print(117, "All text length is", len(alltext), "and is to be divided into", n_cuts, "cuts, each of a length of roughly", max_length_per_cut ,". The are", len(entities_ls), "entities in textjson are divided into", n_selects, "selections, each of", n_eles_per_selected, "entities.")


    # the following is to make processed_text (the processed text)
    ##################################################################### make a processed_text (a dict of text, sentences, etc)
    def make_processed_textjson (selected_entities):
        text=""
        # concate the entities, adding delimiters
        text = entity_delimiter.join(x['text'] for x in selected_entities)
        print(107, len(text), text.find(entity_delimiter))
        # note: cannot determine the text boundary now, because the clean-up in the next step will change length of each text. 

        # text cleaning 
        # ucode, quote, ..., hyphen breaking words spacy or textacy ... 
        print(112, "cleaning text ...")
        cleaned_text = clean_text_rendertest1(text) # clean_text_tendertest1 is a module in modules_common
        print(115, 'length of cleaned_text', len(cleaned_text))

        # determine test boundary
        cleaned_texts_ls = cleaned_text.split(entity_delimiter)
        print(118, len(cleaned_texts_ls))

        # when concatenating entites, a list is created to record the start and end position of the text of each entity
        entities_ls =[]
        start = 0
        for x in cleaned_texts_ls:
            end = start + len(x) -1 # if start=0 and len(x)=2, then end = 1 (text from 0 to 1)
            entities_ls.append({"start":start, "end": end}) 
            start = end + len(entity_delimiter) + 1 # if delimiter length = 3, start of the next text = 1 + 3 +1 = 5 ( 0 to 1 is text1, 2 to 4 is the delimiter, 5 is the start pos of the next text) 

        if len(entities_ls) != len(selected_entities):
            print("some of the delimiters were deleted during text cleaning ... the program stopped. ")
            x=z+1
        else:
            i=-1
            end2=0
            for x in entities_ls:
                i +=1
                x['entity'] = selected_entities[i]['entity']
                try:
                    x['section'] = selected_entities[i]['section']
                except:
                    pass
                # print(138, '-' + cleaned_text[end2+1:x['start']]+'-', x['entity'])
                # end2 = x['end']


        if len(cleaned_text) > 1000000:
            nlp.max_length = len(cleaned_text)


        # make into sentences, tokens, with token lemma, token pos, token dep, 
        def get_span_attrs(thespan):
            # note: all poistions are relative to the text
            # span_tokeni_start = thespan.start
            # span_chari_start = thespan[0].idx 
            tokens_ls = [] 
            for token in thespan:
                like_word=1
                if (token.pos_ == 'DET') | (token.like_num == True) | (token.is_currency == True) | (token.is_quote == True) | (token.is_bracket == True)| (token.is_space == True)| (token.is_punct == True)| (token.is_digit == True):
                    like_word = 0
                tmp_dict={
                    "lemma": token.lemma_.lower(),
                    "pos":token.pos_,
                    "dep":token.dep_,
                    "tokeni": token.i,
                    "start": token.idx,
                    "end": token.idx + len(token.text_with_ws)-1,
                    'like_word':like_word 
                }
                tokens_ls.append(tmp_dict)
            return {
                "tokens": tokens_ls,
            }

        doc = nlp(cleaned_text)
        all_words_ls =[]
        word_lemmas_dict={}
        print(64, "making tokens")
        # from the text, get a map of distict words and lemmas (e.g., skies => sky)
        for token in doc:
            word = token.text.lower().strip()
            lemma = token.lemma_.lower()
            if word not in all_words_ls:
                all_words_ls.append(word)
                try:
                    word_lemmas_dict[word].append(lemma)
                except:
                    word_lemmas_dict[word]=[lemma]
        # sort keys 
        word_lemmas_dict = OrderedDict(sorted(word_lemmas_dict.items()))

        print(75, "making sentences")
        sents_ls=[]
        for sentspan in doc.sents:
            # senttext = sent.text
            # starti = sent.start
            senttokens_ls = [] 
            # for token in sent:
            #     tmp_dict={
            #         "lemma": token.lemma_.lower(),
            #         "pos":token.pos_,
            #         "dep":token.dep_,
            #         "i": token.i,
            #         "start": token.idx,
            #         "end": token.idx + len(token.text_with_ws)-1
            #     }
            #     senttokens_ls.append(tmp_dict)
            spanattrs_dict = get_span_attrs(sentspan)
            sents_ls.append(spanattrs_dict)
        # print(sents_ls[0])

        # phrase_lemmas_ls =[]
        distinct_spans_ls=[]

        # get entities from the text
        # def make_phrases(spans_ls, phrase_lemmas_ls, distinct_spans_ls):
        def make_phrases(spans_ls, distinct_spans_ls):
            results_ls=[]
            for thisspan in spans_ls:
                span_range = str(thisspan.start) + '__' + str(thisspan.end)
                if span_range in distinct_spans_ls:
                    continue
                distinct_spans_ls.append(span_range)
                attrs_dict = get_span_attrs(thisspan)
                # if thisspan.text == "much less":
                    # print(78, attrs_dict)
                lemmas_ls =[]
                token_indices=[]
                for token1 in attrs_dict['tokens']:
                    thislemma=""
                    #!!! why check lemma and words here!!!
                    # try:
                    #     if token1['like_word'] == 1: # if the toke is not digit, number, currency, punct .... 
                    #         thislemma = token1['lemma']
                    # except:
                    #     pass
                    thislemma = token1['lemma'] # to replace the above try, now that all lemmas are included, regardless whether it is like a word

                    if (len(thislemma)>0):
                        lemmas_ls.append(thislemma)
                    
                    token_indices.append(token1['tokeni'])

                # no need to keep words, lemma.. of the tokens as they are in sentence tokens
                attrs_dict['token_indices'] = token_indices
                attrs_dict.pop('tokens', None)

                if len(lemmas_ls) < 1: # this is the switch to exclude single word lemma if lemmas_ls len <2
                    continue
                lemmas_str = '|'.join(lemmas_ls)
                attrs_dict['lemmas'] = lemmas_str
                
                # if (lemmas_str not in phrase_lemmas_ls):
                #     phrase_lemmas_ls.append(lemmas_str)
                results_ls.append(attrs_dict)
            return {
                "results_ls":results_ls,
                # "phrase_lemmas_ls": phrase_lemmas_ls,
                "distinct_spans_ls":distinct_spans_ls
            }

        # print(88, phrase_lemmas_ls[1])
        # print(ents_ls)
        # print(90, len(phrase_lemmas_ls))
        print(147, "making entities")
        # results_dict = make_phrases(doc.ents, phrase_lemmas_ls, distinct_spans_ls)
        results_dict = make_phrases(doc.ents, distinct_spans_ls)
        ents_ls = results_dict['results_ls']
        # phrase_lemmas_ls = results_dict['phrase_lemmas_ls']
        distinct_spans_ls = results_dict['distinct_spans_ls']

        print(153, "making noun_chunks")
        # results_dict = make_phrases(doc.noun_chunks,  phrase_lemmas_ls, distinct_spans_ls)
        results_dict = make_phrases(doc.noun_chunks,   distinct_spans_ls)
        noun_chunks_ls = results_dict['results_ls']
        # phrase_lemmas_ls = results_dict['phrase_lemmas_ls']
        distinct_spans_ls = results_dict['distinct_spans_ls']

        # print(122, noun_chunks_ls[2])
        # print(123, len(phrase_lemmas_ls))

        print(162, "making matched phrases")
        # verb chunks
        patterns_ls =[]
        pattern1= [{"POS": "VERB", "OP": "?"},{"POS": "ADV", "OP": "*"},{"POS": "VERB", "OP": "+"}]
        pattern2= [{"POS": "VERB", "OP": "+"},{"POS":  "ADP"}]
        pattern3= [{"POS": "ADV", "OP": "?"},{"POS":  "ADJ", "OP":"+"}]
        pattern4= [{"POS": "ADP", "OP": "+"},{"OP":"?"}, {"POS":  "ADP", "OP":"+"}]
        patterns_ls.append(pattern1)
        patterns_ls.append(pattern2)
        patterns_ls.append(pattern3)
        patterns_ls.append(pattern4)

        matcher.add('verb_chunks', patterns_ls)

        matched_obj = matcher(doc)
        matched_spans_ls =[]
        for match_id, start, end in matched_obj:
            matched_span = doc[start:end]
            # print(96, matched_span.text)
            matched_spans_ls.append(matched_span)

        # print(139, matched_spans_ls)

        # results_dict = make_phrases(matched_spans_ls,  phrase_lemmas_ls, distinct_spans_ls)
        results_dict = make_phrases(matched_spans_ls,  distinct_spans_ls)
        matchedphrases_ls = results_dict['results_ls']
        # print(143, matchedphrases_ls)
        # phrase_lemmas_ls = results_dict['phrase_lemmas_ls']
        distinct_spans_ls = results_dict['distinct_spans_ls']

        # print(169, matchedphrases_ls[2])
        # print(170, len(phrase_lemmas_ls))


        phrases_ls = ents_ls + noun_chunks_ls + matchedphrases_ls
        # print(175, phrases_ls[0])
        # sort by the key lemmas
        phrases_ls =sorted(phrases_ls, key=lambda x: x['lemmas'])  #sorted(phrases_ls, key=lambda k: k['start'])  # do not sort, the key 'start' has been removed

        # phrase_lemmas_ls.sort() # not used though

        # save everything to local
        # text, sent, tokens, phrases (entities, noun_chunks, verb_chunks)
        processed_textjson ={
            "meta":{
                "source": "",
                "programs": "~/rendertest1/myapps/pymodules.py"
            },
            "data":{
                "text":cleaned_text,
                "article":article,
                "entities": entities_ls,
                "sentences": sents_ls,
                "phrases": phrases_ls,
                "word_lemmas_dict":word_lemmas_dict
            }
        }

        return processed_textjson
    ##################################################################### end of the module make_processed_text (a dict of text, sentences, etc)


    targetjson = []
    start_ele=0
    for n in range(1, n_selects+1): # loop for number of selections
        # if n > 1:
        #     break
        start_ele = (n-1) * n_eles_per_selected
        end_ele = start_ele + n_eles_per_selected
        if end_ele > len(entities_ls)-1: # for the last cut, make end_ele as the index of the last element in textjson + 1
            end_ele = len(entities_ls)
        selected_entities = entities_ls[start_ele:end_ele]
        print(379, "making processed_textjson", n, "of", n_selects, "============ entity", start_ele, "to", end_ele, "number of entities:", len(selected_entities))
        processed_textjson = make_processed_textjson(selected_entities)
        targetjson.append(processed_textjson)

    responsedatafrombackend_json = {'responsedatafrombackend': targetjson}
    return responsedatafrombackend_json

################################# def get_processed_textjson(requestdatafromfrontend_json)#########################################################

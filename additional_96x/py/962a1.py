


def get_matched_spans(text="______", interested_phrases_ls=[], match_patterns_ls=[], include_pos_pattern=True, include_norm_pattern = False, max_text_length=""):

    import spacy
    from spacy.matcher import Matcher
    print('Loading en_core_web_sm, in get_matched_spans() ============ =====================')
    nlp = spacy.load("en_core_web_sm")
    print('Loading en_core_web_lg done ============ =====================')
    if len(str(max_text_length))>0:
        nlp.max_length = max_text_length

    print('10, load Matcher(nlp.vocab) =====')
    matcher = Matcher(nlp.vocab)
    if text =='______':
        text = '5- The July 2017 Housing Engagement Summary reports summarizes on Page 17 titled Affordability and Availability of Housing, Cost of Living, reports the first concern to be lack of opportunities for affordable home ownership affecting future decisions (cost of living or cost of qualified living) to make Vancouver home.'
    textdoc = nlp(text)
    print(15, 'textdoc', len(textdoc))
    # a list of interested phrases (these are not entities, nor noun_chunks, -- not identified by Spacy)
    if len(interested_phrases_ls) == 0:
        interested_phrases_ls = ['Cost of Living', 'Affordability and Availability', 'Housing Engagement Summary reports']
    # interested_phrases_ls = ['Affordability and Availability']
    # 1. for each phrase, make a pattern by lemma (e.g., Cost of Living ==> [{'lemma':'cost'}, {'lemma':'of'}, {'lemma':'living'}])
    # 2. also, pick up the spans by pos pattern (e.g., Cost of Living ==> [{'pos':'Noun'}, {'pos':'Prepn'}, {'pos':'Noun'}], thus to pick up the phrases with the similar structure like lack of opportunities)
    # from the above
    # 3. get all matched spans (token start/end index)
    
    patterns_ls=[]
    if (len(match_patterns_ls) == 0):
        print('30, make patterns ... loop for number of patterns: ', len(interested_phrases_ls))
        for phrase in interested_phrases_ls:
            phrasedoc = nlp(phrase)
            # ignore the single words
            # if len(phrasedoc) < 2:
            #     continue
            verbatim_pattern = []
            # get patterns like [{'lemma':'cost'},{'IS_ASCII': True, 'OP': '*'}, {'lemma':'of'},{'IS_ASCII': True, 'OP': '*'}, {'lemma':'living'}]
            lemmas_pattern = []# verbatim = exactly the words
            # get patterns like [{'pos':'Noun'},{'IS_ASCII': True, 'OP': '*'}, {'pos':'Prepn'},{'IS_ASCII': True, 'OP': '*'}, {'pos':'Noun'}]
            lowers_pattern =[]
            pos_pattern =[]
            norms_pattern=[]
            for token in phrasedoc:
                verbatim = token.text
                pattern_dict ={'orth':verbatim}
                verbatim_pattern.append(pattern_dict)

                lemma= token.lemma_.lower()
                pattern_dict = {'lemma': lemma}
                lemmas_pattern.append(pattern_dict)
                # if token != phrasedoc[-1]:
                #     lemmas_pattern.append({'IS_ASCII': True, 'OP': '*'})

                lemma= token.lemma_.lower()
                pattern_dict = {'lower': lemma}
                lowers_pattern.append(pattern_dict)
                # if token != phrasedoc[-1]:
                #     lemmas_pattern.append({'IS_ASCII': True, 'OP': '*'})

                if include_pos_pattern == True:
                    pos = token.pos_
                    pattern2_dict = {"pos":pos}
                    pos_pattern.append(pattern2_dict)
                    # if token != phrasedoc[-1]:
                    #     pos_pattern.append({'IS_ASCII': True, 'OP': '*'})

                if include_norm_pattern == True:
                    norm = token.norm_
                    norms_dict = {"norm":norm}
                    norms_pattern.append(norms_dict)

            if verbatim_pattern not in patterns_ls:
                patterns_ls.append(verbatim_pattern)
            if lemmas_pattern not in patterns_ls:
                patterns_ls.append(lemmas_pattern)
            if lowers_pattern not in patterns_ls:
                patterns_ls.append(lowers_pattern) # lower and lemma are different: Community is not community
            if include_pos_pattern == True:    
                if pos_pattern not in patterns_ls:
                    patterns_ls.append(pos_pattern)
            if include_norm_pattern == True:
                if norms_pattern not in patterns_ls:
                    patterns_ls.append(norms_pattern)

    # print(85, 'patterns_ls', patterns_ls)
    # print(86, 'match_patterns_ls', match_patterns_ls)
    if len(match_patterns_ls) == 0:
        matcher.add('customized_phrases', patterns_ls, greedy='LONGEST')
    else:
        matcher.add('customized_phrases', match_patterns_ls, greedy='LONGEST')
    
    matched_spans_ls=[]    
    print('85, match patterns from doc ...')
    matches = matcher(textdoc)
    for match_id, start, end in matches:
        matched_span = textdoc[start:end]
        # print(96, matched_span.text)
        matched_spans_ls.append(matched_span)
    print('91, return  matched_spans_ls ===', len(matched_spans_ls))
    return matched_spans_ls



import sys, os, json, gzip 

cwd = os.getcwd().replace('\\', '/')
print (cwd)

# load the json
tmpdir= '/additional_96x/data/history/'
tmpoutdir  = '/additional_96x/data/history/out/'
srcjsonfile = cwd + tmpdir + 'matched_distinct_phrases_acrossthemes.json'
openedfile = open(srcjsonfile, encoding="UTF-8")
srcjson = json.load(openedfile) # it is like {theme1:{phrases:[], lemmas:[]}}
phrases_ofthemes_ls = srcjson['data']
# print(phrases_ofthemes_ls[0])

otherphrases_ls=[]
for x in phrases_ofthemes_ls:
    in_selected_themes=0
    for y in ["harm_reduction",            "housing",            "mental_health",            "youth_children"]:
        if y in x['themes']: # skip if the phrase matches one of the above themes
            # print('is it here')
            in_selected_themes=1
            break # break for y loop
    if in_selected_themes == 0:
        if (x['phrase'] not in otherphrases_ls):
            otherphrases_ls.append(x['phrase'])
# print(len(otherphrases_ls))

# save it
targetjsonfile = cwd + tmpoutdir + '/otherphrases.json'
# save file ls as a json
with open(targetjsonfile, 'w') as f:
    json.dump(otherphrases_ls, f) 



def bigtext_get_otherphrases():


    for nn in ["1", "2"]:
        print(144, nn)
        bigtextgzlocation = cwd + tmpdir + '/bigtext_sents_of_all_sections_{}.json.gz'.format(nn)
        # print(corpusfilepath)
        with gzip.open(bigtextgzlocation, 'r') as fin:        
            json_bytes = fin.read()      
        # convert bytes to string
        json_str = json_bytes.decode('utf-8')  
        # convert string to json  
        srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
        bigtext = srcjson['data']
        max_text_length=len(bigtext)

        # print(155, len(bigtext))

        # bigtext= "hello this is a text."
        # otherphrases_ls = ['this is', 'a text']

        matched_spans_ls = get_matched_spans(
                text=bigtext, 
                interested_phrases_ls=otherphrases_ls, 
                match_patterns_ls=[], 
                include_pos_pattern=True, 
                include_norm_pattern = False, 
                max_text_length= max_text_length
        )

        # print(matched_spans_ls[0])

        matched_ls = []
        for x in matched_spans_ls:
            # print(172, len(list(x)))
            start = x[0].idx
            end = start + len(x.text_with_ws) -1
            text = x.text_with_ws
            tmpdict = {
                "start": start,
                "end": end,
                "text": text,
                "label": "phrases_otherthemes"                 
            }
            matched_ls.append(tmpdict)
        
        print(185, len(matched_ls))

        print('saving....')

        jsonobj = {
            'sources': [
                cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/bigtext_sents_of_all_sections_{}.bin.gz'.format(nn), 
                cwd + '/pyflaskapps/data/output/new_policyanalysis/09_evaluate_phrases/matched_distinct_phrases_acrossthemes.json'
            ],
            'program': r'C:\Users\syao2\AppData\Local\MyWorks\js\ml_text\python\pyflaskapps\example15_spacytests\pymodules\spacy\tests\test962a1.py',
            'data': matched_ls
        }

        # save all entites and noun chunks
        targetjsonfile = cwd + tmpoutdir + '/phrases_otherthemes_uncleaned_bigtext_{}.json.gz'.format(nn)
        json_str = json.dumps(jsonobj) # convert to string
        json_bytes = json_str.encode('utf-8') # convert to bytes
        with gzip.open(targetjsonfile, 'w') as f:
            f.write(json_bytes)

###############################################################


bigtext_get_otherphrases()
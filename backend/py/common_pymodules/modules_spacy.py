# to get matched spans according to phrases (as in test501.py)
def get_matched_spans(text="______", interested_phrases_ls=[], match_patterns_ls=[], include_pos_pattern=True, include_norm_pattern = False, max_text_length=""):

    import spacy
    from spacy.matcher import Matcher
    print('Loading en_core_web_sm, in get_matched_spans() ============ =====================')
    nlp = spacy.load("en_core_web_sm")
    print('Loading en_core_web_sm done ============ =====================')
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


# read sent in 03...json, convert to spacy doc, get tokens, phrases (entities and noun_chunks). 
# Indicate phrases that contains a lemma in python\pyflaskapps\data\output\lemma_classification\classified_lemmas.json
# If so, the matched token index and the associated themes 
# split sentence into tokens, get index, start/end character position of the token in the sentence. 
# For each token, inidcate whether its lemma matches a theme
# or if the token is part of a phrase  
def make_sent_matched_phrase():
    import sys, os, uuid
    cwd = os.getcwd().replace('\\', '/') # the cwd is the location where python starts, in this case, it is C:\Personal\Virtual_Server\PHPWeb\ml_text\python
    import json
    # import the sentences
    sents_jsonfile = cwd + '/pyflaskapps/data/output/policyanalysis/03_sentences_minutes.json'
    openedfile = open(sents_jsonfile, encoding="UTF-8")
    sents_ls = json.load(openedfile)

    # import the lemma_themes_dict, like {"house": ["housing", "homeless"]}
    lemma_themes_dict_jsonfile = cwd + '/pyflaskapps/data/output/policyanalysis/labels/01_lemma_themes_dict.json'
    openedfile = open(lemma_themes_dict_jsonfile, encoding="UTF-8")
    lemmas_themes_dict = json.load(openedfile)

    import spacy
    print('Loading en_core_web_lg, in make_sent_matched_phrase() ============ =====================')
    nlp = spacy.load("en_core_web_lg") # although bigger, it contains many features (like token.vector) that are not provided (or of a wrong verion) by the _sm lib
    print('Loading en_core_web_lg done ============ =====================')
    for sent_dict in sents_ls:
        # if sent_dict['uuid'] != '7a372e15-bad9-4235-a2ac-5deb92e6df1f': #debug
        #     continue
        senttext = sent_dict['sent']
        # print(senttext)

        # convert to spacy doc
        doc = nlp(senttext)
       
        # add bouth entities and noun chunks into the phrases_ls (note: phrases_ls is a spacy obj, not a text)
        phrases_ls =[]
        for x in doc.ents:
            if x not in phrases_ls:
                phrases_ls.append(x)
        for x in doc.noun_chunks:
            if x not in phrases_ls:
                phrases_ls.append(x)

        # find matched phrases
        matched_tokenindices_ls =[]
        matched_tokenindex_themes_phrases_dict ={} # like {<tokenindex1>:{themes:[theme1, theme2], phrases:[{start_tokenindex:.., end_tokenindex}, {}]}, <tokenindex2>{}}
        phrases_dicts_ls=[] # like {phrase:"a housing...", lemmas_themes:[<a lemma like "home">: [<theme1 like housing>, <theme2 like homeless>]]}

        for phrase in phrases_ls:
            # print(phrase)
            # if phrase.text !="Mount Pleasant Neighbourhood House":
            #     continue
            matched_lemma_themes_ls=[] # like[<a lemma like "home">: [<theme1 like housing>, <theme2 like homeless>], [lemma: <lemm2>..]]
            for token in phrase:
                # print(token)
                lemma = token.lemma_.lower() # like 'home
                # print(lemma)
                try:
                    lemma_themes_ls = lemmas_themes_dict[lemma] # if the lemma is in the lemmas_themes_dict, it'll return a list of themes associated with the lemma
                    # print(lemma_themes_ls)
                    tmp_dict = {"tokenindex":token.i,  "themes": lemma_themes_ls} # like {tokenindex:..., themes: [<theme1 like housing>, <theme2 like homeless>]}
                    matched_lemma_themes_ls.append(tmp_dict) # matched_lemma_themes_ls contains, of the current phrase, all tokens associated to themes
                    if token.i not in matched_tokenindices_ls:
                        matched_tokenindices_ls.append(token.i)
                    try:
                        # if theme not in matched_tokenindex_themes_phrases_dict has the key [token.i]
                        x = matched_tokenindex_themes_phrases_dict[token.i]
                        # if x exists 
                        try: # whether x has a key 'theme'
                            y = theme not in matched_tokenindex_themes_phrases_dict
                            # if y exists
                            for theme in lemma_themes_ls:
                                if theme not in y:
                                    y.append(theme) # either add the themes (merge) to the existing themes of the current token 
                        except: # if y does not exists
                            x["themes"] = lemma_themes_ls
                    except: # if x does not exist
                        matched_tokenindex_themes_phrases_dict[token.i] ={} # create x
                        matched_tokenindex_themes_phrases_dict[token.i]["themes"]= lemma_themes_ls # create y

                    # mached phrases
                    matched_phrases_dict = {"start_tokenindex":phrase.start, "end_tokenindex":phrase.end -1}
                    try:
                        if matched_phrases_dict not in matched_tokenindex_themes_phrases_dict[token.i]['phrases']: # to here, matched_tokenindex_themes_phrases_dict[token.i] must exist (created by  the above), the try is only on whether it has a key['phrase]
                            matched_tokenindex_themes_phrases_dict[token.i]['phrases'].append(matched_phrases_dict) # either add the phrase dict (merge) to the existing phrase dict of the current token index
                    except:
                        matched_tokenindex_themes_phrases_dict[token.i]["phrases"] = []
                        matched_tokenindex_themes_phrases_dict[token.i]["phrases"].append(matched_phrases_dict) # or create a new key, and add the dict to that new key                    
                except:
                    pass
            
            phrases_dict = {"phrase": {"start_tokenindex":phrase.start, "end_tokenindex":phrase.end -1}} # phrase.end is span.end, which is the index of the first token after the span
            if len(matched_lemma_themes_ls) > 0:
                phrases_dict["matched_lemmas_themes"] = matched_lemma_themes_ls
            phrases_dicts_ls.append(phrases_dict)
                # print(matched_phrases_ls)

        sent_dict['phrases'] = phrases_dicts_ls

        # make a matched token list (matched_tokenindices_ls) for the whole sentence
        # like [tokenindex1, 2, ...]
        # make a matched_tokenindex_themes_phrases_dict for the whole sentence, matched_dict
        # like {'<tokenindex1>': {themes:[theme1, theme2], phrases: {start_tokenindex, end_tokenindex}, {start_...}}

        # debug
        # if len(matched_tokenindices_ls) >0:
        #     print(matched_tokenindices_ls)
        #     print('themes:====', lemma_themes_ls)
        #     print(matched_tokenindex_themes_phrases_dict)
        # continue

        # save all tokens,with their idex number and start/end char position
        tokens_ls =[]
        for token in doc:
            tokentext = token.text_with_ws
            # tokenlemma = token.lemma_.lower()
            tokenindex = token.i
            tokenstart = token.idx # start and end position of the token text in the sentence string
            tokenend = tokenstart + len(tokentext)-1
            tmp_dict ={ "index":tokenindex, "start":tokenstart, "end":tokenend}
            
            if tokenindex in matched_tokenindices_ls:
                tmp_dict['lemma'] = token.lemma_.lower()
                tmp_dict['matched_themes'] = matched_tokenindex_themes_phrases_dict[tokenindex]['themes']

            # token in a matched phrase is not necessariely a token with matched lemma ('affordable housing', affordable is in the phrase, but may not be a matched lemma)            
            
            # get all keys (token indices) in matched_tokenindex_themes_phrases_dict
            try:
                matched_indices = list(matched_tokenindex_themes_phrases_dict.keys())
                tmp2_dict = []
                for matched_index in matched_indices:
                    # in all phrases that matches a token index, find those matching the current token index
                    for matched_phrase_dict in matched_tokenindex_themes_phrases_dict[matched_index]['phrases']: # like [{start_tokenindex:.., end_tokenindex}, {}]
                        if (tokenindex >= matched_phrase_dict['start_tokenindex']) & (tokenindex <= matched_phrase_dict['end_tokenindex']):
                            tmp2_dict.append(matched_phrase_dict)
                    if len(tmp2_dict) >0:
                        tmp_dict['in_matched_phrases'] = tmp2_dict
            except:
                pass

            tokens_ls.append(tmp_dict)
        sent_dict['tokens'] = tokens_ls

        # print(sent_dict)

    # write to dist
    targetfile = cwd + '/pyflaskapps/data/output/policyanalysis/04_sents_minutes_lemmathemes_matched.json'
    with open(targetfile, 'w') as f:
        json.dump(sents_ls, f)
##################################################################################################



def part1_split_sent_into_tokens(text):
    # print ('part1_split_sent_into_tokens ===========')   

    import spacy
    print('Loading en_core_web_lg, in part1_split_sent_into_tokens() ============ =====================')
    nlp = spacy.load('en_core_web_sm')
    print ('loading lg done ===============================')

    doc = nlp(text)
    tokens_ls = [token.text for token in doc]
    # print ('===tokens:', tokens_ls)
    return tokens_ls
##########################################

# read 02_text_minutes_cleaned1.json and use spacy to split into sents
# split sentences from text using spacy, and clean sentence by removing line breaks, and replace multiple spaces by one
def make_sents_minutes():

    import sys, os, uuid
    cwd = os.getcwd().replace('\\', '/') # the cwd is the location where python starts, in this case, it is C:\Personal\Virtual_Server\PHPWeb\ml_text\python
    import json
    src_jsonfile = cwd + '/pyflaskapps/data/output/policyanalysis/02_text_minutes_cleaned1.json'
    openedfile = open(src_jsonfile, encoding="UTF-8")
    srcdata_ls = json.load(openedfile)

    import spacy
    print('Loading en_core_web_lg, in make_sents_minutes() ============ =====================')
    nlp = spacy.load("en_core_web_lg") # although bigger, it contains many features (like token.vector) that are not provided (or of a wrong verion) by the _sm lib
    print('Loading en_core_web_lg, done ============ =====================')
    target_ls =[]
    for text_dict in srcdata_ls:
        text = text_dict["text"]
        doc = nlp(text)
        for sent in doc.sents:
            # cleaned_senttext = remove_unicode_chars(sent.text) #  done when cleaning text
            # cleaned_senttext = remove_line_breaks(cleaned_senttext)
            # cleaned_senttext = replace_multi_space_by_one(cleaned_senttext)

            tmp_dict={
                "sent":sent.text,  # note: sent is a spacy obj
                "uuid": str(uuid.uuid4()),
                "text":{"uuid":text_dict["uuid"]},
                "file": {
                    "basename": text_dict["file"]["basename"]
                },
                "section": {
                    "title": text_dict["section"]["title"]
                },
                "subsection": {
                    "title": text_dict["subsection"]["title"]
                }
            }
            target_ls.append(tmp_dict)

    print('target_ls ===== ', len(target_ls))

    # write the target data list to disk
    targetfile = cwd + '/pyflaskapps/data/output/policyanalysis/03_sentences_minutes.json'
    with open(targetfile, 'w') as f:
        json.dump(target_ls, f)
##########################################


def make_sent_dep_tree(text, targetfile):
    # covert to doc
    import spacy, os, json
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    # find the root (the core verb of the sentence)
    # about token attributes: https://spacy.io/usage/linguistic-features 
    def get_root(doc):
        for token in doc:
            # dep = token.dep_
            if (token.dep_ =='ROOT') :
                root_token = token
                return root_token

    # make a hierarchy tree of the tokens according to their dependent relationships
    def make_token_tree(token, side):
        dict={}
        dict['text'] = token.text
        dict['pos'] = token.pos_
        dict['tag'] = token.tag_
        dict['name'] = token.text + ' _|'+ side +'|_ ' + token.dep_
        if token.children:
            children=[]
            for child in token.lefts:
                children.append(make_token_tree(child, 'left'))
            for child in token.rights:
                children.append(make_token_tree(child, 'right'))
            dict['children'] = children
        return dict


    # make simplified sentences, only contains a subject, a root verb, and a object (if they are available)
    def make_sent_base(parent_token):
        thesubject=''
        for token in parent_token.lefts:
            if token.dep_.startswith('nsubj'):
                thesubject=token.text_with_ws
        theobject=''
        for token in parent_token.rights:
            if token.dep_ in ['dobj', 'acomp', 'xcomp', 'attr']:
                theobject=token.text_with_ws
        str_base_tokens=[thesubject, parent_token.text_with_ws, theobject]
        base_sent = ''
        for ele in str_base_tokens:
            base_sent = base_sent + ele
        # print (str_base_tokens)
        # print (base_sent)
        return {"text_base_tokens":str_base_tokens, "base_sentence":base_sent}

    sent_trees = {"name":"text", "children": []}
    # loop for each sentence
    for sent in doc.sents:
        # 1. get the root of each sent
        root_token = get_root(sent)
        # 2. get a dict of the dependent tree of the sentence
        dep_tree_dict = make_token_tree(root_token, '')
        # 3. get basic structure of the sentence
        base=make_sent_base(root_token)
        text_base_tokens_ls = base['text_base_tokens']
        base_sent = base['base_sentence']
        components_this_sent ={"name":base_sent, "text_base_tokens":text_base_tokens_ls, "children": [dep_tree_dict] }
        sent_trees['children'].append(components_this_sent)

    # print(sent_trees)
    cwd = os.getcwd().replace('\\', '/') 
    # targetfile = cwd + '/pyflaskapps/data/output/lit/sent_dep_tree.json'
    with open(targetfile, 'w') as f:
        json.dump(sent_trees, f)
##########################################


def get_dep_diagram_html(text):

    import spacy
    nlp = spacy.load('en_core_web_sm')

    from spacy import displacy

    doc = nlp(text)

    html = displacy.render(doc, style="dep")

    return html

    # for token in doc:
    #     print (token.text, token.tag_, token.head.text, token.dep_)

    # # auto open a browser tag and go to the url
    # # note: need to run webbrowser.open() first. If displacy.serve() runs first, it'll stop there, and prevent running webbrowser.open()
    # # the delay for webbrowser.open() (i.e., delay when opening a browser and going to the url) is long enough to catch the contents rendered by displacy.serve()
    # # https://docs.python.org/3.7/library/webbrowser.html
    # # (venv) $ pip install webbrowser
    # portint=1234
    # import webbrowser
    # url = 'http://localhost:' + str(portint) + '/'
    # # webbrowser.open_new_tab(url)
    # webbrowser.open(url)

    # displacy.serve(doc, style='dep',port=portint, host="127.0.0.1")
##########################################
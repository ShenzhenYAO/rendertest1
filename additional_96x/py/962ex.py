import sys, os, json, gzip , re 



cwd = os.getcwd().replace('\\', '/') # the cwd is the location where python starts, in this case, it is C:\Personal\Virtual_Server\PHPWeb\ml_text\python
# add the location of the py common module file 
# location_commonmodules = cwd + '/pyflaskapps/common_pymodules'
# sys.path.insert(1, location_commonmodules) # add the location at the top of the sys.path, thus, by default, the py script file spacy_modules will be loaded from there
# from modules_common import * 
# from modules_spacy import * 

tmpdir= '/additional_96x/data/history/'
tmpoutdir  = '/additional_96x/data/history/out/' 


# read the bigtext gz
def clean5_get_ents_ncs():
    phrases_ls =[]
    for nn in ["1", "2"]:
        gzlocation = cwd + tmpoutdir+ '/entities_cleaned4_nounchunks_bigtext_{}.json.gz'.format(nn)
        # print(corpusfilepath)
        with gzip.open(gzlocation, 'r') as fin:        
            json_bytes = fin.read()      
        # convert bytes to string
        json_str = json_bytes.decode('utf-8')  
        # convert string to json  
        srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
        ents_ncs_ls = srcjson['data']
        # get all labels
        
        new_ents_ncs_ls =[]
        exclude_words='www., zoom'
        exclude_words_ls = [x.strip() for x in exclude_words.split(',')]
        # print(34, exclude_words_ls)

        remove_words = 'january, fabruary, march, april, may, june, july, august, september, october, november, december, by-law, zone, year-, years, year'
        remove_words_ls = [x.strip() for x in remove_words.split(',')]

        for x in ents_ncs_ls:
            # x['text'] = x['text'].replace(r'^(\"', "")
            input = x['text'].lower()
            for y in exclude_words_ls:
                if y in input:
                    input=""
            for y in remove_words_ls:
                input = input.replace(y, "")
            while True:
                output = re.sub(r'^[\"\'#$,.%+\*-:\\_\]\[\>\}\|]', "", input).strip()
                pattern = re.compile('(^|\. )a\s+')
                output = re.sub(pattern, "", input).strip()
                output = re.sub(r'^[\"\'#$,.%+\*-:\\_\]\[\>\}\|]', "", input).strip()
                if output == input:
                    break
                input = output
            output = output.replace('\"', "")

            if len(output) > 0:
                if (output not in phrases_ls):
                    phrases_ls.append(output) # "do not change x['text]"
                new_ents_ncs_ls.append(x)

        print(len(ents_ncs_ls), len(new_ents_ncs_ls))


        # save ents_ncs 
        jsonobj = {
            'sources': [
                cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_cleaned4_nounchunks_bigtext_{}.json.gz'.format(nn),
            ],
            "description": "cleaned by excluding entities that are like a section title (begins with a section title like string",
            'program': r'C:\Users\syao2\AppData\Local\MyWorks\js\ml_text\python\pyflaskapps\example15_spacytests\pymodules\spacy\tests\test962e.py',
            'data': new_ents_ncs_ls
        }

        # save all entites and noun chunks
        targetjsonfile = cwd + tmpoutdir + '/entities_cleaned5_nounchunks_bigtext_{}.json.gz'.format(nn)
        json_str = json.dumps(jsonobj) # convert to string
        json_bytes = json_str.encode('utf-8') # convert to bytes
        with gzip.open(targetjsonfile, 'w') as f:
            f.write(json_bytes)

    phrases_ls.sort(reverse=True)
    print(len(phrases_ls))
    targetfile = cwd + tmpoutdir + '/test_phrases_clean5.json' 
    with open(targetfile, 'w') as f:
        json.dump(phrases_ls, f)
        
clean5_get_ents_ncs()

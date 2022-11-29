# what is going on!!!!!

import sys, os, json, gzip 

cwd = os.getcwd().replace('\\', '/')
print (cwd)

# load the json
tmpdir= '/additional_96x/data/history/'
tmpoutdir  = '/additional_96x/data/history/out/'


# # where is the word 'warming???'
# 962a1
# for nn in ["1", "2"]:
#     gzlocation = cwd + tmpoutdir + '/phrases_otherthemes_uncleaned_bigtext_{}.json.gz'.format(nn)
#     # print(corpusfilepath)
#     with gzip.open(gzlocation, 'r') as fin:        
#         json_bytes = fin.read()      
#     # convert bytes to string
#     json_str = json_bytes.decode('utf-8')  
#     # convert string to json  
#     srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}

#     this_ls = srcjson['data']
#     for x in this_ls:
#         text = x['text']
#         if 'housing' in text:
#             print(x)




# # 962a2
# for nn in ["1", "2"]:
#     gzlocation = cwd + tmpoutdir + '/entities_cleaned0_nounchunks_bigtext_{}.json.gz'.format(nn)
#     # print(corpusfilepath)
#     with gzip.open(gzlocation, 'r') as fin:        
#         json_bytes = fin.read()      
#     # convert bytes to string
#     json_str = json_bytes.decode('utf-8')  
#     # convert string to json  
#     srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
#     this_ls = srcjson['data']
#     # print(this_ls[0])

#     for x in this_ls:
#         text = x['text']
#         if 'housing' in text:
#             print(x)


# # ## 962a3x
# for nn in ["1", "2"]:
#     gzlocation = cwd + tmpoutdir + '/entities_cleaned1_nounchunks_bigtext_{}.json.gz'.format(nn)
#     # print(corpusfilepath)
#     with gzip.open(gzlocation, 'r') as fin:        
#         json_bytes = fin.read()      
#     # convert bytes to string
#     json_str = json_bytes.decode('utf-8')  
#     # convert string to json  
#     srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
#     this_ls = srcjson['data']
#     # print(this_ls[0])

#     for x in this_ls:
#         text = x['text']
#         if 'housing' in text:
#             print(x)

## 962bx
# for nn in ["1", "2"]:
#     gzlocation = cwd + tmpoutdir + '/entities_cleaned2_nounchunks_bigtext_{}.json.gz'.format(nn)
#     # print(corpusfilepath)
#     with gzip.open(gzlocation, 'r') as fin:        
#         json_bytes = fin.read()      
#     # convert bytes to string
#     json_str = json_bytes.decode('utf-8')  
#     # convert string to json  
#     srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
#     this_ls = srcjson['data']
#     # print(this_ls[0])

#     for x in this_ls:
#         text = x['text']
#         if 'housing' in text:
#             print(x)


# # ## 962cx
# for nn in ["1", "2"]:
#     gzlocation = cwd + tmpoutdir + '/entities_cleaned3_nounchunks_bigtext_{}.json.gz'.format(nn)
#     # print(corpusfilepath)
#     with gzip.open(gzlocation, 'r') as fin:        
#         json_bytes = fin.read()      
#     # convert bytes to string
#     json_str = json_bytes.decode('utf-8')  
#     # convert string to json  
#     srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
#     this_ls = srcjson['data']
#     # print(this_ls[0])

#     for x in this_ls:
#         text = x['text']
#         if 'housing' in text:
#             print(x)

# ## 962dx
# for nn in ["1", "2"]:
#     gzlocation = cwd + tmpoutdir + '/entities_cleaned4_nounchunks_bigtext_{}.json.gz'.format(nn)
#     # print(corpusfilepath)
#     with gzip.open(gzlocation, 'r') as fin:        
#         json_bytes = fin.read()      
#     # convert bytes to string
#     json_str = json_bytes.decode('utf-8')  
#     # convert string to json  
#     srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
#     this_ls = srcjson['data']
#     # print(this_ls[0])

#     gzlocation = cwd + tmpoutdir + 'bigtext_and_sents_pos_in_bigtext_{}.json.gz'.format(nn)
#     # print(corpusfilepath)
#     with gzip.open(gzlocation, 'r') as fin:        
#         json_bytes = fin.read()      
#     # convert bytes to string
#     json_str = json_bytes.decode('utf-8')  
#     # convert string to json  
#     srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
#     bigtext = srcjson['data']['bigtext']
#     # print(len(bigtext))

#     for x in this_ls:
#         text = x['text']
#         st = bigtext[x['start']:x['end']+1]
#         if ('housing' in text.lower()) | ('housing' in st.lower()):
#             print(x, st)

# ## 962ex
# for nn in ["1", "2"]:
#     gzlocation = cwd + tmpoutdir + '/entities_cleaned5_nounchunks_bigtext_{}.json.gz'.format(nn)
#     # print(corpusfilepath)
#     with gzip.open(gzlocation, 'r') as fin:        
#         json_bytes = fin.read()      
#     # convert bytes to string
#     json_str = json_bytes.decode('utf-8')  
#     # convert string to json  
#     srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
#     this_ls = srcjson['data']
#     # print(this_ls[0])

#     gzlocation = cwd + tmpoutdir + 'bigtext_and_sents_pos_in_bigtext_{}.json.gz'.format(nn)
#     # print(corpusfilepath)
#     with gzip.open(gzlocation, 'r') as fin:        
#         json_bytes = fin.read()      
#     # convert bytes to string
#     json_str = json_bytes.decode('utf-8')  
#     # convert string to json  
#     srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
#     bigtext = srcjson['data']['bigtext']
#     # print(len(bigtext))

#     for x in this_ls:
#         text = x['text']
#         st = bigtext[x['start']:x['end']+1]
#         if ('housing' in text.lower()) | ('housing' in st.lower()):
#             print(x, st)

## 964x
# str1 = "CONSENT PUBLIC COMMENT".lower()
# str1="housing"
# nn=1
# for nn in ["1", "2"]:
#     gzlocation = cwd + tmpoutdir + '/bigtext_and_sents_pos_in_bigtext_and_entsncs_{}.json.gz'.format(nn)
#     # print(corpusfilepath)
#     with gzip.open(gzlocation, 'r') as fin:        
#         json_bytes = fin.read()      
#     # convert bytes to string
#     json_str = json_bytes.decode('utf-8')  
#     # convert string to json  
#     srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
#     this_ls = srcjson['data']
#     # print(155, this_ls['sents_pos'][0])

#     gzlocation = cwd + tmpoutdir + 'bigtext_and_sents_pos_in_bigtext_{}.json.gz'.format(nn)
#     # print(corpusfilepath)
#     with gzip.open(gzlocation, 'r') as fin:        
#         json_bytes = fin.read()      
#     # convert bytes to string
#     json_str = json_bytes.decode('utf-8')  
#     # convert string to json  
#     srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
#     bigtext = srcjson['data']['bigtext']
#     # print(len(bigtext))


#     for x in this_ls['sents_pos']:
#         ents_ncs_ls = x['ents_ncs']
#         for y in ents_ncs_ls:
#             if (str1 in y):
#                 print(x)
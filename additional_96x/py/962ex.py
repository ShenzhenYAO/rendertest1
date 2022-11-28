# what is going on!!!!!

import sys, os, json, gzip 

cwd = os.getcwd().replace('\\', '/')
print (cwd)

# load the json
tmpdir= '/additional_96x/data/history/'
tmpoutdir  = '/additional_96x/data/history/out/'


# # where is the word 'warming???'
## 962a1
# nn=2
# gzlocation = cwd + tmpoutdir + '/phrases_otherthemes_uncleaned_bigtext_{}.json.gz'.format(nn)
# # print(corpusfilepath)
# with gzip.open(gzlocation, 'r') as fin:        
#     json_bytes = fin.read()      
# # convert bytes to string
# json_str = json_bytes.decode('utf-8')  
# # convert string to json  
# srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}

# this_ls = srcjson['data']
# for x in this_ls:
#     text = x['text']
#     if 'warm' in text:
#         print(x)

# print(this_ls[0])


## 962a2
# nn=2
# gzlocation = cwd + tmpoutdir + '/entities_cleaned0_nounchunks_bigtext_{}.json.gz'.format(nn)
# # print(corpusfilepath)
# with gzip.open(gzlocation, 'r') as fin:        
#     json_bytes = fin.read()      
# # convert bytes to string
# json_str = json_bytes.decode('utf-8')  
# # convert string to json  
# srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
# this_ls = srcjson['data']
# # print(this_ls[0])

# for x in this_ls:
#     text = x['text']
#     if 'warm' in text:
#         print(x)


# ## 962a3x
# nn=2
# gzlocation = cwd + tmpoutdir + '/entities_cleaned1_nounchunks_bigtext_{}.json.gz'.format(nn)
# # print(corpusfilepath)
# with gzip.open(gzlocation, 'r') as fin:        
#     json_bytes = fin.read()      
# # convert bytes to string
# json_str = json_bytes.decode('utf-8')  
# # convert string to json  
# srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
# this_ls = srcjson['data']
# # print(this_ls[0])

# for x in this_ls:
#     text = x['text']
#     if 'warm' in text:
#         print(x)

# ## 962bx
# nn=2
# gzlocation = cwd + tmpoutdir + '/entities_cleaned2_nounchunks_bigtext_{}.json.gz'.format(nn)
# # print(corpusfilepath)
# with gzip.open(gzlocation, 'r') as fin:        
#     json_bytes = fin.read()      
# # convert bytes to string
# json_str = json_bytes.decode('utf-8')  
# # convert string to json  
# srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
# this_ls = srcjson['data']
# # print(this_ls[0])

# for x in this_ls:
#     text = x['text']
#     if 'warm' in text:
#         print(x)


# ## 962cx
# nn=2
# gzlocation = cwd + tmpoutdir + '/entities_cleaned3_nounchunks_bigtext_{}.json.gz'.format(nn)
# # print(corpusfilepath)
# with gzip.open(gzlocation, 'r') as fin:        
#     json_bytes = fin.read()      
# # convert bytes to string
# json_str = json_bytes.decode('utf-8')  
# # convert string to json  
# srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
# this_ls = srcjson['data']
# # print(this_ls[0])

# for x in this_ls:
#     text = x['text']
#     if 'warm' in text:
#         print(x)

# ## 962dx
# nn=2
# gzlocation = cwd + tmpoutdir + '/entities_cleaned4_nounchunks_bigtext_{}.json.gz'.format(nn)
# # print(corpusfilepath)
# with gzip.open(gzlocation, 'r') as fin:        
#     json_bytes = fin.read()      
# # convert bytes to string
# json_str = json_bytes.decode('utf-8')  
# # convert string to json  
# srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
# this_ls = srcjson['data']
# # print(this_ls[0])

# for x in this_ls:
#     text = x['text']
#     if 'warm' in text:
#         print(x)

## 964x
nn=2
gzlocation = cwd + tmpoutdir + '/bigtext_and_sents_pos_in_bigtext_and_entsncs_{}.json.gz'.format(nn)
# print(corpusfilepath)
with gzip.open(gzlocation, 'r') as fin:        
    json_bytes = fin.read()      
# convert bytes to string
json_str = json_bytes.decode('utf-8')  
# convert string to json  
srcjson = json.loads(json_str)   #like {text: '...', meta: {subsection: ..., }}
this_ls = srcjson['data']
print(this_ls['sents_pos'][0])

for x in this_ls['sents_pos']:
    text = x['sent_text']
    if 'warm' in text:
        print(x)
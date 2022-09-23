# read a json from a local file
def readjson(jsonfile):
    # print ('=== running module readjson')
    import os, json
    # get the currentworking path, like C:\Personal\Virtual_Server\PHPWeb\ml_text\python
    openedfile = open(jsonfile, encoding="UTF-8")
    result = json.load(openedfile)
    return result

# get text of a subsection (e.g., a piece of motion) from a file, indicating the filename, section (like Motions, announcement, etc), and subsections
def get_subsection_text_with_src_file_section_subsection(json): # json is like vanmeetingsample.json
    result_ls =[]
    for file in json:
        # print('file name ===', file['file'])
        sections_ls=file['sections']
        for section in sections_ls:
            # print('section ===', section['title'])            
            try:
                subsections_ls = section['subsections']
                for subsection in subsections_ls:
                    try:
                        subsection_text = subsection['text']
                        tmp_dict ={}
                        tmp_dict["file"] = file["file"]
                        tmp_dict["section"] = section["title"]
                        # print('section ===', section['title'])
                        tmp_dict["subsection"] = subsection["subtitle"]
                        # print('         subsection ===', subsection['subtitle'])
                        tmp_dict["subsection_text"] = subsection_text
                        result_ls.append(tmp_dict)
                    except:
                        continue
            except:
                continue
    return result_ls


def match_rootlemma(rootlemmas, lemma_to_match):
    result = ""
    for rootlemma in rootlemmas:
        if rootlemma == lemma_to_match:
            result = rootlemma
            # print('matched lemma ==', lemma_to_match)
            break
    return result

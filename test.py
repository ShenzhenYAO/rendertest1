import spacy
nlp = spacy.load("en_core_web_sm")

# to get a nested strcuture about all 

text = "The current study was aimed at contributing to that growing body of literature, by conducting cost-benefit and cost-effectiveness analyses for the opening of SIFs in Ottawa, Ontario."

doc = nlp(text)

# find the root

def get_children(doc):
    for token in doc:
        # print(list(token.children))
        childreni_ls =[]
        for x in token.children:
            childreni_ls.append(x.i)
        print(childreni_ls)
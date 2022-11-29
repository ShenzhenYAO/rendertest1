
test953

do not select theme (have all phrases otherwise these phrases will be excluded....)
or, in 963 add them back??? (cannot, as the phrases do not have pos in the new bigtext)


A. Adding new pdfs

for the following:
Vancouver 1
Powell River, 2 *** has to rename, has to manually down load oct and nov pdf and delete adgenda and attachments. The Oct 6 package contains minutes of the Sep 22 minutes ...same for Nov 11 and Dec ..
Bowen Island, 3

... only add in the above

Sechelt, 4
West Vancouver, 5


1. pdfs: 
G:\Population Health - Regional\Department Wide\HPP Practitioner Portal\Policy Monitoring\Code\Data\Municipalities


2.html:
C:\Users\syao2\AppData\Local\MyWorks\js\policy_analysis\data\out\council_meetings\html


*** action:
usd the pdf tool in Acrobat (on the VCH machine) to convert pdf to html, save in the following html folder, then, move the html to the city-specific zips

3. json:
C:\Users\syao2\AppData\Local\MyWorks\js\policy_analysis\data\out\council_meetings\json

*** action:
In the policy analysis project folder, run node backend/js/{cityname}.js to make the city-cpecific jsons
(might need to enlarge node max mem: e.g. node --max-old-space-size=8192)


4. corpus:
C:\Users\syao2\AppData\Local\MyWorks\js\policy_analysis\data\out\council_meetings\corpus

*** action:
In the policy analysis project folder, run _make_corpus.js
In the policy analysis project folder, run _get_sections.js

the csv should be read into the excel, and make a json according to the selections manually made in the xlsx file
However, it is not updated as no need to do it (all sectons are kept in the following analysis)

******
The above creates:
in C:\Users\syao2\AppData\Local\MyWorks\js\policy_analysis\data\out\council_meetings\corpus:
meetingsubsections.json.gz
(the rest city_sections.json/csv, selected ... are not used)


*** action:
now switch to the ml_text

*** action:
test950 -- make a textacy corpus.bin, make theme-matched phrases (takes A LOT OF time --- 2 hour), there are many texts in the corpus, have to split into two list of texts and run the matching twice (each takes about 1 hour)


## should consider only take new texts and append to the existing...

1. update the textacy 
run part I of test950

2. make the following
cwd + "/pyflaskapps/data/output/new_policyanalysis/99_test/
matched_distinct_phrases_allselectedthemes.json --  although it is called selected themes, actually it contains phrases for all themes
meetingsubsections.josn.gz  -- meeting minutes by subsections


test 951 --- make distinct phrases across themes...
must run

cwd + "/pyflaskapps/data/output/new_policyanalysis/99_test/
matched_distinct_phrases_acrossthemes


test 952: -- identify future actions Note!!! keep the file combined_match.xlsx, clean rows 2:last in the sheet "combined_matches"
must run

save:
/pyflaskapps/data/output/new_policyanalysis/99_test/combined_match.xlsx
04a_corpus/corpus_withfuture_action_dates.bin.gz


test 953: phrases of selected themes (the selected 4) !!! need to keep all phrases, not only those of selected themes
!!! takes about 4 to 5 hours to complet these docs
must run

src:
cwd + "/pyflaskapps/data/output/new_policyanalysis/09_evaluate_phrases/matched_distinct_phrases_acrossthemes.json", 
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/corpus_withfuture_action_dates.bin.gz'

save:
cwd + "/pyflaskapps/data/output/new_policyanalysis/09_evaluate_phrases/matched_distinct_phrases_across_selected_themes.json"
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/sents_with_matched_phrases.json.gz'

test 954: to keep the subsections of the selected sections  -- not applied, all sections are kept, 
must run

save:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/sents_with_matched_phrases_of_selected_sections.json.gz'



test 955:  --- do not have to run, replaced by test967

save: 
cwd + "/pyflaskapps/data/output/new_policyanalysis/23_tableau/wordclouddata_allcities_auto.xlsx"

test 956: -- do no thave to run, replaced by test 968
save:
cwd + "/pyflaskapps/data/output/new_policyanalysis/23_tableau/themesdata_allcities_auto.xlsx"


test 957: --- make a map for future dates related stuff: matched_futuredates_auto.xlsx -- the target xlsx not used!
save:
cwd + "/pyflaskapps/data/output/new_policyanalysis/23_tableau/matched_futuredates_auto.xlsx"


test 959: --- for checking ... 
nothing to save


test 961: make big text and delimite text by sents  --- take about 5 minutes to run

src:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/corpus_withfuture_action_dates.bin.gz',


save:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/sents_of_all_sections_1 <or 2>.json.gz'
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/bigtext_sents_of_all_sections_1 <or 2>.json.gz'


test 962: 
src:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/bigtext_sents_of_all_sections_{}.bin.gz'.format(nn), 

save:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_uncleaned_nounchunks_bigtext_{}.json.gz'.format(nn)


***************
as a temp:
can I add all phrases from all other themes
use 962a0 to match additionally for phrases in big text?
That way I can have a ents_ncs list plus the phrases of other terms ...

I'll need 

1. python\pyflaskapps\data\output\new_policyanalysis\09_evaluate_phrases\history\matched_distinct_phrases_acrossthemes.json, like data: {phrase:..., themes:[... including all themes], }

2. cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/history/bigtext_sents_of_all_sections_{}.bin.gz'.format(nn)

3. with the above, make a dict like start, end, text, label as for ncs and ents in 962!

add the results to the 

cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/history/entities_uncleaned_nounchunks_bigtext_{}.json.gz'.format(nn)





****************

test 962a:

src:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_uncleaned_nounchunks_bigtext_{}.json.gz'.format(nn),
target:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_cleaned1_nounchunks_bigtext_{}.json.gz'.format(nn)


test 962b:

src:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_cleaned1_nounchunks_bigtext_{}.json.gz'.format(nn),
target:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_cleaned2_nounchunks_bigtext_{}.json.gz'.format(nn)


test 962c:

src:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_cleaned2_nounchunks_bigtext_{}.json.gz'.format(nn),
target:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_cleaned3_nounchunks_bigtext_{}.json.gz'.format(nn)



test 962d: --- !!! 20 minutes

src:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_cleaned3_nounchunks_bigtext_{}.json.gz'.format(nn),
target:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_cleaned4_nounchunks_bigtext_{}.json.gz'.format(nn)


test 963:

src:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/bigtext_sents_of_all_sections_{}.json.gz'.format(nn), 
save:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/bigtext_and_sents_pos_in_bigtext_{}.json.gz'.format(nn)


test 964:

src:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/bigtext_and_sents_pos_in_bigtext_{}.json.gz'.format(nn), 
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/entities_cleaned4_nounchunks_bigtext_{}.json.gz'.format(nn)

save:

cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/bigtext_and_sents_pos_in_bigtext_and_entsncs_{}.json.gz'.format(nn)


test 965:

src:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/bigtext_and_sents_pos_in_bigtext_and_entsncs_{}.json.gz'.format(nn), 
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/sents_of_all_sections_{}.json.gz'.format(nn)


save:

cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/bigtext_and_sents_pos_in_bigtext_and_entsncs_1_2.json.gz', 
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/sents_of_all_sections_1_2.json.gz'



cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/sents_of_all_sections_entsncs_{}.json.gz'.format(nn)

cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/sents_of_all_sections_entsncs_all.json.gz'


test 966:

src:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/bigtext_and_sents_pos_in_bigtext_and_entsncs_{}.json.gz'.format(nn)
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/sents_of_all_sections_1 <or 2>.json.gz'

save:
cwd + '/pyflaskapps/data/output/new_policyanalysis/04a_corpus/sents_of_all_sections_entsncs_all.json.gz'


test 967:

src:

save:
cwd + "/pyflaskapps/data/output/new_policyanalysis/23_tableau/967_wordclouddata_allcities_auto.xlsx"

test 968:

src:

save:
cwd + "/pyflaskapps/data/output/new_policyanalysis/23_tableau/968_themesdata_allcities_auto.xlsx"


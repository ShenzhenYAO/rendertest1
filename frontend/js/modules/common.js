
function show_spacy_sentences(datajson) {
    let spacycontentsbox = d3.select('div#spacycontents')
    datastr = JSON.stringify(datajson)
    spacycontentsbox.attrs({ 'sentences': datastr })
    spacycontentsbox.html('')
    datajson.forEach(d => {
        spacycontentsbox.append('p').text(d)
    })
    spacycontentsbox.styles({
        'display': 'block', 'border': '1px lightgrey solid', 'width': '80%', 'padding': '10px', 'font-size': '16px', 'line-height': '150%',
        'max-height': '380px', 'overflow': 'auto'
    })
} //show_spacy_sentences

async function get_spacytest_data() {

    // get the text in the text box
    let text = d3.select('div#textbox').text().trim()
    if (text.length === 0) { return }

    // console.log(update_keywords_objsents)
    // send a request to the backend to get summary
    d3.select('div#coverall').remove()
    // when a request is sent, temporarily disable everything by adding a cover all box (note: must select position: absolute)
    // so weird, to let text stay in the middle of the div, make 'line-height' = the full window height
    d3.select('body').append('div').attrs({ 'id': 'coverall' }).styles(
        {
            'background-color': 'rgba(0,0,0,0.0)', 'width': '100%', 'height': '100%', 'z-index': '100000', 'position': 'absolute', 'left': '0px', 'top': '0px',
            'color': 'lightgrey', 'text-align': 'center', 'line-height': (window.innerHeight * 1.5) + 'px', 'font-family': 'arial', 'font-size': '100px', 'font-weight:': 'bold'
        }
    ).text('Wait...')

    let somedata_filelocation = '/data/in/test/test.json'

    let requesttask = 'get_spacytest_data' // to save and excel file of text that having different machine v1 labelling and human labelling

    let requestdatajson = {
        requesttask: requesttask,
        requestdatafromfrontend: {
            location: { somedata_filelocation: somedata_filelocation },
            data: text
        } // requestdatafromfrontend
    } // requestdatajson

    let requestdatajson_str = JSON.stringify(requestdatajson)
    let url = '/backend'

    // send a request to backend
    function ajaxcall() {
        return $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: requestdatajson_str,
            success: function (responsedatajson_str) {
                // remove the cover all div
                d3.select('div#coverall').remove()

                let responsedatajson = JSON.parse(responsedatajson_str)
                console.log(responsedatajson)
                let responsedata = responsedatajson['responsedatafrombackend']
                // console.log(responsedata)  
                show_spacy_sentences(responsedata)

            } // success
        }) // ajax
    } // function ajaxcall8
    return $.when(ajaxcall()).done(async () => {
    })
} // get_spacytest_data


function show_some_data(datajson) {
    let textbox = d3.select('div#textbox')
    datastr = JSON.stringify(datajson)
    textbox.attrs({ 'textdata': datastr, 'contenteditable': 'true' })
    textbox.text(datajson[0])
    textbox.styles({ 'display': 'block', 'border': '1px lightgrey solid', 'width': '80%', 'padding': '10px', 'font-size': '16px', 'line-height': '150%' })
} //show_some_data


async function get_some_data() {
    // console.log(update_keywords_objsents)
    // send a request to the backend to get summary
    d3.select('div#coverall').remove()
    // when a request is sent, temporarily disable everything by adding a cover all box (note: must select position: absolute)
    // so weird, to let text stay in the middle of the div, make 'line-height' = the full window height
    d3.select('body').append('div').attrs({ 'id': 'coverall' }).styles(
        {
            'background-color': 'rgba(0,0,0,0.0)', 'width': '100%', 'height': '100%', 'z-index': '100000', 'position': 'absolute', 'left': '0px', 'top': '0px',
            'color': 'lightgrey', 'text-align': 'center', 'line-height': (window.innerHeight * 1.5) + 'px', 'font-family': 'arial', 'font-size': '100px', 'font-weight:': 'bold'
        }
    ).text('Wait...')

    let somedata_filelocation = '/data/in/test/test.json'

    let requesttask = 'get_some_data' // to save and excel file of text that having different machine v1 labelling and human labelling

    let requestdatajson = {
        requesttask: requesttask,
        requestdatafromfrontend: {
            location: { somedata_filelocation: somedata_filelocation },
        } // requestdatafromfrontend
    } // requestdatajson

    let requestdatajson_str = JSON.stringify(requestdatajson)
    let url = '/backend'

    // send a request to backend
    function ajaxcall() {
        return $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: requestdatajson_str,
            success: function (responsedatajson_str) {
                // remove the cover all div
                d3.select('div#coverall').remove()

                let responsedatajson = JSON.parse(responsedatajson_str)
                console.log(responsedatajson)
                let responsedata = responsedatajson['responsedatafrombackend']
                // console.log(responsedata)  

                show_some_data(responsedata)

            } // success
        }) // ajax
    } // function ajaxcall8
    return $.when(ajaxcall()).done(async () => {
    })
} // get_some_data

async function get_processed_textjson() {

    // get the text json to be processed

    let srctextjsonloaction = 'static/testdata/epub_to_json/25091704.json' //'static/testdata/epub_to_json/19423324.json' // 'static/testdata/epub_to_json/ferguson_war.json'
    let urlgznocache = srctextjsonloaction + '?v=' + new Date().getTime()
    let srcentities_arr = await d3.json(urlgznocache).then(d => { return d }) // like [{entity1:..., text: "..." }, {entity2:..., }]
    let articlename = "25091704" //"ferguson_war"
    let json_fromfront = { article: articlename, entities: srcentities_arr }
    // console.log(srctexts_arr)

    // send a request to the backend to get summary
    d3.select('div#coverall').remove()
    // when a request is sent, temporarily disable everything by adding a cover all box (note: must select position: absolute)
    // so weird, to let text stay in the middle of the div, make 'line-height' = the full window height
    d3.select('body').append('div').attrs({ 'id': 'coverall' }).styles(
        {
            'background-color': 'rgba(0,0,0,0.0)', 'width': '100%', 'height': '100%', 'z-index': '100000', 'position': 'absolute', 'left': '0px', 'top': '0px',
            'color': 'lightgrey', 'text-align': 'center', 'line-height': (window.innerHeight * 1.5) + 'px', 'font-family': 'arial', 'font-size': '100px', 'font-weight:': 'bold'
        }
    ).text('Wait...')


    let requesttask = 'get_processed_textjson' // 

    let requestdatajson = {
        requesttask: requesttask,
        requestdatafromfrontend: json_fromfront,
        // requestdatafromfrontend
    } // requestdatajson

    // consider sending a gz buffer instead of a json string !!!

    let requestdatajson_str = JSON.stringify(requestdatajson)
    let url = '/backend'
    // let url = `${_pythontest1url}/backend` // need to set cors at backend (flask_cors.CORS)
    // console.log(url)

    // send a request to backend
    function ajaxcall() {
        return $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: requestdatajson_str,
            success: function (responsedatajson_str) {
                // remove the cover all div
                d3.select('div#coverall').remove()

                let responsedatajson = JSON.parse(responsedatajson_str)
                // console.log(responsedatajson)
                let responsedata = responsedatajson['responsedatafrombackend'] // like [{meta:..., data:{article:, entity:, text:, etc}}]
                console.log(responsedata)

                let processed_textjson_str = JSON.stringify(responsedata)
                d3.select('div#metadatadiv').attrs({ "processedtextjson_from_pyapp": processed_textjson_str })


            } // success
        }) // ajax
    } // function ajaxcall8
    return $.when(ajaxcall()).done(async () => {
    })
} // get_processed_textjson


async function make_test_page() {

    let stage_d3pn = d3.select('div#stage')
    stage_d3pn.html('')

    stage_d3pn.append('p').styles({ 'margin-left': '10px', 'width': '80%', 'font-size': '14px' })
        .html(`This part is to test sending a json [{entity:..., text:...}] to 127.0.0.1:5000, use the Python app (spaCy) there to split text into sentences and tokens and send back.<br><br>By clicking the 'get PYApp treated data' button, the current project sends a request to the python site, fetch result (the processed text json and save in metadatdiv's attr 'processedtextjson_from_pyapp'). `)
    stage_d3pn.append('p')

    stage_d3pn.append('button').text('get PYApp treated data').styles({ 'margin-left': '10px' }).on('click', async (event) => { await get_processed_textjson() })
    stage_d3pn.append('p')

    // stage_d3pn.append('p').styles({ 'margin-left': '10px', 'width': '80%', 'font-size': '14px' })
    //     .html(`This part is to test fetching data from a Python API, which has been deployed at ${_pythontest1url}.<br><br>By clicking the 'Load data' button, the current project sends a request to the python site for a text paragraph which has been pre-stored at the backend of the Python API project. The text paragraph is then returned by the Python API to the current project and displayed in a text box (which is current hidden) below the button 'Load data'.<br><br>The second button 'spaCy it' only works when a text paragraph is brought about in the text box. It captures the contents in the text box, and send a request to the Python API for splitting the text into sentences by the spaCy methods. The sentences are then returned by the Python API to the current project, and displayed in the sentence box (which is hidden now) below the 'spaCy it' button.`)
    // stage_d3pn.append('p')

    // stage_d3pn.append('button').text('Load data').styles({ 'margin-left': '10px' }).on('click', async (event) => { await get_some_data() })
    // stage_d3pn.append('p')

    // stage_d3pn.append('div').attrs({ 'id': 'textbox' }).styles({ 'display': 'none' })
    // stage_d3pn.append('p')

    // stage_d3pn.append('button').text('spaCy it').styles({ 'margin-left': '10px' }).on('click', async (event) => { await get_spacytest_data() })
    // stage_d3pn.append('p')

    stage_d3pn.append('div').attrs({ 'id': 'spacycontents' }).styles({ 'display': 'none' })

} // async function make_lit_search_elements()


async function make_vchdemo_page() {

    let stage_d3pn = d3.select('div#stage')
    stage_d3pn.html('')

    stage_d3pn.append('p').styles({ 'margin-left': '10px', 'width': '80%', 'font-size': '14px' })
        .html(`
        <b>Demo tasks:</b> <br>
        <ul>
            <li id='token'>get tokens, lemmas, pos</li>
            <li id='ent'>get entities and noun chunks </li>
            <li id='phrase'>matching theme phrases by pattern </li>
            <li id='clean'>text cleaning</li>
        </ul>       
        `)
    stage_d3pn.selectAll('li').styles({ 'margin': '10px 0' })
    stage_d3pn.append('p')

    d3.select('li#token').on('click', task_token)
    d3.select('li#ent').on('click', task_ent)
    d3.select('li#phrase').on('click', task_phrase)
    d3.select('li#clean').on('click', task_clean)


    // stage_d3pn.append('button').text('get PYApp treated data').styles({ 'margin-left': '10px' }).on('click', async (event) => { await get_processed_textjson() })
    // stage_d3pn.append('p')

    // stage_d3pn.append('p').styles({ 'margin-left': '10px', 'width': '80%', 'font-size': '14px' })
    //     .html(`This part is to test fetching data from a Python API, which has been deployed at ${_pythontest1url}.<br><br>By clicking the 'Load data' button, the current project sends a request to the python site for a text paragraph which has been pre-stored at the backend of the Python API project. The text paragraph is then returned by the Python API to the current project and displayed in a text box (which is current hidden) below the button 'Load data'.<br><br>The second button 'spaCy it' only works when a text paragraph is brought about in the text box. It captures the contents in the text box, and send a request to the Python API for splitting the text into sentences by the spaCy methods. The sentences are then returned by the Python API to the current project, and displayed in the sentence box (which is hidden now) below the 'spaCy it' button.`)
    // stage_d3pn.append('p')

    // stage_d3pn.append('button').text('Load data').styles({ 'margin-left': '10px' }).on('click', async (event) => { await get_some_data() })
    // stage_d3pn.append('p')

    // stage_d3pn.append('div').attrs({ 'id': 'textbox' }).styles({ 'display': 'none' })
    // stage_d3pn.append('p')

    // stage_d3pn.append('button').text('spaCy it').styles({ 'margin-left': '10px' }).on('click', async (event) => { await get_spacytest_data() })
    // stage_d3pn.append('p')

    stage_d3pn.append('div').attrs({ 'id': 'input', 'contenteditable': 'true' }).styles({ 'box-shadow': 'none', 'display': 'none', 'border': "1px solid grey", 'width': '90%', 'max-height': '200px', 'overflow': 'auto', 'padding': '5px' })
    // stage_d3pn.append('div').attrs({ 'id': 'output', 'contenteditable': 'true' }).styles({ 'display': 'none', 'border':"1px solid grey", 'width':'80%', 'max-height':'200px', 'overflow':'auto', 'padding':'5px'  })

} // async function make_lit_search_elements()


/// following are special tasks for VCH Demo

/////task clean ////////////////////////////////////////////////////////////////////////////////



async function task_clean() {
    let stage_d3pn = d3.select('div#stage')
    stage_d3pn.select('div#input').remove()
    stage_d3pn.selectAll('.demotask').remove()


    stage_d3pn.append('label').attrs({ 'class': 'demotask' }).styles({ 'class': 'demotask', 'font-weight': 'bold' }).text('Input')
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })
    stage_d3pn.append('div').attrs({ 'id': 'input', 'class': 'demotask', 'contenteditable': 'true' })
        .styles({
            'display': 'none', 'border': "0px solid grey", 'width': '90%', 'max-height': '200px',
            'overflow': 'auto', 'padding': '5px', 'font-size': '16px', 'font-family': 'Arial', 'line-height': '1.5'
        })
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })

    stage_d3pn.append('label').attrs({ 'class': 'demotask' }).styles({ 'margin-top': '50px', 'font-weight': 'bold' }).text('Output')
    stage_d3pn.append('button').attrs({ 'class': 'demotask' }).text('Go').styles({ 'margin-left': '10px', 'margin-left': '10px' })
        .on('click', async (event) => { await get_cleaned_text() })
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })
    stage_d3pn.append('div').attrs({ 'id': 'output', 'class': 'demotask', 'contenteditable': 'false' })
        .styles({ 'display': 'none', 'border': "1px solid lightgrey", 'max-height': '300px', 'overflow': 'auto', 'padding': '5px', 'line-height': '1.5', 'width': '90%' })
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })

    stage_d3pn.append('label').attrs({ 'class': 'demotask', 'id': 'code' }).styles({ 'margin-top': '50px', 'class': 'demotask', 'font-weight': 'bold' }).text('')
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })
    stage_d3pn.append('div').attrs({ 'id': 'codebox', 'class': 'demotask', 'contenteditable': 'false' })
        .styles({ 'resize': 'both', 'width': '80%', 'display': 'none', 'border': "0px solid grey", 'overflow': 'auto', 'padding': '5px', 'background-color': 'black' })


    let text = `Almost 7,000 British Columbians \u2022 \u0027 have died from the Province ʼs poisoned,,,,    unre-\ngulated drug supply since the overdose public health emergency was declared on April 14, 2016. 

    www.civicworld.net 
    
    •	Moreover, subsequent to       the declaration of the COVID-19 public       health emergency on March 17, 2020, the rate of overdose events and illicit drug toxicity deaths have increased and surpassed historic highs
    https://www.civicworld.net
     
    
                                                     The City of Vancouver has likewise signalled a state of emergency with respect to the unregulated, contaminated                                                    drug supply \u2022 \u0027 and the associated opioid-related overdose deaths. 
    (604)123-4567 nowhere@mybox.com
    
                      In July 2019, Vancouver City Council approved the Safe Supply Statement, created in collaboration with the Vancouver Community Action Team, whereby the City will share with other government partners, including the Government of Canada, and advocate for access to a safe,   regu-\nlated drug supply. *********************************************
    
    `

    let inputbox = d3.select('div#input')
    inputbox.text(text).styles({ 'display': 'block' })

}



async function get_cleaned_text() {


    // get the text in the text box
    let text = d3.select('div#input').node().textContent.trim()
    // console.log(text)
    if (text.length === 0) { return }

    // console.log(update_keywords_objsents)
    // send a request to the backend to get summary
    d3.select('div#coverall').remove()
    // when a request is sent, temporarily disable everything by adding a cover all box (note: must select position: absolute)
    // so weird, to let text stay in the middle of the div, make 'line-height' = the full window height
    d3.select('body').append('div').attrs({ 'id': 'coverall' }).styles(
        {
            'background-color': 'rgba(0,0,0,0.0)', 'width': '100%', 'height': '100%', 'z-index': '100000', 'position': 'absolute', 'left': '0px', 'top': '0px',
            'color': 'lightgrey', 'text-align': 'center', 'line-height': (window.innerHeight * 1.5) + 'px', 'font-family': 'arial', 'font-size': '100px', 'font-weight:': 'bold'
        }
    ).text('Wait...')

    let requesttask = 'get_cleaned_text' // to save and excel file of text that having different machine v1 labelling and human labelling

    let requestdatajson = {
        requesttask: requesttask,
        requestdatafromfrontend: {
            // location: { somedata_filelocation: somedata_filelocation },
            data: text
        } // requestdatafromfrontend
    } // requestdatajson
    // console.log(requestdatajson['requestdatafromfrontend']['data'])
    let requestdatajson_str = JSON.stringify(requestdatajson)
    let url = '/backend'

    // send a request to backend
    function ajaxcall() {
        return $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: requestdatajson_str,
            success: function (responsedatajson_str) {
                // remove the cover all div
                d3.select('div#coverall').remove()

                let responsedatajson = JSON.parse(responsedatajson_str)
                console.log(responsedatajson)
                let responsedata = responsedatajson['responsedatafrombackend']
                // console.log(responsedata)  
                show_cleaned_text(responsedata)

            } // success
        }) // ajax
    } // function ajaxcall8
    return $.when(ajaxcall()).done(async () => {
    })
} // get_spacytest_data

async function show_cleaned_text(responsedata) {
    // console.log(responsedata)
    // make a table in the outbox
    let outbox_d3pn = d3.select('div#output').styles({ 'display': 'block', 'border': '1px solid grey' })
    let cleaned_text = responsedata['cleaned_text']
    outbox_d3pn.text(cleaned_text)

    // display code in the box
    d3.select('label#code').text('Python code:')
    let codebox_d3pn = d3.select('div#codebox').styles({ "display": "block" })
    let codestr = `<pre><code class="python">def clean_text_rendertest1(text):
    import textacy.preprocessing 
    preproc = textacy.preprocessing.make_pipeline(
        textacy.preprocessing.normalize.unicode, # does not seem to work, cannot remove é \t \u2022 \u0027 ...
        textacy.preprocessing.normalize.quotation_marks, # convert ʼ to '
        textacy.preprocessing.normalize.whitespace, # replace non-break spaces/zero with spaces with a normal space, strip leading/trailing spaces
        textacy.preprocessing.normalize.bullet_points, # replace special bullet points like \u2022(•) with '-'
        textacy.preprocessing.normalize.hyphenated_words, # remove hyphens split the word into segments different lines like Shakes- peare without affecting the hyphens in a normal setting like semi_conductor
    )
    cleanedtext = preproc(text)
    cleanedtext = textacy.preprocessing.normalize.repeating_chars(cleanedtext, chars="*")
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
    </code></pre>
    `
    codebox_d3pn.html(codestr)
    hljs.initHighlightingOnLoad();

}

////////////////////////////////////////////////////////////////////task clean



/////task phrase ////////////////////////////////////////////////////////////////////////////////

async function task_phrase() {
    let stage_d3pn = d3.select('div#stage')
    stage_d3pn.select('div#input').remove()
    stage_d3pn.selectAll('.demotask').remove()


    stage_d3pn.append('label').attrs({ 'class': 'demotask' }).styles({ 'font-weight': 'bold' }).text('Key words/phrases')
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })
    let keywords_d3pn = stage_d3pn.append('div').attrs({ 'id': 'keywords', 'class': 'demotask', 'contenteditable': 'true' })
        .styles({
            'display': 'block', 'border': "0px solid grey", 'width': '90%', 'max-height': '200px', 'overflow': 'auto', 'padding': '5px',
            'font-size': '16px', 'font-family': 'Arial', 'line-height': '1.5'
        })
    keywords_d3pn.node().textContent = 'overdose | opioid'
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })


    stage_d3pn.append('label').attrs({ 'class': 'demotask' }).styles({ 'font-weight': 'bold' }).text('Input')
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })
    stage_d3pn.append('div').attrs({ 'id': 'input', 'class': 'demotask', 'contenteditable': 'true' })
        .styles({
            'display': 'none', 'border': "0px solid grey", 'width': '90%', 'max-height': '200px', 'overflow': 'auto', 'padding': '5px',
            'font-size': '16px', 'font-family': 'Arial', 'line-height': '1.5'
        })
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })

    stage_d3pn.append('label').attrs({ 'class': 'demotask' }).styles({ 'margin-top': '50px', 'font-weight': 'bold' }).text('Output')
    stage_d3pn.append('button').attrs({ 'class': 'demotask' }).text('Go').styles({ 'margin-left': '10px', 'margin-left': '10px' })
        .on('click', async (event) => { await get_phrase() })
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })
    stage_d3pn.append('div').attrs({ 'id': 'output', 'class': 'demotask', 'contenteditable': 'false' }).styles({ 'display': 'none', 'border': "1px solid grey", 'max-height': '300px', 'overflow': 'auto', 'padding': '5px' })
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })

    stage_d3pn.append('label').attrs({ 'class': 'demotask', 'id': 'code' }).styles({ 'margin-top': '50px', 'class': 'demotask', 'font-weight': 'bold' }).text('')
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })
    stage_d3pn.append('div').attrs({ 'id': 'codebox', 'class': 'demotask', 'contenteditable': 'false' })
        .styles({ 'resize': 'both', 'width': '80%', 'display': 'none', 'border': "1px solid grey", 'overflow': 'auto', 'padding': '5px' })

    let text = `Almost 7,000 British Columbians have died from the Province's poisoned, unregulated drug supply since the overdose public health emergency was declared on April 14, 2016. Moreover, subsequent to the declaration of the COVID-19 public health emergency on March 17, 2020, the rate of overdose events and illicit drug toxicity deaths have increased and surpassed historic highs. The City of Vancouver has likewise signalled a state of emergency with respect to the unregulated, contaminated drug supply and the associated opioid-related overdose deaths. In July 2019, Vancouver City Council approved the Safe Supply Statement, created in collaboration with the Vancouver Community Action Team, whereby the City will share with other government partners, including the Government of Canada, and advocate for access to a safe, regulated drug supply.`
    let inputbox = d3.select('div#input')
    inputbox.text(text).styles({ 'display': 'block' })

} // task_phrase

async function get_phrase() {

    let phrases_arr = d3.select('div#keywords').text().split('|').map(x => x.trim()).filter(x => x.length > 0)

    // get the text in the text box
    let text = d3.select('div#input').node().textContent.trim()
    // console.log(text)
    if (text.length === 0) { return }

    // console.log(update_keywords_objsents)
    // send a request to the backend to get summary
    d3.select('div#coverall').remove()
    // when a request is sent, temporarily disable everything by adding a cover all box (note: must select position: absolute)
    // so weird, to let text stay in the middle of the div, make 'line-height' = the full window height
    d3.select('body').append('div').attrs({ 'id': 'coverall' }).styles(
        {
            'background-color': 'rgba(0,0,0,0.0)', 'width': '100%', 'height': '100%', 'z-index': '100000', 'position': 'absolute', 'left': '0px', 'top': '0px',
            'color': 'lightgrey', 'text-align': 'center', 'line-height': (window.innerHeight * 1.5) + 'px', 'font-family': 'arial', 'font-size': '100px', 'font-weight:': 'bold'
        }
    ).text('Wait...')

    let requesttask = 'get_matched_phrases' // to save and excel file of text that having different machine v1 labelling and human labelling

    let requestdatajson = {
        requesttask: requesttask,
        requestdatafromfrontend: {
            phrases: phrases_arr,
            data: text
        } // requestdatafromfrontend
    } // requestdatajson
    // console.log(requestdatajson['requestdatafromfrontend']['phrases'])
    let requestdatajson_str = JSON.stringify(requestdatajson)
    let url = '/backend'

    // send a request to backend
    function ajaxcall() {
        return $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: requestdatajson_str,
            success: function (responsedatajson_str) {
                // remove the cover all div
                d3.select('div#coverall').remove()

                let responsedatajson = JSON.parse(responsedatajson_str)
                console.log(responsedatajson)
                let responsedata = responsedatajson['responsedatafrombackend']
                // console.log(responsedata)  
                show_phrase(responsedata)

            } // success
        }) // ajax
    } // function ajaxcall8
    return $.when(ajaxcall()).done(async () => {
    })
} // get_spacytest_data

function show_phrase(responsedata) {

    // get the tokens
    let tokens_arr = responsedata['tokens']
    let phrases_arr = responsedata['phrases']

    // get list of tokens in phrases
    let tokens_in_phrase_arr = []
    phrases_arr.forEach(d => {
        for (let j = d.starttokenid; j < d.endtokenid; j++) {
            tokens_in_phrase_arr.push(j)
        }
    })

    // make new html to be displayed in the input box

    let newtext_tokens_arr = []
    let newhtml = ""
    tokens_arr.forEach(t => {
        // console.log(t.text)
        let newtokentext = t.text

        if (tokens_in_phrase_arr.includes(t.tokeni)) {
            newtokentext = `<b>${t.text}</b>`
        }
        newtext_tokens_arr.push(newtokentext)
        newhtml += newtokentext
    })
    // console.log(newtext_tokens_arr)
    // console.log(newhtml)
    d3.select('div#input').html(newhtml)


    // make a table in the outbox
    let outbox_d3pn = d3.select('div#output').styles({ 'display': 'block', 'border': '0px solid grey' })
    let table_width_str = `80%`
    outbox_d3pn.html('')
    let table_d3pn = outbox_d3pn.append('table').attrs({ 'class': 'demotask' }).styles({ 'font-size': '12px', 'border': '1px solid grey', 'border-collapse': 'collapse', 'table-layout': 'fixed', 'width': table_width_str })
    let titles_arr = Object.keys(phrases_arr[0])
    let title_tr_d3pn = table_d3pn.append('tr')
    titles_arr.forEach(d => {
        title_tr_d3pn.append('td').text(d).styles({ 'width': '100px', 'overflow': 'hidden', 'border': '1px solid lightgrey', 'padding': '2px', 'font-weight': 'bold' })
    })
    // add the records
    phrases_arr.forEach(e => {
        let new_tr_d3pn = table_d3pn.append('tr')
        titles_arr.forEach(d => {
            new_tr_d3pn.append('td').text(e[d]).styles({ 'width': '100px', 'overflow': 'hidden', 'border': '1px solid lightgrey', 'padding': '2px', 'font-weight': 'bolnormald' })
        })
    })


    // display code in the box
    d3.select('label#code').text('Python code:')
    let codebox_d3pn = d3.select('div#codebox').styles({ "display": "block" })
    let codestr = `<pre><code class="python">def get_matched_phrases(requestdatafromfrontend_json):
    text = requestdatafromfrontend_json['requestdatafromfrontend']['data']
    phrases_to_match_ls = requestdatafromfrontend_json['requestdatafromfrontend']['phrases']
    print(phrases_to_match_ls, text)
    result_phrases_ls=[]

    # get all tokens
    tokens_ls=[]
    doc = nlp(text)
    tokentext_ls = []
    for x in doc:
        tokens_ls.append({"text": x.text_with_ws, "lemma":x.lemma_.lower(), "pos":x.pos_, "dep":x.dep_, "tokeni":x.i})

    matchedspans_thistheme_ls = get_matched_spans(
        text=text, 
        interested_phrases_ls=phrases_to_match_ls, 
        match_patterns_ls=[], 
        include_pos_pattern=False, 
        include_norm_pattern = True, 
        max_text_length=1000000
    ) # get_matched_spans()

    for matchedspan in matchedspans_thistheme_ls:
        matchedphrase = matchedspan.text.lower()
        result_phrases_ls.append({"starttokenid": matchedspan.start, "endtokenid":matchedspan.end, "phrase": matchedphrase})

    responsedatafrombackend_json = {'responsedatafrombackend':{'phrases':result_phrases_ls, "tokens": tokens_ls}}
    return responsedatafrombackend_json
    </code></pre>
    `
    codebox_d3pn.html(codestr)
    hljs.initHighlightingOnLoad();
}



////////////////////////////////////////////////////////////////////task phrase


/////task entities and noun chuncks ////////////////////////////////////////////////////////////////////////////////

async function task_ent() {
    let stage_d3pn = d3.select('div#stage')
    stage_d3pn.select('div#input').remove()
    stage_d3pn.selectAll('.demotask').remove()


    stage_d3pn.append('label').attrs({ 'class': 'demotask' }).styles({ 'class': 'demotask', 'font-weight': 'bold' }).text('Input')
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })
    stage_d3pn.append('div').attrs({ 'id': 'input', 'class': 'demotask', 'contenteditable': 'true' })
        .styles({ 'display': 'none', 'border': "0px solid grey", 'width': '90%', 'max-height': '200px', 'overflow': 'auto', 'padding': '5px', 'font-size': '20px', 'font-family': 'Arial' })
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })

    stage_d3pn.append('label').attrs({ 'class': 'demotask' }).styles({ 'margin-top': '50px', 'font-weight': 'bold' }).text('Output')
    stage_d3pn.append('button').attrs({ 'class': 'demotask' }).text('Go').styles({ 'margin-left': '10px', 'margin-left': '10px' })
        .on('click', async (event) => { await get_ent_nc() })
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })
    stage_d3pn.append('div').attrs({ 'id': 'output', 'class': 'demotask', 'contenteditable': 'false' }).styles({ 'display': 'none', 'border': "1px solid grey", 'max-height': '300px', 'overflow': 'auto', 'padding': '5px' })
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })

    stage_d3pn.append('label').attrs({ 'class': 'demotask', 'id': 'code' }).styles({ 'margin-top': '50px', 'class': 'demotask', 'font-weight': 'bold' }).text('')
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })
    stage_d3pn.append('div').attrs({ 'id': 'codebox', 'class': 'demotask', 'contenteditable': 'false' })
        .styles({ 'resize': 'both', 'width': '80%', 'display': 'none', 'border': "0px solid grey", 'overflow': 'auto', 'padding': '5px' ,'background-color':'black'})


    let text = `The City of Vancouver has likewise signalled a state of emergency with respect to the unregulated, contaminated drug supply and the associated opioid-related overdose deaths.`
    let inputbox = d3.select('div#input')
    inputbox.text(text).styles({ 'display': 'block' })

} // task_ent

async function get_ent_nc() {

    // get the text in the text box
    let text = d3.select('div#input').node().textContent.trim()
    // console.log(text)
    if (text.length === 0) { return }

    // console.log(update_keywords_objsents)
    // send a request to the backend to get summary
    d3.select('div#coverall').remove()
    // when a request is sent, temporarily disable everything by adding a cover all box (note: must select position: absolute)
    // so weird, to let text stay in the middle of the div, make 'line-height' = the full window height
    d3.select('body').append('div').attrs({ 'id': 'coverall' }).styles(
        {
            'background-color': 'rgba(0,0,0,0.0)', 'width': '100%', 'height': '100%', 'z-index': '100000', 'position': 'absolute', 'left': '0px', 'top': '0px',
            'color': 'lightgrey', 'text-align': 'center', 'line-height': (window.innerHeight * 1.5) + 'px', 'font-family': 'arial', 'font-size': '100px', 'font-weight:': 'bold'
        }
    ).text('Wait...')

    let requesttask = 'get_ent_nc' // to save and excel file of text that having different machine v1 labelling and human labelling

    let requestdatajson = {
        requesttask: requesttask,
        requestdatafromfrontend: {
            // location: { somedata_filelocation: somedata_filelocation },
            data: text
        } // requestdatafromfrontend
    } // requestdatajson
    // console.log(requestdatajson['requestdatafromfrontend']['data'])
    let requestdatajson_str = JSON.stringify(requestdatajson)
    let url = '/backend'

    // send a request to backend
    function ajaxcall() {
        return $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: requestdatajson_str,
            success: function (responsedatajson_str) {
                // remove the cover all div
                d3.select('div#coverall').remove()

                let responsedatajson = JSON.parse(responsedatajson_str)
                console.log(responsedatajson)
                let responsedata = responsedatajson['responsedatafrombackend']
                // console.log(responsedata)  
                show_ent_nc(responsedata)

            } // success
        }) // ajax
    } // function ajaxcall8
    return $.when(ajaxcall()).done(async () => {
    })
} // get_spacytest_data

function show_ent_nc(responsedata) {

    // make a table in the outbox
    let outbox_d3pn = d3.select('div#output').styles({ 'display': 'block', 'border': '0px solid grey' })
    let table_width_str = `80%`
    outbox_d3pn.html('')
    let table_d3pn = outbox_d3pn.append('table').attrs({ 'class': 'demotask' }).styles({ 'font-size': '12px', 'border': '1px solid grey', 'border-collapse': 'collapse', 'table-layout': 'fixed', 'width': table_width_str })
    let titles_arr = Object.keys(responsedata[0])
    let title_tr_d3pn = table_d3pn.append('tr')
    titles_arr.forEach(d => {
        title_tr_d3pn.append('td').text(d).styles({ 'width': '100px', 'overflow': 'hidden', 'border': '1px solid lightgrey', 'padding': '2px', 'font-weight': 'bold' })
    })
    // add the records
    responsedata.forEach(e => {
        let new_tr_d3pn = table_d3pn.append('tr')
        titles_arr.forEach(d => {
            new_tr_d3pn.append('td').text(e[d]).styles({ 'width': '100px', 'overflow': 'hidden', 'border': '1px solid lightgrey', 'padding': '2px', 'font-weight': 'bolnormald' })
        })
    })


    // display code in the box
    d3.select('label#code').text('Python code:')
    let codebox_d3pn = d3.select('div#codebox').styles({ "display": "block" })
    let codestr = `<pre><code class="python">def get_ent_nc(requestdatafromfrontend_json):
    text = requestdatafromfrontend_json['requestdatafromfrontend']['data']
    print(text)
    results_ls=[]
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    # get entities and noun chunks
    for x in doc.ents:
        explain = spacy.explain(x.label_)
        print('=======51', explain)
        results_ls.append({"text": x.text, "type": x.label_ + ': '+ explain})
    for x in doc.noun_chunks:
        results_ls.append({"text": x.text, "type": 'noun phrase'})
    responsedatafrombackend_json = {'responsedatafrombackend':results_ls}
    return responsedatafrombackend_json
    </code></pre>
    `
    codebox_d3pn.html(codestr)
    hljs.initHighlightingOnLoad();

}
/////task entities and noun chuncks


/////task token


async function task_token() {
    let stage_d3pn = d3.select('div#stage')
    stage_d3pn.select('div#input').remove()
    stage_d3pn.selectAll('.demotask').remove()


    stage_d3pn.append('label').attrs({ 'class': 'demotask' }).styles({ 'class': 'demotask', 'font-weight': 'bold' }).text('Input')
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })
    stage_d3pn.append('div').attrs({ 'id': 'input', 'class': 'demotask', 'contenteditable': 'true' })
        .styles({ 'display': 'none', 'border': "0px solid grey", 'width': '90%', 'max-height': '200px', 'overflow': 'auto', 'padding': '5px', 'font-size': '20px', 'font-family': 'Arial' })
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })

    stage_d3pn.append('label').attrs({ 'class': 'demotask' }).styles({ 'margin-top': '50px', 'font-weight': 'bold' }).text('Output')
    stage_d3pn.append('button').attrs({ 'class': 'demotask' }).text('Go').styles({ 'margin-left': '10px', 'margin-left': '10px' }).on('click', async (event) => { await get_tokenized_data() })
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })
    stage_d3pn.append('div').attrs({ 'id': 'output', 'class': 'demotask', 'contenteditable': 'false' }).styles({ 'display': 'none', 'border': "1px solid grey", 'max-height': '200px', 'overflow': 'auto', 'padding': '5px' })
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })

    stage_d3pn.append('label').attrs({ 'class': 'demotask', 'id': 'code' }).styles({ 'margin-top': '50px', 'class': 'demotask', 'font-weight': 'bold' }).text('')
    stage_d3pn.append('p').attrs({ 'class': 'demotask' })
    stage_d3pn.append('div').attrs({ 'id': 'codebox', 'class': 'demotask', 'contenteditable': 'false' })
        .styles({ 'resize': 'both', 'width': '80%', 'display': 'none', 'border': "0px solid grey", 'overflow': 'auto', 'padding': '5px','background-color':'black' })


    let text = `The City of Vancouver has likewise signalled a state of emergency with respect to the unregulated, contaminated drug supply and the associated opioid-related overdose deaths.`
    let inputbox = d3.select('div#input')
    inputbox.text(text).styles({ 'display': 'block' })

}



async function get_tokenized_data() {

    // get the text in the text box
    let text = d3.select('div#input').node().textContent.trim()
    // console.log(text)
    if (text.length === 0) { return }

    // console.log(update_keywords_objsents)
    // send a request to the backend to get summary
    d3.select('div#coverall').remove()
    // when a request is sent, temporarily disable everything by adding a cover all box (note: must select position: absolute)
    // so weird, to let text stay in the middle of the div, make 'line-height' = the full window height
    d3.select('body').append('div').attrs({ 'id': 'coverall' }).styles(
        {
            'background-color': 'rgba(0,0,0,0.0)', 'width': '100%', 'height': '100%', 'z-index': '100000', 'position': 'absolute', 'left': '0px', 'top': '0px',
            'color': 'lightgrey', 'text-align': 'center', 'line-height': (window.innerHeight * 1.5) + 'px', 'font-family': 'arial', 'font-size': '100px', 'font-weight:': 'bold'
        }
    ).text('Wait...')

    let requesttask = 'get_tokenized_data' // to save and excel file of text that having different machine v1 labelling and human labelling

    let requestdatajson = {
        requesttask: requesttask,
        requestdatafromfrontend: {
            // location: { somedata_filelocation: somedata_filelocation },
            data: text
        } // requestdatafromfrontend
    } // requestdatajson
    // console.log(requestdatajson['requestdatafromfrontend']['data'])
    let requestdatajson_str = JSON.stringify(requestdatajson)
    let url = '/backend'

    // send a request to backend
    function ajaxcall() {
        return $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: requestdatajson_str,
            success: function (responsedatajson_str) {
                // remove the cover all div
                d3.select('div#coverall').remove()

                let responsedatajson = JSON.parse(responsedatajson_str)
                console.log(responsedatajson)
                let responsedata = responsedatajson['responsedatafrombackend']
                // console.log(responsedata)  
                show_tokenized(responsedata)

            } // success
        }) // ajax
    } // function ajaxcall8
    return $.when(ajaxcall()).done(async () => {
    })
} // get_spacytest_data

async function show_tokenized(responsedata) {
    console.log(responsedata)
    // make a table in the outbox
    let outbox_d3pn = d3.select('div#output').styles({ 'display': 'block', 'border': '0px solid grey' })
    let count_tokens = responsedata['lemmas'].length + 2
    let table_width_str = `${count_tokens * 150}px`
    outbox_d3pn.html('')
    let table_d3pn = outbox_d3pn.append('table').attrs({ 'class': 'demotask' }).styles({ 'border': '1px solid grey', 'border-collapse': 'collapse', 'table-layout': 'fixed', 'width': table_width_str })
    add_tr('token')
    add_tr('text')
    add_tr('lemmas')
    add_tr('pos')
    add_tr('dep')
    function add_tr(datatype) {
        let tr_d3pn = table_d3pn.append('tr')
        let rowhead = datatype
        if (datatype === 'pos') { rowhead = 'part of speech (pos)' }
        if (datatype === 'dep') { rowhead = 'dependency' }
        tr_d3pn.append('td').text(rowhead).styles({ 'width': '30px', 'overflow': 'hidden', 'border': '1px solid lightgrey', 'padding': '2px', 'font-weight': 'bold' }) // add the row head
        if (datatype === 'token') {
            responsedata['text'].forEach((d, i) => {
                tr_d3pn.append('td').text(i).styles({ 'width': '20px', 'overflow': 'hidden', 'border': '1px solid lightgrey', 'padding': '2px' }) // add token i for each cell
            })
        } else {
            responsedata[datatype].forEach((d, i) => {
                tr_d3pn.append('td').text(d).styles({ 'width': '20px', 'overflow': 'hidden', 'border': '1px solid lightgrey', 'padding': '2px' }) // add text/lemma/pos for each cell
            })
        }
    } // function add_tr()

    // display code in the box
    d3.select('label#code').text('Python code:')
    let codebox_d3pn = d3.select('div#codebox').styles({ "display": "block" })
    let codestr = `<pre><code class="python">def get_tokenized_data(requestdatafromfrontend_json):
    text = requestdatafromfrontend_json['requestdatafromfrontend']['data']
    print(text)
    results_dict={}
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    tokentext_ls = []
    lemmas_ls = []
    pos_ls = []
    dep_ls = []
    for x in doc:
        tokentext_ls.append(x.text_with_ws)
        lemmas_ls.append(x.lemma_.lower())
        pos_ls.append(x.pos_)
        dep_ls.append(x.dep_)
    results_dict = {"text": tokentext_ls, "lemmas":lemmas_ls, "pos":pos_ls, "dep":dep_ls}
    responsedatafrombackend_json = {'responsedatafrombackend':results_dict}
    return responsedatafrombackend_json</code></pre>
    `
    codebox_d3pn.html(codestr)
    // codebox_d3pn.styles({ 'background-color': 'lightgrey' })
    hljs.initHighlightingOnLoad();

}

/////task token /////////////////////////////////////////////////////



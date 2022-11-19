
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
    textbox.attrs({ 'textdata': datastr , 'contenteditable': 'true'})
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
    let srcentities_arr = await d3.json(urlgznocache).then(d=>{return d}) // like [{entity1:..., text: "..." }, {entity2:..., }]
    let articlename = "25091704" //"ferguson_war"
    let json_fromfront = {article: articlename, entities: srcentities_arr}
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
        requestdatafromfrontend: json_fromfront
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
                d3.select('div#metadatadiv').attrs({"processedtextjson_from_pyapp":processed_textjson_str })


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

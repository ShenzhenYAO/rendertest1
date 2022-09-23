
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


async function make_test_page() {

    let stage_d3pn = d3.select('div#stage')
    stage_d3pn.html('')

    stage_d3pn.append('button').text('Load data').styles({ 'margin-left': '10px' }).on('click', async (event) => { await get_some_data() })
    stage_d3pn.append('p')

    stage_d3pn.append('div').attrs({ 'id': 'textbox' }).styles({ 'display': 'none' })
    stage_d3pn.append('p')

    stage_d3pn.append('button').text('spaCy it').styles({ 'margin-left': '10px' }).on('click', async (event) => { await get_spacytest_data() })
    stage_d3pn.append('p')

    stage_d3pn.append('div').attrs({ 'id': 'spacycontents' }).styles({ 'display': 'none' })

} // async function make_lit_search_elements()

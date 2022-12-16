async function makeEle() {

    // append a div for data (this one is to be hidden...)
    let datadiv = d3.select('body').append('div')
        .attrs({ 'id': 'metadatadiv' })
        .styles({ 'display': 'none' })

    // add a nav bar
    let navbar_d3pn = d3.select('body').append('div')
        .attrs({
            'class': 'navbar',
            'id': 'navbar',
            'name': 'navbar'
        })
        .styles({
            'background-color': 'rgba(0,0,0,1)',
            // 'border':'solid red 3px',
            'position': 'fixed',
            'width': '100%',
            'height': '70px',
            'top': '0px',
            'z-index': '10000', // note: very important to put the nav bar and its offsprings above all other elements!,
            'color': 'white',
            'text-align': 'center',
            'font-weight': 'bold',
            'font-size': '40px',
            'vertical-align': 'middle'
        })
    // .text('Harm Reduction')

    // add the title button
    navbar_d3pn.append('div')
        .attrs({ 'id': 'pagetitle' })
        .styles({ 'color': 'white', 'text-align': 'center', 'font-weight': 'bold', 'font-size': '40px', 'vertical-align': 'middle', 'border': '0px grey solid' })
        .text('Harm reduction')
    // add button divs
    navbar_d3pn.append('div')
        .attrs({ 'id': 'maketestpagebutton2' })
        .styles({ 'float': 'left', 'color': 'lightgrey', 'text-align': 'center', 'width': '60px', 'font-family': 'arial', 'font-weight': 'bold', 'font-size': '12px', 'vertical-align': 'middle', 'border': '0px grey solid', 'cursor': 'pointer' })
        .text('demo')
        .on('click', async () => { await make_vchdemo_page() })
        .on('mouseover', (event) => { d3.select(event.target).styles({ 'color': 'white' }) })
        .on('mouseleave', (event) => { d3.select(event.target).styles({ 'color': 'lightgrey' }) })


    navbar_d3pn.append('div')
        .attrs({ 'id': 'maketestpagebutton' })
        .styles({ 'float': 'left', 'color': 'lightgrey', 'text-align': 'center', 'width': '60px', 'font-family': 'arial', 'font-weight': 'bold', 'font-size': '12px', 'vertical-align': 'middle', 'border': '0px grey solid', 'cursor': 'pointer' })
        .text('test')
        .on('click', async () => { await make_test_page() })
        .on('mouseover', (event) => { d3.select(event.target).styles({ 'color': 'white' }) })
        .on('mouseleave', (event) => { d3.select(event.target).styles({ 'color': 'lightgrey' }) })



    d3.select('body').append('div')
        .attrs({
            'class': 'stage',
            'id': 'stage',
            'name': 'stage'
        })
        .styles({
            'background-color': 'white',
            'margin-top': '90px',
            'margin-left': '10px',
            'width': '100%',
            'font-family': 'ms sans serif',
            'height': window.innerHeight * .8 + 'px',
            // 'border':'1px solid grey'
        })

} // makeEle



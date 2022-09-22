from flask import Flask

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello2 %s!</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful2 web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# looks for an 'app' callable by default.
app = Flask(__name__)

# add a rule for the index page.
app.add_url_rule('/', 'index', (lambda: header_text +
    say_hello() + instructions + footer_text))

# add a rule when the page is accessed with a name appended to the site
# URL.
app.add_url_rule('/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + home_link + footer_text))

# run the app.
# if __name__ == "__main__":
#     # Setting debug to True enables debug output. This line should be
#     # removed before deploying a production app.
#     # app.debug = True
#     app.run()
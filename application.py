# The file name must by app.py to run this file on render. (this is the default file name for gunicorn app:app). Does not work if the file is application.py and gunicorn app:applcation 
# the command gunicorn app:appFlask is to look into the default app.py and find the variable appFlask within app.py
# the command gunicorn 


from flask import Flask

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello2 %s!</p>\n' % username

def get_name():
    return 'The value of __name__ is {}\n'.format(__name__)

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>Render Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful2 web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# looks for an 'app' callable by default.
appFlask = Flask(__name__)

# add a rule for the index page.
appFlask.add_url_rule('/', 'index', (lambda: header_text +
    say_hello() + get_name() + instructions + footer_text))

# add a rule when the page is accessed with a name appended to the site
# URL.
appFlask.add_url_rule('/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + get_name()+ home_link + footer_text))

# # the following line is not needed for running on RENDER.com
# appFlask.run()
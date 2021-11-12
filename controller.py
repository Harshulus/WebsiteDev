'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''

from bottle import Bottle, route, get, post, error, request, static_file, response

import model

app = Bottle()

#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------

# @app.hook('before_request')
# def before_request():
#     part = request.urlparts
#     if part.scheme == "http":
#         url = request.url.replace('http://', 'https://', 1)
#         code = 301
#         return redirect(url, code=code)

# Allow image loading
@app.route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')

#-----------------------------------------------------------------------------

# Allow CSS
@app.route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')

#-----------------------------------------------------------------------------

# Allow javascript
@app.route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')

#-----------------------------------------------------------------------------
# Pages
#-----------------------------------------------------------------------------

# Redirect to login
@app.get('/')
@app.get('/index')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    return model.index()

#-----------------------------------------------------------------------------

# Display the login page
@app.get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    username = request.cookies.get("account")
    if username != None:
        password = request.cookies.get("password")
        if model.account_check(username, password) == True:
            return model.dashboard(request.cookies.get("account"))
        else:
            response.delete_cookie("account")
            response.delete_cookie("password")
    return model.login_form()

#-----------------------------------------------------------------------------

# Attempt the login
@app.post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    # Call the appropriate method
    html, valid, hashed_pass = model.login_check(username, password)
    if valid == True:
        response.set_cookie("account", username)
        response.set_cookie("password", hashed_pass)
        
    return html

#-----------------------------------------------------------------------------

# Display the register page
@app.get('/register')
def get_register_controller():
    '''
        get_register
        
        Serves the register page
    '''

    return model.register_form()

#-----------------------------------------------------------------------------

# Attempt to register
@app.post('/register')
def post_register():
    '''
        post_register
        
        Handles register
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    # Call the appropriate method
    return model.register(username, password)
    
#-----------------------------------------------------------------------------

# Display the Logout page
@app.get('/logout')
def get_logout_controller():
    '''
        get_logout
        
        Serves the logout page
    '''
    response.delete_cookie("account")
    response.delete_cookie("password")
    return model.logout()

#-----------------------------------------------------------------------------

@app.get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()

#-----------------------------------------------------------------------------

# Attempt to add user
@app.post('/add_user')
def add_user():
    '''
        post_add_user
        
        Serves the add_user valid/invalid page
    '''

    # Handle the form processing
    add_username = request.forms.get('add_username')
    add_password = request.forms.get('add_password')
    
    # Call the appropriate method
    return model.add_user(add_username, add_password)

#-----------------------------------------------------------------------------

# Attempt to mute user
@app.post('/mute_user')
def mute_user():
    '''
        post_mute_user
        
        Serves the mute_user page
    '''

    mute_username = request.forms.get('mute_user_usernames')
    
    return model.mute_user(mute_username)

#-----------------------------------------------------------------------------

# Attempt to unmute user
@app.post('/unmute_user')
def mute_user():
    '''
        post_mute_user
        
        Serves the mute_user page
    '''

    mute_username = request.forms.get('unmute_user_usernames')
    
    return model.unmute_user(mute_username)

#-----------------------------------------------------------------------------

# Attempt to remove user
@app.post('/remove_user')
def remove_user():
    '''
        post_remove_user
        
        Serves the remove_user page
    '''

    remove_username = request.forms.get('remove_user_usernames')
    
    return model.remove_user(remove_username)

#-----------------------------------------------------------------------------

# @get('/dashboard')
# def get_dashboard():
#     '''
#         get_dashboard
        
#         Serves the dashboard page
#     '''
#     return model.dashboard(request.cookies.get("account"))

#-----------------------------------------------------------------------------

@app.get('/messages')
def get_messages():
    '''
        get_messages
        
        Serves the messages page
    '''

    # if request.cookies.get("account") != None:
    #     return model.messages()
    username = request.cookies.get("account")
    if username != None:
        password = request.cookies.get("password")
        if model.account_check(username, password) == True:
            return model.messages()
        else:
            response.delete_cookie("account")
            response.delete_cookie("password")
    return model.no_permission()

#-----------------------------------------------------------------------------

@app.post('/messages')
def add_message():
    '''
        add_message
        
        Serves the add_message page
    '''

    sender = request.cookies.get("account")
    recipient = request.forms.get('usernames')
    content = request.forms.get('message')
    
    if sender != None:
        password = request.cookies.get("password")
        if model.account_check(sender, password) == True:
            return model.add_message(sender, recipient, content)
        else:
            response.delete_cookie("account")
            response.delete_cookie("password")
    return model.no_permission()

#-----------------------------------------------------------------------------

@app.get('/forum')
def get_forum():
    '''
        get_forum
        
        Serves the forum page
    '''

    return model.forum()

@app.post('/forum')
def add_post():
    '''
        add_post
        
        Adds the post to the forum page
    '''

    author = request.cookies.get("account")
    title = request.forms.get('post_title')
    content = request.forms.get('post_content')
    
    if author != None:
        password = request.cookies.get("password")
        if model.account_check(author, password) == True:
            return model.add_post(author, title, content)
        else:
            response.delete_cookie("account")
            response.delete_cookie("password")
    return model.forum_no_permission()
    
    

@app.get('/post')
def get_forum_post():
    '''
        get_forum_post
        
        Serves the forum_post page
    '''
    return model.forum_post()

@app.post('/post')
def add_comment():
    '''
        add_comment
        
        Adds the comment to the post
    '''

    author = request.cookies.get("account")
    comment = request.forms.get('comment')
    post_id = int(request.forms.get('post_id'))
    
    if author != None:
        password = request.cookies.get("password")
        if model.account_check(author, password) == True:
            return model.add_comment(author, comment, post_id)
        else:
            response.delete_cookie("account")
            response.delete_cookie("password")
    return model.forum_no_permission()
    
#-----------------------------------------------------------------------------

@app.get('/contents')
def get_contents():
    '''
        get_content
        
        Serves the content page
    '''
    return model.contents()
    
#-----------------------------------------------------------------------------

@app.get('/web_works')
def get_web_works():
    '''
        get_web_works
        
        Serves the web_works page
    '''
    return model.web_works()

@app.get('/intro')
def get_intro():
    '''
        get_intro
        
        Serves the intro page
    '''
    return model.intro()

@app.get('/run_files')
def get_run_files():
    '''
        get_run_files
        
        Serves the run_files page
    '''
    return model.run_files()

@app.get('/intro_to_html')
def get_intro_to_html():
    '''
        get_intro_to_html
        
        Serves the intro_to_html page
    '''
    return model.intro_to_html()

@app.get('/metadata')
def get_metadata():
    '''
        get_metadata
        
        Serves the metadata page
    '''
    return model.metadata()

@app.get('/textformat')
def get_textformat():
    '''
        get_textformat
        
        Serves the textformat page
    '''
    return model.textformat()

@app.get('/semantics')
def get_semantics():
    '''
        get_semantics
        
        Serves the semantics page
    '''
    return model.semantics()

@app.get('/html_forms')
def get_html_forms():
    '''
        get_html_forms
        
        Serves the html_forms page
    '''
    return model.html_forms()

@app.get('/basics_of_css')
def get_basics_of_css():
    '''
        get_basics_of_css
        
        Serves the basics_of_css page
    '''
    return model.basics_of_css()

@app.get('/css_layout_and_formatting')
def get_css_layout_and_formatting():
    '''
        get_css_layout_and_formatting
        
        Serves the css_layout_and_formatting page
    '''
    return model.css_layout_and_formatting()

@app.get('/css_template')
def get_css_template():
    '''
        get_css_template
        
        Serves the css_template page
    '''
    return model.css_template()

@app.get('/template')
def get_template():
    '''
        get_template
        
        Serves the template page
    '''
    return model.template()

@app.get('/java_script_basics')
def get_java_script_basics():
    '''
        get_java_script_basics
        
        Serves the java_script_basics page
    '''
    return model.java_script_basics()

@app.get('/java_script_frameworks')
def get_java_script_frameworks():
    '''
        get_java_script_frameworks
        
        Serves the java_script_frameworks page
    '''
    return model.java_script_frameworks()

@app.get('/java_script_objects')
def get_java_script_objects():
    '''
        get_java_script_objects
        
        Serves the java_script_objects page
    '''
    return model.java_script_objects()

@app.get('/questions')
def get_questions():
    '''
        get_questions
        
        Serves the questions page
    '''
    return model.questions()
    
#-----------------------------------------------------------------------------

@app.get('/settings')
def get_settings():
    '''
        get_settings
        
        Serves the settings page
    '''
    return model.settings()
    
#-----------------------------------------------------------------------------

# Help with debugging
@app.post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)

#-----------------------------------------------------------------------------

# 404 errors, use the same trick for other types of errors
@app.error(404)
def error(error): 
    return model.handle_errors(error)

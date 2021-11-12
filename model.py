'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
import sql
import datetime
import json
from Crypto.Hash import SHA256

# Initialise our views, all arguments are defaults for the template
page_view = view.View()
sql_db = sql.SQLDatabase("static/db/database.db")
sql_db.database_setup()
salt = "xkAliD9vB3nGT1sgRhO19QKVuc5xUdcBxz1PEOIQGoH02ULf6rtz8v4hDpcnRv"
sql_db.add_user('admin', SHA256.new(('adminabc'+salt).encode()).hexdigest(), admin=1)
sql_db.add_user('John', SHA256.new(('user777'+salt).encode()).hexdigest(), admin=0)
sql_db.add_user('Billy', SHA256.new(('user235111'+salt).encode()).hexdigest(), admin=0)
sql_db.add_user('Jim', SHA256.new(('user6548'+salt).encode()).hexdigest(), admin=0)
sql_db.add_user('Bill', SHA256.new(('user9841'+salt).encode()).hexdigest(), admin=0)

all_posts = [
    {
        "id": 1,
        "title": "Hey I'm new", 
        "author": "John", 
        "date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 
        "content": "Nice to meet you all!", 
        "comments": [
            {
                "author": "Jim", 
                "date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 
                "content": "Hey"
            }, 
            {
                "author": "Bill", 
                "date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 
                "content": "Hey there"
            }, 
        ]
    }
]
all_messages = [
    {
        "sender": "John", 
        "recipient": "Billy", 
        "date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 
        "content": "Hey there"
    }, 
    {
        "sender": "Jim", 
        "recipient": "admin", 
        "date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 
        "content": "Hey there"
    }
]

dict_check = {
    "\"" : "&quo",
    "=" : "&equal",
    "-" : "&hyphen",
    "'" : "&apos",
    "\\" : "&slash",
    ";" : "&semi"
}

js_check = {
    "<" : "&lft",
    ">" : "&grt"
}


#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("Home", header="home_header", tailer="home_tailer")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")
    
def logged_in():
    '''
        logged_in
        Returns the view for the logged_in
    '''
    return page_view("logged_in")

def logout():
    '''
        logout
        Returns the view for the logout
    '''
    return page_view("logout")
    
#-----------------------------------------------------------------------------
# Register
#-----------------------------------------------------------------------------
    
def register_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("register")
    
#-----------------------------------------------------------------------------
# Dashboard
#-----------------------------------------------------------------------------

def dashboard(name):
    '''
        dashboard
        Returns the view for the dashboard
    '''

    usernamearr = list(name.strip())
    for i in range(len(usernamearr)):
        if usernamearr[i] in dict_check:
            usernamearr[i] = dict_check[usernamearr[i]]
        elif usernamearr[i] in js_check:
            usernamearr[i] = js_check[usernamearr[i]]
    name = ""
    for ch in usernamearr:
        name += ch

    status = sql_db.check_if_admin(name)
    if status == True:
        users = sql_db.get_all_users()
        muted_users = sql_db.get_muted_users()
        unmuted_users = sql_db.get_unmuted_users()
        return page_view("Dashboard_admin", name=name, users=json.dumps(users), muted_users=json.dumps(muted_users), unmuted_users=json.dumps(unmuted_users))
    return page_view("Dashboard", name=name)

#-----------------------------------------------------------------------------

# Add user to database
def add_user(username, password):
    '''
        add_user
        Checks username

        :: username :: The username

        Returns either a view for valid credentials, or a view for invalid credentials
    '''
    
    usernamearr = list(username.strip())
    for i in range(len(usernamearr)):
        if usernamearr[i] in dict_check:
            usernamearr[i] = dict_check[usernamearr[i]]
        elif usernamearr[i] in js_check:
            usernamearr[i] = js_check[usernamearr[i]]
    username = ""
    for ch in usernamearr:
        username += ch

    check = sql_db.check_register(username)
    if check:
        passwordarr = list(password.strip())
        for i in range(len(passwordarr)):
            if passwordarr[i] in dict_check:
                passwordarr[i] = dict_check[passwordarr[i]]
            elif passwordarr[i] in js_check:
                passwordarr[i] = js_check[passwordarr[i]]
        password = ""
        for ch in passwordarr:
            password += ch

        password += salt
        hashed_pass = SHA256.new(password.encode()).hexdigest()
        sql_db.add_user(username, hashed_pass)
        return page_view("add_user_valid")
    else:
        return page_view("add_user_invalid")

#-----------------------------------------------------------------------------

# Mute user in database
def mute_user(username):
    '''
        mute_user
        Mutes user

        :: username :: The username

        Returns muted user page
    '''

    sql_db.mute_user(username)
    return page_view("muted_user")

#-----------------------------------------------------------------------------

# Unmute user in database
def unmute_user(username):
    '''
        mute_user
        Mutes user

        :: username :: The username

        Returns muted user page
    '''

    sql_db.unmute_user(username)
    return page_view("unmuted_user")

#-----------------------------------------------------------------------------

# Remove user from database
def remove_user(username):
    '''
        remove_user
        Removes user from the database

        :: username :: The username

        Returns removed user page
    '''

    sql_db.remove_user(username)
    return page_view("removed_user")

#-----------------------------------------------------------------------------
# Messages
#-----------------------------------------------------------------------------

def messages():
    '''
        messages
        Returns the view for the messages
    '''
        
    users = sql_db.get_all_users()
    return page_view("messages", users=json.dumps(users), all_messages=all_messages)

def add_message(sender, recipient, content):
    '''
        add_message
        Adds message to the storage 
    '''
    global all_messages

    usernamearr = list(sender.strip())
    for i in range(len(usernamearr)):
        if usernamearr[i] in dict_check:
            usernamearr[i] = dict_check[usernamearr[i]]
        elif usernamearr[i] in js_check:
            usernamearr[i] = js_check[usernamearr[i]]
    sender = ""
    for ch in usernamearr:
        sender += ch

    muted = sql_db.check_muted(sender)
    if muted == True:
        return page_view("muted")

    contentarr = list(content.strip())
    for i in range(len(contentarr)):
        if contentarr[i] in js_check:
            contentarr[i] = js_check[contentarr[i]]
    content = ""
    for ch in contentarr:
        content += ch

    message = {
        "sender": sender, 
        "recipient": recipient, 
        "date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 
        "content": content
    }
    all_messages.append(message)
    return page_view("add_message")

#-----------------------------------------------------------------------------
# Forum
#-----------------------------------------------------------------------------

def forum():
    '''
        forum
        Returns the view for the forum
    '''
    
    return page_view("forum", all_posts=all_posts)

def add_post(author, title, content):
    '''
        add_post
        Adds post to the storage 
    '''
    global all_posts

    usernamearr = list(author.strip())
    for i in range(len(usernamearr)):
        if usernamearr[i] in dict_check:
            usernamearr[i] = dict_check[usernamearr[i]]
        elif usernamearr[i] in js_check:
            usernamearr[i] = js_check[usernamearr[i]]
    author = ""
    for ch in usernamearr:
        author += ch

    muted = sql_db.check_muted(author)
    if muted == True:
        return page_view("muted")

    titlearr = list(title.strip())
    for i in range(len(titlearr)):
        if titlearr[i] in js_check:
            titlearr[i] = js_check[titlearr[i]]
    title = ""
    for ch in titlearr:
        title += ch

    contentarr = list(content.strip())
    for i in range(len(contentarr)):
        if contentarr[i] in js_check:
            contentarr[i] = js_check[contentarr[i]]
    content = ""
    for ch in contentarr:
        content += ch

    post = {
        "id": len(all_posts)+1,
        "title": title, 
        "author": author, 
        "date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 
        "content": content, 
        "comments": []
    }
    all_posts.append(post)
    return page_view("add_post")

def forum_post():
    '''
        forum_post
        Returns the view for the forum_post
    '''

    return page_view("post", all_posts=all_posts)

def add_comment(author, comment, post_id):
    '''
        add_comment
        Adds comment to the post 
    '''
    global all_posts

    usernamearr = list(author.strip())
    for i in range(len(usernamearr)):
        if usernamearr[i] in dict_check:
            usernamearr[i] = dict_check[usernamearr[i]]
        elif usernamearr[i] in js_check:
            usernamearr[i] = js_check[usernamearr[i]]
    author = ""
    for ch in usernamearr:
        author += ch

    muted = sql_db.check_muted(author)
    if muted == True:
        return page_view("muted")

    commentarr = list(comment.strip())
    for i in range(len(commentarr)):
        if commentarr[i] in js_check:
            commentarr[i] = js_check[commentarr[i]]
    comment = ""
    for ch in commentarr:
        comment += ch

    comment = {
        "author": author, 
        "date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 
        "content": comment
    }
    comments = all_posts[post_id-1].get('comments')
    comments.append(comment)
    update_comments = {"comments": comments}
    all_posts[post_id-1].update(update_comments)
    return page_view("add_comment")

#-----------------------------------------------------------------------------
# Contents
#-----------------------------------------------------------------------------

def contents():
    '''
        contents
        Returns the view for the content
    '''
    return page_view("Contents")
    
def web_works():
    '''
        web_works
        Returns the view for the web_works
    '''
    return page_view("web_works")

def intro():
    '''
        intro
        Returns the view for the intro
    '''
    return page_view("Intro")

def run_files():
    '''
        run_files
        Returns the view for the run_files
    '''
    return page_view("runFiles")

def intro_to_html():
    '''
        intro_to_html
        Returns the view for the intro_to_html
    '''
    return page_view("Intht")

def metadata():
    '''
        metadata
        Returns the view for the metadata
    '''
    return page_view("Metadata")

def textformat():
    '''
        textformat
        Returns the view for the textformat
    '''
    return page_view("TextFormat")

def semantics():
    '''
        semantics
        Returns the view for the semantics
    '''
    return page_view("Semantics")

def html_forms():
    '''
        html_forms
        Returns the view for the html_forms
    '''
    return page_view("html_forms")

def basics_of_css():
    '''
        basics_of_css
        Returns the view for the basics_of_css
    '''
    return page_view("basics_of_css")

def css_layout_and_formatting():
    '''
        css_layout_and_formatting
        Returns the view for the css_layout_and_formatting
    '''
    return page_view("css_layout_&_formatting")

def css_template():
    '''
        css_template
        Returns the view for the css_template
    '''
    return page_view("css_template")

def template():
    '''
        template
        Returns the view for the template
    '''
    return page_view("template", header="template_header", tailer="template_tailer")

def java_script_basics():
    '''
        java_script_basics
        Returns the view for the java_script_basics
    '''
    return page_view("java_script_basics")

def java_script_frameworks():
    '''
        java_script_frameworks
        Returns the view for the java_script_frameworks
    '''
    return page_view("java_script_frameworks")

def java_script_objects():
    '''
        java_script_objects
        Returns the view for the java_script_objects
    '''
    return page_view("java_script_objects")

def questions():
    '''
        questions
        Returns the view for the questions
    '''
    return page_view("questions")

#-----------------------------------------------------------------------------
# Settings
#-----------------------------------------------------------------------------

def settings():
    '''
        settings
        Returns the view for the content
    '''
    return page_view("Settings")
    
#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''
    # By default assume good creds
    '''
    login = True
    
    
    if username != "admin" and username != "user": # Wrong Username
        err_str = "Incorrect Username"
        login = False
    
    if password != "password": # Wrong password
        err_str = "Incorrect Password"
        login = False

    if login:
        return page_view("valid", name=username)
    else:
        return page_view("invalid", reason=err_str)
    '''
    
    usernamearr = list(username.strip())
    for i in range(len(usernamearr)):
        if usernamearr[i] in dict_check:
            usernamearr[i] = dict_check[usernamearr[i]]
        elif usernamearr[i] in js_check:
            usernamearr[i] = js_check[usernamearr[i]]
    username = ""
    for ch in usernamearr:
        username += ch

    passwordarr = list(password.strip())
    for i in range(len(passwordarr)):
        if passwordarr[i] in dict_check:
            passwordarr[i] = dict_check[passwordarr[i]]
        elif passwordarr[i] in js_check:
                passwordarr[i] = js_check[passwordarr[i]]
    password = ""
    for ch in passwordarr:
        password += ch

    password += salt
    hashed_pass = SHA256.new(password.encode()).hexdigest()
    login = sql_db.check_credentials(username, hashed_pass)
    err_str = "Username or password is incorrect"
    if login:
        return page_view("valid", name=username), True, hashed_pass
    else:
        return page_view("invalid", reason=err_str), False, hashed_pass

        
#-----------------------------------------------------------------------------

# Check the register credentials
def register(username, password):
    '''
        register_check
        Checks username

        :: username :: The username

        Returns either a view for valid credentials, or a view for invalid credentials
    '''
    
    usernamearr = list(username.strip())
    for i in range(len(usernamearr)):
        if usernamearr[i] in dict_check:
            usernamearr[i] = dict_check[usernamearr[i]]
        elif usernamearr[i] in js_check:
            usernamearr[i] = js_check[usernamearr[i]]
    username = ""
    for ch in usernamearr:
        username += ch

    check = sql_db.check_register(username)
    if check:
        passwordarr = list(password.strip())
        for i in range(len(passwordarr)):
            if passwordarr[i] in dict_check:
                passwordarr[i] = dict_check[passwordarr[i]]
            elif passwordarr[i] in js_check:
                passwordarr[i] = js_check[passwordarr[i]]
        password = ""
        for ch in passwordarr:
            password += ch

        password += salt
        hashed_pass = SHA256.new(password.encode()).hexdigest()
        sql_db.add_user(username, hashed_pass)
        return page_view("register_valid")
    else:
        return page_view("register_invalid")
    
#-----------------------------------------------------------------------------

def no_permission():
    '''
        no_permission
        Returns the view for the no_permission
    '''
    return page_view("no_permission")

#-----------------------------------------------------------------------------

def forum_no_permission():
    '''
        forum_no_permission
        Returns the view for the forum_no_permission
    '''
    return page_view("forum_no_permission")

#-----------------------------------------------------------------------------

def account_check(username, password):
    '''
        account_check
        Checks whether the account details is correct
        Returns true or false
    '''

    usernamearr = list(username.strip())
    for i in range(len(usernamearr)):
        if usernamearr[i] in dict_check:
            usernamearr[i] = dict_check[usernamearr[i]]
        elif usernamearr[i] in js_check:
            usernamearr[i] = js_check[usernamearr[i]]
    username = ""
    for ch in usernamearr:
        username += ch

    valid = sql_db.check_credentials(username, password)
    return valid

#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("AboutUs")



# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)

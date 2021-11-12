from bottle import run, request, post, get
import re
import string
import smtplib

#dictionary
dict_check = {
    "<" : "&lt;",
    ">" : "&gt;",
    "\"" : "&quot",
    "=" : "&equals",
    " " : "&nbsp",
    "-" : "&hyphen",
    "'" : "&apos",
    "?" : "&quest",
    "$" : "&dollar",
    "&" : "&amp",
    "\\" : "&bsol", #
    "*" : "&ast",
    "#" : "&num",
    ";" : "&semi"  # jellyandbeans -> [] x check # OR 1=1  and or -> [and, or] -> malicious
}

flag_dict = ["and", "or", "select", "drop", "table", "insert", "from", "where", "database", "join", "update", "count", "delete", "limit", "index", "group", "having", "php", "<script>", "img", "src", "<?"]



def send():
    emailserver = smtplib.SMTP('smtp.gmail.com', 587)
    emailserver.starttls()
    sender_email = "alaninfo2021@gmail.com"
    sender_password = "info2222"
    receiver_email = "raymondtton@gmail.com"
    emailserver.login(sender_email, sender_password)

    message = "User is attempting malicious attacks"
    subject = "WARNING!"

    body = "Subject: {}\n\n{}".format(subject,message)

    emailserver.sendmail(sender_email, receiver_email, body)

#Check and alert the user
def check_notify(string):

    ls = string.split(" ")

    count = 0
    if len(ls) > 0:
        for i in ls:
            for s in flag_dict:
                if i == s:
                    count += 1
    
    if count != 0:
        send()
        


#Function to clean the input
def clean(string):
    temp = ""
    for i in string:
        if i in dict_check.keys():
            temp += dict_check.get(i)
        else:
            temp += i
    
    return temp
     

# Debug mode to check whether or not attacks are working
# Start with it as "True", try the attack, flip it to false, try the attack again and see if your WAF blocked it
# Debug should be set to false when launching the final version
debug = False

@post('/waf/detect/<string_in:path>')
def detect_attack(string_in):
    if not debug:
        if 'attack' in string_in:
            return 'False'
        return 'True'
    return 'False'

@post('/waf/username/<username:path>')
def verify_username(username):
    check_notify(username)
    username = clean(username)

@post('/waf/password/<password:path>')
def verify_password(password):
    if len(password) < 8:
        return "Password is too short"

    if not any(c in string.ascii_lowercase for c in password):
        return "Password must contain at least one lowercase character"

    if not any(c in string.ascii_uppercase for c in password):
        return "Password must contain at least one uppercase character"
    
    check_notify(password)
    password = clean(password)

    return 'True'

# Rather than using paths, you could throw all the requests with form data filled using the
# requests module and extract it here. Alternatively you could use JSON objects.

# Custom definition waf
@post('/waf/custom/field=<field:path>%20test=<test:path>')
def custom_waf(field, test):
    if re.search(test, field) is not None:
        return "True"
    return "False"

# Debug toggle
@post('/waf/debug')
def enable_debugger():
    global debug
    if debug:
        debug = False
    else:
        debug = True



# Run the server
run(host="0.0.0.0", port=8081)

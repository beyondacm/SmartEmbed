from flask import Flask, flash, redirect, render_template, request, session, abort
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import pymysql
import numpy as np
import bug
from clone_detect import Clone_Detect

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '123'

clone_detect = Clone_Detect()

class ReusableForm(Form):
    code = TextAreaField(render_kw={"rows": 40, "cols": 100},validators=[validators.required()])
    
class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = "******"
        db = "******"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor,autocommit=True)
        self.cur = self.con.cursor()
        
    def insert_bug(self,user,code,sl,el,bugtype,rate):
        query = """INSERT INTO `bug` (user, code, sl,el,bugtype,rate) VALUES (%s, %s, %s, %s, %s, %s)"""
        self.cur.execute(query, (str(user[1:-1]), str(code), str(sl),str(el),str(bugtype),str(rate)))
        result = self.cur.fetchall()
        return result
    
    def insert_clone(self,user,code,clone,sim,rate):
        query = """INSERT INTO `clone` (user, code, clone,sim,rate) VALUES (%s, %s, %s, %s, %s)"""
        self.cur.execute(query, (str(user[1:-1]), str(code), str(clone),str(sim),str(rate)))
        result = self.cur.fetchall()
        return result

def cust_similarity(user_in):
    return clone_detect.get_similarity(user_in)

def cust_bug(user_in,display_these_bugs,bug_types):
    return bug.get_bugs_cat(user_in,display_these_bugs,bug_types)

@app.route('/', methods=['GET', 'POST'])
def home():
    # bug_types = ['blockhash_bug','contract_not_refund','international_scam','public_moves','re_entrancy','unchecked_send_bug','unprotected_functions', 'withdraw_option','wrong_constructor_name']
    bug_types = ['Overflow_bug', 'Honeypot_bug', 'OwnerCVE_bug', 'PRNG_bug', 'blockhash_bug','contract_not_refund','international_scam','public_moves','re_entrancy']

    # bug_desc = ['bb desc','Contract does not refund the funds','Known international scams','pm desc','Calling external contracts changing or taking over the control flow','Failing send method','Functions unprotected from anauthorized call','wo desc','Constructor name mismatch']
    bug_desc = ['Arithmetic operation reach the maximum/minimum size of the type', 'Designed to entice user to deposit', 'The vulnerability can be exploited by the owner', 'Pseudo-random number generator vulnerability', 'bb desc','Contract does not refund the funds','Known international scams','pm desc','Calling external contracts changing or taking over the control flow']
    
    disp_bug = [[a] + [b] for a, b in zip([(w.replace('_', ' ')).title() for w in bug_types], bug_desc)]
    disp_results = 0
    form = ReusableForm(request.form)

    if request.method == 'POST':
        code=request.form['code']
        bug_selects = request.form.getlist('bug_select')
        bug_selects = list(map(int,bug_selects))

    if form.validate():
        if ((100 in bug_selects) or (len(bug_selects)==0)):
            display_these_bugs = bug_types
        else:
            display_these_bugs = [bug_types[x-1] for x in bug_selects]
        bugs_as_strings = ", ".join(str(x) for x in [(w.replace('_', ' ')).title() for w in display_these_bugs])
        top_result = cust_similarity(code)
        len_top_result = len(top_result)
        top_bug = cust_bug(code, display_these_bugs, bug_types)
        len_top_bug = len(top_bug)
        disp_results = 1
        startLines = [[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]

    else:
        flash('Error: All the form fields are required. ')
    return render_template('home.html',**locals())

@app.route('/test/')
def test():
    return render_template('test.html',**locals())

@app.route('/about/')
def about():
    return render_template('about.html',**locals())

@app.route('/dbhandle_bug/', methods=['GET', 'POST'])
def dbhandle_bug():
    if request.method == 'GET':
        def db_query():
            db = Database()
            emps = db.insert_bug(request.args['user'],request.args['code'],request.args['sl'],request.args['el'],request.args['bugtype'],request.args['rate'])
            return emps
        res = db_query()
        return render_template('about.html',**locals())
    
@app.route('/dbhandle_clone/', methods=['GET', 'POST'])
def dbhandle_clone():
    if request.method == 'GET':
        def db_query():
            db = Database()
            emps = db.insert_clone(request.args['user'],request.args['code'],request.args['clone'],request.args['sim'],request.args['rate'])
            return emps
        res = db_query()
        return render_template('about.html',**locals())

if __name__ =="__main__":
    app.run(debug=True,port=9000)

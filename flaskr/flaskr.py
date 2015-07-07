import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = '.\\flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()
    c=g.db.cursor()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select name_id, mail_id, amount from entries order by id desc')
    entries = [dict(name_id=row[0], mail_id=row[1], amount=row[2]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (name_id, mail_id, amount) values (?, ?, ?)',
                 [request.form['name_id'], request.form['mail_id'], request.form['amount']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
##To="sunil@gmail.com"
##From="shiv@gmail.com"
##amount=400

@app.route('/update', methods=['GET'])
def updation():
    From = request.args.get('from','')
    To =request.args.get('to','')
    amount=request.args.get('amount','')
    t=(To,)
    u=(From,)
    cursor=g.db.execute('SELECT amount FROM entries WHERE mail_id=?',u)
    rhat=-1
    for row in cursor:
        rhat=row[0]
    if rhat == -1:
        text=From+" is not found in database"
        #flash(text)
    else:
        cursor=g.db.execute('SELECT amount FROM entries WHERE mail_id=?', t)
        rhat2=-1
        for row in cursor:
            rhat2=row[0]
        if rhat2==-1:
            text=To+" is not found in database"
            #flash(text)
        else: 
            #rhat=(int)(c.fetchone())
            rhat=rhat-float(amount)
            rhat2=rhat2+float(amount)
            print rhat
            print rhat2
            if rhat<0:
                text="balance of "+From+" is not enough to proceed"
                #flash(text)
            else:
                q = "UPDATE entries set amount=" + str(rhat) + " where mail_id=?" 
                g.db.execute(q,u)
                g.db.commit()
                q = "UPDATE entries set amount=" + str(rhat2) + " where mail_id=?"
                g.db.execute(q,t)
                g.db.commit()
                text='Transaction complete.'
                #flash(text)
    return text
##    return redirect(url_for('show_entries'))
    

@app.route('/form')
def form():
    return render_template('form.html')

if __name__ == '__main__':
    app.run()

from flask import Flask, request, g, render_template_string, url_for, render_template
import re
import os
import sqlite3
import json
from urllib.parse import parse_qs,unquote_to_bytes
app = Flask(__name__)

application = app # WSGI ...

CWD = os.getcwd()
DB = './data/i.sqlite3'
STORE = './data/files/'

def get_db():
    db = getattr(g,'_database',None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
    return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr('g', '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    d_q = get_db().execute(
        "SELECT devices.id, devices.name, count(audits.id) " +
            "FROM devices LEFT JOIN audits ON devices.id = audits.device_id " +
            "GROUP BY devices.id;")
    d_r = d_q.fetchall()
    res = render_template_string("""<ul>
    {% for i in r %}
        <li><a href="{{url_for('show',dev_id=i[0])}}">{{i[1]}}</a> ({{i[2]}})</li>
    {% endfor %}
</ul>
""",r=d_r)
    d_q.close()
    return res


@app.route('/reg/<path:mcode>',methods=['PUT','POST'])
def reg(mcode):
    def recv(request, file_path):
        if request.content_length and request.content_length > 0  \
                and request.content_length < 1e6:
            tar_fn=file_path+'.tar'
            data=request.get_data()
            #data=unquote_to_bytes(request.data)
            with open(tar_fn,'wb') as f:
                f.write(data)
            try:
                os.mkdir(file_path)
            except FileExistsError:
                pass
            os.chdir(file_path)
            tar=os.popen('tar -xf '+tar_fn).close()
            os.chdir(CWD)
            if tar:
                return 'tar failed: '+str(tar)
        else:
            return 'invalid length.'

    name=re.sub('[^a-zA-Z0-9_-]','_',mcode)
    if request.method=='POST' or request.method=='PUT':
        file_path=STORE+name
        r=recv(request, file_path)
        if r:
            return r
        db=get_db()
        c=db.cursor()
        with open(file_path+'/inventory/lshw.json',encoding='utf-8') as f:
            lshw=f.read()
            jlshw=json.loads(lshw)
        with open(file_path+'/inventory/neofetch.txt',encoding='utf-8') as f:
            neofetch=f.read()
        c.execute('INSERT INTO i(name, version, serial, lshw, neofetch) '+
                'VALUES (?,?,?,?,?);', 
                (name, jlshw['version'], jlshw['serial'] if 'serial' in jlshw else '', lshw, neofetch))
        c.close()
        db.commit()
        return 'ok.'


@app.route('/show/<int:dev_id>')
def show(dev_id):
    c = get_db().cursor()
    c.row_factory = sqlite3.Row
    dev_q = c.execute(
        "SELECT id, name, location, manual, sticker_id, comment, created_at, "
            "updated_at "
        "FROM devices WHERE id = ?;", 
        (str(dev_id)))
    dev_r = dev_q.fetchone()
    man = json.loads(dev_r["manual"])
    if not hasattr(man, '__iter__'):
        man = []

    audit_q = c.execute(
        "SELECT audits.id, audits.created_at, audits.invalid "
        "FROM audits WHERE audits.device_id = ?;",
        (str(dev_id)))
    audit_r = audit_q.fetchall()
    c.close()

    return render_template("device_show.html",
        dev = dev_r, man = man, audit = audit_r)

@app.route('/audit/add/<int:dev_id>')
def audit_add(dev_id):
    db = get_db()
    c = db.cursor()
    dev_q = c.execute("INSERT INTO audits ('device_id') VALUES(?);",
         (str(dev_id)))
    db.commit()
    c.close()
    return "Pr&uuml;fung erstellt"

@app.route('/audit/invalidate/<int:dev_id>/<int:audit_id>')
def audit_invalidate(dev_id, audit_id):
    db = get_db()
    c = db.cursor()
    dev_q = c.execute(
        "UPDATE audits SET invalid = TRUE "
        "WHERE device_id = ? AND id = ?;",
        (str(dev_id), str(audit_id)))
    db.commit()
    c.close()
    return "Pr&uuml;fung zur&uuml;ckgerufen"

@app.route('/edit/<int:dev_id>')
def edit(dev_id):
    c = get_db().cursor()
    c.row_factory = sqlite3.Row
    dev_q = c.execute(
        "SELECT id, name, location, manual, sticker_id, comment, created_at, "
            "updated_at "
        "FROM devices WHERE id = ?;", 
        (str(dev_id)))
    dev_r = dev_q.fetchone()
    man = json.loads(dev_r["manual"])
    if not hasattr(man, '__iter__'):
        man = []

    audit_q = c.execute(
        "SELECT audits.id, audits.created_at "
        "FROM audits WHERE audits.device_id = ? and audits.invalid != TRUE;",
        (str(dev_id)))
    audit_r = audit_q.fetchall()
    c.close()

    return render_template("device_edit.html",
        dev = dev_r, man = man, audit = audit_r)

# , methods=['PUT','POST']

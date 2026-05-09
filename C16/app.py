from flask import Flask, request, render_template_string, g
import sqlite3, os

app = Flask(__name__)
DB  = '/tmp/avengers.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB)
    return g.db

def init_db():
    if not os.path.exists(DB):
        db = sqlite3.connect(DB)
        db.execute('''CREATE TABLE agents (
            id INTEGER PRIMARY KEY,
            codename TEXT,
            clearance TEXT,
            secret TEXT
        )''')
        db.execute("INSERT INTO agents VALUES (1,'rogers','LEVEL_7','not_the_flag')")
        db.execute("INSERT INTO agents VALUES (2,'stark','LEVEL_9','not_the_flag_either')")
        db.execute("INSERT INTO agents VALUES (3,'romanoff','LEVEL_9','nope')")
        db.execute("INSERT INTO agents VALUES (4,'ultron','OMEGA','cyn0x{sql_1nj3ct10n_4ss3mbl3d}')")
        db.commit()
        db.close()

TEMPLATE = """
<!DOCTYPE html><html>
<head><title>Avengers Initiative — Clearance Portal</title>
<style>
  body{background:#0a0a10;color:#ccc;font-family:monospace;padding:40px;}
  h2{color:#e8b800;} input{background:#111;color:#0f0;border:1px solid #333;padding:8px;width:280px;font-family:monospace;}
  button{background:#e8b800;color:#000;border:none;padding:8px 16px;cursor:pointer;font-weight:bold;margin-top:8px;}
  .box{border:1px solid #333;padding:20px;max-width:400px;}
  .result{color:#4f4;margin-top:15px;font-size:13px;} .err{color:#f44;}
</style></head>
<body>
<h2>⚙ AVENGERS INITIATIVE — AGENT CLEARANCE PORTAL</h2>
<p style="color:#555">Enter your codename to retrieve your clearance level.</p>
<div class="box">
  <form method="POST">
    <input name="codename" placeholder="Agent codename" autocomplete="off"><br>
    <button type="submit">Check Clearance</button>
  </form>
  {% if result %}<p class="result">{{ result }}</p>{% endif %}
  {% if err    %}<p class="err">{{ err }}</p>{% endif %}
</div>
</body></html>
"""

@app.route('/', methods=['GET','POST'])
def index():
    result = err = None
    if request.method == 'POST':
        codename = request.form.get('codename','')
        try:
            db  = get_db()
            row = db.execute(
                f"SELECT codename, clearance FROM agents WHERE codename='{codename}'"
            ).fetchone()
            if row:
                result = f"Agent: {row[0]} | Clearance: {row[1]}"
            else:
                err = "Agent not found."
        except Exception as e:
            err = f"DB error: {e}"
    return render_template_string(TEMPLATE, result=result, err=err)

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db: db.close()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
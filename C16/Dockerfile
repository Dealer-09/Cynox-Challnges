FROM python:3.11-slim

WORKDIR /app
RUN pip install flask --no-cache-dir
COPY web/ .

RUN python -c "
import sqlite3, os
DB='/tmp/avengers.db'
db=sqlite3.connect(DB)
db.execute('CREATE TABLE agents (id INTEGER PRIMARY KEY, codename TEXT, clearance TEXT, secret TEXT)')
db.execute(\"INSERT INTO agents VALUES (1,'rogers','LEVEL_7','not_the_flag')\")
db.execute(\"INSERT INTO agents VALUES (2,'stark','LEVEL_9','not_the_flag_either')\")
db.execute(\"INSERT INTO agents VALUES (3,'romanoff','LEVEL_9','nope')\")
db.execute(\"INSERT INTO agents VALUES (4,'ultron','OMEGA','cyn0x{sql_1nj3ct10n_4ss3mbl3d}')\")
db.commit(); db.close()
"

EXPOSE 5000
CMD ["python", "app.py"]
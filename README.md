# Aufsetzen

```
apt-get install python3-flask sqlite3
mkdir ./data
sqlite3 ./data/i.sqlite3 < ./init.sql 
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```


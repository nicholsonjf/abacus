from mini import db, app

db.create_all()

app.run(host='0.0.0.0')

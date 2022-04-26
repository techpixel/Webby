from flask import Flask, render_template, request, url_for, redirect, abort
from db import DB, generatePass
app = Flask('app')

db = DB()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
      title = request.form['title']
      color = request.form['color']

      return redirect(url_for('build', title=title, color=color))

@app.route('/build/<title>/<color>', methods=['GET','POST'])      
def build(title, color):
  if request.method == 'POST':
    markdown = request.form['markdown']
    passw = generatePass()

    uuid = db.setContent(markdown, passw, title, color)

    return render_template('finish.html', uuid=uuid, passw=passw)
  return render_template('builder.html', title=title, color=color)

@app.route('/view/<id>')
def view(id):
  content = db.getContent(id)
  if content == False:
    abort(404)
  else:
    dictContent = content.get().to_dict()
    md = dictContent['md']
    title = dictContent['title']
    color = dictContent['color']
    return render_template('view.html', md=md, title=title, color=color)

@app.route('/dashboard/<id>', methods=['GET', 'POST'])
def dashboard(id):
  content = db.getContent(id)
  if request.method == 'POST':
    dictContent = content.get().to_dict()
    if dictContent['pass'] == request.form['pass']:
      md = dictContent['md']
      title = dictContent['title']
      color = dictContent['color']
      passw = dictContent['pass']
      return render_template('dashboard.html', md=md, title=title, color=color, passw=passw,id=id)

  if request.method == 'GET':
    if content == False:
      abort(404)
    else:
      dictContent = content.get().to_dict()
      md = dictContent['md']
      title = dictContent['title']
      return render_template('dashboardlogin.html', md=md, title=title)

@app.route('/completechanges', methods=['GET','POST'])
def completechanges():
  if request.method == 'POST':
    content = db.getContent(request.form['id'])

    md = request.form['md']
    title = request.form['title']
    color = request.form['color']
    passw = request.form['pass']
      
    db.editContent(request.form['id'], md, title, color, passw)

    return render_template('sucess.html')
  else:
    return render_template('sucess.html')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

app.run(host='0.0.0.0', port=8080)
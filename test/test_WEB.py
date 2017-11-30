from flask import Flask
from flask import request

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
	return '<h1>Home</h1>'

@app.route('/signin',methods=['GET'])
def fignin_form():
	return '''<form action="/signin" method="post">
				<p><input name="username"></p>
				<p><input name="password" type="psddword"></p>
				<p><input name="submit">Sign In</p>
				</form>'''

@app.route('/signin',methods=['POST'])
def signin():
	if request.form['username']=='admin' and request.form['password']=='password':
		return '<h3>Hello Admin!</h3>'
	return '<h3>Bad username or password</h3>'

if __name__=='__main__':
	app.run()
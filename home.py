from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for
from flaskext.mysql import MySQL
import datetime
import bcrypt

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'x'
app.config['MYSQL_DATABASE_PASSWORD'] = 'x'
app.config['MYSQL_DATABASE_DB'] = 'bawk'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

app.secret_key = 'HSDG#$%T34t35t3tREGgfsDG34t34543t3455fdsfgdfsgd'
####################################################

@app.route('/')
def home():
	print session.get('user_id')
	print session.get('username')
	if session.get('user_id'):
		return redirect('/main')
	else:
		return render_template('/index.html')



# Register - - - - - - - - - - - - - - - - - - - 
@app.route('/register')
def reigster():
	print "Register"
	return render_template('/register.html')

@app.route('/register_submit', methods=['POST'])
def register_submit():
	print request.form['user_name']
	#Check to see if username is available or not
	check_username_query = "SELECT * FROM user WHERE username = '%s'" % request.form['user_name']
	cursor.execute(check_username_query)
	check_username_result = cursor.fetchone()
	print check_username_result
	if check_username_result is None:
		#No duplicate, insert the new username
		nickname = request.form['name']
		user_name = request.form['user_name']
		email = request.form['email']
		pw = request.form['password']
		confirm_pw = request.form['confirm-password']
		image = request.files['photo']
		image.save('static/profile/' + image.filename)
		image_path = image.filename
		if pw == confirm_pw:
			password = request.form['password'].encode('utf-8')
			hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
			username_insert_query = "INSERT INTO user (nickname, username, password, email, image) VALUES ('"+nickname+"', '"+user_name+"', '"+hashed_password+"', '"+email+"', '"+image_path+"')"
			cursor.execute(username_insert_query)
			conn.commit()
			return redirect('/login')
		else:
			return render_template('register.html',
				message = "Passwords did not match. Try again.")
	else:
		return render_template('register.html',
				message = "Username you entered is taken. Try a different username. ")
	print check_username_result
	return "DONE"



# Log In - - - - - - - - - - - - - - - - - - - 
@app.route('/login')
def login():	
	if session.get('user_id'):
		return redirect('/main')
	else:
		return render_template('login.html')

@app.route('/login_submit', methods=['POST'])
def login_submit():
	print request.form['username']
	print request.form['password']
	if request.form['username'] is None or "":
		return render_template('login.html',
			message = "Please enter your username.")
	elif request.form['password'] is None or "":
		return render_template('login.html',
			message = "Please enter your password.")
	else: 
		check_username_query = "SELECT id, password FROM user WHERE username = '%s'" % request.form['username']
		cursor.execute(check_username_query)
		check_username_result = cursor.fetchone()
		password = request.form['password'].encode('utf-8')
		hashed_password = check_username_result[1].encode('utf-8')
		if check_username_result is not None:
			print "returned password: %s" % check_username_result[1]
			# Check a hash against English
			if bcrypt.hashpw(password, hashed_password) == hashed_password:
				# it's a match
				session['username'] = request.form['username']
				session['user_id'] = check_username_result[0]
				return redirect('/main')
			else:
				return render_template('/login.html',
					message = "Please enter your password again.")
		else:
			return render_template('/login.html',
				message = "No username was found. Please try again.")

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')


# Main - - - - - - - - - - - - - - - - - - - 
@app.route('/main')
def main():
	if session.get('user_id'):
		user_info_query = "SELECT id, username, nickname, followers, following, image, total_votes FROM user WHERE id = '%s'" % session['user_id']
		cursor.execute(user_info_query)
		data1 = cursor.fetchone()

		all_posts_query = "SELECT post.id, post.user_id, user.username, user.image, post.post, post.votes, post.posted_at FROM user INNER JOIN post ON user.id = post.user_id ORDER BY post.posted_at DESC"
		cursor.execute(all_posts_query)
		data2 = cursor.fetchall()

		user_id = session['user_id']
		username = session['username']
		return render_template('main.html',
			user_info = data1,
			posts = data2,
			user_id = user_id,
			username = username)
	else:
		return redirect('/')


# My page - - - - - - - - - - - - - - - - - - - 
@app.route('/my_page')
def my_page():
	user_id = session['user_id']
	user_info_query = "SELECT id, username, nickname, followers, following, image, total_votes FROM user WHERE id = '%s'" % user_id
	cursor.execute(user_info_query)
	data1 = cursor.fetchone()
	print data1
	user_post_query = "SELECT post.id, user.id, user.username, post.post, post.posted_at, post.votes FROM user INNER JOIN post ON user.id = post.user_id WHERE user.id = '%s' ORDER BY post.posted_at DESC" % user_id
	cursor.execute(user_post_query)
	data2 = cursor.fetchall()
	following_query = "SELECT u.id, u.username, u.nickname, u.image, u.total_votes from followers as f INNER JOIN user as u ON f.uid_followed = u.id WHERE uid_following = '%s'" % user_id
	cursor.execute(following_query)
	data3 = cursor.fetchall()
	follower_query = "SELECT u.id, u.username, u.nickname, u.image, u.total_votes from followers as f INNER JOIN user as u ON f.uid_following = u.id WHERE uid_followed = '%s'" % user_id
	cursor.execute(follower_query)
	data4 = cursor.fetchall()
	return render_template('my_page.html',
				user_info = data1,
				user_posts = data2,
				user_stat = [len(data2), len(data3), len(data4)],
				followings = data3,
				followers =  data4,
				user_id = session['user_id'],
				username = session['username'])

# User page - - - - - - - - - - - - - - - - - - - 
@app.route('/user_page/<id>', methods=['GET'])
def user_page(id):
	user_id = id
	print "go to this page: %s" % user_id
	user_info_query = "SELECT id, username, nickname, followers, following, image, total_votes FROM user WHERE id = '%s'" % user_id
	cursor.execute(user_info_query)
	data1 = cursor.fetchone()
	print data1
	user_post_query = "SELECT post.id, user.id, user.username, post.post, post.posted_at, post.votes FROM user INNER JOIN post ON user.id = post.user_id WHERE user.id = '%s' ORDER BY post.posted_at DESC" % user_id
	cursor.execute(user_post_query)
	data2 = cursor.fetchall()
	print data2
	user_post_query = "SELECT post.id, user.id, user.username, post.post, post.posted_at, post.votes FROM user INNER JOIN post ON user.id = post.user_id WHERE user.id = '%s' ORDER BY post.posted_at DESC" % user_id
	cursor.execute(user_post_query)
	data2 = cursor.fetchall()
	following_query = "SELECT u.id, u.username, u.nickname, u.image, u.total_votes from followers as f INNER JOIN user as u ON f.uid_followed = u.id WHERE uid_following = '%s'" % user_id
	cursor.execute(following_query)
	data3 = cursor.fetchall()
	follower_query = "SELECT u.id, u.username, u.nickname, u.image, u.total_votes from followers as f INNER JOIN user as u ON f.uid_following = u.id WHERE uid_followed = '%s'" % user_id
	cursor.execute(follower_query)
	data4 = cursor.fetchall()
	my_followings = "SELECT u.id from followers as f INNER JOIN user as u ON f.uid_followed = u.id WHERE uid_following = '%s'" % user_id
	cursor.execute(my_followings)
	data3 = cursor.fetchall()
	following = "0"
	for user in data3:
		if user == session['user_id']:
			following = 1

	return render_template('user_page.html',
			user_info = data1,
			posts = data2,
			user_stat = [len(data2), len(data3), len(data4)],
			followings = data3,
			followers =  data4,
			following = following,
			user_id = session['user_id'],
			username = session['username'])


# Post - - - - - - - - - - - - - - - - - - - 
@app.route('/post_submit', methods=['POST'])
def post_submit():
	user_id = session['user_id']
	content = request.form['post_content']
	print content
	post_query = 'INSERT INTO post (post, user_id) values (%s, %s)'
	cursor.execute(post_query, (content, user_id))
	conn.commit()
	return redirect('/main')

# Vote - - - - - - - - - - - - - - - - - - - 
@app.route('/vote', methods=['POST'])
def vote():
	pid = request.form['pid']
	calc = int(request.form['calc'])
	print "pid: %s, cacl: %s" % (pid, calc)

	pid_query = "SELECT post.id, post.votes, post.user_id, user.total_votes FROM post INNER JOIN user ON post.user_id = user.id WHERE post.id = '%s'" % pid
	print pid_query
	cursor.execute(pid_query)
	post = cursor.fetchone()
	post_votes = post[1]
	post_user_id = post[2]
	user_votes = post[3]
	print "post_votes: %s, post_user_id: %s, user_votes: %s" % (post_votes, post_user_id, user_votes)

	if calc == 1:
		post_votes = post_votes + 1
		user_votes = user_votes + 1
	else:
		post_votes = post_votes - 1
		user_votes = user_votes - 1
	print "updated post_votes: %s, user_votes: %s" % (post_votes, user_votes)

	vote_query = "UPDATE post SET votes = '%s' WHERE id = '%s'" % (post_votes, pid)
	cursor.execute(vote_query)
	conn.commit()
	updated_post = cursor.fetchone()

	user_query = "UPDATE user SET total_votes = '%s' WHERE id = '%s'" % (user_votes, post_user_id)
	cursor.execute(user_query)
	conn.commit()
	updated_user = cursor.fetchone()
	return jsonify({
		'pid': pid,
		'post_votes': post_votes,
		'userid': post_user_id,
		'user_votes': user_votes
		})

# Remove post - - - - - - - - - - - - - - - - - - - 
@app.route('/removePost', methods=['POST'])
def remove_post():
	post_id = request.form['pid']
	remove_query = "DELETE FROM post WHERE id = '%s'" % post_id
	cursor.execute(remove_query)
	conn.commit()
	return jsonify({
		'status': post_id + "removed"
		})

# Follow - - - - - - - - - - - - - - - - - - - 
@app.route('/follow')
def follow():
	user_info_query = "SELECT id, username, nickname, followers, following, image, total_votes FROM user WHERE id = '%s'" % session['user_id']
	cursor.execute(user_info_query)
	data1 = cursor.fetchone()
	user_post_query = "SELECT post.id, user.id, user.username, post.post, post.posted_at, post.votes FROM user INNER JOIN post ON user.id = post.user_id WHERE user.id = '%s' ORDER BY post.posted_at DESC" % session['user_id']
	cursor.execute(user_post_query)
	data2 = cursor.fetchall()
	followers_query = "SELECT * FROM followers WHERE uid_followed = '%s'" % session['user_id']
	cursor.execute(followed_query)
	data3 = cursor.fetchall()
	follwing_query = "SELECT * FROM followers WHERE uid_following = '%s'" % session['user_id']
	data4 = cursor.fetchall()
	print 'all followers - - - - -- - - - '
	print data3
	print 'all following - - - - - -- - '
	print data4

	return render_template('follow.html'
					)

####################################################
if (__name__) == "__main__":
	app.run(debug = True)
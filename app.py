from flask import Flask,render_template,redirect,url_for,session,g, flash
from wtform_fields import *
from flask_socketio import SocketIO, send,emit,join_room,leave_room
from time import localtime,strftime
from user import User
import utils
import sign
app=Flask(__name__)
app.secret_key='replace later'

socketio=SocketIO(app)

CONNECTED_USERS=[]
for item in sign.getConnectedUsers():
    if User(*item) not in CONNECTED_USERS:
       CONNECTED_USERS.append(User(*item).pseudo)


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = sign.getUserById(session['user_id'])
        g.user = user
        # if g.user not in CONNECTED_USERS:
        #     CONNECTED_USERS.append(g.user)





@app.route("/",methods=['GET','POST'])
def index():
    reg_form=RegistrationForm()
    if reg_form.validate_on_submit():
        nom = reg_form.nom.data
        prenom = reg_form.prenom.data
        num_card = reg_form.num_card.data
        pseudo = reg_form.pseudo.data
        email = reg_form.email.data
        pwd = reg_form.pwd.data
        cerPath = f'build/{nom}{num_card}.cert'
        keyPath = f'build/{nom}{num_card}.key'
        utils.createCertRequest(nom, 'TN', 'Tunis', 'insat', nom, email, cerPath, keyPath)
        utils.createCert(f'build/{nom}{num_card}.cert')
        sign.signUp(num_card, nom, prenom, pseudo, email, pwd, cerPath, keyPath)
        return redirect(url_for('login'))
    return render_template("index.html",form=reg_form)

@app.route("/login",methods=['GET','POST'])
def login():
    login_form=LoginForm()


    if login_form.validate_on_submit():
        session.pop('user_id', None)
        user=sign.getUserByEmail(login_form.email.data)

        session['user_id'] = user.id
        sign.connecter(user.id)
        return redirect(url_for('chat'))
    else:
        flash('Please login before accessing chat','danger')
        return render_template("login.html",form=login_form)

@app.route("/logout", methods=['GET'])
def logout():

    # Logout user
    sign.deconnecter(g.user.id)
    session.clear()
    return redirect(url_for('login'))



@app.route("/chat",methods=['GET','POST'])
def chat():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('chat.html', username=g.user.pseudo,rooms=CONNECTED_USERS)


@socketio.on('message')
def message(data):
    # print(data)
    send({'msg':data['msg'], 'username': data['username'], 'time_stamp':strftime('%b-%d %I:%M%p', localtime())},room=data['room'])
    # emit('some-event','this is a custom event messqge')
@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({'msg':data['username']+"  has joined the disscussion with "+data['room']}, room=data['room'])


@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + "  has left the disscussion with " + data['room']}, room=data['room'])


if __name__=="__main__":
    socketio.run(app,debug=True, allow_unsafe_werkzeug=True)

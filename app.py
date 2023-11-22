from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import random
from flask_socketio import SocketIO, join_room, leave_room


local_server = True
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config.update(
    APPLICATION_ROOT='/'
)


socketio = SocketIO(app)

game = {1: [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]],2: [[2,1,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]}

def check(user):
    coun = 0
    for i in game[user]:
        a=0
        for j in i:
            a=a+j
        if a==0:
            coun=coun+1
            print('hello1'+str(coun))
    print(coun)
    print('1')
    for i in range(5):
        a=0
        for j in range(5):
            a=a+game[user][j][i]
        if a==0:
            coun=coun+1
            print('hello2'+str(coun))

    print(coun)
    print('2')

    a=0
    for i in range(5):
        
        a=a+game[user][i][i]

    if a==0:
        coun=coun+1
        print('hello3'+str(coun))

    print(coun)
    print('3')

    a=0
    for i in range(5):
        for j in range(5):
            if i+j==4:
                a=a+game[user][i][j]
    if a==0:
        coun=coun+1
        print('hello4'+str(coun))
    

    if coun>=5:
        print(game)
        print('True')
        return True
    else:
        print('False')
        return False



def reset(user):
    
    a = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    # code to shuffle the list
    random.shuffle(a)
    
    for i in game[user]:
        for j in i:
            game[user][game[user].index(i)][i.index(j)]=a.pop()

def re():
    
    game = {1: [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]],2: [[2,1,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]}
    reset(1)
    reset(2)


def dot(user,text):
    for i in game[user]:
        print(i)
        if text in i:
            a = str(10*game[user].index(i)+i.index(text))
            game[user][game[user].index(i)][i.index(text)]=0
            return a




@app.route("/",methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'user1' and password == 'user':
            session['activeUser'] = 1
            return redirect('/game')
        elif username == 'user2' and password == 'user':
            session['activeUser'] = 2
            return redirect('/game')



        return redirect('/')

    return render_template('index.html')


@app.route("/game")
def bingo():
    if not 'activeUser' in session:
        return redirect('/')

    return render_template('game.html', post = game[session['activeUser']],user=session['activeUser'])


@socketio.on('play')
def play(data):
    print(data)
    print('hello')
    user = int(data['user'])
    text = int(data['text'])
    anuser = (user%2)+1
    print(user)
    print(text)
    

    p1 = dot(user,text)
    p2 = dot(anuser,text)

    if check(user):
        data = {'win':user,'user':{'user':user,'position':p1}, 'anuser':{'user':anuser,'position':p2}}
        # data = {'win':user,'user':{'user':user,'position':position(user,text)}, 'anuser':{'user':anuser,'position':position(anuser,text)}}
        # data['text']=session['activeUser']




        # return jsonify(dict(text=1, user=user))
        
        socketio.emit('receive_message', data, room=123)
    
    data = {'win':0,'user':{'user':user,'position':p1}, 'anuser':{'user':anuser,'position':p2}}
    # data = {'win':0,'user':{'user':user,'position':position(user,text)}, 'anuser':{'user':anuser,'position':position(anuser,text)}}
    # return jsonify(dict(text=0,user=str(user)))

    socketio.emit('receive_message', data, room=123)


# @socketio.on('play')
# def play(data):
#     print(data)
#     print('hello')
#     user = int(data['user'])
#     text = int(data['text'])
#     anuser = (user%2)+1
#     print(user)
#     print(text)
#     for i in game[user]:
#         if text in i:
#             # code to pri5thelemen of list


#             game[user][game[user].index(i)][i.index(text)]=0
#             print(game)

#             if check(user):
#                 data = {'win':user,'user':{'user':user,'position':position(user,text)}, 'anuser':{'user':anuser,'position':position(anuser,text)}}
#                 # data['text']=session['activeUser']

#                 # return jsonify(dict(text=1, user=user))
                
#                 socketio.emit('receive_message', data, room=123)
        

#     data = {'win':0,'user':{'user':user,'position':position(user,text)}, 'anuser':{'user':anuser,'position':position(anuser,text)}}
#     # return jsonify(dict(text=0,user=str(user)))

#     socketio.emit('receive_message', data, room=123)





@app.route('/win')
def win():
    return render_template('win.html')

@app.route('/lose')
def lose():
    return render_template('lose.html')

@app.route('/reset',methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        password = request.form['password']

        if password == 'dkandi':
            re()
            print(game)


    return render_template('reset.html')





@socketio.on('join_room')
def handle_join_room_event(data):
    join_room(123)
    socketio.emit('join_room_announcement', data, room=123)


@socketio.on('leave_room')
def handle_leave_room_event(data):
    leave_room(123)
    socketio.emit('leave_room_announcement', data, room=123)




if __name__ == "__main__":
    #code to run app on 10.250.93.252

    # socketio.run(app, debug=True, port=3002)
    socketio.run(app,host='10.206.4.114', debug=True, port=3002)
    # socketio.run(app,host='10.250.93.252', debug=True, port=3002)
    # app.run(port=3002,debug=True)
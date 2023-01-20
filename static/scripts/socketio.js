document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
let room

socket.on('message',data=>{
const p=document.createElement('p');
const span_username=document.createElement('span')
const br=document.createElement('br');

const span_timestamp = document.createElement('span');
span_username.innerHTML=data.username;
span_timestamp.innerHTML=data.time_stamp
p.innerHTML=span_username.outerHTML+br.outerHTML+data.msg+br.outerHTML+span_timestamp.outerHTML;
document.querySelector('#display-message-section').append(p);
});


    // Send messages
    document.querySelector('#send_message').onclick = () => {
    socket.send({'msg': document.querySelector('#user_message').value,'username': username,'room': room});

    };

document.querySelectorAll('.select-room').forEach(p =>{
p.onclick=()=>{
let newRoom =p.innerHTML;
if(newRoom==room){
msg="you already in the discussion with "+ room;
printSysMsg(msg);
}else{
leaveRoom(room);
joinRoom(newRoom);
room=newRoom;
}

}
});

function leaveRoom(room){
socket.emit('leave', {'username': username, 'room': room});
}

 function joinRoom(room) {

        // Join room
        socket.emit('join', {'username': username, 'room': room});



        // Clear message area
        document.querySelector('#display-message-section').innerHTML = '';


    }

     function printSysMsg(msg) {
        const p = document.createElement('p');
//        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
//        scrollDownChatWindow()
//
//        // Autofocus on text box
//        document.querySelector("#user_message").focus();
    }


});
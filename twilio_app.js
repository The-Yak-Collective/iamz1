const button = document.getElementById('join_leave');
const container = document.getElementById('container');
const par_count = document.getElementById('par_count');
var connected = false;
var room;
var localtrack;



function addLocalVideo() {
    Twilio.Video.createLocalVideoTrack().then(track => {
        localtrack=track;
        var video = document.getElementById('vid_local').firstChild;
        video.appendChild(track.attach());
    });
};
function rmLocalVideo() {

//have no idea what to put here to actually disconnect the video

localtrack.stop();
room.localParticipant.unpublishTrack(localtrack);
document.getElementById('vid_local').firstChild.firstChild.remove();
};

function connectButtonHandler(event) {
    event.preventDefault();
    if (!connected) {
        var username = my_user_name;
        button.disabled = true;
        button.innerHTML = 'Connecting...';
        connect(username).then(() => {
            button.innerHTML = 'Leave call';
            button.disabled = false;
        }).catch(() => {
            alert('Connection failed. Is the backend running?');
            button.innerHTML = 'Join call';
            button.disabled = false;
        });
    }
    else {
        disconnect();
        button.innerHTML = 'Join call';
        connected = false;
    }
};

function connect(username) {
    var promise = new Promise((resolve, reject) => {
        // get a token from the back end
        fetch('https://visavis.chat/twilio_iamz1_token_new', {
            method: 'POST',
            body: JSON.stringify({'username': username})
        }).then(res => res.json()).then(data => {
            // join video call
            return Twilio.Video.connect(data.token,{audio: false});
        }).then(_room => {
            room = _room;
            console.log(room);
            room.participants.forEach(participantConnected);
            room.on('participantConnected', participantConnected);
            room.on('participantDisconnected', participantDisconnected);
            connected = true;
            updateParticipantCount();
            resolve();
        }).catch(() => {
            reject();
        });
    });
    return promise;
};

function updateParticipantCount() {
    if (!connected)
        par_count.innerHTML = 'Disconnected.';
    else
        par_count.innerHTML = (room.participants.size + 1) + ' participants online.';
};

function participantConnected(participant) {
    var participant_div = document.createElement('div');
    participant_div.setAttribute('id', participant.sid);
    participant_div.setAttribute('class', 'participant');

    var tracks_div = document.createElement('div');
    participant_div.appendChild(tracks_div);

    var label_div = document.createElement('div');
    label_div.innerHTML = participant.identity;
    participant_div.appendChild(label_div);

    container.appendChild(participant_div);

    participant.tracks.forEach(publication => {
        if (publication.isSubscribed)
            trackSubscribed(tracks_div, publication.track);
    });
    participant.on('trackSubscribed', track => trackSubscribed(tracks_div, track));
    participant.on('trackUnsubscribed', trackUnsubscribed);

    updateParticipantCount();
};

function participantDisconnected(participant) {
    document.getElementById(participant.sid).remove();
    updateParticipantCount();
};

function trackSubscribed(div, track) {
    div.appendChild(track.attach());
};

function trackUnsubscribed(track) {
    track.detach().forEach(element => element.remove());
};

function disconnect() {
    room.disconnect();
    while (container.lastChild.id != 'vid_local')
        container.removeChild(container.lastChild);
    button.innerHTML = 'Join call';
    connected = false;
    updateParticipantCount();
};


button.addEventListener('click', connectButtonHandler);


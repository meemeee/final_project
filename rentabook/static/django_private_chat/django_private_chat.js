// Template for new websocket message
const template = Handlebars.compile(document.querySelector('#ws_new_message').innerHTML);

// Get user name
const user = document.querySelector('#user_name').innerHTML;

// Handlebars helper
// Compareing usernames
Handlebars.registerHelper('if_eq', function(a, opts) {
    if (a === user) {
        return opts.fn(this);
    } else {
        return opts.inverse(this);
    }
});

// Returns first letter of username
Handlebars.registerHelper('firstLetter', function(a) {
    return a[0];
});


// Insert referrer url to 'go back' text if available
if (document.querySelector("#referrer")) {
    document.querySelector("#referrer").href = document.referrer;
}

$(function () {
    // Sidebar toggle behavior
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar, #content').toggleClass('active');
    });
});

// Set up websocket
var base_ws_server_path = ws_server_path;
$(document).ready(function () {

    
    // Remove footer
    document.querySelector('footer').remove();

    var websocket = null;
    var monitor = null;

    function initReadMessageHandler(containerMonitor, elem) {
        var id = $(elem).data('id');
        var elementWatcher = containerMonitor.create(elem);
        elementWatcher.enterViewport(function () {
            var opponent_username = getOpponnentUsername();
            var packet = JSON.stringify({
                type: 'read_message',
                session_key: request_session_sessionKey,
                username: opponent_username,
                message_id: id
            });
            $(elem).removeClass('msg-unread').addClass('msg-read');
            websocket.send(packet);

        });
    }

    function initScrollMonitor() {
        var containerElement = $("#messages");
        var containerMonitor = scrollMonitor.createContainer(containerElement);

        // Mark 'Read' when scrolling messages
        document.querySelectorAll('.msg-unread').forEach(div => {
            if (div.classList.contains('opponent')) {
                initReadMessageHandler(containerMonitor, div);
            };
        });

        return containerMonitor
    }

    function getOpponnentUsername() {
        return username_of_opponent;
    }

    function addNewMessage(packet) {
        // Add new message to DOM.
        let mess = template({'data': packet});        
        $('#messages').append(mess);
        scrollToLastMessage();
    }

    function scrollToLastMessage() {
        var allmess = document.querySelector('#messages');    
        allmess.scrollTop = allmess.scrollHeight;
    }

    function gone_online() {
        $("#offline-status").hide();
        $("#online-status").show();
    }

    function gone_offline() {
        $("#online-status").hide();
        $("#offline-status").show();
    }

    // alert new messages and add 'Unread' icon
    function alert_new_message(username) {
        var newmess_channel = document.querySelector("#user-" + username);
        var newmess_channel_name = document.querySelector(`[id='${username}']`);
     
        // Discard action if there has been an earlier alert
        if (newmess_channel.classList.contains('convo-unread'))
            return false;
        else {
            const newmess_alert = document.createElement('i');
            newmess_alert.setAttribute('id', 'unread-' + username);
            newmess_alert.setAttribute('class', 'fa fa-circle ml-2');
            newmess_channel.classList.add('convo-unread');
            newmess_channel_name.append(newmess_alert);
        }
    }

    function setupChatWebSocket() {
        var opponent_username = getOpponnentUsername();
        websocket = new WebSocket(base_ws_server_path + request_session_sessionKey + '/' + opponent_username);

        websocket.onopen = function (event) {
            var opponent_username = getOpponnentUsername();
            console.log(opponent_username);
            var onOnlineCheckPacket = JSON.stringify({
                type: "check-online",
                session_key: request_session_sessionKey,
                username: opponent_username
                // Sending username because the user needs to know if his opponent is online
            });
            var onConnectPacket = JSON.stringify({
                type: "online",
                session_key: request_session_sessionKey

            });

            console.log('connected, sending:', onConnectPacket);
            websocket.send(onConnectPacket);
            console.log('checking online opponents with:', onOnlineCheckPacket);
            websocket.send(onOnlineCheckPacket);
            monitor = initScrollMonitor();
        };


        window.onbeforeunload = function () {
            // remove 'Unread' alert (if any) when closing a chat box 
            if (document.querySelector("#unread-" + opponent_username)) {
                document.querySelector("#unread-" + opponent_username).remove();
            }

            var onClosePacket = JSON.stringify({
                type: "offline",
                session_key: request_session_sessionKey,
                username: opponent_username,
                // Sending username because to let opponnent know that the user went offline
            });
            console.log('unloading, sending:', onClosePacket);
            websocket.send(onClosePacket);
            websocket.close();

        };


        websocket.onmessage = function (event) {
            var packet;

            try {
                packet = JSON.parse(event.data);
                console.log(packet)
            } catch (e) {
                console.log(e);
            }

            switch (packet.type) {
                case "new-dialog":
                    // TODO: add new dialog to dialog_list
                    break;
                case "user-not-found":
                    // TODO: dispay some kind of an error that the user is not found
                    break;
                case "gone-online":
                    if (packet.usernames.indexOf(opponent_username) != -1) {
                        gone_online();
                    } else {
                        gone_offline();
                    }
                    for (var i = 0; i < packet.usernames.length; ++i) {
                        // setUserOnlineOffline(packet.usernames[i], true);
                    }
                    break;
                case "gone-offline":
                    if (packet.username == opponent_username) {
                        gone_offline();
                    }
                    break;
                case "new-message":
                    if (packet['sender_name'] == opponent_username || packet['sender_name'] == $("#owner_username").val()) {
                        addNewMessage(packet);
                        if (packet['sender_name'] == opponent_username) {
                            initReadMessageHandler(monitor, $("div[data-id='" + packet['message_id'] + "']"));
                        }
                        else {
                            // remove 'Unread' alert (if any) when send a response 
                            if (document.querySelector("#unread-" + opponent_username)) {
                                document.querySelector("#unread-" + opponent_username).remove();
                                document.querySelector(`[data-name='${opponent_username}']`).classList.remove('convo-unread');

                            }
                        }
                    } else {
                        alert_new_message(packet['sender_name']);
                    }
                    break;
         
                case "opponent-read-message":
                    if (packet['username'] == opponent_username) {
                        $("div[data-id='" + packet['message_id'] + "']").removeClass('msg-unread').addClass('msg-read');
                    }
                    break;

                default:
                    console.log('error: ', event)
            }
        }
    }

    function sendMessage(message) {
        var opponent_username = getOpponnentUsername();
        var newMessagePacket = JSON.stringify({
            type: 'new-message',
            session_key: request_session_sessionKey,
            username: opponent_username,
            message: message
        });
        websocket.send(newMessagePacket)
    }

    $('#chat-message').keypress(function (e) {
        if (e.which == 13 && this.value) {
            sendMessage(this.value);
            this.value = "";
            return false
        } else {
            var opponent_username = getOpponnentUsername();
            var packet = JSON.stringify({
                type: 'is-typing',
                session_key: request_session_sessionKey,
                username: opponent_username,
                typing: true
            });
            websocket.send(packet);
        }
    });

    $('#btn-send-message').click(function (e) {
        var $chatInput = $('#chat-message');
        var msg = $chatInput.val();
        if (!msg) return;
        sendMessage($chatInput.val());
        $chatInput.val('')
    });

    setupChatWebSocket();
    scrollToLastMessage();
});


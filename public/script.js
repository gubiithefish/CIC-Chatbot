document.getElementById("inputBox").select();
document.getElementById("inputBox")
    .addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.keyCode === 13) {
            addMessageToConversation(document.getElementById("inputBox").value)
            sendMessage(document.getElementById("inputBox").value)
            document.getElementById("inputBox").value = ""
        }
    });


// USER: Add message to frontend
function addMessageToConversation(msg) {
    var userChatTemplate = document.getElementById('me-msg')
    var userChatCloning = userChatTemplate.cloneNode(true);
    userChatCloning.id = "";
    userChatCloning.firstElementChild.firstElementChild.firstElementChild.firstElementChild.innerText = msg

    // Append clone to <Conversation container>
    const conversation = document.getElementById("conversation");
    conversation.appendChild(userChatCloning);
}


// CHATBOT: Add message to frontend
function addBotMessageToConversation(msg) {
    var botChatTemplate = document.getElementById('bot-msg')
    var botChatCloning = botChatTemplate.cloneNode(true);
    botChatCloning.id = "";
    botChatCloning.firstElementChild.firstElementChild.firstElementChild.firstElementChild.innerText = msg

    // Append clone to <Conversation container>
    const conversation = document.getElementById("conversation");
    conversation.appendChild(botChatCloning);

    // Scroll view down to inputBox
    var element = document.getElementById("inputBox");
    element.scrollIntoView();
}


// Send message to backend to be processed by the dialog flow
function sendMessage(msg) {
    fetch("http://127.0.0.1:8000/api/v1/dialog?input_text=" + msg, {
            "headers": {
                "accept": "application/json",
                "accept-language": "da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7",
                "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-platform": "\"Android\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin"
            },
            "referrer": "http://127.0.0.1:8000/docs",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "body": null,
            "method": "POST",
            "mode": "cors",
            "credentials": "omit"
        }).then(response => response.json())
        .then(data => addBotMessageToConversation(data.msg));;
}


const el = document.getElementById('messages')
el.scrollTop = el.scrollHeight

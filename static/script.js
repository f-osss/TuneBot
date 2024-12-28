const handleSendMessages = (e) => {
    e.preventDefault()
    const chat = document.getElementById('chat')
    const message = chat.value
    const xhr = new XMLHttpRequest()
    if (message.trim() !== '') {
        xhr.open('POST', '/chat', true)
        xhr.setRequestHeader('Content-Type', 'application/json')
        xhr.withCredentials = true
        const data = JSON.stringify({message: message})

        xhr.onload = () => {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                const messagesContainer = document.getElementById('messages');
                const userMessage = document.createElement('div');
                userMessage.className = 'message-right';
                userMessage.textContent = message;
                messagesContainer.appendChild(userMessage);

                if (response.reply && response.reply.trim() !== '') {
                    const botReply = document.createElement('div');
                    botReply.className = 'message-left';
                    botReply.textContent = response.reply;
                    messagesContainer.appendChild(botReply);
                } else {
                    console.error('No reply from the server.');
                }

                messagesContainer.scrollTop = messagesContainer.scrollHeight;


            } else {
                console.error('Error sending message:', xhr.statusText);
            }
        };

        xhr.send(data)
        chat.value = ''
    }
}


document.addEventListener("DOMContentLoaded", () => {

    const send = document.getElementById('send');
    send.addEventListener('click', handleSendMessages);


    const chatInput = document.getElementById('chat');
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleSendMessages(e);
        }
    });
});

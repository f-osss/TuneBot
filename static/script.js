const handleSendMessages = (e) => {
    e.preventDefault();

    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'message-left';
    typingIndicator.id = 'typing-indicator';
    typingIndicator.style.display = 'none';

    const typingDots = document.createElement('span');
    typingDots.className = 'typing-dots';
    typingDots.textContent = 'Thinking...';
    typingIndicator.appendChild(typingDots);


    const chat = document.getElementById('chat');
    const message = chat.value;
    if (message.trim() !== '') {
        const data = JSON.stringify({message: message});
        const messagesContainer = document.getElementById('messages');

        const userMessage = document.createElement('div');
        userMessage.className = 'message-right';
        userMessage.textContent = message;
        messagesContainer.appendChild(userMessage);

        messagesContainer.appendChild(typingIndicator);
        typingIndicator.style.display = 'block';
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: data,
            credentials: 'include',
        })
            .then(response => response.json())
            .then(response => {
                typingIndicator.style.display = 'none';

                if (response.reply && response.reply.trim() !== '') {
                    const botReply = document.createElement('div');
                    botReply.className = 'message-left';
                    botReply.innerHTML = response.reply;
                    messagesContainer.appendChild(botReply);
                } else {
                    console.error('No reply from the server.');
                    const botReply = document.createElement('div');
                    botReply.className = 'message-left';
                    botReply.textContent = "There was an error getting a response, please try again";
                    messagesContainer.appendChild(botReply);
                }

                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            })
            .catch(error => {
                console.error('Error sending message:', error);
                const botReply = document.createElement('div');
                botReply.className = 'message-left';
                botReply.textContent = "Oops! Something went wrong. Please try again.";
                messagesContainer.appendChild(botReply);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            });

        chat.value = '';
    }
};

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

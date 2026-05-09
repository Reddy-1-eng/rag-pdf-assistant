// RAG PDF Assistant JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const questionInput = document.getElementById('question-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    const status = document.getElementById('status');

    // Send question function
    async function sendQuestion() {
        const question = questionInput.value.trim();
        if (!question) return;

        // Add user message to chat
        addMessage(question, 'user');
        questionInput.value = '';
        sendButton.disabled = true;
        status.textContent = 'Processing your question...';
        status.className = 'status loading';

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question })
            });

            const data = await response.json();

            if (response.ok) {
                // Add bot response to chat
                addMessage(data.answer, 'bot', data.sources);
                status.textContent = 'Ready to answer questions';
                status.className = 'status';
            } else {
                throw new Error(data.detail || 'Failed to get response');
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, I encountered an error while processing your question. Please try again.', 'bot');
            status.textContent = 'Error occurred - Ready to try again';
            status.className = 'status error';
        } finally {
            sendButton.disabled = false;
        }
    }

    // Add message to chat
    function addMessage(content, sender, sources = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        let messageHTML = `<div class="message-content">`;
        
        if (sender === 'user') {
            messageHTML += `<strong>You:</strong> ${content}`;
        } else {
            messageHTML += `<strong>Assistant:</strong> ${content}`;
            
            if (sources && sources.length > 0) {
                messageHTML += `<div class="sources"><strong>Sources:</strong><br>`;
                sources.forEach(source => {
                    const fileName = source.source ? source.source.split('/').pop() : 'Unknown';
                    messageHTML += `• ${fileName} (Page ${source.page || 'N/A'})<br>`;
                });
                messageHTML += `</div>`;
            }
        }
        
        messageHTML += `</div>`;
        messageDiv.innerHTML = messageHTML;

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Event listeners
    sendButton.addEventListener('click', sendQuestion);
    
    questionInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendQuestion();
        }
    });

    // Focus on input
    questionInput.focus();
});

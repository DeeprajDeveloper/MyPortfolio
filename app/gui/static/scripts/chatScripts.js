import { getFormattedDateTime } from "./utils/customDatetime.js";
import { DEFAULT_TEXTAREA_HEIGHT } from "./constants/constants.js";
const formattedDateTime = getFormattedDateTime();

// Description: This script handles the chat dialog functionality, including showing and hiding the dialog, sending messages, and formatting the date and time.
const dialog = document.getElementById("dialog");
const showButton = document.getElementById("chat");
const closeButton = document.getElementById("dialog_close_button");
const messageInput = document.getElementById("message_input");
var chatMessages = document.getElementById("dialog_body");

const textarea = document.getElementById("message_input");

textarea.addEventListener("input", () => {
    var scroll_height = textarea.scrollHeight;
    textarea.style.height = `${DEFAULT_TEXTAREA_HEIGHT}px`;
    textarea.style.height = scroll_height + "px";
    if(textarea.value === "") {
        textarea.style.height = `${DEFAULT_TEXTAREA_HEIGHT}px`;
    }
});

// showButton.addEventListener("click", () => {
//     dialog.showModal();
//     document.body.style.overflow = "hidden";
// });

// closeButton.addEventListener("click", () => {
//     dialog.close();
//     document.body.style.overflow = "";
// });

function sendMessage() {
    const message = messageInput.value.trim();
    sendChatToServer(message).then((response) => {
        const chatBubble = document.createElement("p");
        const messageElement = document.createElement("span");
        const userDetails = document.createElement("span");
        
        // userDetails.innerText = `${response['sender']} • ${response['timestamp']}`;
        userDetails.innerText = `You`;
        userDetails.className = "user_details";

        chatBubble.className = "chat_bubble";
        chatBubble.id = "user";
        messageElement.textContent = 'Sample Text';
        messageElement.className = "message";

        chatBubble.appendChild(messageElement);
        chatBubble.appendChild(userDetails);

        chatMessages.appendChild(chatBubble);
        messageInput.value = "";
    });
}

async function sendChatToServer(event) {
    event.preventDefault();
    const message = messageInput.value.trim();
    if (message) {
        const response = await fetch("{{ url_for('bp_gui.chat') }}", {
            method: "POST",
            headers: { "Content-Type": "application/json", },
            body: JSON.stringify({
                message: message,
                timestamp: `${formattedDateTime()}`,
            }),
        });
        const data = await response.json();
        return data.response;
    }
}

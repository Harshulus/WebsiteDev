// var messages = document.getElementById("messages")
// var textbox = document.getElementById("textbox")
// var button = document.getElementById("button")

// button.addEventListener("click", function() {
//     if (textbox.value != "") {
//         var message = document.createElement("p");
//         message.innerHTML = textbox.value;
    
//         messages.appendChild(message);
//     }
//     textbox.value = "";
// })


var messagesTemp = [
    {
        sender: "John", 
        recipient: "Billy", 
        date: Date.now(), 
        content: "Hey there"
    }, 
    {
        sender: "Jim", 
        recipient: "admin", 
        date: Date.now(), 
        content: "Hey there"
    }, 
    {
        sender: "Billy", 
        recipient: "user", 
        date: Date.now(), 
        content: "Hey user"
    }, 
    {
        sender: "admin", 
        recipient: "user", 
        date: Date.now(), 
        content: "Hey"
    }
]

var messages = messagesTemp;
if (sessionStorage && sessionStorage.getItem('messages')) {
    messages = JSON.parse(sessionStorage.getItem('messages'));
}
else {
    messages = messagesTemp;
    sessionStorage.setItem('messages', JSON.stringify(messagesTemp));
}





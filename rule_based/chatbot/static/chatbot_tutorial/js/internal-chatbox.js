// function selfpause(millis)
// {
//     var date = new Date();
//     var curDate = null;
//     do { curDate = new Date(); }
// 	while(curDate-date < millis);
// 	return;
// }

function generate_typing_effect(){
	$('#messages-container').append(`<div id='typing-effect' class="msg-row"><div class="col-xs-11 col-sm-11 col-md-11 col-lg-11 no-sides-padding msg-animate"><div class="bot-icon-div">EZBot:</div><div class="panel message-panel bot-msg "><div class="panel-body bot-msg-body"><div><div class="message-text">`+`<span class='message-text'>Typing ...</span>`+'</div></div></div></div></div></div>');
	setTimeout(function(){$('#typing-effect').remove()},2000);
}
// Function to simply format the text in the right way. May end up being more complicated when you have MCQs, etc.
function generate_formatted_chat_message(data){
	if(data.type == 'text'){
		messages = data.text.split('\n Also, \n')
		message_text = '<span class="message-text">' + data.text + '</span>'
		return message_text;
	}
	console.log("invalid data format");
	return "";
}


// Function that adds a message to the chat window
function add_message_to_chat(data, formatted_div){
	var chat = $('#messages-container');
	var new_source = data["source"]; //Bot or Human
	if (new_source == "BOT"){
		// generate_typing_effect();
		setTimeout(function(){
			chat.append('<div class="msg-row"><div class="col-xs-11 col-sm-11 col-md-11 col-lg-11 no-sides-padding msg-animate"><div class="bot-icon-div">EZBot:</div><div class="panel message-panel bot-msg "><div class="panel-body bot-msg-body"><div><div class="message-text">'+formatted_div+'</div></div></div></div></div></div>')
		},2000);
	}else if(new_source == "CANDIDATE"){
		var child = $('<div class="msg-row">');
		$(child).append('<div class="row"><div class="col-xs-10 col-sm-10 col-md-10 col-lg-10  pull-right no-sides-padding msg-animate"><div class="panel message-panel user-msg"><div class="panel-body user-msg-body"><div class="message-text"><span></span></div></div></div><div class="user-msg-bubble">you</div></div>');
		$(child).find('span').html(formatted_div);
		chat.append(child);
	}
	$("#body-container").scrollTop( $('#body-container')[0].scrollHeight);	
}  


// Function taht is called when the server sends a message via websockets to my front end.
function processAndDisplayChatMessage(message){
	// console.log(message) # Message key `text` contians data with our splitter filterable
	const message_sessions = JSON.parse(message.data)['text'].split(`\n Also, \n`)
	for (let msg of message_sessions){
		var content_data = JSON.parse(message.data);
		content_data['text']=msg;
		var formatted_div = generate_formatted_chat_message(content_data);
		if(formatted_div.length > 0){
			if(content_data['source']=='BOT'){
				generate_typing_effect();
			}
			add_message_to_chat(content_data, formatted_div);
		}		
	}
}


function sendTextMessage() {
    if ($('#messageToSend').text() == "") {
        return
    }

    message = {}
    message.text = $('#messageToSend').html().replace("</div>", "").replace("<div>", "\n").replace("<br>", "\n");
    message.command= 'send'
    message.timestamp = new Date();
    
    
    $('#messageToSend').text('');
	chatsock.send(JSON.stringify(message));
	$("#message").val('').focus();
    return false;   
}

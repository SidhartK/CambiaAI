
var suits = ["C", "D", "H", "S"]
var labels = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
function find_card(num){
	if (num >= 52) {
		return "BJ";
	}
	label = labels[num % 13];
	suit = suits[Math.floor(num/13)];
	return suit + label;
}

function find_val(num){
	if (find_card(num)[1] == "A"){
		return 1;
	}
	if (find_card(num)[1] == "J"){
		if (find_card(num)[0] == "B"){
			return 0;
		}
		else{
			return 11;
		}
	}
	if (find_card(num)[1] == "Q"){
		return 12;
	}
	if (find_card(num)[1] == "K"){
		if (find_card(num)[0] == "D" || find_card(num)[0] == "H"){
			return -1;
		}
		else{
			return 13;
		}
	}
	return find_card(num)[1];
}

function find_card_loc(num){
	if (num <= -1){
		return "static/images/cards/card.jpg";
	}
	if (num >= 52) {
		return "static/images/cards/" + "BJ" + ".png";
	}
	label = labels[num % 13];
	suit = suits[Math.floor(num/13)];
	return "static/images/cards/" + suit + label + ".png"
}
// console.log(`${find_card(45)}`);
function make_card(num, id_num){
	if (id_num == "played_"){
		console.log(`${num} is the num`);
	}
	card = find_card(num);
	if (num == -1){
		return `<img class="${id_num}img" src="${find_card_loc(num)}" alt="cardback" width=80px height=112px>`;
	}
	return `<img class="${id_num}img" src="${find_card_loc(num)}" alt="${card}" width=80px height=112px>`;
}

// document.addEventListener(('DOMContentLoaded'), () => {
var socket = io();
var username = "";
var your_index = -1;
var your_board = [-1, -1, -1, -1];
var players = [];
// var numplayers = 0;
var board = [];
var draws_card = false;
var distance = 20000;
socket.on('connect', function() {
		socket.emit('start_game', 'Ready To Start');
});
// var socket = io();
// console.log(`I fuckin did it`)
// socket.on('connect', () => {
// 	socket.send("I am connected");
// });

function use_card(card_index){
	// console.log(`I am using the card ${card_index}, ${draws_card}`);
	if (draws_card) {
		socket.emit('selected_card', card_index);
		draws_card = false;
	}
}

function flip_card(card_index, played_card, clicked_player_index){
	console.log(`I got to flip card with ${card_index, played_card, clicked_player_index}`);
	observed_card = board.slice(4 * clicked_player_index, 4 * clicked_player_index + 4)[card_index];
	if (observed_card == played_card){
		if (your_index == clicked_player_index){
			$(`#${your_index}_board`).find(`.${card_index}img`).hide();
			board[4 * your_index + card_index] = -2;
			socket.emit('flipped_card', {'board': board, 'player_index': clicked_player_index});
		}
		else{
			// $(`#${clicked_player_index}_board`).find(`.${card_index}img`).hide();
			socket.emit('freeze_flip_cards', {'player': your_index});
			for (var i = 0; i < 4; i++){
				$(`#${your_index}_board`).find(`.${i}button`).on('click', function(){
					// $(`#${clicked_player_index}_board`).find(`.${card_index}img`)
					board[4 * clicked_player_index + card_index] = your_board[i];
					board[4 * your_index + i] = -2;
					$(`#${your_index}_board`).find(`.${i}button`).hide();
					distance = 0;
					$(`#${your_index}_board`).find(`.${i}button`).attr("onclick", `card_ability(${i}, ${played_card}, ${clicked_player_index})`);
				});
			}

			$(`#${your_index}_board`).find($("#hidecards_text")).text(`Choose which card to give player ${clicked_player_index + 1}`);

			// distance = 20000;
			// var x = setInterval(function() {
			// 	$("#hidecards_text").text(`Choose which card to give player ${clicked_player_index + 1} in ${distance/1000} sec`);
			// 	if (distance <= 0){
			// 		clearInterval(x);
			// 		for (var i = 0; i < 4; i++){
			//
			// 		}
			// 		$("#hidecards_text").hide();
			// 	}
			// }, 1000);
			socket.emit('flipped_card', {'board': board, 'player_index': your_index});
		}
	}
}
function look_at_your(){
	console.log(`look at your called`);
	// $(`#${your_index}_board`).find($("#hidecards")).hide();
	$(`#${your_index}_board`).find($("#hidecards_text")).text("");
	// $(`#${your_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(-1)}`);
	// $(`#${your_index}_board`).find(`.${card_index}img`).attr("alt", `cardback`);
	for (var i = 0; i < 4; i++){
		board[4 * your_index + i] = your_board[i];
	}
	console.log(`I am calling next_round`);
	socket.emit('next_round', {'board': board});
}

function look_at_oppo(){
	console.log(`look at oppo called`);
	// $(`#${your_index}_board`).find($("#hidecards")).hide();
	$(`#${your_index}_board`).find($("#hidecards_text")).text("");
	// $(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(-1)}`);
	// $(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("alt", `cardback`);
	for (var i = 0; i < 4; i++){
		board[4 * your_index + i] = your_board[i];
	}
	console.log(`I am calling next_round`);
	socket.emit('next_round', {'board': board});
}

var switch_select_card = false;
function card_ability(card_index, played_card, clicked_player_index){
	// $("#hidecards").show();
	// var x = setInterval(function() {
	// 	console.log(`The ${distance} is `);
	// 	$("#hidecards_text").text(`The Memorize your cards in ${distance/1000} sec`);
	// 	if (distance <= 0) {
	// 		clearInterval(x);
	// 		$("#hidecards").hide();
	// 		$("#hidecards_text").text("");
	// 		for (var i = 2; i < 4; i++){
	// 			$(`#${your_index}_board`).find(`.${i}img`).attr("src", `${find_card_loc(-1)}`);
	// 			$(`#${your_index}_board`).find(`.${i}img`).attr("alt", `cardback`);
	// 		}
	// 	}
	// 	distance -= 1000;
	// }, 1000);
	console.log(`I got to card ability with ${card_index} played card is ${played_card}, and the 3rd arg is ${clicked_player_index}`);
	if (find_val(played_card) < 7 && find_val(played_card) >= 0){
		socket.emit('next_round', {'board': board});
	}
	if (find_val(played_card) == 7 || find_val(played_card) == 8){
		if (your_index == clicked_player_index){
			console.log(`The find val is 7`);
			var observed_card = your_board[card_index];
			$(`#${your_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(observed_card)}`);
			$(`#${your_index}_board`).find(`.${card_index}img`).attr("alt", `${find_card(observed_card)}`);
			$(`#${your_index}_board`).find(`.lookyourcards`).attr("hidden", false);
			// $(`#${your_index}_board`).find(`.hidecards`).on('click', look_at_your());
			// $(`#${your_index}_board`).find(`.${card_index}button`).on('click', look_at_your());
			console.log(`Changed the ${card_index} button on ${clicked_player_index} to look_at_your`);
			// 	// $(`#${your_index}_board`).find($("#hidecards")).hide();
			// 	$(`#${your_index}_board`).find($("#hidecards_text")).text("");
			// 	// $(`#${your_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(-1)}`);
			// 	// $(`#${your_index}_board`).find(`.${card_index}img`).attr("alt", `cardback`);
			// 	for (var i = 0; i < 4; i++){
			// 		board[4 * your_index + i] = your_board[i];
			// 	}
			// 	console.log(`I am calling next_round`);
			// 	socket.emit('next_round', {'board': board});
			// });
			// $(`#${your_index}_board`).find($("#hidecards")).show();
			$(`#${your_index}_board`).find($("#hidecards_text")).text(`Remember the card shown`);
			// $(`#${your_index}_board`).find($("#hidecards")).on('click', function(){
			// 	$(`#${your_index}_board`).find($("#hidecards")).hide();
			// 	$(`#${your_index}_board`).find($("#hidecards_text")).text("");
			// 	$(`#${your_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(-1)}`);
			// 	$(`#${your_index}_board`).find(`.${card_index}img`).attr("alt", `cardback`);
			// 	for (var i = 0; i < 4; i++){
			// 		board[4 * your_index + i] = your_board[i];
			// 	}
			// 	console.log(`I am calling next_round`);
			// 	socket.emit('next_round', {'board': board});
			// });
			// distance = 20000;
			// console.log(`I have just set the distance to ${distance}`);
			// var x1 = setInterval(function() {
			// 	$("#hidecards_text").text(`Have to Memorize the card shown in ${distance/1000} sec`);
			// 	console.log(`${distance} is `);
			// 	if (distance <= 0) {
			// 		clearInterval(x1);
			// 		$("#hidecards").hide();
			// 		$("#hidecards_text").text("");
			// 		$(`#${your_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(-1)}`);
			// 		$(`#${your_index}_board`).find(`.${card_index}img`).attr("alt", `cardback`);
			// 	}
			// 	distance -= 1000;
			// }, 1000);
			console.log(`The find val is 7 ending`);

		}
	}

	if (find_val(played_card) == 9 || find_val(played_card) == 10){
		console.log(`The find val is 9`);
		if (your_index != clicked_player_index){
			var observed_card = board.slice(4 * clicked_player_index, 4 * clicked_player_index + 4)[card_index];
			$(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(observed_card)}`);
			$(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("alt", `${find_card(observed_card)}`);
			$(`#${your_index}_board`).find(`.lookoppocards`).attr("hidden", false);
			// $(`#${clicked_player_index}_board`).find(`.hidecards`).on('click', look_at_oppo());
			// $(`#${clicked_player_index}_board`).find(`.${card_index}button`).on('click', look_at_oppo());
			console.log(`Changed the ${card_index} button on ${clicked_player_index} to look_at_oppo`);
			// 	// $(`#${your_index}_board`).find($("#hidecards")).hide();
			// 	$(`#${your_index}_board`).find($("#hidecards_text")).text("");
			// 	// $(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(-1)}`);
			// 	// $(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("alt", `cardback`);
			// 	for (var i = 0; i < 4; i++){
			// 		board[4 * your_index + i] = your_board[i];
			// 	}
			// 	console.log(`I am calling next_round`);
			// 	socket.emit('next_round', {'board': board});
			// });

			// $(`#${your_index}_board`).find($("#hidecards")).show();
			$(`#${your_index}_board`).find($("#hidecards_text")).text(`Remember the card shown`);
			// $(`#${your_index}_board`).find($("#hidecards")).on('click', function(){
			// 	$(`#${your_index}_board`).find($("#hidecards")).hide();
			// 	$(`#${your_index}_board`).find($("#hidecards_text")).text("");
			// 	$(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(-1)}`);
			// 	$(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("alt", `cardback`);
			// 	for (var i = 0; i < 4; i++){
			// 		board[4 * your_index + i] = your_board[i];
			// 	}
			// 	console.log(`I am calling next_round`);
			// 	socket.emit('next_round', {'board': board});
			// });

			// distance = 20000;
			// console.log(`I have just set the distance to ${distance}`);
			// var x2 = setInterval(function() {
			// 	$("#hidecards_text").text(`Memorize the card shown in ${distance/1000} sec`);
			// 	console.log(`${distance} is `);
			//   if (distance <= 0) {
			//     clearInterval(x2);
			// 		$("#hidecards").hide();
			//     $("#hidecards_text").text("");
			// 		$(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(-1)}`);
			// 		$(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("alt", `cardback`);
			//   }
			// 	distance -= 1000;
			// }, 1000);
			console.log(`The find val is 9 ending`);
		}
	}

	if (find_val(played_card) == 11 || find_val(played_card) == 12){
		console.log(`The find val is 11`);
		if (your_index == clicked_player_index){
			if (switch_select_card == false){
				switch_select_card = [your_index, card_index];
			}
			else{
				var tmp = board.slice(4 * switch_select_card[0], 4 * switch_select_card[0] + 4)[switch_select_card[1]];
				board[4 * switch_select_card[0] + switch_select_card[1]] = your_board[card_index];
				your_board[card_index] = tmp;
				switch_select_card = false;
			}
		}
		if (your_index != clicked_player_index){
			if (switch_select_card == false){
				switch_select_card = [clicked_player_index, card_index];
			}
			else{
				var tmp = your_board[switch_select_card[1]];
				your_board[switch_select_card[1]] = board.slice(4 * clicked_player_index, 4 * clicked_player_index + 4)[card_index];
				board[4 * clicked_player_index + card_index] = tmp;
			}
		}
		console.log(`The find val is 11 ending with ${switch_select_card}`);
		if (switch_select_card == false){
			for (var i = 0; i < 4; i++){
				board[4 * your_index + i] = your_board[i];
			}
			console.log(`I am calling next_round`);
			socket.emit('next_round', {'board': board});
		}
	}

	if (find_val(played_card) == 13 || find_val(played_card) == -1){
		console.log(`The find val is 13`);
		if (your_index == clicked_player_index){
			var observed_card = your_board[card_index];
			if (switch_select_card == false){
				switch_select_card = [your_index, card_index];
				$(`#${your_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(observed_card)}`);
				$(`#${your_index}_board`).find(`.${card_index}img`).attr("alt", `${find_card(observed_card)}`);
				$(`#${your_index}_board`).find($("#hidecards_text")).text("Please select one of your opponents' cards to look at");
			}
			else{
				$(`#${your_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(observed_card)}`);
				$(`#${your_index}_board`).find(`.${card_index}img`).attr("alt", `${find_card(observed_card)}`);
				$(`#${your_index}_board`).append(`<button type="button" id="yes_button"> Swap </button> <button type="button" id="no_button"> Don't Swap </button>`);
				$(`#${your_index}_board`).find($("#hidecards_text")).text(`Decide whether or not to swap`);
				$(`#${your_index}_board`).find($("#yes_button")).on('click', function(){
					console.log(`I am inside the yes_button1`)
					your_board[card_index] = board.slice(4 * switch_select_card[0], 4 * switch_select_card[0] + 4)[switch_select_card[1]];
					board[4 * switch_select_card[0] + switch_select_card[1]] = observed_card;
					// var tmp = board[4 * switch_select_card[0] : 4 * switch_select_card[0] + 4][switch_select_card[1]];
					// board[4 * switch_select_card[0] : 4 * switch_select_card[0] + 4][switch_select_card[1]] = your_board[card_index];
					// your_board[card_index] = tmp;
					// distance = 0;
					$(`#${your_index}_board`).find($("#hidecards_text")).text("");
					$(`#${your_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(-1)}`);
					$(`#${your_index}_board`).find(`.${card_index}img`).attr("alt", `cardback`);
					$(`#${switch_select_card[0]}_board`).find(`.${switch_select_card[1]}img`).attr("src", `${find_card_loc(-1)}`);
					$(`#${switch_select_card[0]}_board`).find(`.${switch_select_card[1]}img`).attr("alt", `cardback`);
				});
				$(`#${your_index}_board`).find($("#no_button")).on('click', function(){
					console.log(`I am inside the no_button1`)
					$(`#${your_index}_board`).find($("#hidecards_text")).text("");
					$(`#${your_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(-1)}`);
					$(`#${your_index}_board`).find(`.${card_index}img`).attr("alt", `cardback`);
					$(`#${switch_select_card[0]}_board`).find(`.${switch_select_card[1]}img`).attr("src", `${find_card_loc(-1)}`);
					$(`#${switch_select_card[0]}_board`).find(`.${switch_select_card[1]}img`).attr("alt", `cardback`);
					// distance = 0;
				});

			// 	distance = 20000;
			// 	console.log(`I have just set the distance to ${distance}`);
			// 	var x3 = setInterval(function() {
			// 		console.log(`${distance} is `);
			// 		$(`#${your_index}_board`).find($("#hidecards_text")).text(`Decide whether or not to swap in ${distance/1000} sec`);
			// 		if (distance <= 0) {
			// 			clearInterval(x3);
			// 			// $("#hidecards").hide();
			// 			$(`#${your_index}_board`).find($("#hidecards_text")).text("");
			// 			$(`#${your_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(-1)}`);
			// 			$(`#${your_index}_board`).find(`.${card_index}img`).attr("alt", `cardback`);
			// 			$(`#${switch_select_card[0]}_board`).find(`.${switch_select_card[1]}img`).attr("src", `${find_card_loc(-1)}`);
			// 			$(`#${switch_select_card[0]}_board`).find(`.${switch_select_card[1]}img`).attr("alt", `cardback`);
			// 		}
			// 		distance -= 1000;
			// 	}, 1000);
				switch_select_card = false;
			}
		}
		else{
			var observed_card = board.slice(4 * clicked_player_index, 4 * clicked_player_index + 4)[card_index];
			if (switch_select_card == false){
				switch_select_card = [clicked_player_index, card_index];
				$(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(observed_card)}`);
				$(`#${your_index}_board`).find($("#hidecards_text")).text("Please select one of your own cards to look at");
			}
			else{
				$(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(observed_card)}`);
				$(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("alt", `${find_card(observed_card)}`);
				$(`#${your_index}_board`).find($("#hidecards_text")).text(`Decide whether or not to swap`);
				$(`#${your_index}_board`).append(`<button type="button" id="yes_button"> Swap </button> <button type="button" id="no_button"> Don't Swap </button>`);
				$(`#${your_index}_board`).find($("#yes_button")).on('click', function(){
					console.log(`I am inside the yes_button2`)
					board[4 * clicked_player_index + card_index] = your_board[switch_select_card[1]]
					your_board[switch_select_card[1]] = observed_card;
					$(`#${your_index}_board`).find($("#hidecards_text")).text("");
					$(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(-1)}`);
					$(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("alt", `cardback`);
					$(`#${switch_select_card[0]}_board`).find(`.${switch_select_card[1]}img`).attr("src", `${find_card_loc(-1)}`);
					$(`#${switch_select_card[0]}_board`).find(`.${switch_select_card[1]}img`).attr("alt", `cardback`);
					// distance = 0;
				});
				$(`#${your_index}_board`).find($("#no_button")).on('click', function(){
					console.log(`I am inside the no_button2`)
					$(`#${your_index}_board`).find($("#hidecards_text")).text("");
					$(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(-1)}`);
					$(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("alt", `cardback`);
					$(`#${switch_select_card[0]}_board`).find(`.${switch_select_card[1]}img`).attr("src", `${find_card_loc(-1)}`);
					$(`#${switch_select_card[0]}_board`).find(`.${switch_select_card[1]}img`).attr("alt", `cardback`);
					// distance = 0;
				});

				// distance = 20000;
				// var x = setInterval(function() {
				// 	console.log(`${distance} is `);
				// 	$(`#${your_index}_board`).find($("#hidecards_text")).text(`Decide whether or not to swap in ${distance/1000} sec`);
				// 	if (distance <= 0) {
				// 		clearInterval(x);
				// 		// $("#hidecards").hide();
				// 		$(`#${your_index}_board`).find($("#hidecards_text")).text("");
				// 		$(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("src", `${find_card_loc(-1)}`);
				// 		$(`#${clicked_player_index}_board`).find(`.${card_index}img`).attr("alt", `cardback`);
				// 		$(`#${switch_select_card[0]}_board`).find(`.${switch_select_card[1]}img`).attr("src", `${find_card_loc(-1)}`);
				// 		$(`#${switch_select_card[0]}_board`).find(`.${switch_select_card[1]}img`).attr("alt", `cardback`);
				// 	}
				// 	distance -= 1000;
				// }, 1000);
				switch_select_card = false;
			}
		}
		console.log(`The find val is 13 with ${switch_select_card}`);
		if (switch_select_card == false){
			for (var i = 0; i < 4; i++){
				board[4 * your_index + i] = your_board[i];
			}
			console.log(`I am calling next_round`);
			socket.emit('next_round', {'board': board});
		}
	}
	// if (switch_select_card == false){
	// 	for (var i = 0; i < 4; i++){
	// 		board[4 * your_index + i] = your_board[i];
	// 	}
	// 	console.log(`I am calling next_round`);
	// 	socket.emit('next_round', {'board': board});
	// }
}

socket.on('message', data => {
	console.log(`Message received: ${data}`);
	username = data;
	// $(document.body).append("<p>" + data + "</p>");
	// const p = document.createElement('p');
	// p.innerHTML = data;
	// document.body.append(p);
});

socket.on('make board drawcard', function(data) {
	console.log(`I am now making the board`);
	$("#game_board").text("");
	$("#game_board").append(`<div id="placed_card"> ${make_card(-1, "played_")} </div>`);

	your_index = data['players'].findIndex((element) => element == username);

	console.log(`The index we have is ${your_index}`);
	for (var i = 0; i < data['players'].length; i++){
		$("#game_board").append(`<div id="${i}_board"> </div>`);
		for (var j = 0; j < 4; j++){
			// $(`#${i}_board`).append(`<span class="${j}_card"> <button type="button" class="${j}button"> ${make_card(-1, j)} </button> </span>`);
			if (your_index == i){
				$(`#${i}_board`).append(`<span class="${j}_card"> <button type="button" class="${j}button" onclick="use_card(${j})"> ${make_card(-1, j)} </button> </span>`);
				// $(`#${i}_board`).find(`.${j}button`).on('click', use_card(j));
			}
			else{
				$(`#${i}_board`).append(`<span class="${j}_card"> <button type="button" class="${j}button"> ${make_card(-1, j)} </button> </span>`);
			}
			// <p id="username" hidden=true>{{ username }}</p>
			// button
			// <button type="button" class="join_room_button" onclick="rand_function()"> <img id="card1" src="{{ url_for('static', filename='images/cards/S7.png') }}" alt="A&spades" width=100px> </button>
			// <button type="button" class="join_room_button" onclick="rand_function()"> <img src="{{ url_for('static', filename='images/cards/card.jpg') }}" alt="cardback" width=100px height=140px> </button>
			// <br>
			// <br>
			// <button type="button" class="join_room_button" onclick="rand_function()"> <img src="{{ url_for('static', filename='images/cards/DJ.png') }}" alt="A&spades" width=100px> </button>
			// <button type="button" class="join_room_button" onclick="rand_function()"> <img src="{{ url_for('static', filename='images/cards/CK.png') }}" alt="A&spades" width=100px> </button>

			if (j == 1){
				$(`#${i}_board`).append("<br> <br>");
			}
			if (data['board'][4 * i + j] < -1){
				$(`#${i}_board`).find(`.${j}_card`).hide();
			}
		}
		// ${make_card(-1, 1)} <br> <br // 	${make_card(-1, 2)} ${make_card(-1, 3)} </div>`);
		$("#game_board").append(`<p> Player ${i+1}: ${data['players'][i]} </p>`);
	}
	$("#game_board").append(`<div id = "drawn_card">
														<p id="drawn_card_text"> </p>
														<button type="button" class="4button" onclick="use_card(4)">
															${make_card(-1, 4)}
														</button>
														</div>`);
	// $("#drawn_card").find(".4button").on('click', use_card(4));
	$("#drawn_card").before(`<button type="button" id="hidecards">Hide Cards</button>`);
	$("#hidecards").on('click', function(){
		distance = 0;
	});
	$("#drawn_card").before(`<p id="hidecards_text"> </p>`);
	// var the_index = 0;
	// var the_i = 1;
	// $(`#${the_index}_board`).find(`#${the_i}img`).attr("src", "static/images/cards/BJ.png");
	// $("#0_board").find("#1img").attr("src", "static/images/cards/BJ.png");
	// console.log($("#0_board").text());
});

socket.on('load game drawcard', function(data) {
	console.log(`I got here draw card`)
	// numplayers = data['players'].length;
	board = data['board'];
	console.log(`The board is ${board} and the players are ${data['players']}`)
	your_board = board.slice(4 * your_index, 4 * your_index + 4);
	if (data['firsttime']){
		for (var i = 2; i < 4; i++){
			$(`#${your_index}_board`).find(`.${i}img`).attr("src", `${find_card_loc(your_board[i])}`);
			$(`#${your_index}_board`).find(`.${i}img`).attr("alt", `${find_card(your_board[i])}`);
			// console.log(`I have done ${i} and the source is ${$("#0_board").html()}`);
		}
		// $("#drawn_card").before(`<button type="button" id="hidecards">Hide Cards</button>`);
		// $("#hidecards").on('click', function(){
		// 	distance = 0;
		// });
		// $("#drawn_card").before(`<p id="hidecards_text"> </p>`);
		distance = 20000;
		var x = setInterval(function() {
			console.log(`We have the distance is ${distance}`);
			$("#hidecards_text").text(`We have to Memorize your cards in ${distance/1000} sec`);
		  if (distance <= 0) {
		    clearInterval(x);
				$("#hidecards").hide();
		    $("#hidecards_text").text("");
				for (var i = 2; i < 4; i++){
					$(`#${your_index}_board`).find(`.${i}img`).attr("src", `${find_card_loc(-1)}`);
					$(`#${your_index}_board`).find(`.${i}img`).attr("alt", `cardback`);
				}
		  }
			distance -= 1000;
		}, 1000);
	}
	$("#drawn_card").find("#drawn_card_text").text(`${data['players'][data['player']]} is drawing the card: `);
	if (your_index == data['player']){
		$("#drawn_card").find(`.4img`).attr("src", `${find_card_loc(data['drawn card'])}`);
		$("#drawn_card").find(`.4img`).attr("alt", `${find_card(data['drawn card'])}`);
		draws_card = true;
		// console.log(`I am the chosen one, ${draws_card}`);
		// $("#drawn_card").append(`<button type="button" onclick="use_card(3)"> Click here to test </button>`);
	}

	// console.log(`I have done 4`);

	//
	// $(document.body).append(`<div id=${your_index} board> ${make_card(-1, 0)} ${make_card(-1, 1)} <br> <br>
	// 		${make_card(your_board[2], 2)} ${make_card(your_board[3], 3)} </div>`);
	//
	// $(document.body).append(`<div id = "${your_index} drawn card"> ${make_card(data['drawn card'], 4)} </div>`)
	// if (your_index != 0){
	// 	$(`${your_index} drawn card`).hide();
	// }
	// console.log(`<div id=${your_index} board> ${make_card(-1, 0)} ${make_card(-1, 1)} <br> <br>
	// 		${make_card(your_board[2], 2)} ${make_card(your_board[3], 3)} </div>`)

	// const p = document.createElement('p');
	// p.innerHTML = "First player is " + data['player'] + "their card is " + find_card(data['drawn card']);
	// document.body.append(p);
	// card1 = document.querySelector('#card1');
});

socket.on('create board playcard', function(data) {
	console.log(`I am now making the board create board drawcard`);
	$("#game_board").text("");
	$("#game_board").append(`<div id="placed_card"> ${make_card(data['played card'], "played_")} </div>`);

	your_index = data['players'].findIndex((element) => element == username);
	board = data['board'];
	console.log(`The index we have is ${your_index} and the players we have is ${data['players']} and the card is ${data['played card']}`);
	for (var i = 0; i < data['players'].length; i++){
		$("#game_board").append(`<div id="${i}_board"> </div>`);
		for (var j = 0; j < 4; j++){
			if (your_index == data['player']){
				$(`#${i}_board`).append(`<span class="${j}_card"><button type="button" class="${j}button" onclick="card_ability(${j}, ${data['played card']}, ${i})"
							ondblclick="flip_card(${j}, ${data['played card']}, ${i})"> ${make_card(-1, j)} </button> </span>`);
			}
			else{
				$(`#${i}_board`).append(`<span class="${j}_card"><button type="button" class="${j}button" ondblclick="flip_card(${j}, ${data['played card']}, ${i})">
							${make_card(-1, j)} </button> </span>`);
			}

			// else{
			// 	$("#game_board").append(`<button type="button" class="${j}button" onclick="card_ability(${j}, ${data['played card']})" ondblclick="flip_card(${j}, ${data['played card']})">
			// 				${make_card(-1, j)} </button>`);
			// }
			if (j == 1){
				$(`#${i}_board`).append("<br> <br>");
			}
			if (data['board'][4 * i + j] < -1){
				$(`#${i}_board`).find(`.${j}_card`).hide();
			}
		}
		$(`#${i}_board`).append(`<p> Player ${i+1}: ${data['players'][i]} </p>`);
		// $(`#${i}_board`).append(`<button type="button" class="hidecards" hidden>Hide Card</button>`);
		$(`#${i}_board`).append(`<button type="button" class="lookyourcards" onclick="look_at_your()" hidden>Hide Card</button>`);
		$(`#${i}_board`).append(`<button type="button" class="lookoppocards" onclick="look_at_oppo()" hidden>Hide Card</button>`);

		// $(`#${i}_board`).find($("#hidecards")).hide();
		// $(`#${i}_board`).find($("#hidecards")).on('click', function(){
		// 	distance = 0;
		// });
		$(`#${i}_board`).append(`<p id="hidecards_text"> </p>`);
		if (find_val(data['played card']) < 7 && find_val(data['played card']) >= 0){
			card_ability(0, data['played card'], 0);
		}
	}

});
// })

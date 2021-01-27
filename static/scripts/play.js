function rand_function(){
	location.href = "home";
}

var suits = ["C", "D", "H", "S"]
var labels = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
function find_card_loc(num){
	if (num == 52) {
		return "static/images/cards/" + "BJ" + ".png";
	}
	label = labels[num % 13];
	suit = suits[Math.floor(num/13)];
	return "static/images/cards/" + suit + label + ".png"
}


card1 = document.querySelector('#card1');
card1.src = find_card_loc(41);

document.addEventListener(('DOMContentLoaded'), () => {
	console.log(document.querySelector('#room_code_button'));
})

document.write("This indeed is some more shit written in test.js");

document.addEventListener('DOMContentLoaded', () => {
	document.querySelector('#start_button').onclick = () => {
		console.log(`Holy shit this actually works!`);
		alert("This works");
		const p = document.createElement('p');
		p.innerHTML = document.querySelector('#input_field').value
		document.body.append(p)
	}
})

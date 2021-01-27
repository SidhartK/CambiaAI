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
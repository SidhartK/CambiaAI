document.write("This actually fuckin works!");
console.log(`Please for the love of gods`);

document.addEventListener('DOMContentLoaded', () => {
	document.querySelector('#sbutton').onclick = () => {
		console.log(`Holy shit this actually works!`);
		alert("This works");
		const p = document.createElement('p');
		p.innerHTML = document.querySelector('#input_field').value
		document.body.append(p)
	}
})

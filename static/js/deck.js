const request = new XMLHttpRequest();
const url = "http://localhost:5000/";


window.addEventListener("load", () => {
	console.log("On it");
	let deck_id = window.location.pathname.substring(6);
	request.open("GET", url + `api/decks/${deck_id}`);
	request.send();
	request.onload = () => {
		let response_text = request.responseText;
		show_deck(JSON.parse(response_text));

		get_cards(deck_id);
	};

	document.querySelector(".bottom-button.new-card").setAttribute('href', `http://127.0.0.1:5000/new_card/${deck_id}`);
});

function show_deck(deck) {
	console.log(deck);
	document.querySelector(".title").innerText += ` "${deck["d_name"]}"`
	document.querySelector(".description-text").innerText += ` "${deck["d_description"]}"`

}

function get_cards(deck_id) {
	console.log("Here we are");
	request.open("GET", url + `api/cards/${deck_id}`);
	request.send();
	request.onload = () => {
		let response_text = request.responseText;
		show_cards(JSON.parse(response_text));
	};
}

function show_cards(cards) {
	console.log(cards);
	let table = document.getElementById("cards-table");
	cards.forEach((card) => {
		// <th>Front header</th>
		// <th>Front text</th>
		// <th>Back header</th>
		// <th>Back text</th>
		let tr = document.createElement("tr");
		let front_header = document.createElement("td");
		front_header.innerText = card["front_header"];
		let front_text = document.createElement("td");
		front_text.innerText = card["front_body"];
		let back_header = document.createElement("td");
		back_header.innerText = card["back_header"];
		let back_text = document.createElement("td");
		back_text.innerText = card["back_body"];
		tr.appendChild(front_header);
		tr.appendChild(front_text);
		tr.appendChild(back_header);
		tr.appendChild(back_text);
		// td.classList.add("category-wrapper");
		// let content = document.createElement("div");
		// content.classList.add("category");
		// td.appendChild(content);

		// content.innerText = category["c_name"];

		table.appendChild(tr);
	})
}
const request = new XMLHttpRequest();
const url = "http://localhost:5000/";

window.addEventListener("load", async function (event) {
	data_categories();
});

async function data_categories() {
	let text = document.getElementById("categories");
	request.open("GET", url + "api/cats");
	request.send();
	request.onload = () => {
		let response_text = request.responseText;
		show_categories(JSON.parse(response_text));
		data_decks();
	};
}

async function show_categories(category_list) {
	let category_table = document.querySelector("#category-table");
	await category_list.forEach((category) => {
		let tr = document.createElement("tr");
		let td = document.createElement("td");
		tr.appendChild(td);
		td.classList.add("category-wrapper");
		let content = document.createElement("div");
		content.classList.add("category");
		td.appendChild(content);

		content.innerText = category["c_name"];

		category_container.appendChild(td);
	});
}

async function data_decks() {
	request.open("GET", url + "api/decks");
	request.send();

	request.onload = () => {
		let response_text = request.responseText;
		show_decks(JSON.parse(response_text));
	};
}

async function show_decks(deck_list) {
	let deck_container = document.querySelector("#deck-container");
	await deck_list.forEach((deck) => {
		let wrapper = document.createElement("div");
		wrapper.classList.add("deck-wrapper");

		let title = document.createElement("h3");
		title.classList.add("deck-title");
		title.innerText = deck["d_name"];

		let description = document.createElement("description");
		description.classList.add("deck-desc");
		description.innerText = deck["d_description"];

		wrapper.appendChild(title);
		wrapper.appendChild(description);
		deck_container.appendChild(wrapper);
	});
}

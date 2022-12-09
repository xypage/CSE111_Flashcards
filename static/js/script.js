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
	let cat_list = [];
	await category_list.forEach((category) => {
		if (cat_list.includes(category["c_name"])) {
			// nop
		} else {
			cat_list.push(category["c_name"]);
			let tr = document.createElement("tr");
			let td = document.createElement("td");
			tr.appendChild(td);
			td.classList.add("category-wrapper");
			let content = document.createElement("div");
			content.classList.add("category");
			td.appendChild(content);

			content.innerText = category["c_name"];

			category_table.appendChild(td);
		}
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
		let link = document.createElement("a");
		link.classList.add("deck-link");
		link.setAttribute("href", `http://127.0.0.1:5000/deck/${deck["deck_id"]}`);
		let wrapper = document.createElement("div");
		wrapper.classList.add("deck-wrapper");
		link.appendChild(wrapper);

		let title = document.createElement("h3");
		title.classList.add("deck-title");
		title.innerText = deck["d_name"];

		let description = document.createElement("description");
		description.classList.add("deck-desc");
		description.innerText = deck["d_description"];

		wrapper.appendChild(title);
		wrapper.appendChild(description);
		deck_container.appendChild(link);
	});
}

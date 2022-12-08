const request = new XMLHttpRequest();
const url = "http://localhost:5000/";

window.addEventListener("load", async function (event) {
	// data_categories.then(data_decks, dc_error).then(console.log("Done"));
	// console.log("complete");
	// data_categories();

	this.setTimeout(data_categories, 250);
	data_decks();
});

function dc_error(reason) {
	console.log(`Data categories failed, gave reason ${reason}`);
}

async function data_categories() {
	let text = document.getElementById("categories");
	request.open("GET", url + "api/cats");
	request.send();
	request.onload = () => {
		console.log("Request loaded");
		let response_text = request.responseText;
		console.log(response_text);
		show_categories(JSON.parse(response_text));
		console.log("Showed categories");
	};
	console.log("Should be done");
}

// const data_categories = new Promise((resolve, reject) => {
// 	// We call resolve(...) when what we were doing asynchronously was successful, and reject(...) when it failed.
// 	// In this example, we use setTimeout(...) to simulate async code.
// 	// In reality, you will probably be using something like XHR or an HTML API.
// 	request.open("GET", url + "api/cats");
// 	request.send();
// 	console.log("In data_categories function");
// 	request.onload = () => {
// 		let response_text = request.responseText;
// 		// console.log(response_text);
// 		show_categories(JSON.parse(response_text));
// 		resolve("Success!"); // Yay! Everything went well!
// 	};

// 	request.onerror = () => {
// 		reject("Category load failed");
// 	}
// });

async function show_categories(category_list) {
	console.log(category_list);
	console.log("Functioning");
	let category_container = document.querySelector("#category-container");
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

const data_decks = new Promise((resolve, reject) => {
	// We call resolve(...) when what we were doing asynchronously was successful, and reject(...) when it failed.
	// In this example, we use setTimeout(...) to simulate async code.
	// In reality, you will probably be using something like XHR or an HTML API.
	request.open("GET", url + "api/decks");
	request.send();

	request.onload = () => {
		let response_text = request.responseText;
		// console.log(response_text);
		show_decks(JSON.parse(response_text));
		resolve("Success!"); // Yay! Everything went well!
	};

	request.onerror = () => {
		reject("Deck load failed");
	};
});

// async function data_decks() {
// 	request.open("GET", url + "api/decks");
// 	request.send();

// 	request.onload = () => {
// 		let response_text = request.responseText;
// 		// console.log(response_text);
// 		show_decks(JSON.parse(response_text));
// 	};
// }

async function show_decks(deck_list) {
	// console.log(deck_list);
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

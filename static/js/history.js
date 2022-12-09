const request = new XMLHttpRequest();
const url = "http://localhost:5000/";

window.addEventListener("load", async function (event) {
	data_history();
});

async function data_history() {
	let data = document.getElementById("data");
	request.open("GET", url + "api/history");
	request.send();
	request.onload = () => {
		let response_text = request.responseText;
		// console.log(response_text);
		show_history(JSON.parse(response_text));
	};
}

function show_history(history_list) {
	let history_table = document.querySelector("#history-table");
	history_list.forEach((history) => {
		let tr = document.createElement("tr");

		let ratio = document.createElement("td");
		tr.appendChild(ratio);
		let date = document.createElement("td");
		tr.appendChild(date);

		// td.classList.add("history-wrapper");
		// let content = document.createElement("div");
		// content.classList.add("history");
		// td.appendChild(content);

		ratio.innerText = `${(history["correct_ratio"] * 100).toFixed(2)}%`;
		date.innerText = history["cur_date"];

		history_table.appendChild(tr);
	});
}

function myFunction() {
	document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function (event) {
	if (!event.target.matches(".dropbtn")) {
		var dropdowns = document.getElementsByClassName("dropdown-content");
		var i;
		for (i = 0; i < dropdowns.length; i++) {
			var openDropdown = dropdowns[i];
			if (openDropdown.classList.contains("show")) {
				openDropdown.classList.remove("show");
			}
		}
	}
};

function dropdown(row) {
	let dropdown_element = a;
	if(row.classList.contains("session")) {
		// show decks in session
	} else if(row.classList.contains("deck")) {
		// show cards in deck

	}
}
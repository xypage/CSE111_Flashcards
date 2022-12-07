const request = new XMLHttpRequest();
const url = 'http://localhost:5000/';

function data_categories() {

    let text = document.getElementById("categories")
    request.open('GET', url + 'api/cats');
    request.send();

  request.onload = () => text.innerText += request.responseText;
}

function data_decks() {

  let text = document.getElementById("decks")
  request.open('GET', url + 'api/decks');
  request.send();

  request.onload = () => text.innerText += request.responseText;
}
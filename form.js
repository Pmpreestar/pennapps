(function {
  function submitForm() {
    location = document.getElementById('where')
    duration = document.getElementById('when')
    description = document.getElementById('desc')


    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        alert('Submitted!')
      }
    };
    xhttp.open("POST", "http://localhost:5000/request?".concat(
        "name=", name, "&phone=", phone, "&lat=", lat, "&long=", long,
        "&text=", text, "&duration=", dur), true);
    xhttp.send();

  }

  document.getElementById('submit').addEventListener('click', submitForm)



})()
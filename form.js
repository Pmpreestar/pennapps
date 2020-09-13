(function() {
  async function submitForm(event) {
    event.preventDefault()
    location = document.getElementById('where')
    duration = document.getElementById('when')
    description = document.getElementById('desc')
    name = "bob"
    phone = "123"
    lat = 14
    long = 20
    text = "help me out"
    dur = 500

    var url = "http://localhost:5000/request?".concat(
      "name=", name, "&phone=", phone, "&lat=", lat, "&long=", long,
      "&text=", text, "&duration=", dur)
    fetch(url).then()
  }

  document.getElementById('form').addEventListener('submit', submitForm)



})()
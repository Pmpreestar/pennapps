(function() {
  function submitForm() {
//    location = document.getElementById('where')
//    duration = document.getElementById('when')
//    description = document.getElementById('desc')
    sendData().then()
  }

  async function sendData() {
  name = "bob"
    phone = "123"
    lat = 14
    long = 20
    text = "help me out"
    dur = 500

    var url = "http://localhost:5000/request?".concat(
      "name=", name, "&phone=", phone, "&lat=", lat, "&long=", long,
      "&text=", text, "&duration=", dur)
    var response = await fetch(url)
    if (!response.ok) {
        console.log("wrong")
    }
    }

  document.getElementById('submit').addEventListener('click', submitForm)

})()
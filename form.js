(function() {
  function submitForm() {
    var name = document.getElementById('name').value
    var phone = document.getElementById('phone').value
    var location = document.getElementById('map-link').innerHTML
    var lat, long
    if (!location) {
      lat = -1
      long = -1
    } else {
      lat = -1
      long = -1
      locs = location.split(" ")
      if (locs.length >= 4) {
        lat = locs[1]
        long = locs[4]
      }
    }
    var duration = document.getElementById('sel1').value
    if (duration == "hr") {
      duration = 3 * 60 * 60
    } else if (duration == "day") {
      duration = 3 * 24 * 60 * 60
    } else {
      duration = 7 * 24 * 60 * 60
    }
    var text = document.getElementById('desc').value
    sendData(name, phone, lat, long, text, duration).then()
  }

  async function sendData(name, phone, lat, long, text, duration) {
    var url = "http://localhost:5000/request?".concat(
      "name=", name, "&phone=", phone, "&lat=", lat, "&long=", long,
      "&text=", text, "&duration=", duration)
    await fetch(url)
  }

  document.getElementById('submit').addEventListener('click', submitForm)

})()
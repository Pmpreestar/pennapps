(function() {

  var list

  function getList() {
    function success(position) {
        fetchList(position.coords.latitude, position.coords.longitude)
    }
    
    function error() {
        alert("Location not found")
    }
    
    if(navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(success, error);
    } 
  }

  function fetchList(lat, long) {
    var url = "http://localhost:5000/list?".concat(
      "lat=", lat, "&long=", long)
    fetch(url)
    .then((response) => {return response.json()})
    .then((json) => {list = json;})
    .then(() => {
        var requestList = document.getElementById('request-list')
        var requests = Object.keys(list.Name)
        var lis = ""
        var currtime = Math.floor(Date.now() / 1000)
        for (var i = 0; i < requests.length; i++) {
            var key = requests[i]
            lis += '<li class="list-group-item">'
            lis += '<h5>' + list.Name[key] + '</h5>'
            lis += '<p>Phone Number: ' + list.Phone[key] + '</p>'
            var time = list.ExpireTime[key] - currtime
            var days = Math.floor(time / (24 * 3600))
            time %= (24 * 3600)
            var hours = Math.floor(time / 3600)
            time %= 3600
            var mins = Math.floor(time / 60)
            time = Math.floor(time % 60)
            lis += '<p>I need help in the next ' + days + ':' + 
                    hours.toString().padStart(2, '0') + ':' + 
                    mins.toString().padStart(2, '0') + ':' + 
                    time.toString().padStart(2, '0') + '</p>'
            lis += '<p>Description: ' + list.Text[key] + '</p>'
            lis += '</li>'
        }
        requestList.innerHTML = lis
    })
    .catch((e) => console.log(e))
  }

  document.getElementById('find-me').addEventListener('click', getList)

})()
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
        for (var i = 0; i < requests.length; i++) {
            var key = requests[i]
            lis += '<li class="list-group-item">'
            lis += list.Name[key]
            lis += '</li>'
        }
        requestList.innerHTML = lis
    })
    .catch((e) => console.log(e))
  }

  document.getElementById('find-me').addEventListener('click', getList)

})()
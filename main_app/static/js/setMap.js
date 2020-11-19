var input = document.getElementById("destination");
const posts_id = JSON.parse(document.getElementById("posts_id").textContent);

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

if (window.google && input) {
  var myLatLng = { lat: 43.6532, lng: -79.3832 };
  var mapOptions = {
    center: myLatLng,
    zoom: 1,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
  };
  var map = new google.maps.Map(document.getElementById("map"), mapOptions);
  var options = {
    types: ["(cities)"],
  };
  var autocomplete = new google.maps.places.Autocomplete(input, options);
  autocomplete.bindTo("bounds", map);
  autocomplete.setFields(["address_components", "geometry", "icon", "name"]);
  autocomplete.addListener("place_changed", function () {
    const place = autocomplete.getPlace();
    const marker = new google.maps.Marker({
      position: {
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng(),
      },
      map: map,
    });
    map.setCenter({
      lat: place.geometry.location.lat(),
      lng: place.geometry.location.lng(),
    });
    map.setZoom(6);
    var markerPosition = {
      lat: place.geometry.location.lat(),
      lng: place.geometry.location.lng(),
    };
    fetch(
      "https://project-travelogue.herokuapp.com/" +
        posts_id +
        "/saveDestinationOnMap",
      {
        method: "POST",
        credentials: "same-origin",
        headers: {
          Accept: "application/json",
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ markerPosition: markerPosition }),
      }
    )
      .then((response) => {
        console.log(response.body);
        return response.json();
      })
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
}

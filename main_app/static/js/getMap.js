function initMap() {
  const markerPositionLat = JSON.parse(
    document.getElementById("markerPositionLat").textContent
  );
  const markerPositionLng = JSON.parse(
    document.getElementById("markerPositionLng").textContent
  );
  console.log(markerPositionLat);
  console.log(markerPositionLng);
  var markerPosition = { lat: markerPositionLat, lng: markerPositionLng };

  console.log(markerPosition);
  var mapOptions = {
    center: markerPosition,
    zoom: 6,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
  };
  var map = new google.maps.Map(document.getElementById("map"), mapOptions);
  const marker = new google.maps.Marker({
    position: markerPosition,
    map: map,
  });
}

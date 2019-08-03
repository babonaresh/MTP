
var DenverText;

var DenverString;

var infowindowDenver;

var imgDenver;


function initiate(){
DenverText = "Denver, officially the City and County of Denver, is the capital and most populous municipality of the U.S. state of Colorado. Denver is in the South Platte River Valley on the western edge of the High Plains just east of the Front Range of the Rocky Mountains. The Denver downtown district is immediately east of the confluence of Cherry Creek with the South Platte River, approximately 12 mi (19 km) east of the foothills of the Rocky Mountains";


DenverString = '<p class="infoWindow">Denver, Capitol of Colorado!</p>';

infowindowDenver = new google.maps.InfoWindow({content: DenverString});

imgDenver = document.createElement('img');
imgDenver.src = "/static/images/Denver.JPG";
imgDenver.setAttribute("id", "imageInfoBox");

}


      function initMap() {
      initiate();
      var map;
        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: 41.247144, lng: -96.016774},
          zoom: 4
        });

        var latlngDenver = new google.maps.LatLng(39.777128, -104.989211);
        var latlngSanFran = new google.maps.LatLng(37.77105,  -122.423851);

        var markerDenver = new google.maps.Marker(
			{
				position: latlngDenver,
				map: map,
				draggable: false,
				animation: google.maps.Animation.DROP,
				title: 'Denver'
			});

			var markerSanFran = new google.maps.Marker(
			{
				position: latlngSanFran,
				map: map,
				draggable: false,
				animation: google.maps.Animation.DROP,
				title: 'San Francisco'
			});

			google.maps.event.addListener(markerDenver,'click',function() {
                        map.setZoom(11);
                        map.setCenter(markerDenver.getPosition());
                        infowindowDenver.open(map, markerDenver);
                        infoBox('denver');
                        });




     function infoBox(nummer){
    var elementMap = document.getElementById("map");
    var boxText;
    var boxImage;
    switch (nummer){
        case "denver": boxText = DenverText;
                      boxImage = imgDenver;
                      break;
        case "sanfran": boxText = sanfranText;
                       boxImage = imgsanfran;
                     break;

       case "maike": boxText = MaikeText;
                      boxImage = imgMaike;
                      break;

        default: alert("Default Anweisung in der switch Anweisung!");
    }

     var worldmap = document.getElementById("worldmap");

     //test if there is already an infoBox displaying
    if (document.getElementById("infoBox")){
        worldmap.removeChild(document.getElementById("infoBox"));
        var neuerContainer = document.createElement("div");
        neuerContainer.setAttribute("id", "infoBox");
        neuerContainer.style.width = window.getComputedStyle(elementMap, "").width;
        worldmap.appendChild(neuerContainer);
        //add text and image for the new created container
         infoText( boxText, boxImage);
    } else {
        var neuerContainer = document.createElement("div");
        neuerContainer.setAttribute("id", "infoBox");
        neuerContainer.style.width = window.getComputedStyle(elementMap, "").width;
        worldmap.appendChild(neuerContainer);
        //add text and image for the new created container
         infoText( boxText, boxImage);
    }
      }

      function infoText(textBox, image) {
    var container = document.getElementById("infoBox");
    var text = document.createElement("p");
    text.innerHTML = textBox;
    container.appendChild(image);
    container.appendChild(text);
    container.style.height = window.getComputedStyle(image, "").height;
}

}
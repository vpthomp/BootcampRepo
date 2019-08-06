// var url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
var url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"

// Function for marker size
function markerSize(mag){
  return mag * 5;
}

// Function for marker color
function markerColor(mag){
  if (mag <= 1) {
    return "#ADFF2F";
  } else if (mag <= 2){
    return "#9ACD32";
  } else if (mag <=3){
    return "#FFFF00";
  } else if (mag <=4) {
    return "#FFD700";
  } else if (mag <=5) {
    return "#FFA500";
  } else {
    return "#FF0000"; 
  };
}

// Grab JSON data 
d3.json(url, function(data){
    // console.log(data)
    createFeatures(data.features);
})

function createFeatures(earthquakeData){
  //   // simple version, without colored markers
  //   // Define a function we want to run once for each feature in the features array
  //   // Give each feature a popup describing the place and time of the earthquake
  
  //   function onEachFeature(feature, layer) {
  //     layer.bindPopup("<h3>" + feature.properties.place +
  //       "</h3><hr><p>" + new Date(feature.properties.time) + "</p>");
  //   }
    
  //   // Create a GeoJSON layer containing the features array on the earthquakeData object
  //   // Run the onEachFeature function once for each piece of data in the array
 
  //   var earthquakes = L.geoJSON(earthquakeData, {
  //     onEachFeature: onEachFeature
  //   });
  
  //   //Sending earthquake layer to the createMap function
  //   createMap(earthquakes)
  // }



  // With markers according
  // Create a GeoJSON layer containing the features array on the earthquakeData object
  // Run the onEachFeature function once for each piece of data in the array
  var earthquakes = L.geoJSON(earthquakeData, {
    // onEachFeature: onEachFeature
    // Define a function we want to run once for each feature in the features array
    // Give each feature a popup describing the place and time of the earthquake
    onEachFeature: function (feature, layer) {
      layer.bindPopup("<h3>" + feature.properties.place +
        "</h3><hr><p>" + new Date(feature.properties.time) + "</p>" + 
        "<p> Magnitude: " + feature.properties.mag + "</p>")
      } , 
      pointToLayer: function (feature, latlng){
        return new L.circleMarker(latlng, 
          {radius: markerSize(feature.properties.mag), 
          fillColor: markerColor(feature.properties.mag), 
          fillOpacity: 0.8,
          opacity: 0.5, 
          stroke: false,
          })
      }
  //end of earthquakes
  });

  //Sending earthquake layer to the createMap function
  createMap(earthquakes);
// End of createFeatures function
}

function createMap(earthquakes){
    // Define streetmap and darkmap layers
    var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.streets",
        accessToken: API_KEY
    });
    
      var darkmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.dark",
        accessToken: API_KEY
    });

    // Define a baseMaps object to hold our base layers
    var baseMaps = {
        "Street Map": streetmap,
        "Dark Map": darkmap
    };

    //Create overay object to hold overlay layer
    var overlayMaps = {
        Earthquakes: earthquakes
    };
    
    // Create our map, giving it the streetmap and earthquakes layers to display on load
    var myMap = L.map("map", {
        //center: [37.09, -95.71],
        center: [31.57853542647338, -99.580078125],
    zoom: 4,
    layers: [streetmap, earthquakes]
  });

    // Create a layer control
    // Pass in our baseMaps and overlayMaps
    // Add the layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
    collapsed: false
    }).addTo(myMap);

    // Create a legend
    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function(){

        var div = L.DomUtil.create("div", "info legend");

        magnitude = [0,1,2,3,4,5,6];

        for (var i = 0; i < magnitude.length; i++) {
          div.innerHTML +=
              '<i style="background:' + markerColor(magnitude[i] + 1) + '"></i> ' +
              magnitude[i] + (magnitude[i + 1] ? '&ndash;' + magnitude[i + 1] + '<br>' : '+');
        }
  
      return div;
    //end function of legend    
    };
  
    // Adding legend to the map
    legend.addTo(myMap);
    

// End createMap function
}

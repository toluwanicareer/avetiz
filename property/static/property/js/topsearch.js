
 google.maps.event.addDomListener(window, 'load', initialize);
			function initialize() {
				var options = {
								types: ['(cities)'],
								radius: '2000',
								location:'6.5243793,3.379205700000057',
								componentRestrictions: {country: "us,ng"}
								
								};
				var input = document.getElementById('id_search',options);
				var autocomplete = new google.maps.places.Autocomplete(input);
				autocomplete.addListener('place_changed', function () {
				var place = autocomplete.getPlace();
        var info = '';
        place.address_components.forEach(function (item) {
        if (item.types.indexOf("administrative_area_level_1") > -1) {
            info += '<div>State: ' + item.long_name + '</div>';
            document.getElementById("id_state").value= item.long_name;

        }
        if (item.types.indexOf("locality") > -1) {
            info += '<div>City: ' + item.long_name + '</div>';
            document.getElementById("id_city").value = item.long_name;
        }
        });
        console.log(info)


			// place variable will have all the information you are looking for.
				console.log(place.geometry['location'].lat());
				console.log(place.geometry['location'].lng());
				longitude=place.geometry['location'].lng();
				latitude=place.geometry['location'].lat();
				//displayLocation(latitude,longitude);
				
				
				});
				//sdisplayLocation(latitude,longitude);
				//form=document.getElementById('form-buscar');

				//form.submit();
				}

function setType(a){
	document.getElementById('id_propertytype').value=a;
	document.getElementById('type').firstChild.nodeValue=a;
}
function setBath(a){
	document.getElementById('id_bathno').value=a;
	document.getElementById('bath').firstChild.nodeValue=a+'  Bath';
}
function setBed(a){
	document.getElementById('id_bedno').value=a;
	document.getElementById('bed').firstChild.nodeValue=a+'  Bed';
}
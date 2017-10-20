      function geoFindMe() {
             $.getJSON('https://openexchangerates.org/api/latest.json?app_id=0f46fcde638946f59d4c5b72c2454ae3',
              function(data) {
                //alert('gotten the conversion');
                })
            .done(function(data){
               if ( typeof fx !== "undefined" && fx.rates ) {
                fx.rates = data.rates;
                fx.base = data.base;
            } else {
                // If not, apply to fxSetup global:
                var fxSetup = {
                    rates : data.rates,
                    base : data.base
                }
            }
            fx.settings = { from: "NGN", to: "USD" };
            if(navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(success, error, geoOptions);
            } else {
          console.log("Geolocation services are not supported by your web browser.");
          $.get('/request/?location=abuja',function(data,status){
              $('div.js-feature').html(data.featurelatest)
              $('.temphide').show()
              $('#city').html('Abuja');
              $('#state').html('Abuja');
          })
          }
            })

            .fail(function(){
              console.log('fail')
            });
        
          
      }

      function success(position) {
        var latitude = position.coords.latitude;
        var longitude = position.coords.longitude;
        var altitude = position.coords.altitude;
        var accuracy = position.coords.accuracy;
        console.log("lat: " + latitude + " long: " + longitude);
        displayLocation(latitude,longitude);
        }

      function error(error) {
        $.get('/request/?location=abuja',function(data,status){
              console.log("Unable to retrieve your location due to " + error.code + ": " + error.message)
              $('div.js-feature').html(data.featurelatest)
              $('.temphide').show();
              $('#city').html('Abuja');
              $('#state').html('Abuja');
          })
          }
      

      var geoOptions = {
      enableHighAccuracy: true,
      maximumAge: 30000,
      timeout: 27000
      };
google.maps.event.addDomListener(window, 'load', initialize);
      function initialize() {
        var options = {
                types: ['(cities)'],
                radius: '2000',
                location:'6.5243793,3.379205700000057',
                componentRestrictions: {country: "us,ng"}
                
                };
        var input = document.getElementById('id_query',options);
        var autocomplete = new google.maps.places.Autocomplete(input);
        autocomplete.addListener('place_changed', function () {
        var place = autocomplete.getPlace();
        var info = '';
        place.address_components.forEach(function (item) {
        if (item.types.indexOf("administrative_area_level_1") > -1) {
            info += '<div>State: ' + item.long_name + '</div>';
            $("#id_state").val(item.long_name)

        }
        if (item.types.indexOf("locality") > -1) {
            info += '<div>City: ' + item.long_name + '</div>';
            $("#id_city").val(item.long_name)
        }
        if (item.types.indexOf("country")> -1){
          $("#id_country").val(item.long_name)
        }
        });
        console.log(info)
        });

        var locator2=document.getElementById('pac-input', options);
        var autocomplete2=new google.maps.places.Autocomplete(locator2);
        autocomplete2.addListener('place_changed', function(){
          var place2 =autocomplete2.getPlace();
          var info2 ='';
          place2.address_components.forEach(function(item){
             if (item.types.indexOf("administrative_area_level_1") > -1) {
            info2 += '<div>State: ' + item.long_name + '</div>';
            $('#state').html(item.long_name);
            $('#city').html(item.long_name);
             $.get('/request/?location='+item.long_name,function(data,status){
              //alert('failure'+data.featurelatest);
              $('div.js-feature').html(data.featurelatest)
              chkcurr('.js-price','#id_country')
              $('.temphide').show()
          })
          }
          if (item.types.indexOf("country")> -1){
          $("#id_country").val(item.long_name)
          //chkcurr('.js-price','#id_country')
          //console.log('fufe')
        }

        });
          }) 
        var pmiform=document.getElementById('id_pmi_query', options);
        var autocomplete3=new google.maps.places.Autocomplete(pmiform);
        autocomplete3.addListener('place_changed', function(){
          var place3 =autocomplete3.getPlace();
          
          place3.address_components.forEach(function(item){
             if (item.types.indexOf("administrative_area_level_1") > -1) {
                        $('#id_pmi_state').val(item.long_name)
                        console.log(item.long_name)

          }

          if (item.types.indexOf("country")> -1){
             $('#id_pmi_country').val(item.long_name)
             console.log(item.long_name)
        }
        if (item.types.indexOf("locality")> -1){
             $('#id_pmi_city').val(item.long_name)
             console.log(item.long_name)
        }
        });
          })      
      }
function displayLocation(latitude,longitude){
    var geocoder;
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(latitude, longitude);

    geocoder.geocode(
        {'latLng': latlng}, 
        function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                if (results[0]) {
                    var add= results[0].formatted_address ;
                    var  value=add.split(",");
                    count=value.length;
                    country=value[count-1];
                    state=value[count-2];
                    city=value[count-3];
          try{
          var x=document.getElementById("city");
          var y=document.getElementById("state");
          y.innerHTML = state;
          x.innerHTML = state;
        }
        catch(err){
          //do nothing
        }
          $('#id_country').val(country)
           $.get('/request/?location='+state,function(data,status){
              //alert('failure'+data.featurelatest);
              $('div.js-feature').html(data.featurelatest)
              $('.temphide').show()
              chkcurr('.js-price','#id_country')
          })
                    console.log ("city name is: " + city);
                }
                else  {
                    console.log ("address not found");
                }
            }
            else {
                console.log( "Geocoder failed due to: " + status);
            }
        }
    );
}

function getCountry(id) {
  return $(id).val()
}

function chkcurr(priceclass, countryid){
   var country=getCountry(countryid)
   country=country.replace(' ','')
   if(country !='Nigeria'){
  convertToDollar(priceclass)
}
}
function convertTo(value, el){
  dollarvalue=Math.ceil(fx.convert(value, {from:"NGN", to:"USD"}))
  dollarvalue='$'+(dollarvalue.toString())
  $(el).text(dollarvalue)
}

function convertToDollar(priceclass){
  $(priceclass).each(function(){
  nairavalue=$(this).text()
  nairavalue=Number(nairavalue.replace('₦', ''))
  convertTo(nairavalue, this)
})
}

function convertToNaira(priceclass){
  $(priceclass).each(function(){
    dollarvalue=$(this).text()
    dollarvalue=Number(dollarvalue.replace('$',''))
    convertToN(dollarvalue, this)
  })
}
function convertToN(value, el){
  nairavalue=Math.ceil(fx.convert(value, {from: "USD", to: "NGN"}))
  nairavalue='₦'+(nairavalue.toString())
  $(el).text(nairavalue)
}

$('.js-curr').on('change', function(){
  //alert('im here')
  currency=$(this).val();
  console.log(currency)
  switch(currency){
    case 'USD':
      //alert('im here')
      convertToDollar('.js-price')
      break;

    case 'NGN':
      convertToNaira('.js-price')
      break;
    default:
      convertToDollar('.js-price');
  
  }
})



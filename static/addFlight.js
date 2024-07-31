$(function(){
	$('#button1').click(function(){
		$.ajax({
			url: '/staffAddAirport',
			data: $('form').serialize(),
			type: 'POST',	
			success: function(response){
				console.log(response);
				$("#res").html('<p>'+response.data.toString()+'</p>');
			},
			error: function(error){
				console.log(error);
			}
		// })
		// .done(function(data){
		// 	console.log('here is data')
		// 	$('#res').html(data)
		});
    });
    $('#button2').click(function(){
		$.ajax({
			url: '/staffAddAirplane',
			data: $('form').serialize(),
			type: 'POST',	
			success: function(response){
				console.log(response);
				$("#res").html('<p>'+response.data.toString()+'</p>');
			},
			error: function(error){
				console.log(error);
			}
		// })
		// .done(function(data){
		// 	console.log('here is data')
		// 	$('#res').html(data)
		});
    });
    $('#button3').click(function(){
		$.ajax({
			url: '/staffProcessCustomers',
			data: $('form').serialize(),
			type: 'POST',	
			success: function(response){
                var htmltext='<table style="width:100%;text-align: center;"><tr>'
                htmltext+="<th>Airline Company</th>"
                htmltext+="<th>Arrival</th>"
                htmltext+="<th>Arrival Time</th>"
                htmltext+="<th>Departure</th>"
                htmltext+="<th>Departure Time</th>"
                htmltext+="<th>Flight Number</th>"
                htmltext+="<th>Price</th></tr>"
                
                for(i=0;i<response.data.length;i++){
                    htmltext+="<tr>"
                    htmltext+="<td>"+ response.data[i].airline_name +"</td>"
                    htmltext+="<td>"+ response.data[i].arrival_airport +"</td>"
                    htmltext+="<td>"+ response.data[i].arrival_time +"</td>"
                    htmltext+="<td>"+ response.data[i].departure_airport +"</td>"
                    htmltext+="<td>"+ response.data[i].departure_time +"</td>"
                    htmltext+="<td>"+ response.data[i].flight_num +"</td>"
                    htmltext+="<td>"+ response.data[i].price +"</td></tr>"

                }
                htmltext +='</table>'
				console.log(response);
				$("#res").html(htmltext);
			},
			error: function(error){
				console.log(error);
			}
		// })
		// .done(function(data){
		// 	console.log('here is data')
		// 	$('#res').html(data)
		});
	});
});
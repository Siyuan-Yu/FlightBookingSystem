$(function(){
	$('button').click(function(){
		// var departureCity = $('#departureCity').val();
        // var arrivalCity = $('#arrivalCity').val();
        // var flightDate = $('#flightDate').val();
        // var flightNum = $('#flightNum').val();
		$.ajax({
			url: '/publicSearch',
			data: $('form').serialize(),
			type: 'POST',	
			success: function(response){
				// console.log(response);
				// $('#res').html(response);
			},
			error: function(error){
				console.log(error);
			}
		})
		.done(function(data){
			console.log('here is data')
			$('#res').html(data)
		});
	});
});
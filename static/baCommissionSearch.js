$(function(){
	$('button').click(function(){
		$.ajax({
			url: '/baCommissionSearch',
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
$(function(){
	$('#button1').click(function(){
		$.ajax({
			url: '/cusTrackSearch',
			data: $('form').serialize(),
			type: 'POST',	
			success: function(response){
				console.log('res',response);
				$('#res').html("<p>sss</p>");
			},
			error: function(error){
				console.log(error);
			}
		})
		.done(function(data){
			console.log('here is data',data)
			$('#res').html(data)
		});
    });   
});
$(function(){
	$('#button1').click(function(){
		$.ajax({
			url: '/staffHomePage',
			data: $('#form1').serialize(),
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
			$('#res1').html(data)
		});
    });
    $('#button2').click(function(){
		$.ajax({
			url: '/staffHomePage',
			data: $('#form2').serialize(),
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
			console.log('here is data1')
			$('#res2').html(data)
		});
	});
});
$.ajax({
	type: 'GET',
	url: 'api/users/',
	success: function(data) {
		console.log(data);
	}
});
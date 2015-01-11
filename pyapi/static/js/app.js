$(function() {
	

	$('#sendReq').on('click', function() {
		var user = {
			username: $('#username').val(),
			password: $('#password').val()
		};
		
		$.ajax({
			type: 'POST',
			url: '/api/users/',
			data: user,
			success: function(res) {
				console.log(res);
			}
		});
	});

	$('#deleteReq').on('click', function() {
		var deleteID = parseInt($('#delete').val());

		$.ajax({
			type: 'DELETE',
			url: '/api/users/' + deleteID,
			success: function(res) {
				console.log('del:', res);
			}
		});

	});

	$('#updateReq').on('click', function() {
		var user = {
			id: $('#uid').val(),
			username: $('#uname').val(),
			password: $('#upas').val()
		};

		$.ajax({
			type: 'PUT',
			url: '/api/users/' + user.id,
			data: user,
			success: function(res) {
				console.log('update:',res);
			}
		})
	});

	$('#sendPostReq').on('click', function() {
		var post = {
			title: $('#title').val(),
			text: $('#text').val(),
			creator_id: $('#creator').val()
		}

		$.ajax({
			type: 'POST',
			url: 'api/posts/',
			data: post,
			success: function(res) {
				console.log('new post:', res);
			}
		})
	});

	$('#deletePostReq').on('click', function() {
		var deleteID = parseInt($('#deletePost').val());

		$.ajax({
			type: 'DELETE',
			url: '/api/posts/' + deleteID,
			success: function(res) {
				console.log('delete post:', res);
			}
		});

	});

	$('#updatePostReq').on('click', function() {
		var post = {
			id: $('#pid').val(),
			title: $('#ptitle').val(),
			text: $('#ptext').val()
		};

		$.ajax({
			type: 'PUT',
			url: '/api/posts/' + post.id,
			data: post,
			success: function(res) {
				console.log('update post:',res);
			}
		})
	});
});
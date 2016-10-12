$(document).ready(function() {

	$('#carousel').owlCarousel({
		autoPlay: 3500,
		stopOnHover: true
	});

	var userId = $('#user_holder').attr('uid');
	var userPosts = $('.user-post-info');
	var postIds = [];
	for (var i = 0; i < userPosts.length; i++) {
		postIds.push(userPosts[i].attributes[1].value);
	}
	console.log(userPosts);
	console.log(postIds);

	$('.vote-up, .vote-down').click(function() {
		var pid = $(this).parent().attr('pid');
		var post_user = $(this).parent().attr('uid');
		console.log(pid);
		console.log('post_user: ' + post_user);
		console.log(userId);
		var calc;
		if (post_user == userId) {
			alert('You cannot vote for yourself!');
		} else {
			if ($(this).hasClass('vote-up')) {
			calc = 1;
		} else {
			calc = 0;
			console.log('vote-down!');
		}
		console.log({pid: pid, calc: calc});
		$.ajax({
			url: 'vote',
			type: 'POST',
			data: {pid: pid, calc: calc},
			success: function(result) {
				location.reload();
				console.log(result);
				// var pid = result.pid;
				// var pVotes = result.post_votes;
				// var uid = result.userid;
				// var uVotes = result.user_votes;
				// if (uid == userId) {
				// 	console.log("userId matches!");
				// 	$('#votes_num').text = uVotes;
				// 	var userPosts = $('.user-post-info');
				// 	for (var i = 0; i < userPosts.length; i++) {
				// 		if (userPosts[i].attributes['pid'].value == pid) {
				// 			$('.user-post-votes')[i].value = pVotes;
				// 		}
				// 	}
				// } 
			},
			error: function(err) {
				console.log(err);
				alert('Sorry, something went wrong. Try again.');
			}
		});	

		}	
	});

	$('.removePost').click(function() {
		var postId = $(this).attr('pid');
		console.log(postId);
		$.ajax({
			url: 'removePost',
			type: 'POST',
			data: {pid: postId},
			success: function(result) {
				console.log(result);
				location.reload();
			}
		})
	});

	$('#showVoted').click(function() {

	});

});

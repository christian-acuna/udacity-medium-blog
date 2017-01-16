$(function() {
  $( ".like-button" ).on( "click", "i", function( event ) {
    event.preventDefault();
    var icon = $( this );
    var postId = icon.attr('data-postid');
    console.log(postId);
    var path = '/blog/posts/like'
    $.post(path, {"postID": postId}, function(data, textStatus, xhr) {
      var response = JSON.parse(data)
      console.log(response);
      if (response['error']) {
        errorHTML = '<div class="ui negative message"><div class="header">' + response['error'] + '</div></div>'
        $('.ui.main.text.container').prepend(errorHTML)
        $('.ui.negative.message').fadeOut(4000)
      } else if (response.addLikes >= 0) {
        icon.removeClass('outline')
        icon.addClass('red')
        icon.siblings()[0].innerHTML = response.addLikes + ' likes'
      } else if (response.removeLikes >= 0) {
        icon.removeClass('red')
        icon.addClass('outline')
        icon.siblings()[0].innerHTML = response.removeLikes + ' likes'
      }
    });
  });

  $("#comment-form").submit(function(event) {
    event.preventDefault();

    console.log('steotanhoeu');
    var commentForm = $(this);
    var parent = commentForm.attr('data-postid');
    var textArea = commentForm.find('textarea')
    var body = textArea.val()
    var data = {"parent": parent, "body": body}
    $.post('/comments', data, function(data, textStatus, xhr) {
      var comment_response = JSON.parse(data)
      commentForm.siblings().last().append(comment_response["comment"])
      textArea.val("")
    });
  });

  $('.ui.comments').on('click', 'a.reply', function(event) {
    event.preventDefault();
    var deleteButton = $(this);
    var comment = deleteButton.closest('.comment')
    var commentId = comment.attr('data-commentId')
    var postId = $('form[data-postid]').attr('data-postid')
    var data = {"commentId": commentId, "postId": postId}
    $.post('/comments/delete', data, function(data, textStatus, xhr) {
      console.log(data);
      var comment_response = JSON.parse(data)
      console.log(comment_response.comment, commentId);
      if (comment_response.comment === parseInt(commentId)) {
        deleteButton.closest('.comment').remove()
      } else if (comment_response.error) {
          console.log(comment_response.error);
      }
    });
  })
})

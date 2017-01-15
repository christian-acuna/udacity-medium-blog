$(function() {
  console.log('hello');
  $( ".like-button" ).on( "click", "i", function( event ) {
    event.preventDefault();
    var icon = $( this );
    var postId = icon.attr('data-postid');
    console.log(postId);
    var path = '/blog/posts/like'
    console.log(path);
    $.post(path, {"postID": postId}, function(data, textStatus, xhr) {
      var response = JSON.parse(data)
      icon.removeClass('outline')
      icon.addClass('red')
      icon.siblings()[0].innerHTML = response.likes + ' likes'
    });
  });

  $("#comment-form").submit(function(event) {
    event.preventDefault();

    console.log('steotanhoeu');
    var commentForm = $(this);
    var parent = commentForm.attr('data-postid');
    var textArea = commentForm.find('textarea')
    var body = textArea.val()
    data = {"parent": parent, "body": body}
    $.post('/comments', data, function(data, textStatus, xhr) {
      var comment_response = JSON.parse(data)
      commentForm.siblings().last().append(comment_response["comment"])
      textArea.val("")
    });
  });
})

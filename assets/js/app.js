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
      response = JSON.parse(data)
      icon.removeClass('outline')
      icon.addClass('red')
      icon.siblings()[0].innerHTML = response.likes + ' likes'
    });
});
})

$(function() {

  // event listener for icont on like-button
  $( ".like-button" ).on( "click", "i", function( event ) {
    event.preventDefault();

    var icon = $( this );
    var postId = icon.attr('data-postid');

    var path = '/blog/posts/like'

    $.post(path, {"postID": postId}, function(data, textStatus, xhr) {
      var response = JSON.parse(data)
      // if response['error'] show error message on top
      if (response['error']) {
        errorHTML = '<div class="ui negative message"><div class="header">' + response['error'] + '</div></div>'
        $('.ui.main.text.container').prepend(errorHTML)
        $('.ui.negative.message').fadeOut(4000)
        // Add like
      } else if (response.addLikes >= 0) {
        icon.removeClass('outline')
        icon.addClass('red')
        icon.siblings()[0].innerHTML = response.addLikes + ' likes'
        // Romove like
      } else if (response.removeLikes >= 0) {
        icon.removeClass('red')
        icon.addClass('outline')
        icon.siblings()[0].innerHTML = response.removeLikes + ' likes'
      }
    });
  });

  $("#comment-form").submit(function(event) {
    event.preventDefault();

    var commentForm = $(this);
    var parent = commentForm.attr('data-postid');
    var textArea = commentForm.find('textarea')
    var body = textArea.val()

    var data = {"parent": parent, "body": body}
    $.post('/comments', data, function(data, textStatus, xhr) {
      var comment_response = JSON.parse(data)
      commentForm.siblings().last().append(comment_response["comment"])
      // reset textArea
      textArea.val("")
    });
  });

  // delete button on comment
  $('.ui.comments').on('click', 'a.delete', function(event) {
    event.preventDefault();


    var deleteButton = $(this);
    var comment = deleteButton.closest('.comment')

    // data to build POST request
    var commentId = comment.attr('data-commentId')
    var postId = $('form[data-postid]').attr('data-postid')
    var data = {"commentId": commentId, "postId": postId}

    $.post('/comments/delete', data, function(data, textStatus, xhr) {
      var comment_response = JSON.parse(data)
      if (comment_response.comment === parseInt(commentId)) {
        deleteButton.closest('.comment').remove()
      } else if (comment_response.error) {
          console.log(comment_response.error);
      }
    });
  })

  // Edit comment button evenet listener
  $('.ui.comments').on('click', 'a.edit', function(event) {
    event.preventDefault();
    var editButton = $(this);
    var comment = editButton.closest('.comment')
    var commentText = comment.find('.text>p')
    var text = commentText[0].innerHTML;

    // show textarea with existing comment
    var commentFrom = '<div class="ui form"><div class="field"><label>Edit Comment</label><textarea rows="2">'+ text + '</textarea></div></div>'
    comment.find('.text').append(commentFrom)
    // remove existing p tag with comment
    comment.find('.text>p').remove()
    // hide editbutton to show later when user clicks "save"
    editButton.hide()
    // create and append save button which has a event listener to send new comment text
    var saveButton = '<a class="save">Save</a>'
    editButton.parent().append(saveButton)
  })

  $('.ui.comments').on('click', 'a.save', function(event) {
    event.preventDefault();

    var saveButton = $(this);

    // parent comment
    var comment = saveButton.closest('.comment')


    var commentId = comment.attr('data-commentId')
    var postId = $('form[data-postid]').attr('data-postid')

    // get new text that user entered with .val(), note .innerHTML does not work for textarea
    var commentText = saveButton.closest('textarea')
    var editCommentTextDiv = saveButton.parent().siblings('.text')[0]
    var textArea = $(editCommentTextDiv).find('textarea')[0]
    var TextAreaUpdatedComment = $(textArea).val()

    // data to build post request
    var data = {"commentId": commentId, "postId": postId, commentText: TextAreaUpdatedComment }

    $.post('/comments/edit', data, function(data, textStatus, xhr) {

      var editCommentResponse = JSON.parse(data)
      if (editCommentResponse.comment === parseInt(commentId)) {
        var editButton = $('a.edit');
        editButton.show()
        saveButton.remove()
        var newPar = '<p>'+ TextAreaUpdatedComment + '</p>'
        var textDiv = comment.find('.text')
        textDiv.empty().append(newPar)
      } else if (editCommentResponse.error) {
          console.log(editCommentResponse.error);
      }
    });
  })
})

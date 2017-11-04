function updateCommentCount(){
    var comment_count = parseInt(jQuery('#comment_count').text())+1;
    var commentscount = jQuery('#comments-count');
    if (comment_count == 1) {
        commentscount.innerHTML = comment_count + " Note";
    } else {
        commentscount.innerHTML = comment_count + " Notes";
    }
}
$(function() {
    // ADD COMMENT //
    $('.form_add_comment').submit(function(event){
        event.preventDefault();
        var form = $(this);
        var data =  new FormData(form.get(0));
        $.ajax({
            url: $('.form_add_comment').attr('action'),
            type: "POST",
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(json) {
                if (json['success'] == 0) {
                  errors = ""
                  for (var err in json['error']){
                    errors += "" + err + ": " + json['error'][err] + "\n"
                  }
                  alert(errors)                      
                }
                else {
                    updateCommentCount();
                    $('#comment-list').html();
                    $('textarea#id_comment').val(" ");
                }

            },
            error: function(response) {
                alert("error")
            }
         });        
    });
    

    // COMMENT EDIT //
    $('.comments-wrapper').on('click', '.comment-edit-class', function(event){

        var id = $(this).attr('data-id');
        $('#comment-edit-' + id).show();
        $('#comment-' + id).hide();
    });

    $('.comments-wrapper').on('submit', '.edit-form', function(event){
    event.preventDefault();
    var form = $(this);
    var data = form.serialize();
    var id = $(this).attr('data-id');
    var comment = document.getElementById('comment-'+id);
    var error = document.getElementById('edit-form-errors');
    $.ajax({
            type: "POST",
            url: form.attr('action'),
            data: data,

            success: function(data){
                json = JSON.parse(data);
                if(json.success == 1) {
                    comment.innerHTML = $('#input-comment-' + id).val();
                    $('#comment-edit-' + id).hide();
                    $('#comment-' + id).show();
                } else if(json.success == 0){
                     errors = ""
                  for (var err in json.error){
                    errors += "" + json.error[err] + "\n";
                }
                error.innerHTML = errors;
            }
            },
            dataType: 'html'
        });
    });
});
$(function() {
    $(".note_header").on("click", function(e){
        var which = this.id.endsWith('internal') ? 'internal' : 'external';
        var $form = $(this).closest("form");
        var $internalexternal = $form.find("#id_internal_external");
        var currentval = $internalexternal.val();
        if (currentval === which) return;
        $(".note_header").each(function( index ) {
          $( this ).removeClass("active_note");
        });
        $( this ).addClass("active_note");
        $internalexternal.val(which);
        $comment = $form.find("#id_comment");
        if (which === "internal"){
            if ( !$comment.hasClass("internal_external_editor_internal") ){
                $comment.addClass("internal_external_editor_internal");
            }
        } else{
            $comment.removeClass("internal_external_editor_internal");
        }
    })
});
$(document).ready(function() {

  $('.deleteNote').on('click', function(){

    var note_ID = $(this).attr('note_id');
    //technically for this AJAX request I dont need note var.
    var note = $('#noteNumber'+note_ID).val();

    req = $.ajax({
      url : '/my_books/edit/note',
      type: 'POST',
      data: {note_ID : note_ID, note : note}
    });

    $('#noteNumber'+note_ID).fadeOut(500);
  });


  $('.deleteBook').on('click', function(){
    //this referes to the global or owner object. In out case this points to deleteBook button
    //deleteBook button has attribute book_id, which we assign to book_Id var.
    var book_ID = $(this).attr('book_id');

    req = $.ajax({
      url : '/my_books/delete/book',
      type: 'POST',
      data: {book_ID : book_ID}
    });

    $('#bookNumber'+book_ID).fadeOut(500);
  });


});

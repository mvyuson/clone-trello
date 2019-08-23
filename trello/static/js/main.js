'use strict'
    
function add_board(){
    $('#create-board').click(function(){
        console.log('click')
        $('#modal').modal('show');
    });

    $('#modal').on('shown.bs.modal', function () {
        console.log('hello');
        var modal = $(this);
        $.ajax({
            'method': 'get',
            'url': '/create-board/'
        }).done(function(response){
            modal.find('.modal-body').html(response)
            createBoard();
        });
    });
}

function createBoard() {
    $('#board-form').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            method: 'POST'
        }).done(function(data){
            $('#modal').modal('hide');
            window.location.href = '/board/'+data.board;  
        }).fail(function(xhr, data){
            console.log("ffdfdf");
            $('.error').show();
        });        
    });
}

function editBoard(){
    $('#board_container').on('click', function(e){
        console.log('Click');
        var edit_board = $(this).attr('contenteditable', 'true');
        $(this).attr('focus');

        $('#board_container[contenteditable]').keypress(function(e){
            if(event.keyCode == "13"){
                $(edit_board).blur();
                console.log('EDIT BOARD');
            }
        });
    });
}

function getBoard(){
    board_id = $()
    $.ajax({
        url: '/board',
        method: 'GET',
    })
}


// function addList(){
//     console.log("LIST");
//      $.ajax({
//          url: '/create-list/',
//          method: 'get',
//      }).done(function(response){
//          $("body").find('#list-container').html(response)
//      })
// }

$(document).ready(function (){
    add_board();
    editBoard();
});
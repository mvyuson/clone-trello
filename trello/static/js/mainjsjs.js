'use strict'
    
function add_board(){
    $('#create-board').click(function(){
        $('#modal').modal('show');
    });

    $('#modal').on('shown.bs.modal', function () {
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
        var editBoard = $(this).attr('contenteditable', 'true');
        $(this).attr('focus');
        var updatedBoard = $(editBoard).text();
        console.log("sdsd", updatedBoard);

        $('#board_container[contenteditable]').keypress(function(e){
            if(event.keyCode == "13"){
                $(editBoard).blur();
                //editBoard = $(this).attr('data-listid');

                text = $(editBoard).text();
                console.log(updatedBoard); 
                // $.ajax({
                //     url: '/board/{{ board.id }}',
                //     data: 
                // })
            }
        });
    });
}


function cardDescription(){
    $('h4').on('click', function(e){
        console.log('ClickClackBada')
        $('#card-modal').modal('show');
    });

    $('#card-modal').on('shown.bs.modal', function () {
        console.log(Shown);
        var modal = $(this);
        $.ajax({
            method: 'get',
            url: '/create-board/'
        }).done(function(response){
            console.log(response)
            modal.find('.modal-body').html(response)
        });
    });
}

$(document).ready(function (){
    add_board();
    editBoard();
    cardDescription();
});
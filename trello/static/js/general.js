'use strict'
    


function archieveView(){
    $('#archive').click(function(){
        console.log('Archive');
        $('#modal').modal('show');
    });

    $('#modal').on('shown.bs.modal', function () {
        var modal = $(this);
        $.ajax({
            'method': 'get',
            'url': '/board_archive/'
        }).done(function(response){
            modal.find('.modal-body').html(response);
            createBoard();
        });
    });
}


function editBoard(){
    $('#board_container').on('click', function(e){
        var editBoard = $(this).attr('contenteditable', 'true', function(i, origValue){
            return origValue + 'Jojo';
            console.log(origValue);
        });
        $(this).attr('focus');
        
        var updatedBoard = $(editBoard).val();

        $('#board_container[contenteditable]').keypress(function(e){
            if(event.keyCode == "13"){
                $(editBoard).blur();
                //editBoard = $(this).attr('data-listid');

                var text = $(editBoard).val();
                console.log(text); 
                // $.ajax({
                //     url: '/board/{{ board.id }}',
                //     data: 
                // })
            }
        });
    });
}

$(document).ready(function (){
    archieveView();
    editBoard();

    $('#modal-card').on('shown.bs.modal', function (e) {
        var remoteUrl = $(e.relatedTarget).data('remote');
        var modal = $(this);
        $.ajax({
            'method': 'get',
            'url': remoteUrl
        }).done(function(response){
            modal.find('.modal-body').html(response);
        });
    });

    $('#modal-id').on('shown.bs.modal', function (e) {
        var remoteUrl = $(e.relatedTarget).data('remote');
        console.log(remoteUrl);
        var modal = $(this);
        $.ajax({
            'method': 'get',
            'url': remoteUrl
        }).done(function(response){
            modal.find('.modal-body').html(response);
            createBoard();
        });
    });
});

function createBoard() {
    $('#board-form').on('submit', function(e){
        console.log('Create Board');
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            method: 'POST'
        }).done(function(data){
            $('#modal-id').modal('hide');
            window.location.href = '/board/'+data.board;  
        }).fail(function(xhr, data){
            console.log("ffdfdf");
            $('.error').show();
        });        
    });
}
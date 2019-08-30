'use strict'
    
function archieveView(){
    $('#archive').click(function(){
        console.log('Archive KOKOKOKOK'); 
        $('#modal').modal('show');        
    });

    $('#modal').on('shown.bs.modal', function () {   
        console.log('Archive');           
        var modal = $(this);
        $.ajax({
            'method': 'get',
            'url': '/archive/',
        }).done(function(response){
            modal.find('.modal-body').html(response);
        });
    });
}

function editBoard(){
    $('#board_container').on('click', function(e){
        e.preventDefault();
        console.log('Edit Board');
        $(this).hide();
        $('#updateBoardForm').show();
        updateBoard();
    });
}

function updateBoard(){
    $('#updateBoardForm').on('submit', function(e){
        console.log('Gigigi')
        $(this).hide();
        $('#board_container').show()
    })
}


function editList(){
    $('h3').on('click', function(e){
        e.preventDefault();
        console.log('Edit sassList');
        $('#input-list').show();
        $(this).hide();
        updateList();
    });
}

function updateList(){
    $('#input-list').on('submit', function(e){
        $(this).hide();
        $('h3').show()
    })
}

function editCard(){
    $('#card_container').on('click', function(e){
        e.preventDefault();
        console.log('Edit Card');
        $(this).hide();
        $('#updateCardForm').show();
        updateCard();
    })
}

function updateCard(){
    $('#updateCardForm').on('submit', function(e){
        $(this).hide();
        $('#card_container').show();
       
    })
}

function createBoard() {
    $('#board-form').on('submit', function(e){
        console.log('Create Boardsssssssssssssssssssss');
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

function cardDescription(){
    $('.description-form').on('submit', function(e){
        console.log('CARD DESCRIPTION')
        e.preventDefault();
        $(this).hide();
        $('#card_description').show();
    })
}

$(document).ready(function (){
    archieveView();
    editBoard();
    editList();
    editCard();
    cardDescription();

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
        console.log('CREATRTSRTYDRYSD')
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


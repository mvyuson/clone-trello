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


    function createBoard() {
        $('#board-form').on('submit', function(e){
        console.log('submit');
        e.preventDefault();

        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            method: 'POST'
        }).done(function(data){
            $('#modal').modal('hide');
            window.location.href = '/board/'+data.id;     //undefine id
        }).fail(function(err){
            alert(err)
        })
    });

    }
}


function addList(){
    $('#list-form').on('click', function(){
        console.log("GET2.....");
        $.ajax({
            url: $(this).attr('action'),
            method: 'get',
        }).done(function(response){
            console.log("GET.....");
            createList();
        })
    });
}


function viewList(){
    $.ajax({
        url: '/create-list/',
        method: 'get',
    }).done(function(response){

    })
}

function createList(){
    $('#list-form').on('submit', function(e){
        console.log('submit formlist');

        // $.ajax({
        //     url: $(this).attr('action'),
        //     data: $(this).serialize(),
        //     method: 'POST'
        // }).done(function(data){   
        // }).fail(function(err){
        //     alert(err)
        //     console.log(error)
        // })
    });
}

function editListTitle(){
    $('.ltitle').click(function(e){
        var edited_list = $(this).attr('contenteditable', 'true');
        $(this).attr('focus');

        $('.ltitle[contenteditable').keypress(function(e){
            if(e.keyCode == "13"){
                $(edited_list).blur();
            }
        });
    });
}

$(document).ready(function (){
    add_board();
    addList();
    editListTitle();
});
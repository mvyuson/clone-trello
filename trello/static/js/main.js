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
            e.preventDefault();
            $.ajax({
                url: $(this).attr('action'),
                data: $(this).serialize(),
                method: 'POST'
            }).done(function(data){
                $('#modal').modal('hide');
                window.location.href = '/board/'+data.board;  
            }).fail(function(xhr, data){
                $('.error').show();
            });        
        });

    }
}

function clist(){
    $.ajax({
        method: 'get',
        url: '/board/'
    }).done(function(response){
        vlist();
        console.log('HA');
    });
}

function vlist(){
    $('#list-form').on('submit', function(e){
        console.log('submit list');
        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            method: 'POST'
        }).done(function(data){
            console.log(data);
            //window.location.href = '/create-list/';
            $('#list-form').attr('');
            //$("body").find('.container').html(data)
            $("body").find('.container').append(data.board_list)
        }).fail(function(xhr, data){

        });
    })
}

function addList(){
     $.ajax({
         url: '/create-list/',
         method: 'get',
     }).done(function(response){
         $("body").find('.container').html(response)
         updateList();
     })
}


// function updateList(){
//     $('#b_list').click(function(e){
//         var edit_list = $(this).attr('contenteditable', 'true');
//         $(this).attr('focus');

//         $('#b_list[contenteditable]').keypress(function(e){
//             if(event.keyCode == "13"){
//                 $(edit_list).blur();
//                 console.log('HA')
//             }
//         });
//     });
// }

function updateList(){
    $('h5').click(function(e){
        var data = $('#b-list').val();
        console.log(data);
            var edit_list = $(this).attr('contenteditable', 'true');
            $(this).attr('focus');
        $.ajax({
            url: '/create-list/',
            method: 'get',
        }).done(function(response){

        })
    })
}

$(document).ready(function (){
    add_board();
    //addList();
    //updateList();
});
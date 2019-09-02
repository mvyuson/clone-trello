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
    $('.board-title').on('click', function(e){
        e.preventDefault();
        $(this).hide();
        $('#edit-board').show();
        updateBoard();
    });
}

function updateBoard(){
    $('#board-edit-form').on('submit', function(e){
        console.log('Board Submit!');
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            method: 'POST'
        }).done(function(data){
            e.preventDefault();
            $('.board-title').show();
            $('header').find('.board-title').html(data.board)
            console.log(data)
            $('#edit-board').hide();
        });
    });
}


function editList(){
    $('.list-span').on('click', function(e){
        console.log('JJJJJJ')
        $(this).hide();
        $('#edit-list').show();

    });
}

function updateList(template, list_id){
    $('#edit-list-form').on('submit', function(e){
        console.log("JOJOJO");
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            method: 'POST'
        }).done(function(data){
            e.preventDefault();
            $('.list-span').show();
            $('#edit-list').hide();
            $('body').find('.list-span').html(data.board_list)
            console.log(data);
        })
    });
}

// function editList(){
//     $('h3').on('click', function(e){
//         e.preventDefault();
//         console.log('Edit sassList');
//         $('#input-list').show();
//         $(this).hide();
//         updateList();
//     });
// }

// function updateList(){
//     $('#input-list').on('submit', function(e){
//         $(this).hide();
//         $('h3').show()
//     })
// }

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
    $('#board-edit-form').on('submit', function(e){
        console.log('Joho Boardsie');
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

function archiveList(){
    $('.archive-list').on('click', function(e){
        var archive = $(this).data('id');
        console.log(archive);
        $.ajax({
            url: '/list-archive/'+archive,
            method: 'get',
        }).done(function(res){
            console.log('GUGU');
            $(this).parent().parent().parent().parent().remove();
            
        });
    });
}


$(document).ready(function (){
    archieveView();
    editBoard();
    editList();
    editCard();
    cardDescription();
    archiveList();
    var i = 0;

    $('#list-form').on('submit', function(e){
        console.log('CREATE LIST');
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            method: 'POST'
        }).done(function(data){
            console.log(data)
            var template = `
                        <div class="card p-1 ml-4 mt-5">
                        <div class="card-title pt-3 pb-0 d-flex justify-content-between">
                        <span class="list-span">${data.board_list}</span> 
                        <div class="dropdown p-0 float-right" id="list-dropdown">
                        <button class="btn " type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            ...
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <a class="archive-list text-dark ml-5" id="archive-list" href="" data-id=${data.id}>Archive List</a>
                        </div>
                        </div>
                        </div>
                        <div class="card-body pb-0">
                        </div>
                        </form>
                        </div>
                        </div>
                        `;
            console.log(i);        
            archiveList();  

            $('#list-board').append(template);
            $('#list-form').trigger('reset');
        }).fail(function(data){
            console.log("error")
        });
        return false;
    });



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
        console.log('Boardsie')
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


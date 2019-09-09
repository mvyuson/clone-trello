'use strict'

$(document).ready(function (){
    archieveView();
    editBoard();
    editList();
    editCard();
    archiveBoard();
    archiveList();
    createCard();
    createList();
    createCardDescription();
    cardDraggable();
    leaveBoard();
    mouseoutBoard();

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

function createList(){
    $('#list-form').on('submit', function(e){
        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            method: 'POST'
        }).done(function(data){
            var template = `
                        <div class="card p-1 ml-4 mt-5 list-content-${data.id}" data-id=${data.id}>
                        <div class="card-title pt-3 pb-0 d-flex justify-content-between">
                        <span class="list-span" value="${data.board_list}" contenteditable="true" data-title="${data.board_list}" data-id="${data.id}"><b>${data.board_list}</b></span> 
                        <a href="/edit-list/${data.id}/"></a>
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
                        
                        <form class="create-card mt-3" method="POST" draggable="false" action="/board/${data.id}/list/">
                            <input type="text" class="input-card" name="card_title" placeholder="+ Add Card">
                        </form>
                        </div>
                        </form>
                        </div>
                        </div>
                        `;  
            $('#list-board').append(template);
            $('#list-form').trigger('reset');
        }).fail(function(data){
            console.log("error")
        });
        return false;
    });
}

function createCard(){
    $(document).on('submit', '.create-card', function(e){
        e.preventDefault();
        var parent_list = $(this).parents('.card').data('id');

        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            method: 'POST'
        }).done(function(data){
            var card_template = `
                                <li class="list-unstyled m-0 ui-sortable-handle ui-draggable ui-draggable-handle" droppable="true" draggable="true" data-id="${data.id}">
                                <a href="/drag-and-drop/${data.id}/">
                                <a href="" data-toggle="modal" data-remote="/description/${data.id}" data-target="#modal-card">
                                <h4 class="addcard w-100" data-id="${data.id}" id="card">
                                    ${data.card}
                                <button class="btn float-right" id="description">
                                    <span class="glyphicon glyphicon-pencil"></span>
                                </button>
                                </h4>
                                </a>
                                </a>
                                </li>
                                `;
            
            var listContent = $(`.list-content-${parent_list}`);
            $(listContent).find('.create-card').before(card_template);
            $('.create-card').trigger('reset');
            cardDraggable();
        }).fail(function(err){
            console.log('error');
        });
    });
}


function editCard(){
    $(document).on('click', '.card-title-description', function(e){
        e.preventDefault();
        $(this).hide();
        $('#updateCardForm').show();
        updateCard();
        mouseoutBoard();
    })
}

function updateCard(){
    $('#card-edit-form').on('submit', function(e){
        e.preventDefault();

        var title = $(this).find('input').val();
        var description = $('#card-description').data('title');
        console.log('card_title:', title, 'card_description: ', description);
        $.ajax({
            url: $(this).attr('action'),
            data: {card_title: title, card_description: description},
            method: 'POST'
        }).done(function(data){
            e.preventDefault();
            $('.card-title-description').show();
            $('header').find('.card-title-description').html(data.card);
            console.log(data.board, data.card);
            $.ajax({
                url: '/board/'+data.board,
                method: 'get'
            }).done(function(res){
                $('body').find('.card-body').find('h4').html(data.card);
                console.log('board'+data.board);
            })

            $('#updateCardForm').hide();
        });
    });
}

function addCardDescription(){
    $('#card-description').on('submit', function(e){
        e.preventDefault();
        var description = $(this).find('textarea').val();
        var title= $(this).data('title');
        console.log('card description', description, 'card: ', title);

        $.ajax({
            url: $(this).attr('action'),
            data: {card_title: title, card_description: description},
            method: 'POST'
        }).done(function(data){
            $('.card2').show();
            $('body').find('.card2').html(data.card_description);
            $('#add-card-description').hide();
            $('#save-button').hide();
        }).fail(function(err){
            console.log(err);
        });
    })
}

function createCardDescription(){
    $('.card').on('click', function(e){
        $('.card2').hide();
        console.log('KOKOKOKO');
        $('#add-card-description').show();
        $('#save-button').show();
        addCardDescription();
        mouseoutBoard();
    })
}

function cardDraggable(){
    $('.card-body').sortable({
        cancel: 'form'
    });

    $('li').draggable({
        connectToSortable: '.card-body'
    });

    $('.card-body').droppable({
        accepts: 'li', 
        revert: 'false',
        drop: function(event, ui){
            event.preventDefault();

            var list_id = $(this).prev().find('span').data('id');
            var card_id = $(ui.draggable).data("id");

            $.ajax({
                url: $(ui.draggable).find('a').attr('href'),
                method: 'POST',
                data: {blist: list_id, card: card_id}
            }).done(function(data){
                console.log(data);
            })
        }
    });
}

function editList(){
    $(document).on('click', '.list-span', function(){
        var editList = $(this).attr('contenteditable', 'true');

        $(editList).attr('focus');
        $(editList).css({"background-color": "white", "height": "21px", "padding-right":"2px"});
      
        $('.list-span').on('keypress', function(e){
            if(e.keyCode == '13'){
                e.preventDefault();
                var edit = $(this).text();
                var list_id = $(this).data('id');
                var list_con = $(`.list-content-${list_id}`);
                $(list_con).data('title', edit);
                
                var this_url = $('.list-span').next().attr('href');
                var update_list = $(list_con).data('title'); 
                var update_list_id = $(list_con).data('id');

                $.ajax({
                    url: this_url,
                    method: 'POST',
                    data: {list_data: update_list, list_id: update_list_id}
                }).done(function(data){
                    $(editList).blur();
                    $(editList).css({"background-color": "transparent"});
                }).fail(function(err){
                    console.log(err);
                }); 
            }
        });
    })

    $(document).mouseup(function(e){
        var con = $('.list-span');

        if(!con.is(e.target) && con.has(e.target).length === 0){
           $('.list-span').css({"background-color":"transparent"});
        }
    });
}


function archieveView(){
    $('#archive').click(function(){
        $('#modal').modal('show');        
    });

    $('#modal').on('shown.bs.modal', function () {       
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
        mouseoutBoard();
    });   
}

function updateBoard(){
    $('#board-edit-form').on('submit', function(e){
        e.preventDefault();

        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            method: 'POST'
        }).done(function(data){
            e.preventDefault();
            $('.board-title').show();
            $('header').find('.board-title').html(data.board)
            $('#edit-board').hide();
        });
    });
}

function mouseoutBoard(){
    $(document).mouseup(function(e){

        var con = $('#board-edit-form');
        var con2 = $('#card-edit-form');
        var con3 = $('#card-description');

        if(!con.is(e.target) && con.has(e.target).length === 0){
            $('.board-title').show();
            $('#edit-board').hide();
        }

        if(!con2.is(e.target) && con2.has(e.target).length === 0){
            $('.card-title-description').show();
            $('#updateCardForm').hide();
        }

        if(!con3.is(e.target) && con3.has(e.target).length === 0){
            $('.card2').show();
            $('#add-card-description').hide();
        }
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
            e.preventDefault();
            $('#modal-id').modal('hide');
            window.location.href = '/board/'+data.board;  
        }).fail(function(xhr, data){
            $('.error').show();
        });        
    });
}


function leaveBoard(){
    $('#leave-board').on('click', function(e){
        e.preventDefault();
        $.ajax({
            url: $(this).attr('href'),
            method: 'get'
        }).done(function(res){
            window.location.href = '/dashboard/';
        }).fail(function(err){
            console.log(err);
        });
    });
}

function archiveBoard(){
    $('#board-archive').on('click', function(e){
        e.preventDefault();

        $.ajax({
            url: $(this).attr('href'),
            method: 'get'
        }).done(function(res){
            window.location.href = '/dashboard/';
        }).fail(function(err){
            console.log(err);
        });
    });
}

function archiveList(){
    $(document).on('click', '.archive-list', function(e){
        var archive = $(this).data('id');

        $.ajax({
            url: '/list-archive/'+archive,
            method: 'get',
        }).done(function(res){
            $(this).parents('.card').remove();
        }).fail(function(err){
            console.log(err);
        });
    });
}

function archiveCard(){
    $('#archive-card').on('click', function(e){
        e.preventDefault();
        var archive = $(this).data('id');

        $.ajax({
            url: '/card-archive/'+archive,
            method: 'get'
        }).done(function(res){
            e.preventDefault();
            $('li').find('h4').remove();
            $('#modal-card').close();
        }).fail(function(err){
            console.log(err)
        });
    });
}

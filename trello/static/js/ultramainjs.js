'use strict'
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

            console.log(list_id, card_id);

            var tt = $(ui.draggable).find('a').attr('href');

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
    $('.list-span').on('click', function(){
        var editList = $(this).attr('contenteditable', 'true');
        $(editList).attr('focus');
        $('.list-span').on('keypress', function(e){
            if(e.keyCode == '13'){
                e.preventDefault();
                var edit = $(this).text();
                var list_id = $(this).data('id');
                var list_con = $(`.list-content-${list_id}`); //unique list id
                $(list_con).data('title', edit);
                var this_url = $('.list-span').next().attr('href');
                
                console.log('Edit', edit);
                console.log('List', list_id);
                console.log('Url', this_url);

                var update_list = $(list_con).data('title'); //updated value of list
                var update_list_id = $(list_con).data('id');
                console.log(update_list);


                $.ajax({
                    url: this_url,
                    method: 'POST',
                    data: {list_data: update_list, list_id: update_list_id}
                }).done(function(data){
                    console.log(data);
                    $(editList).blur();
                }).fail(function(err){
                    console.log(err);
                });
                
            }
        });
    })
}


    
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
        mouseoutBoard();
    });   
}

function mouseoutBoard(){
    $(document).mouseup(function(e){

        var con = $('#board-edit-form');
        var con2 = $('#card-edit-form');

        if(!con.is(e.target) && con.has(e.target).length === 0){
            $('.board-title').show();
            $('#edit-board').hide();
        }

        if(!con2.is(e.target) && con2.has(e.target).length === 0){
            $('.card-title-description').show();
            $('#updateCardForm').hide();
        }
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


function editCard(){
    $('.card-title-description').on('click', function(e){
        e.preventDefault();
        console.log('Edit Card');
        $(this).hide();
        $('#updateCardForm').show();
        updateCard();
        mouseoutBoard();
    })
}

function updateCard(){
    $('#card-edit-form').on('submit', function(e){
        console.log('Card Submit!');
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            method: 'POST'
        }).done(function(data){
            e.preventDefault();
            $('.card-title-description').show();
            $('header').find('.card-title-description').html(data.card)
            console.log(data)
            $('#updateCardForm').hide();
        });
    })
}



function createBoard() {
    $('#board-form').on('submit', function(e){
        console.log('Joho Boardsie KOOO');
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
            console.log("ffdfdf");
            $('.error').show();
        });        
    });
}

function createCard(){
    $('.create-card').on('submit', function(e){
        var gy = $(this).attr('action');
        var parent_list = $(this).parents('.card').data('id');
        console.log('PARENT', parent_list)
        console.log(gy);
        e.preventDefault();
        console.log('Create Card');
        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            method: 'POST'
        }).done(function(data){
            console.log(data.card);
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
        }).fail(function(err){
            console.log('error');
        });
    });
}

function leaveBoard(){
    $('#leave-board').on('click', function(e){
        console.log('Leave')
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
        console.log('Archive Boatd');
        $.ajax({
            url: $(this).attr('href'),
            method: 'get'
        }).done(function(res){
            console.log(res);
            window.location.href = '/dashboard/';
        }).fail(function(err){
            console.log(err);
        });
    });
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
            $(this).parents('.card').remove();
            
        }).fail(function(err){
            console.log(err);
        });
    });
}

function archiveCard(){
    $('#archive-card').on('click', function(e){
        console.log('CLOSE');
        e.preventDefault();
        var archive = $(this).data('id');
        console.log(archive);
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

function createCardDescription(){
    $('.card').on('click', function(e){
        $('.card2').hide();
        $('#add-card-description').show();
        console.log('Description');
        addCardDescription();
    })
}

function addCardDescription(){
    console.log('FUnc');
    $('#card-description').on('submit', function(e){
        console.log('Add Card Description');
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            method: 'POST'
        }).done(function(data){
            $('.card2').show();
            $('body').find('.card2').html(data.card_description);
            console.log(data.card_description);
            $('#add-card-description').hide();
        }).fail(function(err){
            console.log(err);
        });
    })
}


$(document).ready(function (){
    console.log('KAKAKA')
    archieveView();
    editBoard();
    editList();
    editCard();
    archiveBoard();
    archiveList();
    createCard();
    createCardDescription();
    cardDraggable();
    leaveBoard();

    $('#list-form').on('submit', function(e){
        console.log('CREATE LIST LISTer');
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            method: 'POST'
        }).done(function(data){
            console.log(data.id);
            var template = `
                        <div class="card p-1 ml-4 mt-5 list-content-${data.id}" data-id=${data.id}>
                        <div class="card-title pt-3 pb-0 d-flex justify-content-between">
                        <span class="list-span" value="${data.board_list}" contenteditable="true" data-title="${data.board_list}" data-id="${data.id}">${data.board_list}</span> 
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
                        
                        <form class="create-card mt-2" method="POST" draggable="false" action="/board/${data.id}/list/">
                            <input type="text" name="card_title" placeholder="+ Add Card">
                        </form>
                        </div>
                        </form>
                        </div>
                        </div>
                        `;  
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
        console.log('Boardsiesder KooKoo')
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


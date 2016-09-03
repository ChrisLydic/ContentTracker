function showNewItem() {
    $( '#itemForm' ).css( 'display', 'flex' );
    $( '#itemForm' ).each( function(){ this.scrollIntoView() } );
    $( '#id_name' ).val( '' );
    $( '#id_description' ).val( '' );
    $( '#id_name' ).focus();
}

function hideNewItem() {
    $( '#itemForm' ).css( 'display', 'none' );
}

function showDeleteList( listpk ) {
    var question = document.createElement( 'a' );
    question.innerHTML = 'Really delete?';
    question.style.margin = '1em 0.5em 1em 0';
    question.id = 'idQuestion';
    
    var linkYes = document.createElement( 'a' );
    linkYes.innerHTML = 'Yes';
    linkYes.href = '/lists/' + listpk + '/delete/';
    linkYes.style.margin = '1em 0.5em 1em 0';
    linkYes.id = 'idYes';
    
    var linkNo = document.createElement( 'a' );
    linkNo.innerHTML = 'No';
    linkNo.href = 'javascript:void(0);';
    linkNo.onclick = function () {
        hideDeleteList( listpk );
    };
    linkNo.id = 'idNo';
    
    var item = document.getElementById( 'links' );
    item.replaceChild( question, item.childNodes[5] );
    item.childNodes[5].insertAdjacentElement( 'afterEnd', linkNo );
    item.childNodes[5].insertAdjacentElement( 'afterEnd', linkYes );
}

function hideDeleteList( listpk ) {
    var linkDelete = document.createElement( 'a' );
    linkDelete.innerHTML = 'Delete List';
    linkDelete.href = 'javascript:void(0);';
    linkDelete.onclick = function () {
        showDeleteList( listpk );
    };
    
    var item = document.getElementById( 'links' );
    item.replaceChild( linkDelete, item.childNodes[5] );
    
    item.removeChild( document.getElementById( 'idYes' ) );
    item.removeChild( document.getElementById( 'idNo' ) );
}
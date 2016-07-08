// ajax for item editing, deletion, and re-ordering

$( document ).ready( function() {
    //
    // set up ajax to use django's csrf cookies
    // csrf cookie code is from https://docs.djangoproject.com/en/1.9/ref/csrf/
    //

    function getCookie( name ) {
        var cookieValue = null;

        if ( document.cookie && document.cookie != '' ) {
            var cookies = document.cookie.split( ';' );
            for ( var i = 0; i < cookies.length; i++ ) {
                var cookie = jQuery.trim( cookies[i] );
                // Does this cookie string begin with the name we want?
                if ( cookie.substring( 0, name.length + 1 ) == ( name + '=' ) ) {
                    cookieValue = decodeURIComponent( cookie.substring( name.length + 1 ) );
                    break;
                }
            }
        }

        return cookieValue;
    }

    var csrftoken = getCookie( 'csrftoken' );

    function csrfSafeMethod( method ) {
        // these HTTP methods do not require CSRF protection
        return ( /^(GET|HEAD|OPTIONS|TRACE)$/.test( method ) );
    }

    $.ajaxSetup( {
        beforeSend: function( xhr, settings ) {
            if ( !csrfSafeMethod( settings.type ) && !this.crossDomain ) {
                xhr.setRequestHeader( 'X-CSRFToken', csrftoken );
            }
        }
    } );

    //
    // ajax for the item buttons ( edit, delete, moveUp, moveDown )
    //

    var listpk = $( '.listWrapper' ).prop( 'id' );

    $( '[id^=itemOptions]' ).each( function () {

       	var itempk = this.id.slice( 'itemOptions'.length );

        $( this ).find( 'img:eq(0)' ).click( function () {
            var itemPrev = $( '#item' + itempk ).clone( withDataAndEvents=true );
            var item = $( '#item' + itempk );
            var itemForm = $( '#itemForm' ).clone();
            itemForm.css( 'display', 'flex');
            itemForm.prop( 'id','itemEditForm' + itempk );

            // put text from the item section into the form
            var inputs = itemForm.children().children()
            inputs.children( 'input[id=id_name]' ).val(
                item.children( '.itemHeader' ).children( 'h1' ).children( 'a' ).text().trim() );

            if ( inputs.children( 'input[id=id_description]' ).length ) {
                inputs.children( 'input[id=id_description]' ).val(
                    item.children( '.descWrapper' ).children( 'p' ).text().trim() );
            }

            if ( inputs.children( 'input[id=id_url]' ).length ) {
                inputs.children( 'input[id^=id_url]' ).val(
                    item.children( '.itemHeader' ).children( 'h1' ).children( 'a' ).prop( 'href' ) );
            }

            if ( inputs.children( 'input[id=id_cover]' ).length ) {
                inputs.children( 'input[id=id_cover]' ).val(
                    item.children( '.descWrapper' ).children( 'img' ).prop( 'src' ).trim() );
                
                inputs.children( 'input[id=id_description]' ).val(
                    item.children( '.descWrapper' ).children( 'div' ).children( 'p' ).text().trim() );
                
                inputs.children( 'input[id=id_authors]' ).val(
                    item.children( '.descWrapper' ).children( 'div' ).children( 'div' ).children( 'p' ).first().text().trim() );
                
                inputs.children( 'input[id=id_pageNumber]' ).val(
                    parseInt( $( '#page' + itempk ).text().trim() ) );
            }

            var buttons = itemForm.children().children( '.button' );
            var submit = buttons.children( 'input[type=submit]' );
            var exit = buttons.children( 'input[type=button]' );

            // get and submit form values with ajax when submit is clicked
            submit.val( 'Update' );
            submit.click( function () {
                var inputs = $( '#itemEditForm' + itempk ).children().children();
                var args = {
                    'name': inputs.children( 'input[id=id_name]' ).val(),
                    'description': inputs.children( 'input[id=id_description]' ).val(),
                    'url': inputs.children( 'input[id^=id_url]' ).val(),
                };

                $.ajax( {
                    type: 'POST',
                    url: '/lists/' + listpk + '/item/' + itempk + '/edit/',
                    contentType: 'application/json; charset=utf-8',
                    dataType: 'json',
                    data: JSON.stringify( args ),
                    success: function ( data ) {
                        if ( data.errors.length ) {
                            alert( data.errors.toString() );
                        } else {
                            itemPrev.children( '.itemHeader' ).children( 'h1' ).children( 'a' ).text( data['name'] );
                            itemPrev.children( '.itemHeader' ).children( 'h1' ).children( 'a' ).prop( 'href', data['url'] );
                            itemPrev.children( '.descWrapper' ).children( 'p' ).text( data['description'] );
                            
                            $( '#itemEditForm' + itempk ).replaceWith( itemPrev );
                        }
                    },
                } )

                // stop page from auto-reloading
                return false;
            } );

            // exit button will switch out form with old item section
            exit.prop( 'onclick', null ).off( 'click' );
            exit.click( function () {
                $( '#itemEditForm' + itempk ).replaceWith( itemPrev );
            } );
            
            $( '#item' + itempk ).replaceWith( itemForm );
        } );

        $( this ).find( 'img:eq(1)' ).click( function () {
            
            $.ajax( {
                type: 'POST',
                url: '/lists/' + listpk + '/item/' + itempk + '/delete/',
                success: function () {
                    $( '#item' + itempk ).remove();
                },
            } );

        } );
        
        $( this ).find( 'img:eq(2)' ).click( function () {
            
            $.ajax( {
                type: 'POST',
                url: '/lists/' + listpk + '/item/' + itempk + '/move/down/',
                success: function () {
                    var section1Id = '#item' + itempk;

                    if ( $( section1Id ).next().length ) {
                        var section2Id = '#' + $( section1Id ).next().prop( 'id' );
                        
                        var section1 = $( section1Id ).detach();
                        $( section1 ).insertAfter( section2Id );
                    }
                },
            } );

        } );
        
        $( this ).find( 'img:eq(3)' ).click( function () {
            
            $.ajax( {
                type: 'POST',
                url: '/lists/' + listpk + '/item/' + itempk + '/move/up/',
                success: function () {
                    var section1Id = '#item' + itempk;
                    
                    if ( $( section1Id ).prev( '[id!=itemForm]' ).length ) {
                        var section2Id = '#' + $( section1Id ).prev( '[id!=itemForm]' ).prop( 'id' );
                        
                        var section1 = $( section1Id ).detach();
                        $( section1 ).insertBefore( section2Id );
                    }
                },
            } );

        } );

    } );
} );
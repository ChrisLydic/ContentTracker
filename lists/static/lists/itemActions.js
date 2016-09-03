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
                    cookieValue = decodeURIComponent( cookie.substring(
                        name.length + 1 ) );
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

        // edit item button
        $( this ).find( 'img:eq(0)' ).click( function () {
            // save the item, it will either be used to recover itself
            //    or updated with new data and placed back into the html
            var itemPrev = $( '#item' + itempk ).clone( withDataAndEvents=true );
            // initial data will be taken from the item's html
            var item = $( '#item' + itempk );

            // copy the item form used to create new items
            //    and populate it with current item's data
            var itemForm = $( '#itemForm' ).clone();
            itemForm.css( 'display', 'flex');
            itemForm.prop( 'id','itemEditForm' + itempk );

            // put text from the item section into the form
            var inputs = itemForm.children().children()
            inputs.children( 'input[id=id_name]' ).val(
                item.children( '.itemHeader' ).children( 'h1' ).children( 'a' )
                    .text().trim() );

            if ( inputs.children( 'input[id=id_description]' ).length ) {
                inputs.children( 'input[id=id_description]' ).val(
                    item.children( '.descWrapper' ).children( 'p' ).text().trim() );
            }

            if ( inputs.children( 'input[id=id_url]' ).length ) {
                inputs.children( 'input[id^=id_url]' ).val(
                    item.children( '.itemHeader' ).children( 'h1' )
                        .children( 'a' ).prop( 'href' ) );
            }
            
            // get data from items of type: book, show, and movie
            if ( itemForm.children( 'form[id^=custom]' ).length ) {
                // show the correct form, hide the search form
                itemForm.children( 'form[id^=custom]' ).css( 'display', 'block' );
                itemForm.children( 'form[id^=search]' ).remove();

                // get data that is shared across the common types
                if ( inputs.children( 'input[id=id_cover]' ).length &&
                    item.children( '.descWrapper' ).children( 'img' ).length ) {

                    inputs.children( 'input[id=id_cover]' ).val(
                        item.children( '.descWrapper' ).children( 'img' )
                        .prop( 'src' ).trim() );
                }

                if ( inputs.children( 'input[id=id_description]' ).length ) {
                    inputs.children( 'input[id=id_description]' ).val(
                        item.children( '.descWrapper' ).children( 'div' )
                            .children( 'p:nth-child(2)' ).text().trim() );
                }

                // a zero value for units == false, they do not show up on the page
                var units = 0;
                if ( $( '#unit' + itempk ).length ) {
                	units = parseInt( $( '#unit' + itempk ).text().trim() );
                }

                // get item type
                var type = itemForm.children( 'form[id^=custom]' ).prop( 'id' )
                    .slice( 'custom'.length );
                
                // get data specific to item type
                if ( type === 'Book' ) {

                    if ( inputs.children( 'input[id=id_authors]' ).length ) {
                        inputs.children( 'input[id=id_authors]' ).val(
                            item.children( '.descWrapper' ).children( 'div' )
                                .children( 'div' ).children( 'p' ).first()
                                .text().trim() );
                    }

                    if ( inputs.children( 'input[id=id_pageNumber]' ).length ) {
                        inputs.children( 'input[id=id_pageNumber]' ).val( units );
                    }
                    
                } else if ( type === 'Show' ) {

                    if ( inputs.children( 'input[id=id_writers]' ).length ) {
                        inputs.children( 'input[id=id_writers]' ).val(
                            item.children( '.descWrapper' ).children( 'div' )
                                .children( 'div' ).children( 'p' ).first()
                                .text().trim() );
                    }

                    if ( inputs.children( 'input[id=id_seasons]' ).length ) {
                        inputs.children( 'input[id=id_seasons]' ).val( units );
                    }

                } else if ( type === 'Movie' ) {

                    if ( inputs.children( 'input[id=id_directors]' ).length ) {
                        inputs.children( 'input[id=id_directors]' ).val(
                            item.children( '.descWrapper' ).children( 'div' )
                                .children( 'div' ).children( 'p' ).first()
                                .text().trim() );
                    }

                    if ( inputs.children( 'input[id=id_runtime]' ).length ) {
                        inputs.children( 'input[id=id_runtime]' ).val( units );
                    }
                }
            }

            // modify form buttons
            var buttons = itemForm.children().children( '.button' );
            var submit = buttons.children( 'input[type=submit]' );
            var exit = buttons.children( 'input[type=button]' );
            // remove search button if applicable
            buttons.children( 'input[id=searchButton]' ).remove();

            // get and submit form values with ajax when submit is clicked
            submit.val( 'Update' );
            submit.click( function () {
                var inputs = $( '#itemEditForm' + itempk ).children().children();
                var args = {
                    'name': inputs.children( 'input[id=id_name]' ).val(),
                    'description': inputs.children( 'input[id=id_description]' ).val(),
                    'url': inputs.children( 'input[id^=id_url]' ).val(),
                    'cover': inputs.children( 'input[id=id_cover]' ).val(),
                    'authors': inputs.children( 'input[id=id_authors]' ).val(),
                    'pageNumber': inputs.children( 'input[id=id_pageNumber]' ).val(),
                    'writers': inputs.children( 'input[id=id_writers]' ).val(),
                    'seasons': inputs.children( 'input[id=id_seasons]' ).val(),
                    'directors': inputs.children( 'input[id=id_directors]' ).val(),
                    'runtime': inputs.children( 'input[id=id_runtime]' ).val(),
                };

                $.ajax( {
                    type: 'POST',
                    url: '/lists/' + listpk + '/item/' + itempk + '/edit/',
                    contentType: 'application/json; charset=utf-8',
                    dataType: 'json',
                    data: JSON.stringify( args ),
                    success: function ( data ) {
                        if ( data.errors.length ) {
                            // these are form validation errors, not ajax errors
                            alert( data.errors.toString() );
                        } else {
                            // now the form will be updated and inserted back
                            //    into the page
                            itemPrev.children( '.itemHeader' ).children( 'h1' )
                                .children( 'a' ).text( data['name'] );
                            itemPrev.children( '.itemHeader' ).children( 'h1' )
                                .children( 'a' ).prop( 'href', data['url'] );
                            itemPrev.children( '.descWrapper' ).children( 'p' )
                                .text( data['description'] );
                            itemPrev.children( '.descWrapper' ).children( 'div' )
                                .children( 'p:nth-child(2)' ).text( data['description'] );

                            if ( data['authors'] ) {
                                itemPrev.children( '.descWrapper' ).children( 'div' )
                                    .children( 'div' ).children( 'p' ).first()
                                    .text( data['authors'] );
                                
                                // if the new pageNumber is not 0 and the previous
                                //    was not 0, insert new number.
                                // if the new pageNumber is 0 and the previous was
                                //    not 0, remove the pageNumber html
                                // if the new pageNumber is not 0 and the previous
                                //    was 0, add the html back in
                                if ( itemPrev.children( '.descWrapper' ).children( 'div' )
                                    .children( 'div' ).children( 'p' )
                                    .children( 'span' ).length ) {

                                    itemPrev.children( '.descWrapper' ).children( 'div' )
                                        .children( 'div' ).children( 'p' )
                                        .children( 'span' ).text( data['pageNumber'] );
                                    
                                    if ( data['pageNumber'] === 0 ) {
                                        itemPrev.children( '.descWrapper' )
                                            .children( 'div' ).children( 'div' )
                                            .children( 'p:nth-child(2)' ).remove();
                                    }

                                } else if ( data['pageNumber'] !== 0 ) {
                                     itemPrev.children( '.descWrapper' ).children( 'div' )
                                        .children( 'div' ).append( '<p><span id="unit' +
                                        data['itempk'] + '"> ' + data['pageNumber'] +
                                        '</span> pages</p>' );
                                }

                            } else if ( data['writers'] ) {
                                itemPrev.children( '.descWrapper' ).children( 'div' )
                                    .children( 'div' ).children( 'p' ).first()
                                    .text( data['writers'] );
                                
                                if ( itemPrev.children( '.descWrapper' ).children( 'div' )
                                    .children( 'div' ).children( 'p' )
                                    .children( 'span' ).length ) {

                                    itemPrev.children( '.descWrapper' ).children( 'div' )
                                        .children( 'div' ).children( 'p' )
                                        .children( 'span' ).text( data['seasons'] );
                                    
                                    if ( data['seasons'] === 0 ) {
                                        itemPrev.children( '.descWrapper' )
                                            .children( 'div' ).children( 'div' )
                                            .children( 'p:nth-child(2)' ).remove();
                                    }

                                } else if ( data['seasons'] === 1 ) {
                                     itemPrev.children( '.descWrapper' ).children( 'div' )
                                        .children( 'div' ).append( '<p><span id="unit' +
                                        data['itempk'] + '"> ' + data['seasons'] +
                                        '</span> season</p>' );

                                } else if ( data['seasons'] > 1 ) {
                                     itemPrev.children( '.descWrapper' ).children( 'div' )
                                        .children( 'div' ).append( '<p><span id="unit' +
                                        data['itempk'] + '"> ' + data['seasons'] +
                                        '</span> seasons</p>' );
                                }

                            } else if ( data['directors'] ) {
                                itemPrev.children( '.descWrapper' ).children( 'div' )
                                    .children( 'div' ).children( 'p' ).first()
                                    .text( data['directors'] );
                                
                                if ( itemPrev.children( '.descWrapper' ).children( 'div' )
                                    .children( 'div' ).children( 'p' )
                                    .children( 'span' ).length ) {

                                    itemPrev.children( '.descWrapper' ).children( 'div' )
                                        .children( 'div' ).children( 'p' )
                                        .children( 'span' ).text( data['runtime'] );
                                    
                                    if ( data['runtime'] === 0 ) {
                                        itemPrev.children( '.descWrapper' )
                                            .children( 'div' ).children( 'div' )
                                            .children( 'p:nth-child(2)' ).remove();
                                    }

                                } else if ( data['runtime'] !== 0 ) {
                                     itemPrev.children( '.descWrapper' ).children( 'div' )
                                        .children( 'div' ).append( '<p><span id="unit' +
                                        data['itempk'] + '"> ' + data['runtime'] +
                                        '</span> minutes</p>' );
                                }
                            }

                            if ( data['cover'] ) {
                                itemPrev.children( '.descWrapper' ).children( 'img' )
                                    .prop( 'src', data['cover'] );
                                
                                // the html may need to be modified depending on
                                //    previous and new state of the cover image
                                if ( data['cover'] === 'none' ) {
                                    itemPrev.children( '.descWrapper' ).children( 'img' )
                                        .remove();
                                } else if ( itemPrev.children( '.descWrapper' )
                                    .children( 'img' ).length === 0 ) {
                                    
                                    itemPrev.children( '.descWrapper' )
                                        .prepend( '<img src="' + data['cover'] + '">' );
                                }
                            }
                            
                            // insert modified item into the page
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
            
            // show the item form where the item was located
            $( '#item' + itempk ).replaceWith( itemForm );
        } );

        // delete item button
        $( this ).find( 'img:eq(1)' ).click( function () {
            
            $.ajax( {
                type: 'POST',
                url: '/lists/' + listpk + '/item/' + itempk + '/delete/',
                success: function () {
                    $( '#item' + itempk ).remove();
                },
            } );

        } );
        
        // move item down button
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
        
        // move item up button
        $( this ).find( 'img:eq(3)' ).click( function () {
            
            $.ajax( {
                type: 'POST',
                url: '/lists/' + listpk + '/item/' + itempk + '/move/up/',
                success: function () {
                    var section1Id = '#item' + itempk;
                    
                    if ( $( section1Id ).prev( '[id!=itemForm]' ).length ) {
                        var section2Id = '#' + $( section1Id )
                            .prev( '[id!=itemForm]' ).prop( 'id' );
                        
                        var section1 = $( section1Id ).detach();
                        $( section1 ).insertBefore( section2Id );
                    }
                },
            } );
        } );
    } );
} );
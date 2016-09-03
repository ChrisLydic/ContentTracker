// item editing, deletion, and re-ordering, modified for the sample lists
// this code does nothing permanent

$( document ).ready( function() {

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
            // remove search button if applicable
            buttons.children( 'input[id=searchButton]' ).remove();
            var submit = buttons.children( 'input[type=button]:nth-child(1)' );
            var exit = buttons.children( 'input[type=button]:nth-child(2)' );

            // get and submit form values with ajax when submit is clicked
            submit.val( 'Update' );

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
            $( '#item' + itempk ).remove();
        } );
        
        // move item down button
        $( this ).find( 'img:eq(2)' ).click( function () {
            var section1Id = '#item' + itempk;

            if ( $( section1Id ).next().length ) {
                var section2Id = '#' + $( section1Id ).next().prop( 'id' );

                var section1 = $( section1Id ).detach();
                $( section1 ).insertAfter( section2Id );
            }
        } );
        
        // move item up button
        $( this ).find( 'img:eq(3)' ).click( function () {
            var section1Id = '#item' + itempk;

            if ( $( section1Id ).prev( '[id!=itemForm]' ).length ) {
                var section2Id = '#' + $( section1Id )
                    .prev( '[id!=itemForm]' ).prop( 'id' );

                var section1 = $( section1Id ).detach();
                $( section1 ).insertBefore( section2Id );
            }
        } );
    } );
} );
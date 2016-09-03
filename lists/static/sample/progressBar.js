$( document ).ready( function() {
    //
    // fake progress bar setup
    //

    $( '[id^=barCont]' ).each( function () {

       	var itempk = this.id.slice( 'barCont'.length );
        var bar = '#bar' + itempk;
        var barOffset = '#barOffset' + itempk;

        $( this ).mousemove( function ( event ) {
            if (event.which == 1) {
                var percent = ( event.pageX - $( this ).offset().left - 14 ) / ( $( this ).outerWidth() - 28 );
                if ( percent > 1 ) { percent = 1; }
                else if ( percent < 0 ) { percent = 0; }
                $( bar ).css( 'flex', String( percent ) + ' 0 auto' );
                $( barOffset ).css( 'flex', String( 1 - percent ) + ' 0 auto' );
            }
        } );

        $( this ).mousedown( function () {
            var percent = ( event.pageX - $( this ).offset().left - 14 ) / ( $( this ).outerWidth() - 28 );
            if ( percent > 1 ) { percent = 1; }
            else if ( percent < 0 ) { percent = 0; }
            $( bar ).css( 'flex', String( percent ) + ' 0 auto' );
            $( barOffset ).css( 'flex', String( 1 - percent ) + ' 0 auto' );
        } );

        // find integer value of percent stored in flex style
        function getPercent( barId ) {
            var percent = $( barId ).css( 'flex' ).split( ' ' )[0];
            return Math.round( percent * 100 );
        }

        $( this ).mouseup( function () {
            var prog = getPercent( bar );

            if ( prog >= 100 ) {
                $( '#barCont' + itempk ).css('background-color','#DCE8E8');
                $( '#item' + itempk ).css('opacity','0.4');
            } else {
                $( '#barCont' + itempk ).css('background-color','#4883A3');
                $( '#item' + itempk ).css('opacity','1');
            }
        } );

        $( this ).mouseleave( function () {
            if (event.which == 1) {
                var prog = getPercent( bar );

                if ( prog >= 100 ) {
                    $( '#barCont' + itempk ).css('background-color','#DCE8E8');
                    $( '#item' + itempk ).css('opacity','0.4');
                } else {
                    $( '#barCont' + itempk ).css('background-color','#4883A3');
                    $( '#item' + itempk ).css('opacity','1');
                }
            }
        } );

    } );
} );
function search () {
    var type = $( 'form[id^=search]' ).prop( 'id' ).slice( 'search'.length );

    $( '#mCSB_3_container' ).empty();
    $( '#searchWrapper' ).css( 'display', 'block' );

    if ( type === 'Book' ) {
        searchBooks();
    }
}

function searchBooks () {
    var dataStr = $( '#searchData' ).prop( 'value' );
    dataStr = dataStr.replace( / /g, '+' );

    $.ajax( {
        type: 'GET',
        url: 'https://openlibrary.org/search.json?q=' + dataStr,
        dataType: "json",
        success: function ( data ) {
            
            if ( data.num_found > 0 ) {
                var dataList = data.docs;
                
                for ( var i = 0; ( i < dataList.length ) && ( i < 200 ); i++ ) {
                    var itemNode = $( '<div class="searchItem"></div>' );

                    itemNode.click( { olidList: dataList[i].edition_key }, searchBookOLIDs );

                    if ( dataList[i].cover_i ) {
                        itemNode.append( '<img src="https://covers.openlibrary.org/b/id/' + dataList[i].cover_i + '-S.jpg">' );
                    }

                    itemNode.append( '<div><h1></h1><p></p></div>' );

                    if ( dataList[i].title_suggest ) {
                        itemNode.children( 'div' ).children( 'h1' )
                            .append( dataList[i].title_suggest );
                    }

                    if ( dataList[i].author_name ) {
                        itemNode.children( 'div' ).children( 'h1' )
                            .append( ', by ' + dataList[i].author_name.join( ', ' ) );
                    }

                    itemNode.children( 'div' ).children( 'p' )
                        .append( dataList[i].edition_key.length + ' editions' );

                    $( '#mCSB_3_container' ).append(itemNode);
                }
            } else {
                var itemNode = $( '<div class="searchItem"><div><h1></h1></div></div>' );
                itemNode.children( 'div' ).children( 'h1' ).append( 'No results found' );
                $( '#mCSB_3_container' ).append(itemNode);
            }
        },
    } );
}

function searchBookOLIDs ( event ) {
    var olidList = event.data.olidList;

    $( '#mCSB_3_container' ).empty();

    for ( var i = 0; i < olidList.length; i++ ) {
        var olid = olidList[i];
        
        $.ajax( {
            type: 'GET',
            url: 'https://openlibrary.org/api/books?bibkeys=OLID:' +
                olid + '&jscmd=details&format=jsonp',
            dataType: "jsonp",
            success: function ( data ) {
                var priority = false;
                var bookData = data[ Object.keys(data)[0] ];
                
                var customData = {
                    name: 'none',
                    description: '',
                    cover: 'none',
                    pageNumber: bookData.details.number_of_pages || 0,
                    authors: 'Anonymous',
                    olid: olid,
                };

                if ( bookData.details.authors ) {
                    customData.authors = bookData.details.authors[0].name;

                    for ( var j = 1; j < bookData.details.authors.length; j++ ) {
                        customData.authors += ', ' + bookData.details.authors[j].name;
                    }
                }

                var itemNode = $( '<div class="searchItem"></div>' );
                
                if ( bookData.thumbnail_url ) {
                    itemNode.append( '<img src="' + bookData.thumbnail_url + '">' );
                    priority = true;
                    customData.cover = bookData.thumbnail_url;
                    console.log(customData.cover);
                }

                itemNode.append( '<div><h1></h1><p></p></div>' );

                if ( bookData.details.title ) {
                    itemNode.children( 'div' ).children( 'h1' )
                        .append( bookData.details.title +
                        ', by ' + customData.authors );
                    
                    customData.name = bookData.details.title;
                }

                if ( bookData.details.isbn_13 && bookData.details.isbn_10 ) {
                    var isbn = '(ISBN: ' + bookData.details.isbn_13 +
                        ', ' + bookData.details.isbn_10 + ') ';

                    itemNode.children( 'div' ).children( 'p' )
                        .append( isbn );
                            
                    customData.description = isbn;

                } else if ( bookData.details.isbn_13 ) {
                    var isbn = '(ISBN: ' + bookData.details.isbn_13 + ') ';

                    itemNode.children( 'div' ).children( 'p' )
                        .append( isbn );
                        
                    customData.description = isbn;

                } else if ( bookData.details.isbn_10 ) {
                    var isbn = '(ISBN: ' + bookData.details.isbn_10 + ') ';

                    itemNode.children( 'div' ).children( 'p' )
                        .append( isbn );
                    
                    customData.description = isbn;
                }

                if ( bookData.details.description ) {
                    itemNode.children( 'div' ).children( 'p' )
                        .append( bookData.details.description );
                    
                    customData.description += bookData.details.description;
                }

                itemNode.click( { bookData: customData }, createBookItem );

                if ( priority ) {
                    $( '#mCSB_3_container' ).prepend(itemNode);
                } else {
                    $( '#mCSB_3_container' ).append(itemNode);
                }
            },
        } );
    }
}

function createBookItem ( event ) {
    bookData = event.data.bookData;
    $( '#id_name' ).prop( 'value', bookData.name );
    $( '#id_description' ).prop( 'value', bookData.description );
    $( '#id_cover' ).prop( 'value', bookData.cover.slice( 0, bookData.cover.length - 5) + 'M.jpg' );
    $( '#id_pageNumber' ).prop( 'value', bookData.pageNumber );
    $( '#id_authors' ).prop( 'value', bookData.authors );
    $( '#id_olid' ).prop( 'value', bookData.olid );

    document.forms[ 'bookForm' ].submit();
}

function showCustom () {
    $( '#mCSB_3_container' ).empty();
    $( '#searchWrapper' ).css( 'display', 'none' );

    $( 'form[id^=search]' ).css( 'display', 'none' );
    $( 'form[id^=custom]' ).css( 'display', 'block' );
}

function showSearch () {
    $( 'form[id^=search]' ).css( 'display', 'block' );
    $( 'form[id^=custom]' ).css( 'display', 'none' );
}
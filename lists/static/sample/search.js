function search () {
    var type = $( 'form[id^=search]' ).prop( 'id' ).slice( 'search'.length );

    $( '#mCSB_3_container' ).empty();
    $( '#searchWrapper' ).css( 'display', 'block' );

    if ( type === 'Book' ) {
        searchBooks();
    } else if ( type === 'Show' ) {
        searchVideos( 'series' );
    } else if ( type === 'Movie' ) {
        searchVideos( 'movie' );
    } 
}

// Search funtionality for books
// Uses OpenLibrary API, openlibrary.org/developers/api
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

                    itemNode.click( { olidList: dataList[i].edition_key },
                        searchBookOLIDs );

                    if ( dataList[i].cover_i ) {
                        var imgStr = '<img src="https://covers.openlibrary.org/b/id/';
                        itemNode.append( imgStr + dataList[i].cover_i + '-S.jpg">' );
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

                    if ( dataList[i].edition_key.length > 1 ) {
                        itemNode.children( 'div' ).children( 'p' )
                            .append( dataList[i].edition_key.length +
                                ' editions. Click to view.' );
                    } else {
                        itemNode.children( 'div' ).children( 'p' )
                            .append( dataList[i].edition_key.length +
                                ' edition. Click to view.' );
                    }

                    $( '#mCSB_3_container' ).append(itemNode);
                }
            } else {
                var itemNode = $( '<h1 style="font-size:1em;">No results found</h1>' );
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
    alert( 'This functionality is not available for sample content' );
}

// Search functionality for tv and movies
// Uses OMDb API, omdbapi.com
function searchVideos( type ) {
    var dataStr = $( '#searchData' ).prop( 'value' );
    dataStr = dataStr.replace( / /g, '+' );

    event = { data: {
        type: type,
        dataStr: dataStr,
        pageNumber: 1,
    } }
    searchVideosPage( event );
}

function searchVideosPage( event ) {
    var type = event.data.type;
    var dataStr = event.data.dataStr;
    var pageNumber = event.data.pageNumber;
    var urlArgs = dataStr + '&type=' + type + '&r=json' + '&page=' + pageNumber;

    $( '#pageLink' ).remove();

    $.ajax( {
        type: 'GET',
        url: 'http://www.omdbapi.com/?s=' + urlArgs,
        dataType: "json",
        success: function ( data ) {

            if ( data.Response === "True" ) {
                var dataList = data.Search;

                for ( var i = 0; i < dataList.length; i++ ) {
                    var itemNode = $( '<div class="searchItem"></div>' );

                    itemNode.click( { key: dataList[i].imdbID, type: type },
                        createVideoItem );

                    if ( dataList[i].Poster !== 'N/A' ) {
                        itemNode.append( '<img src="' + dataList[i].Poster + '">' );
                    }

                    itemNode.append( '<div><h1></h1></div>' );

                    if ( dataList[i].Title ) {
                        itemNode.children( 'div' ).children( 'h1' )
                            .append( dataList[i].Title );
                    }

                    if ( dataList[i].Year ) {
                        itemNode.children( 'div' ).children( 'h1' )
                            .append( ' (' + dataList[i].Year + ')' );
                    }

                    $( '#mCSB_3_container' ).append(itemNode);
                }

                var pageNode = $( '<div id="pageLink" class="searchItem">' +
                    'More Results</div>' );
                pageNode.click( {
                    type: type,
                    dataStr: dataStr,
                    pageNumber: pageNumber + 1,
                }, searchVideosPage );
                
                $( '#mCSB_3_container' ).append( pageNode );

            } else {
                var itemNode = $( '<h1 style="font-size:1em;">No results found</h1>' );
                $( '#mCSB_3_container' ).append(itemNode);
            }
        },
    } );
}

function createVideoItem ( event ) {
    alert(  'This functionality is not available for sample content' );
}

// Functions for buttons in search html
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
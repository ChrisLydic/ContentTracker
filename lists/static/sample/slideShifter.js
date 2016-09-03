var slideShifter = {
    
    // list of css selectors for the slides
    slides: [],
    
    slideNumber: 0,
    
    curSlide: 0,
    
    transitions: [],
    
    // time between slides in milliseconds
    interval: 10000,
    
    run: function ( args ) {
        this.parseArgs( args );

        for ( var i = 0; i < this.slideNumber; i++ ) {
            this.slides[i] = "div[id='s" + i + "']";
        }
        
        var scope = this;
        
        setInterval( function(){ scope.change(); }, this.interval );
    },
    
    change: function () {
        if ( this.curSlide === this.slides.length - 1 ) {

            $( this.slides[this.curSlide] )
                .css( 'z-index', this.slides.length );
            
            for ( var i = 0; i < this.curSlide; i++ ){
                $( this.slides[i] ).removeClass( this.transitions[i] );
            }

            $( this.slides[this.curSlide] )
                .addClass( this.transitions[this.curSlide] );

            this.curSlide = 0;
            
        } else if ( this.curSlide === 0 ) {
            
            $( this.slides[this.slides.length - 1] )
                .removeClass( this.transitions[this.slides.length - 1] );
            $( this.slides[this.slides.length - 1] )
                .css( 'z-index', this.curSlide );

            $( this.slides[this.curSlide] )
                .addClass( this.transitions[this.curSlide] );
            this.curSlide++;
            
        } else {
            
            $( this.slides[this.curSlide] )
                .addClass( this.transitions[this.curSlide] );
            this.curSlide++;
            
        }
    },
    
    parseArgs: function ( args ) {
        this.interval = args.interval || 10;
        
        this.interval *= 1000;
        
        this.slideNumber = $( '#slideCont > div' ).length;
        
        for ( var i = 0; i < this.slideNumber; i++ ) {
            this.transitions.push( args.transition );
        }

        if ( args.slides ) {
            for ( var i = 0; i < args.slides.length; i++ ) {
                if ( args.slides[i].transition ) {
                    this.transitions[i] = args.slides[i].transition;
                }
            }
        }
    },
};
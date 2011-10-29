jQuery.fn.urlize = function( base ) {
	var x = this.html();
	list = x.match( /\b(http:\/\/|www\.|http:\/\/www\.)[^ <>]{2,100}\b/g );
	if ( list ) {
		for ( i = 0; i < list.length; i++ ) {
		    x = x.replace( list[i], "<a href='" + list[i] + "'>"+ list[i] + "</a>" );
		}
		this.html(x);
	}
};

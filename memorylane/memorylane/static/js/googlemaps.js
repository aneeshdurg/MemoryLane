var styles = [{"featureType":"all","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"administrative","elementType":"all","stylers":[{"visibility":"off"},{"color":"#efebe2"}]},{"featureType":"landscape","elementType":"all","stylers":[{"color":"#efebe2"}]},{"featureType":"poi","elementType":"all","stylers":[{"color":"#efebe2"}]},{"featureType":"poi.attraction","elementType":"all","stylers":[{"color":"#efebe2"}]},{"featureType":"poi.business","elementType":"all","stylers":[{"color":"#efebe2"}]},{"featureType":"poi.government","elementType":"all","stylers":[{"color":"#dfdcd5"}]},{"featureType":"poi.medical","elementType":"all","stylers":[{"color":"#dfdcd5"}]},{"featureType":"poi.park","elementType":"all","stylers":[{"color":"#bad294"}]},{"featureType":"poi.place_of_worship","elementType":"all","stylers":[{"color":"#efebe2"}]},{"featureType":"poi.school","elementType":"all","stylers":[{"color":"#efebe2"}]},{"featureType":"poi.sports_complex","elementType":"all","stylers":[{"color":"#efebe2"}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"visibility":"off"}]},{"featureType":"road.arterial","elementType":"geometry.fill","stylers":[{"color":"#ffffff"}]},{"featureType":"road.arterial","elementType":"geometry.stroke","stylers":[{"visibility":"off"}]},{"featureType":"road.local","elementType":"geometry.fill","stylers":[{"color":"#fbfbfb"}]},{"featureType":"road.local","elementType":"geometry.stroke","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#a5d7e0"}]}];

function get_static_style(styles) {
    var result = [];
    styles.forEach(function(v, i, a){
        var style='';
        if( v.stylers ) { // only if there is a styler object
            if (v.stylers.length > 0) { // Needs to have a style rule to be valid.
                style += (v.hasOwnProperty('featureType') ? 'feature:' + v.featureType : 'feature:all') + '|';
                style += (v.hasOwnProperty('elementType') ? 'element:' + v.elementType : 'element:all') + '|';
                v.stylers.forEach(function(val, i, a){
                    var propertyname = Object.keys(val)[0];
                    var propertyval = val[propertyname].toString().replace('#', '0x');
                    style += propertyname + ':' + propertyval + '|';
                });
            }
        }
        result.push('style='+encodeURIComponent(style));
    });
    
    return result.join('&');
}
$(function() {
	$('.map').each(function() {
	  	var url = $(this).css("background-image");
        // Chrome automatically injects a " at the end of a url in a background-image
        // value. We compensate by checking if that extra " was injected or not, and
        // if not, then we add one in
        if (url.charAt(url.length-2) !== '"') {
            var revisedurl = url.substring(0,4) + '"' + url.substring(4, url.length - 1) + '&' + get_static_style(styles) + '")';
        }
        else {
            var revisedurl = url.substring(0, url.length - 2) + '&' + get_static_style(styles) + '")';
        }
        if (revisedurl.charAt(5) === '"') {
            revisedurl = revisedurl.substring(0,5) + revisedurl.substring(6,revisedurl.length);
        }
		$(this).css("background-image", revisedurl);
	});
});
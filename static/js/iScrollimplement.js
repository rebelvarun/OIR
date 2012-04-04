/*This javascript file initializes iScroll objects (using iscroll.js) 
	for each wrapper styles.
*/
function loaded() {

	/*For Vertical Scroller*/
	Vscroll = new iScroll('Vwrapper', {
		onBeforeScrollMove: function (e) { 
			e.preventDefault(); 
			e.stopPropagation();
			console.warn("e: ",e );
		}
	});
	
    var url = 'http://ec2-23-20-45-79.compute-1.amazonaws.com/museum/podcast/1/';
    makePodcastRequest(url);
    
}
function makePodcastRequest(query_url, parse_xml){
    
       $.ajax({
            url: query_url,
            dataType: "xml",
            success: function(xml){     
                parse_podcast(xml);
               
            }
       });
    
}

function parse_podcast(xml){
    var number_of_scrolls=0;
    
    $('category', xml).each(function (i) {
        number_of_scrolls++;
        var category_name = $(this).attr("name");
        var element = '';
        element = '<div class="caption"><a>'+ category_name + '</a></div>';
        element+= '<div class="Hwrapper" id="Hwrapper'+i+'"><div class="scroller">';
        
        $('museum_item',this).each(function(i){
            var image = $(this).find("image").attr("src");
            var caption = $(this).find("caption").text();
            var podcast = $(this).find("podcast").text();
            element += '<div class="wrapper" onclick="changeBorder(this)">';
            element += '<img src="'+ image +'"></img><div class="description"><div class="description_content">'+caption+'</div></div></div>';
                        
        });
        element += '</div></div>';
        $('#podcast').append($(element));    
    });
    
    var i=0;
    for(i=0;i<number_of_scrolls;i++)
    {
            var scroll_name = 'Hscroll' + i;
            var wrapper_name = 'Hwrapper' + i;
        	scroll_name = new iScroll(wrapper_name, {
            onBeforeScrollMove: function (e) { 
                e.preventDefault(); 
                e.stopPropagation();
                console.warn("e: ",e );
            }
	});
    
    }
    console.log(element);
    

}   
document.addEventListener('touchmove', function (e) { e.preventDefault(); }, false);
document.addEventListener('DOMContentLoaded', loaded, false);

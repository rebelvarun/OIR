$(function() {

    var button = $('.button');
    var menu = $('.menu');
    
    
    button.toggle(function(e) {
        e.preventDefault();
        menu.css({display: 'block'});
        $('.ar', this).html('&#9650;').css({top: '3px'});
        $(this).addClass('active');
    },function() {
        menu.css({display: 'none'});
        $('.ar', this).html('&#9660;').css({top: '5px'});
        $(this).removeClass('active');
    });
    
    
    $('.menu ul li a').click(function(e){
        menu.css({display: 'none'});
        $('.ar', this).html('&#9660;').css({top: '5px'});
        $(this).removeClass('active');
        var selected_text = $(this).html();
        $('.button .txt').html(selected_text);
    });
    
        
});
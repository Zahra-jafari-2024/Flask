jQuery(document).ready(function($){'use strict';if($(".notification-list").length){$('.notification-list').slimScroll({height:'250px'});}
if($(".menu-list").length){$('.menu-list').slimScroll({});}
if($(".sidebar-nav-fixed a").length){$('.sidebar-nav-fixed a').click(function(event){if(location.pathname.replace(/^\//,'')==this.pathname.replace(/^\//,'')&&location.hostname==this.hostname){var target=$(this.hash);target=target.length?target:$('[name='+this.hash.slice(1)+']');if(target.length){event.preventDefault();$('html, body').animate({scrollTop:target.offset().top-90},1000,function(){var $target=$(target);$target.focus();if($target.is(":focus")){return false;}else{$target.attr('tabindex','-1');$target.focus();};});}};$('.sidebar-nav-fixed a').each(function(){$(this).removeClass('active');})
$(this).addClass('active');});}
if($('[data-toggle="tooltip"]').length){$('[data-toggle="tooltip"]').tooltip()}
if($('[data-toggle="popover"]').length){$('[data-toggle="popover"]').popover()}
if($('.chat-list').length){$('.chat-list').slimScroll({color:'false',width:'100%'});}});
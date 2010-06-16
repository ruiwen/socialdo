
// Initialise the global 'sodo' namespace/object
var sodo = (typeof(sodo) == 'undefined')?{}:sodo;
sodo.user = (typeof(sodo.user) == 'undefined')?{}:sodo.user;
sodo.list = (typeof(sodo.list) == 'undefined')?{}:sodo.list;
sodo.item = (typeof(sodo.item) == 'undefined')?{}:sodo.item;


/** Item bindings **/

// Takes two elements, usually the additional bars under an Item display, and toggles them
sodo.item.flip_extra = function(desired, other) {
	
	if($(other).css('display') == 'block') {
		$(other).slideUp(function() {
			$(desired).slideDown();
		})
	}
	else {
		$(desired).slideDown();
	}		
}


// Bind the appearance of the 'assign' and 'info' links for each Item
$('.item, .item-desc').live('mouseenter mouseleave', function(event){
	if(event.type == 'mouseover') {
		if($(event.target).is('.item')) {
			$(event.target).find('.item-buttons').css('display', 'inline-block');
		}
		else if($(event.target).is('.item-desc')) {
			$(event.target).siblings('.item-buttons').css('display', 'inline-block');
		}
	}
	else if(event.type == 'mouseout') {
		if($(event.target).is('.item')) {
			$(event.target).find('.item-buttons').css('display', 'none');
		}
		else if($(event.target).is('.item-desc')){
			$(event.target).siblings('.item-buttons').css('display', 'none');
		}
	}
})


// Events for the toggling of the more info Item bar
$('.item-more-info').live('click', function(event){

	more_info_block = $(event.target).parent().siblings('.item-info');
	assign_block = $(event.target).parent().siblings('.item-assign');
	
	sodo.item.flip_extra(more_info_block, assign_block);
})


// Events for the toggling of the assign Item bar
$('.item-reassign').live('click', function(event){

	more_info_block = $(event.target).parent().siblings('.item-info');
	assign_block = $(event.target).parent().siblings('.item-assign');

	sodo.item.flip_extra(assign_block, more_info_block);
})
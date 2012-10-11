// same as listfilter.js, but serves pages that use .grid-box items instead

// custom jQuery filter selector `icontains` for text matching
// http://answers.oreilly.com/topic/1055-creating-a-custom-filter-selector-with-jquery/
$.expr[':'].icontains = function(element, index, match) {
    return (element.textContent || element.innerText || "").toUpperCase().indexOf(match[3].toUpperCase()) >= 0;
};

$(document).ready(function() {
    // set up initial vars
    var filterForm = '<div id="js-filter-form">\
        <label>Start typing to filter list</label>\
        <input class="filter" type="text" id="list-filter" />\
    </div>';
    var filteredList = $('#filterable-list');
    
    // insert filter form because we know we have js
    $(filterForm).insertBefore(filteredList);
    
    // after each keystroke in #list-filter input, do a case-insensitive
    // search against all the `.grid-box` elements inside #filterable-list
    $('#list-filter').change(function() {
        var filterVal = $(this).val();
        if (filterVal) {
            // hide the primary container to avoid potential repaints
            filteredList.css('display','none');
            // hide grid-boxes that don't have matching text, 
            // and filter-blocks that don't have visible grid-boxes
            filteredList.find('.grid-box:not(:icontains(' + filterVal + '))').css('display','none');
            filteredList.find('.filter-block:not(:has(.grid-box:visible))').css('display','none');
            // show blocks/boxes that contain matching text
            filteredList.find('.filter-block:has(.grid-box:icontains(' + filterVal + '))').css('display','block');
            filteredList.find('.grid-box:icontains(' + filterVal + ')').css('display','inline-block');
            // show the primary container again
            filteredList.css('display','block');
        } else {
            // nothing in filter form, so make sure everything is visible
            filteredList.find('.filter-block').css('display','block');
            filteredList.find('.grid-box').css('display','inline-block');
        }
        
        // show 'no results' message if we've removed all the items
        if ($('.filter-block > div:visible').length == 0) {
            $('#no-results').remove();
            $('#js-filter-form').after('<p id="no-results">No matching results found.</p>');
        } else {
            $('#no-results').remove();
        }
        return false;
    }).keyup(function() {
        $(this).change();
    });
});

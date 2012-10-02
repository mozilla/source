// icontains for text matching
$.expr[':'].icontains = function(a, i, m) {
    return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
};

$(document).ready(function() {
    // only provide filter form if js is enabled
    $('#js-filter-form').show();
    var listFilter = $('#list-filter');
    var filteredList = $('#filterable-list');
    $(listFilter).change(function() {
        var filterVal = $(this).val();
        if (filterVal) {
            // hide items that don't have matching text, lists that don't have
            // visible items, and blocks that don't have visible lists
            $(filteredList).find('li:not(:icontains(' + filterVal + '))').hide();
            $(filteredList).find('.filter-list:not(:has(li:visible))').hide();
            $(filteredList).find('.filter-block:not(:has(li:visible))').hide();
            // show blocks/lists/items that contain matching text
            $(filteredList).find('.filter-block:has(li:icontains(' + filterVal + '))').show();
            $(filteredList).find('.filter-list:has(li:icontains(' + filterVal + '))').show();
            $(filteredList).find('li:icontains(' + filterVal + ')').show();
        } else {
            // nothing in filter form, so make sure everything is visible
            $(filteredList).find(".filter-block").show();
            $(filteredList).find(".filter-list").show();
            $(filteredList).find("li").show();
        }
        
        // show 'no results' message if we've removed all the items
        if ($('.filter-list > li:visible').length == 0) {
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

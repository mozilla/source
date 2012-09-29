$.expr[':'].icontains = function(a, i, m) {
    return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
};
$(document).ready(function() {
    $('.js-filter-form').show();
    var listFilter = $('#list-filter');
    var filteredList = $('#filterable-list');
    $(listFilter).change(function() {
        var filterVal = $(this).val();
        if (filterVal) {
            $(filteredList).find('li:not(:icontains(' + filterVal + '))').hide();
            $(filteredList).find('.filter-block:not(:has(li:visible))').hide();
            $(filteredList).find('.filter-block:has(li:icontains(' + filterVal + '))').show();
            $(filteredList).find('li:icontains(' + filterVal + ')').show();
        } else {
            $(filteredList).find("li").show();
            $(filteredList).find(".filter-block").show();
        }
        return false;
    }).keyup(function() {
        $(this).change();
    });
});

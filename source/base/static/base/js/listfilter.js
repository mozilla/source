function ListFilter(options) {
    var filter = filter || {};
    
    filter.init = function(options) {
        // required args
        filter.listContainer = options.listContainer;
        filter.filterItemClass = options.filterItemClass;
        
        // optional args
        filter.inputContainer = options.inputContainer || null;
        filter.inputPrompt = options.inputPrompt || 'Search list';
        filter.inputClass = options.inputClass || '';
        filter.filterBlockClass = options.filterBlockClass || null;
        
        // built here
        filter.filteredList = $(filter.listContainer);
        filter.filterFormID = 'list-filter-form';
        filter.filterFormInputID = 'list-filter-input';
        
        filter.filterForm = '<div id="'+filter.filterFormID+'">\
            <label for="'+filter.filterFormInputID+'">'+filter.inputPrompt+'</label>\
            <input class="'+filter.inputClass+'" type="text" id="'+filter.filterFormInputID+'" />\
        </div>';
        
        filter.make();
        return filter;
    }
    
    filter.make = function() {
        filter.addFilterForm();
        filter.addMatcher();
        
        return filter;
    }
    
    filter.addFilterForm = function() {
        // add filterForm to the inputContainer if present,
        // otherwise insert onto page before listContainer
        if (!!filter.inputContainer) {
            $(filter.inputContainer).prepend(filter.filterForm);
        } else {
            $(filter.filterForm).insertBefore(filter.listContainer);
        }
    }
    
    filter.addMatcher = function() {
        // after each keystroke in filterForm input, do a case-insensitive
        // search against all filterItemClass elements inside listContainer
        $('#'+filter.filterFormInputID).change(function() {
            filter.filterValue = $(this).val();
            
            if (!!filter.filterValue) {
                filter.match();
            } else {
                filter.showAllItems();
            }
            
            filter.checkNoResults();

            return false;
        }).keyup(function() {
            $(this).change();
        });
    }
    
    filter.match = function() {
        // hide the list container to avoid potential repaints
        filter.filteredList.css('display','none');
        
        // perform the matching
        filter.hideUnmatchedItems();
        filter.showMatchedItems();
        
        // show the list container again
        filter.filteredList.css('display','block');
    }
    
    filter.hideUnmatchedItems = function() {
        // hide items that don't have matching text
        filter.filteredList.find(filter.filterItemClass+':not(:icontains(' + filter.filterValue + '))').css('display','none');
        if (!!filter.filterBlockClass) {
            filter.filteredList.find(filter.filterBlockClass+':not(:has('+filter.filterItemClass+':visible))').css('display','none');
        }
    }
    
    filter.showMatchedItems = function() {
        // show items that contain matching text
        if (!!filter.filterBlockClass) {
            filter.filteredList.find(filter.filterBlockClass+':has('+filter.filterItemClass+':icontains(' + filter.filterValue + '))').css('display','block');
        }
        filter.filteredList.find(filter.filterItemClass+':icontains(' + filter.filterValue + ')').css('display','block');
    }
    
    filter.showAllItems = function () {
        // nothing in filter form, so make sure everything is visible
        filter.filteredList.find(filter.filterBlockClass).css('display','block');
        filter.filteredList.find(filter.filterItemClass).css('display','block');
    }
    
    filter.checkNoResults = function() {
        // show 'no results' message if we've removed all the items
        $('#filter-no-results').remove();
        if ($(filter.filterItemClass+':visible').length == 0) {
            filter.filteredList.append('<p id="filter-no-results">No matching results found.</p>');
        }
    }
    
    // ready, set, go
    filter.init(options);
    return filter;
}

// custom jQuery filter selector `icontains` for text matching
// http://answers.oreilly.com/topic/1055-creating-a-custom-filter-selector-with-jquery/
$.expr[':'].icontains = function(element, index, match) {
    return (element.textContent || element.innerText || "").toUpperCase().indexOf(match[3].toUpperCase()) >= 0;
};

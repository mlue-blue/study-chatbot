// Script for enhanced to-do app

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Advanced To-Do App Loaded!');
    console.log('Features: Add, Edit, Delete, Complete, Search, Filter, Categories, Priorities, Due Dates');
});

// Auto-submit filter form on select change
document.querySelectorAll('.filter-select').forEach(select => {
    select.addEventListener('change', function() {
        this.closest('.filter-form').submit();
    });
});

// Custom file input label update for Django forms
// Shows selected file name, styled like .comment-date

document.addEventListener('DOMContentLoaded', function() {
    function updateFileLabel(wrapper) {
        var input = wrapper.querySelector('input[type="file"]');
        var label = wrapper.querySelector('.custom-file-input-label');
        if (!input || !label) return;
        input.addEventListener('change', function() {
            var fileName = input.files && input.files.length > 0 ? input.files[0].name : 'No file chosen';
            label.textContent = fileName;
        });
    }
    var wrappers = document.querySelectorAll('.custom-file-input-wrapper');
    wrappers.forEach(updateFileLabel);
});

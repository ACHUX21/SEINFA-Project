document.addEventListener('DOMContentLoaded', function() {
// Select all delete links
var deleteLinks = document.querySelectorAll('a[href*="/api/delete_user/"]');

deleteLinks.forEach(function(link) {
    link.addEventListener('click', function(event) {
        // Prevent the link from immediately navigating
        event.preventDefault();

        // Confirmation dialog
        Swal.fire({
            title: 'Are you sure?',
            text: "Do you really want to delete this user? This action cannot be undone.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'No, cancel!'
        }).then((result) => {
            if (result.isConfirmed) {
                // If confirmed, proceed with the action by manually setting the window location
                window.location.href = this.href;
            }
        });
    });
});
});


document.addEventListener('DOMContentLoaded', function() {
    // Select all delete links
    var deleteLinks = document.querySelectorAll('a[href*="/api/delete_user/"]');
    var toggleLinks = document.querySelectorAll('a[href*="/api/update_actif/"]'); // Selector for activation/deactivation links

    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            Swal.fire({
                title: 'Are you sure?',
                text: "Do you really want to delete this user? This action cannot be undone.",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'No, cancel!'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = this.href;
                }
            });
        });
    });

    toggleLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            var actionText = link.textContent.trim() === 'Désactiver' ? 'deactivate' : 'activate';
            Swal.fire({
                title: 'Are you sure?',
                text: "Do you really want to " + actionText + " this user?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, ' + actionText + ' it!',
                cancelButtonText: 'No, cancel!'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = this.href;
                }
            });
        });
    });
});

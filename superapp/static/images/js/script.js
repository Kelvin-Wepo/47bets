<script>
    document.addEventListener("DOMContentLoaded", function() {
        function toggleSidebar(sidebarId, toggleButtonId) {
            var sidebar = document.getElementById(sidebarId);
            var toggleButton = document.getElementById(toggleButtonId);

            toggleButton.addEventListener("click", function() {
                sidebar.classList.toggle("collapsed");
            });
        },z

        toggleSidebar("leftSidebar", "leftSidebarToggle");
        toggleSidebar("rightSidebar", "rightSidebarToggle");
    });
</script>

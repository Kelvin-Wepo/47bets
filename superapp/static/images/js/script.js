document.addEventListener('DOMContentLoaded', function() {
    const leftSidebar = document.getElementById('leftSidebar');
    const rightSidebar = document.getElementById('rightSidebar');
    const mainContent = document.getElementById('mainContent');
    const leftSidebarToggle = document.getElementById('leftSidebarToggle');
    const rightSidebarToggle = document.getElementById('rightSidebarToggle');

    function toggleSidebar(sidebar, isLeft) {
        const isMobile = window.innerWidth <= 768;
        
        if (isMobile) {
            sidebar.classList.toggle('expanded');
        } else {
            sidebar.classList.toggle('collapsed');
            if (isLeft) {
                mainContent.style.marginLeft = sidebar.classList.contains('collapsed') ? '60px' : '16.666%';
            } else {
                mainContent.style.marginRight = sidebar.classList.contains('collapsed') ? '60px' : '16.666%';
            }
        }
    }

    leftSidebarToggle.addEventListener('click', function() {
        toggleSidebar(leftSidebar, true);
    });

    rightSidebarToggle.addEventListener('click', function() {
        toggleSidebar(rightSidebar, false);
    });

    function handleResize() {
        const isMobile = window.innerWidth <= 768;
        
        if (isMobile) {
            leftSidebar.classList.remove('collapsed');
            rightSidebar.classList.remove('collapsed');
            mainContent.style.marginLeft = '0';
            mainContent.style.marginRight = '0';
        } else {
            leftSidebar.classList.remove('expanded');
            rightSidebar.classList.remove('expanded');
            mainContent.style.marginLeft = leftSidebar.classList.contains('collapsed') ? '60px' : '16.666%';
            mainContent.style.marginRight = rightSidebar.classList.contains('collapsed') ? '60px' : '16.666%';
        }
    }

    window.addEventListener('resize', handleResize);
    handleResize(); // Call once to set initial state
});
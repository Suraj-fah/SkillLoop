// SkillLoop Bharat — Interactive JS helpers

document.addEventListener("DOMContentLoaded", () => {
    // Setup tab buttons if present
    const tabBtns = document.querySelectorAll(".tab-btn");
    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-tab");
            
            // Toggle active buttons
            tabBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            // Toggle active content panes
            const tabContents = document.querySelectorAll(".tab-content");
            tabContents.forEach(content => {
                if (content.id === targetId) {
                    content.classList.add("active");
                } else {
                    content.classList.remove("active");
                }
            });
        });
    });

    // Auto-dismiss alerts after 5 seconds if desired
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.4s ease, transform 0.4s ease";
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-6px)";
            setTimeout(() => alert.remove(), 400);
        }, 7000);
    });
});

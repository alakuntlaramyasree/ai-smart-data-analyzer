// ==========================================
// AI Smart Data Analyzer Pro - script.js
// ==========================================


/* ------------------------------
   1. File Upload Enhancement
------------------------------ */

document.addEventListener("DOMContentLoaded", function () {

    const fileInput = document.querySelector("input[type='file']");
    const uploadForm = document.querySelector("form");

    if (fileInput) {

        fileInput.addEventListener("change", function () {

            const fileName = this.files[0]?.name;

            if (fileName) {
                showToast(`Selected file: ${fileName}`);
            }

        });

    }


    if (uploadForm) {

        uploadForm.addEventListener("submit", function () {

            showLoadingOverlay();
        });

    }

});


/* ------------------------------
   2. Loading Overlay
------------------------------ */

function showLoadingOverlay() {

    const overlay = document.createElement("div");

    overlay.id = "loadingOverlay";

    overlay.innerHTML = `
        <div class="loader"></div>
        <h3 style="margin-top:20px;color:#4a69bd;">
            Analyzing your dataset...
        </h3>
        <p>Please wait while AI processes your data</p>
    `;

    Object.assign(overlay.style, {

        position: "fixed",
        top: "0",
        left: "0",
        width: "100%",
        height: "100%",
        background: "rgba(255,255,255,0.9)",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        zIndex: "9999"

    });

    document.body.appendChild(overlay);
}


/* ------------------------------
   3. Toast Notifications
------------------------------ */

function showToast(message) {

    const toast = document.createElement("div");

    toast.innerText = message;

    Object.assign(toast.style, {

        position: "fixed",
        bottom: "20px",
        right: "20px",
        background: "#4a69bd",
        color: "white",
        padding: "12px 18px",
        borderRadius: "10px",
        boxShadow: "0 10px 20px rgba(0,0,0,0.2)",
        zIndex: "9999",
        opacity: "0",
        transform: "translateY(20px)",
        transition: "all 0.4s ease"

    });

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.style.opacity = "1";
        toast.style.transform = "translateY(0)";

    }, 100);

    setTimeout(() => {

        toast.style.opacity = "0";
        toast.style.transform = "translateY(20px)";

        setTimeout(() => toast.remove(), 500);

    }, 3000);

}


/* ------------------------------
   4. Smooth Scroll Effect
------------------------------ */

document.querySelectorAll("a[href^='#']").forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        e.preventDefault();

        const target = document.querySelector(this.getAttribute("href"));

        if (target) {

            target.scrollIntoView({
                behavior: "smooth"
            });

        }

    });

});


/* ------------------------------
   5. Animate Cards on Load
------------------------------ */

window.addEventListener("load", () => {

    document.querySelectorAll(".card, .dashboard-card, .stat-card").forEach((el, i) => {

        setTimeout(() => {

            el.classList.add("fade-up");

        }, i * 100);

    });

});
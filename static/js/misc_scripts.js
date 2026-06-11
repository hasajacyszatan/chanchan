// przycisk skrolluj w góre

const topBtn = document.getElementById("scrollToTopBtn");


window.onscroll = function() {
           if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 300) {
        topBtn.style.display = "block";
    } else {
        topBtn.style.display = "none";
    }
};


topBtn.addEventListener("click", function() {
    window.scrollTo({
        top: 0, 
        behavior: "smooth" 
    });
});


// Klik w miniaturę → przełącza na pełny rozmiar (używa data-fullpng)
function togglefav(postid, el) {
    fetch("/post/" + postid + "/favourite/")
        .then(() => {
            const faved = el.dataset.faved === "true";
            if (faved) {
                el.dataset.faved = "false";
                el.innerText = "☆ Dodaj do ulubionych";
            } else {
                el.dataset.faved = "true";
                el.innerText = "★ Usuń z ulubionych";
            }
        });
}
document.addEventListener('click', e => {
    const img = e.target.closest('.images img');
    if (!img) return;

    if (img.dataset.expanded) {
        // Wróć do miniatury
        img.src = img.dataset.thumbnailSrc;
        img.style.cssText = '';
        delete img.dataset.expanded;
    } else {
        // Pokaż pełne zdjęcie
        img.dataset.thumbnailSrc = img.src;
        img.src = img.dataset.fullpng || img.src;
        img.style.cssText = 'max-height:500px;max-width:500px;width:auto;height:auto;flex-basis:100%;cursor:zoom-out;';
        img.dataset.expanded = '1';
    }
});


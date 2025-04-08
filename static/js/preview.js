document.body.addEventListener('click', function(e) {
    if (e.target === document.body) window.close();
});

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') window.close();
});
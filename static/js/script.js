function hideFlash() {
    const flash = document.getElementById('flashMsg');
    flash.classList.add('hide');

    setTimeout(() => {
        flash.style.display = 'none';
    }, 300);
}
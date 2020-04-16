function selectElement(e) {
    if (e.target.tagName !== 'LI') return;
    if (e.ctrlKey || e.metaKey) {
        e.target.classList.toggle('selected');
    } else {
        let selected = ul.querySelectorAll('.selected');
        selected.forEach(li => li.classList.remove('selected'));
        e.target.classList.add('selected')
    }
}

ul.onmousedown = function() { return false }
ul.addEventListener('click', selectElement);

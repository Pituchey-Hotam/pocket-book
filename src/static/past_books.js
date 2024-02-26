const searchInput = document.querySelector('input#name-filter');
let genreInput = document.querySelector('select#genre-filter');
let eraInput = document.querySelector('select#era-filter');

function updateSearch() {
    let nameFilter = searchInput.value;
    let genreFilter = genreInput.value;
    let eraFilter = eraInput.value;

    document.querySelectorAll('.card').forEach(card => {
        let nameFilterPass = card.getAttribute('aria-book-name').includes(nameFilter)
            || card.getAttribute('aria-book-author').includes(nameFilter);
        let genreFilterPass = card.getAttribute('aria-book-genre').includes(genreFilter);
        let eraFilterPass = card.getAttribute('aria-book-era').includes(eraFilter);
        
        if (nameFilterPass && genreFilterPass && eraFilterPass)
            {
            card.classList.remove('hide');
        }
        else {
            card.classList.add('hide');
        }
    });
}

searchInput.addEventListener('keyup', updateSearch);
genreInput.addEventListener('change', updateSearch);
eraInput.addEventListener('change', updateSearch);
const likes = document.querySelectorAll("button.WishButton_button");

likes.forEach((like) => {
    const color = document.getElementsByClassName("is");
    like.addEventListener("click", (e) => {
        // console.log(e.target.classList);
        e.target.classList.toggle("active");
        e.ariaPressed = "true";
    });
});

const lists = document.querySelectorAll(".css-qn01ot");
const writeList = document.querySelectorAll("div.css-ivvewn");

lists.forEach((list) => {
    list.addEventListener("mouseover", (e) => {
        list.classList.add("list-active");
        // console.log(list.children[1]);
        // list.children[1].style.display = "block";
    });

    list.addEventListener("mouseout", (e) => {
        list.classList.remove("list-active");
        // list.children[1].style.display = "none";
    });
});


// 페이지네이션

let currentRangeStart = 1;

function changePageRange(direction) {
    const rangeSize = 10;
    const totalPages = parseInt(document.getElementById('total-pages').innerText, 10);

    currentRangeStart += direction * rangeSize;
    if (currentRangeStart < 1) {
        currentRangeStart = 1;
    } else if (currentRangeStart > totalPages) {
        currentRangeStart = totalPages - (totalPages % rangeSize) + 1;
    }
    renderPaginationButtons(totalPages, currentRangeStart);
}

function renderPaginationButtons(totalPages, currentPage) {
    const rangeSize = 10;
    const paginationButtons = document.getElementById('pagination-buttons');
    paginationButtons.innerHTML = '';

    const currentRangeEnd = Math.min(currentRangeStart + rangeSize - 1, totalPages);
    for (let i = currentRangeStart; i <= currentRangeEnd; i++) {
        const pageLink = document.createElement('a');
        pageLink.href = `?page=${i}`;
        pageLink.innerText = i;
        if (i === currentPage) {
            pageLink.classList.add('current');
        }
        paginationButtons.appendChild(pageLink);
    }

    document.getElementById('prev-btn').style.display = currentRangeStart > 1 ? 'inline' : 'none';
    document.getElementById('next-btn').style.display = currentRangeEnd < totalPages ? 'inline' : 'none';
}

document.addEventListener('DOMContentLoaded', () => {
    const totalPages = parseInt(document.getElementById('total-pages').innerText, 10);
    const currentPage = parseInt(document.getElementById('current-page').innerText, 10);
    renderPaginationButtons(totalPages, currentPage);
});

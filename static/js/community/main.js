document.addEventListener('DOMContentLoaded', function () {
    let currentCount = 4;
    let totalBoards = 0;
    const loadMoreButton = document.getElementById('load-more');

    loadMoreButton.addEventListener('click', function () {
        fetch(`/community/load-more-boards/?start=${currentCount}&limit=4`)
            .then(response => response.json())
            .then(data => {
                totalBoards = data.total_boards_count;
                const boardsUl = document.getElementById('boards__ul');
                data.boards.forEach(board => {
                    const boardHtml = `
                        <li id="boards__li">
                            <h2 id="board__name"><a href="/community/${board.id}/">${board.name}</a></h2>
                            <ul id="posts__ul">
                                ${board.posts.slice(-5).reverse().map(post => `
                                    <a href="/community/${board.id}/post/${post.id}/">
                                        <li id="posts__li">
                                            <h2 id="post__name">
                                                ${post.title.length > 10 ? post.title.slice(0, 10) + '...' : post.title}
                                            </h2>
                                            <h2 id="post__date">
                                                ${new Date(post.created_time).toLocaleDateString('en-US', { month: 'numeric', day: 'numeric' })}
                                            </h2>
                                        </li>
                                    </a>
                                `).join('')}
                            </ul>
                        </li>
                    `;
                    boardsUl.insertAdjacentHTML('beforeend', boardHtml);
                });
                currentCount += 4;
                console.log(currentCount, totalBoards);
                if (currentCount >= totalBoards) {
                    loadMoreButton.style.display = 'none';
                }
            })
            .catch(error => console.error('Error:', error));
    });
});
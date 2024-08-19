document.addEventListener('DOMContentLoaded', function () {
    let currentCount = 4;
    let totalBoards = 0;
    const loadMoreButton = document.getElementById('load-more');

    // 초기 로드 시에 게시판의 총 개수를 가져오기 위해 fetch 요청을 수행합니다.
    fetch(`/community/load-more-boards/?start=0&limit=0`)  // limit=0으로 요청하여 게시판 수만 가져옴
        .then(response => response.json())
        .then(data => {
            totalBoards = data.total_boards_count;
            console.log("Total boards count:", totalBoards); // 디버그용 콘솔 출력

            // 게시판의 총 개수가 4개 이하이면 "더보기" 버튼을 숨깁니다.
            if (totalBoards <= 4) {
                loadMoreButton.style.display = 'none';
            }
        })
        .catch(error => console.error('Error fetching total boards count:', error));

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
                // debug
                console.log(currentCount, totalBoards);
                if (currentCount >= totalBoards) {
                    loadMoreButton.style.display = 'none';
                }
            })
            .catch(error => console.error('Error:', error));
    });
});
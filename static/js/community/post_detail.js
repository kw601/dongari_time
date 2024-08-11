document.addEventListener('DOMContentLoaded', function() {
    const scrapBtn = document.getElementById('scrap-btn');
    const likeBtn = document.getElementById('like-btn');
    //const scrapCount = document.getElementById('scrap-count');
    const likeCount = document.getElementById('like-count');

    scrapBtn.addEventListener('click', function() {
        const postId = this.dataset.postId;
        fetch(`/community/post/${postId}/scrap/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.scrapped) {
                scrapBtn.textContent = '스크랩 취소';
            } else {
                scrapBtn.textContent = '스크랩';
            }
        });
    });

    likeBtn.addEventListener('click', function() {
        const postId = this.dataset.postId;
        fetch(`/community/post/${postId}/like/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            likeCount.textContent = data.likes;
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
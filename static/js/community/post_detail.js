document.addEventListener('DOMContentLoaded', function() {
    const scrapBtn = document.getElementById('scrap-btn');
    const likeBtn = document.getElementById('like-btn');
    const scrapCount = document.getElementById('scrap-count');
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
            likeCount.textContent = data.likes;  // 이 부분이 중요합니다
            if (data.is_liked) {
                likeBtn.textContent = '좋아요 취소';
            } else {
                likeBtn.textContent = '좋아요';
            }
            likeBtn.textContent += ` (${data.likes})`;  // 좋아요 수를 버튼 텍스트에 추가
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
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
            if (data.is_scraped) {
                scrapBtn.textContent = '스크랩 취소';
            } else {
                scrapBtn.textContent = '스크랩';
            }
        })
        .catch(error => console.error('Error:', error));
    });

    updateLikeButtonState();

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
            this.dataset.isLiked = data.is_liked.toString();
            updateLikeButtonState();
        });
    });

    function updateLikeButtonState() {
        if (likeBtn.dataset.isLiked === 'true') {
            likeBtn.textContent = '좋아요 취소 ';
        } else {
            likeBtn.textContent = '좋아요 ';
        }
        likeBtn.appendChild(likeCount);
    }

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
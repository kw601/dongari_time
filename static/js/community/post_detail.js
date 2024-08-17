document.addEventListener('DOMContentLoaded', function() {
    const scrapBtn = document.getElementById('scrap-btn');
    const likeBtn = document.getElementById('like-btn');
    const scrapCount = document.getElementById('scrap-count');
    const likeCount = document.getElementById('like-count');
    const likeDescription = document.getElementById('like__description');
    const scrapDescription = document.getElementById('scrap__description');

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
            scrapDescription.textContent = data.scrap_count;
            if (data.is_scraped) {
                scrapBtn.textContent = '스크랩 취소';
            } else {
                scrapBtn.textContent = '스크랩';
            }
        })
        .catch(error => console.error('Error:', error));
    });
    function updateScrapButtonState() {
        if (data.is_scraped) {
            scrapBtn.textContent = '스크랩 취소';
        } else {
            scrapBtn.textContent = '스크랩';
        }
    }
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
            console.log(data);

            // likeCount.textContent = data.likes;
            likeDescription.textContent = data.likes;
            this.dataset.isLiked = data.is_liked.toString();
            updateLikeButtonState();
            
        })
        .catch(error => console.error('Error:', error));
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

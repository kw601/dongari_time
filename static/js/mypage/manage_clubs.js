document.addEventListener('DOMContentLoaded', function() {
    const clubList = document.getElementById('club-list');
    const messageDiv = document.getElementById('message');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    clubList.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-club')) {
            const clubId = e.target.dataset.clubId;
            const listItem = e.target.closest('li');
            
            deleteClub(clubId, listItem);
        }
    });

    function deleteClub(clubId, listItem) {
        fetch('/mypage/delete-club/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: `club_id=${clubId}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                listItem.remove();
                showMessage('동아리가 성공적으로 삭제되었습니다.', 3000);
            } else {
                showMessage(data.message, 5000);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            showMessage('오류가 발생했습니다. 다시 시도해주세요.', 3000);
        });
    }

    function showMessage(message, duration) {
        messageDiv.textContent = message;
        messageDiv.style.display = 'block';
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, duration);
    }
});
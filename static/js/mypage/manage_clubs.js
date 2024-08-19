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
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: `club_id=${clubId}`
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message || 'Network response was not ok');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                listItem.remove();
                showMessage('동아리가 성공적으로 삭제되었습니다.', 3000, 'success');
            } else {
                showMessage(data.message, 5000, 'error');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            showMessage(error.message || '오류가 발생했습니다. 다시 시도해주세요.', 5000, 'error');
        });
    }

    function showMessage(message,/* duration,*/ type) {
        messageDiv.textContent = message;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';
        /*setTimeout(() => {
            messageDiv.style.display = 'none';
        }, duration);*/
    }
});
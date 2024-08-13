document.addEventListener('DOMContentLoaded', function() {
    const newPostDiv = document.getElementById('new_post');
    const showFormButton = document.getElementById('show-post-form');
    const formContainer = document.getElementById('post-form-container');
    const cancelButton = document.getElementById('cancel-post');
    const postForm = document.getElementById('post-form');
    const postList = document.getElementById('post__ul');

    function toggleForm() {
        formContainer.classList.toggle('active');
        if (formContainer.classList.contains('active')) {
            newPostDiv.style.display = 'none';
            formContainer.style.display = 'block';
        } else {
            newPostDiv.style.display = 'block';
            formContainer.style.display = 'none';
        }
    }

    showFormButton.addEventListener('click', toggleForm);
    cancelButton.addEventListener('click', function() {
        toggleForm();
        postForm.reset();
    });

    postForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(postForm);
        const boardId = window.location.pathname.split('/')[2];
        
        fetch(`/community/${boardId}/create/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 새 게시글 요소 생성
                const newPost = document.createElement('a');
                newPost.href = `/community/${boardId}/post/${data.post_id}/`;
                newPost.innerHTML = `
                    <li>
                        <h2 id="post__title">${data.title}</h2>
                        <p id="post__content">${data.content}</p>
                        <div id="post__description">
                            <p id="post__created">${data.created_time}</p>
                            <p id="post__user">${data.anonymous ? '익명' : data.user}</p>
                        </div>
                    </li>
                `;
                
                // 새 게시글을 목록의 맨 위에 추가
                postList.insertBefore(newPost, postList.firstChild);
                
                // 폼 리셋 및 숨기기
                postForm.reset();
                toggleForm();
            } else {
                console.error('Error:', data.errors);
                // 에러 처리 (예: 에러 메시지 표시)
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
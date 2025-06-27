document.addEventListener("DOMContentLoaded", function() {
    var cardItems = document.querySelectorAll('.card-container-item');

    cardItems.forEach(function(item) {
        var coverCard = item.querySelector('.cover-card');
        var characterCard = item.querySelector('.card');
        var characterName = characterCard.querySelector('h2').textContent.trim();
        var cardContent = characterCard.querySelector('.card-content');

        // 처음에는 커버 카드만 보이도록 설정
        characterCard.style.display = 'none';

        coverCard.addEventListener('click', function() {
            // 커버 카드를 숨기고 캐릭터 카드를 보여줌
            coverCard.style.display = 'none';
            characterCard.style.display = 'block';

            // 글자 자르기 기능 실행
            updateContent(cardContent);
        });

        characterCard.addEventListener('click', function() {
            openModal(characterName);
        });
    });

    // 모달 열기 함수
    function openModal(characterName) {
        var modal = document.getElementById('modal-' + characterName);
        if (modal) {
            modal.style.display = 'flex';
        }
    }

    // 모달 닫기 함수
    function closeModal(characterName) {
        var modal = document.getElementById('modal-' + characterName);
        if (modal) {
            modal.style.display = 'none';
        }
    }

    // 모달 외부 클릭 시 모달 닫기 기능
    window.onclick = function(event) {
        var modals = document.getElementsByClassName('modal');
        for (var i = 0; i < modals.length; i++) {
            if (event.target == modals[i]) {
                modals[i].style.display = "none";
            }
        }
    }

    // 모달 내부의 닫기 버튼에 이벤트 리스너 추가
    var closeButtons = document.getElementsByClassName('close');
    for (var i = 0; i < closeButtons.length; i++) {
        closeButtons[i].addEventListener('click', function(event) {
            var characterName = event.target.getAttribute('onclick').split("'")[1];
            closeModal(characterName);
        });
    }

    // 글자 자르기 기능 함수
    function updateContent(content) {
        var paragraphs = content.querySelectorAll('p');
        var originalTexts = [];

        paragraphs.forEach(function(p) {
            originalTexts.push(p.textContent);
        });

        function checkOverflow() {
            paragraphs.forEach(function(p, index) {
                p.textContent = originalTexts[index];
            });

            for (let i = 0; i < paragraphs.length; i++) {
                let truncatedText = originalTexts[i];

                // 텍스트가 넘치는지 확인
                if (content.scrollHeight > content.clientHeight) {
                    // 텍스트의 끝부분을 잘라내고 "더보기" 추가 (기능 없이 텍스트만 추가)
                    while (content.scrollHeight > content.clientHeight && truncatedText.length > 0) {
                        truncatedText = truncatedText.slice(0, -1);
                        paragraphs[i].textContent = truncatedText.trim() + '... 더보기';
                    }
                    break; // 텍스트가 잘린 부분에서 멈춤
                }
            }
        }

        checkOverflow(); // 초기에 한번 실행
    }
});

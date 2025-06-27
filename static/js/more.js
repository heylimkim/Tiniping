document.addEventListener("DOMContentLoaded", function() {
    var cardContents = document.querySelectorAll('.card-content');

    cardContents.forEach(function(content) {
        var paragraphs = content.querySelectorAll('p');
        var originalTexts = [];

        paragraphs.forEach(function(p) {
            originalTexts.push(p.textContent);
        });

        function updateContent() {
            var isOverflowing = false;
            paragraphs.forEach(function(p, index) {
                p.textContent = originalTexts[index];
            });

            for (let i = 0; i < paragraphs.length; i++) {
                if (content.scrollHeight > content.clientHeight) {
                    isOverflowing = true;
                    let truncatedText = originalTexts[i];

                    // 텍스트를 자르고 '더보기' 추가
                    while (content.scrollHeight > content.clientHeight && truncatedText.length > 0) {
                        truncatedText = truncatedText.slice(0, -1);
                        paragraphs[i].textContent = truncatedText.trim() + '... 더보기'; // 기능 없이 텍스트만 추가
                    }

                    break;
                }
            }

            if (!isOverflowing) {
                paragraphs.forEach(function(p, index) {
                    p.textContent = originalTexts[index];
                });
            }
        }

        updateContent(); // 초기 실행
    });
});

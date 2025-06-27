    function findCharacter() {
        const inputWord = document.getElementById('input-word').value;
        if (!inputWord) {
            alert("Please enter a word!");
            return;
        }

        fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `word=${encodeURIComponent(inputWord)}`,
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('result');
            const characterName = document.getElementById('character-name');
            const characterImage = document.getElementById('character-image');

            if (data.error) {
                characterName.textContent = "Character not found.";
                characterImage.src = "";
                resultDiv.style.display = "block";
            } else {
                characterName.textContent = `Character: ${data.character}`;
                characterImage.src = data.image;
                resultDiv.style.display = "block";
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while finding the character.");
        });
    }
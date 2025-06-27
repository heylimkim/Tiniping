
function openModal(characterName) {
    var modal = document.getElementById('modal-' + characterName);
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeModal(characterName) {
    var modal = document.getElementById('modal-' + characterName);
    if (modal) {
        modal.style.display = 'none';
    }
}

// 클릭했을 때 모달이 닫히는 기능 추가
window.onclick = function(event) {
    var modals = document.getElementsByClassName('modal');
    for (var i = 0; i < modals.length; i++) {
        if (event.target == modals[i]) {
            modals[i].style.display = "none";
        }
    }
}

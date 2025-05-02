// Inicializa o modal do Bootstrap e manipula eventos de exclusão
document.addEventListener('DOMContentLoaded', function () {
    let currentForm = null;
    const deleteModalEl = document.getElementById('confirmDeleteModal');

    if (!deleteModalEl) return; // garante que o modal existe

    const deleteModal = new bootstrap.Modal(deleteModalEl);
    const confirmBtn = document.getElementById('confirmDeleteBtn');

    // Captura o clique em qualquer botão com classe delete-button
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            currentForm = button.closest('form');
            deleteModal.show();
        });
    });

    // Se confirmado, envia o formulário armazenado
    if (confirmBtn) {
        confirmBtn.addEventListener('click', function () {
            if (currentForm) {
                currentForm.submit();
            }
        });
    }
});

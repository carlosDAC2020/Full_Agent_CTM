// frontend/js/email.js

document.addEventListener('DOMContentLoaded', () => {
    const API_URL = document.body?.dataset?.api || window.location.origin;
    // Elements
    const sendEmailPanel = document.getElementById('sendEmailPanel');
    const emailFabBtn = document.getElementById('emailFabBtn');
    const modalOverlay = document.getElementById('modalOverlay');
    const closeSendEmailPanel = document.getElementById('closeSendEmailPanel');
    const recipientInput = document.getElementById('recipientInput');
    const recipientTagsContainer = document.getElementById('recipientTagsContainer');
    const showFavoritesBtn = document.getElementById('showFavoritesBtn');
    const favoritesDropdown = document.getElementById('favoritesDropdown');
    const sendEmailBtn = document.getElementById('sendEmailBtn');
    // Nuevo input de remitente y botón de edición
    const senderInput = document.getElementById('senderInput');
    const editSenderBtn = document.getElementById('editSenderBtn');
    // Nuevos controles de favoritos (modal)
    const favoritesModal = document.getElementById('favoritesModal');
    const closeFavoritesModalBtn = document.getElementById('closeFavoritesModalBtn');
    const addRecipientBtn = document.getElementById('addRecipientBtn');
    const fileDropArea = document.getElementById('fileDropArea');
    const fileInput = document.getElementById('fileInput');
    const filePreview = document.getElementById('filePreview');
    const removeFileBtn = document.getElementById('removeFileBtn');

    // State
    let recipients = [];
    let favorites = [];
    let currentSenderEmail = '';
    let currentPdfUrl = '';
    let suppressDocumentClickClose = false; // evita cierre inmediato al abrir

    // Initialize
    async function init() {
        loadEmailSettings();
        setupEventListeners();
    }

    // Event Listeners
    function setupEventListeners() {
        // Open/Close panel
        if (emailFabBtn) {
            emailFabBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                openPanel('');
            });
        }

        // Add recipient button
        const addRecipientBtn = document.getElementById('addRecipientBtn');
        if (addRecipientBtn) {
            addRecipientBtn.addEventListener('click', (e) => {
                e.preventDefault();
                addRecipientFromInput();
                if (recipientInput) recipientInput.value = '';
            });
        }
        if (closeSendEmailPanel) {
            closeSendEmailPanel.addEventListener('click', closePanel);
        }

        // Add recipient on Enter or comma
        if (recipientInput) {
            recipientInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ',') {
                    e.preventDefault();
                    addRecipientFromInput();
                    recipientInput.value = '';
                }
            });
        }

        // Global drag/drop guards to prevent navigation on drop outside the drop area
        document.addEventListener('dragover', (e) => { e.preventDefault(); }, true);
        document.addEventListener('drop', (e) => {
            if (!fileDropArea || !fileDropArea.contains(e.target)) {
                e.preventDefault();
            }
        }, true);

        // Drag & Drop for file upload
        if (fileDropArea) {
            fileDropArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.stopPropagation();
                fileDropArea.classList.add('drag-over');
            });
            fileDropArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                e.stopPropagation();
                fileDropArea.classList.remove('drag-over');
            });
            fileDropArea.addEventListener('drop', (e) => {
                e.preventDefault();
                e.stopPropagation();
                fileDropArea.classList.remove('drag-over');
                if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
                    handleFile(e.dataTransfer.files[0]);
                }
            });
            // Click to open file chooser
            fileDropArea.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (fileInput) fileInput.click();
            });
        }

        // Handle manual file selection
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                e.stopPropagation();
                const file = e.target && e.target.files && e.target.files[0];
                if (file) handleFile(file);
            });
        }

        // Remove uploaded file and return to drop area
        if (removeFileBtn) {
            removeFileBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (sendEmailPanel) sendEmailPanel.dataset.pdfPath = '';
                // Toggle UI
                if (filePreview) filePreview.classList.add('hidden');
                if (fileDropArea) fileDropArea.classList.remove('hidden');
            });
        }

        // Favorites modal open/close
        if (showFavoritesBtn) {
            showFavoritesBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                openFavoritesModal();
            });
        }
        if (closeFavoritesModalBtn) {
            closeFavoritesModalBtn.addEventListener('click', () => {
                if (favoritesModal) favoritesModal.classList.add('hidden');
            });
        }
        if (favoritesModal) {
            favoritesModal.addEventListener('click', (e) => {
                if (e.target === favoritesModal) favoritesModal.classList.add('hidden');
            });
        }

        // Send email
        if (sendEmailBtn) {
            sendEmailBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                sendEmail();
            });
        }

        // Edit sender email button
        if (editSenderBtn) {
            editSenderBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                editSenderEmail();
            });
        }
    }

    // Panel Controls
    function openPanel(pdfUrl) {
        currentPdfUrl = pdfUrl || '';
        sendEmailPanel.classList.remove('hidden');
        sendEmailPanel.setAttribute('aria-hidden', 'false');
        if (modalOverlay) {
            modalOverlay.classList.remove('hidden');
            modalOverlay.setAttribute('aria-hidden', 'false');
        }
        document.body.style.overflow = 'hidden';
        recipientInput.focus();

        // Suprimir el primer click del documento que disparó la apertura
        suppressDocumentClickClose = true;
        setTimeout(() => { suppressDocumentClickClose = false; }, 0);
    }

    // =======================================================
    //          1. FUNCIÓN closePanel() CON DIAGNÓSTICO
    // =======================================================
    function closePanel() {
        // Log para saber que la función se ejecutó
        console.log('%c--- INTENTO DE CERRAR PANEL DE EMAIL ---', 'color: red; font-weight: bold;');

        // La traza que nos dirá QUIÉN llamó a esta función
        console.trace('La función closePanel fue llamada desde esta pila de ejecución:');

        // La acción que oculta el panel (la dejamos como estaba)
        sendEmailPanel.classList.add('hidden');
        sendEmailPanel.setAttribute('aria-hidden', 'true');
        if (modalOverlay) {
            modalOverlay.classList.add('hidden');
            modalOverlay.setAttribute('aria-hidden', 'true');
        }
        document.body.style.overflow = '';
        // Clear form
        recipients = [];
        renderRecipients();
        recipientInput.value = '';
        if (favoritesModal) favoritesModal.classList.add('hidden');
        if (typeof favoritesDropdown !== 'undefined' && favoritesDropdown) favoritesDropdown.classList.add('hidden');
        // Reset file selection and preview
        if (fileInput) fileInput.value = '';
        if (sendEmailPanel) sendEmailPanel.dataset.pdfPath = '';
        if (filePreview) filePreview.classList.add('hidden');
        if (fileDropArea) fileDropArea.classList.remove('hidden');
    }

    // Recipient Management
    function addRecipient(email) {
        if (!email || !isValidEmail(email)) return;

        // Check if already added
        if (recipients.some(r => r.email === email)) return;

        recipients.push({ email, isFavorite: isFavorite(email) });
        renderRecipients();
    }

    function removeRecipient(email) {
        recipients = recipients.filter(r => r.email !== email);
        renderRecipients();
    }

    function renderRecipients() {
        recipientTagsContainer.innerHTML = '';

        recipients.forEach(recipient => {
            const tag = document.createElement('div');
            tag.className = 'recipient-tag';
            tag.innerHTML = `
                <span class="tag-email">${recipient.email}</span>
                <span class="favorite-star" data-email="${recipient.email}">
                    ${recipient.isFavorite ? '★' : '☆'}
                </span>
                <button class="remove-tag-btn" data-email="${recipient.email}" type="button" title="Quitar">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" width="16" height="16"><path d="M6 7h1v9H6V7zm7 0h1v9h-1V7z"/><path d="M3 5h14v1H3z"/><path d="M8 3h4v1H8z"/><path d="M5 6h10l-1 12H6L5 6z"/></svg>
                    <span class="tooltiptext">Quitar</span>
                </button>
            `;

            // Add event listeners
            tag.querySelector('.remove-tag-btn').addEventListener('click', (e) => {
                e.stopPropagation();
                removeRecipient(recipient.email);
            });

            tag.querySelector('.favorite-star').addEventListener('click', (e) => {
                e.stopPropagation();
                toggleFavorite(recipient.email);
            });

            recipientTagsContainer.appendChild(tag);
        });
    }

    // Favorites Management
    function toggleFavorite(email) {
        const recipient = recipients.find(r => r.email === email);
        if (!recipient) return;

        recipient.isFavorite = !recipient.isFavorite;

        // Update in favorites list
        if (recipient.isFavorite && !favorites.includes(email)) {
            favorites.push(email);
        } else if (!recipient.isFavorite) {
            favorites = favorites.filter(f => f !== email);
        }

        // Save to storage
        saveEmailSettings();

        // Re-render
        renderRecipients();
        renderFavorites();
    }

    function isFavorite(email) {
        return favorites.includes(email);
    }

    function toggleFavoritesDropdown() {
        favoritesDropdown.classList.toggle('hidden');
        if (!favoritesDropdown.classList.contains('hidden')) {
            renderFavorites();
        }
    }

    function renderFavorites() {
        if (!favorites.length) {
            favoritesDropdown.innerHTML = '<div class="favorite-item">No hay favoritos guardados</div>';
            return;
        }

        favoritesDropdown.innerHTML = `
            <div class="favorites-list">
                ${favorites.map(email => `
                    <div class="favorite-item">
                        <span class="favorite-email">${email}</span>
                        <div class="favorite-actions">
                            <button class="add-favorite" data-email="${email}" title="Añadir">
                                <i class="fa-solid fa-plus"></i>
                            </button>
                            <button class="remove-favorite" data-email="${email}" title="Eliminar">
                                <i class="fa-solid fa-trash"></i>
                            </button>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

        // Add event listeners
        document.querySelectorAll('.add-favorite').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const email = btn.dataset.email;
                if (!recipients.some(r => r.email === email)) {
                    addRecipient(email);
                }
            });
        });

        document.querySelectorAll('.remove-favorite').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const email = btn.dataset.email;
                removeFavorite(email);
            });
        });
    }

    function removeFavorite(email) {
        favorites = favorites.filter(f => f !== email);

        // Update recipient tags
        const recipient = recipients.find(r => r.email === email);
        if (recipient) {
            recipient.isFavorite = false;
        }

        saveEmailSettings();
        renderRecipients();
        renderFavorites();
    }

    // Sender Email Management
    let isEditing = false;
    let currentEditIcon = null;

    function editSenderEmail() {
        if (isEditing) {
            // If already editing, save the changes
            const newEmail = senderInput.value.trim();
            if (newEmail && isValidEmail(newEmail)) {
                currentSenderEmail = newEmail;
                saveEmailSettings();
            } else {
                senderInput.value = currentSenderEmail; // Revert if invalid
            }

            // Reset UI
            senderInput.readOnly = true;
            if (currentEditIcon) {
                currentEditIcon.classList.remove('fa-check');
                currentEditIcon.classList.add('fa-pencil');
            }
            if (editSenderBtn) {
                editSenderBtn.title = 'Editar';
            }
            isEditing = false;
            return;
        }

        // Start editing
        isEditing = true;
        const currentEmail = senderInput.value;
        senderInput.readOnly = false;

        // Change button to save icon
        const icon = editSenderBtn.querySelector('i');
        if (icon) {
            icon.classList.remove('fa-pencil');
            icon.classList.add('fa-check');
            currentEditIcon = icon;
        }
        if (editSenderBtn) {
            editSenderBtn.title = 'Guardar';
        }

        senderInput.focus();

        const saveEdit = () => {
            if (!isEditing) return;

            const newEmail = senderInput.value.trim();
            if (newEmail && isValidEmail(newEmail)) {
                currentSenderEmail = newEmail;
                saveEmailSettings();
            } else {
                senderInput.value = currentSenderEmail; // Revert if invalid
            }

            // Reset UI
            senderInput.readOnly = true;
            if (currentEditIcon) {
                currentEditIcon.classList.remove('fa-check');
                currentEditIcon.classList.add('fa-pencil');
            }
            if (editSenderBtn) {
                editSenderBtn.title = 'Editar';
            }
            isEditing = false;
        };

        const handleKeyDown = (e) => {
            if (!isEditing) return;

            if (e.key === 'Enter') {
                e.preventDefault();
                saveEdit();
            } else if (e.key === 'Escape') {
                e.preventDefault();
                senderInput.value = currentSenderEmail;
                saveEdit(); // Revert and exit edit mode
            }
        };

        // Remove any existing event listeners to prevent duplicates
        senderInput.removeEventListener('keydown', handleKeyDown);

        // Only add keydown listener, no blur listener
        senderInput.addEventListener('keydown', handleKeyDown);
    }

    // Email Sending
    async function sendEmail() {
        if (!recipients.length) {
            showNotification('Por favor, añade al menos un destinatario', 'error');
            return;
        }
        // Preferir pdf_path (archivo subido), con fallback a pdf_url (PDF generado)
        const pdfPath = sendEmailPanel?.dataset?.pdfPath || '';
        const hasPath = !!pdfPath;
        const hasUrl = !!currentPdfUrl;
        if (!hasPath && !hasUrl) {
            showNotification('Debes adjuntar un PDF o generar uno antes de enviar.', 'error');
            return;
        }

        const sendBtn = document.getElementById('sendEmailBtn');
        const originalText = sendBtn.innerHTML;

        try {
            // Show loading state
            sendBtn.disabled = true;
            sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';

            const response = await fetch(`${API_URL}/send_email`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    pdf_path: hasPath ? pdfPath : undefined,
                    pdf_url: !hasPath && hasUrl ? currentPdfUrl : undefined,
                    sender: (senderInput && isValidEmail(senderInput.value.trim())) ? senderInput.value.trim() : currentSenderEmail,
                    recipients: recipients.map(r => r.email),
                    subject: 'Revista de Convocatorias COTECMAR'
                })
            });

            const data = await response.json();

            if (response.ok) {
                showNotification('¡Correo enviado con éxito!', 'success');
                setTimeout(closePanel, 1500);
            } else {
                throw new Error(data.detail || 'Error al enviar el correo');
            }
        } catch (error) {
            console.error('Error sending email:', error);
            showNotification(error.message || 'Error al enviar el correo', 'error');
        } finally {
            sendBtn.disabled = false;
            sendBtn.innerHTML = originalText;
        }
    }

    // Upload helper (standalone)
    async function handleFile(file) {
        if (!file || (file.type && file.type !== 'application/pdf') || !/\.pdf$/i.test(file.name)) {
            showNotification('Por favor selecciona un archivo PDF válido.', 'error');
            return;
        }
        const formData = new FormData();
        formData.append('pdf_file', file);
        try {
            const res = await fetch(`${API_URL}/upload_pdf`, { method: 'POST', body: formData });
            if (!res.ok) throw new Error('Error al subir el archivo');
            const data = await res.json();
            if (sendEmailPanel) sendEmailPanel.dataset.pdfPath = data.pdf_path || '';
            // Toggle to preview UI
            if (fileDropArea) fileDropArea.classList.add('hidden');
            if (filePreview) {
                const nameEl = filePreview.querySelector('.file-name');
                if (nameEl) nameEl.textContent = file.name;
                filePreview.classList.remove('hidden');
            }
        } catch (err) {
            showNotification(err.message || 'Error al subir el archivo', 'error');
        }
    }

    // =======================================================
    // 2. ESTANDARIZACIÓN A sender / favorites
    // =======================================================
    async function loadEmailSettings() {
        try {
            const response = await fetch(`${API_URL}/email_settings`);
            if (!response.ok) throw new Error('No se pudo cargar la configuración.');

            const data = await response.json();
            console.log('Datos de email recibidos (estandarizados):', data);

            // Leemos solo las claves estándar, con fallback por compatibilidad
            currentSenderEmail = data.sender || data.sender_email || '';
            favorites = Array.isArray(data.favorites)
                ? data.favorites
                : (Array.isArray(data.favorite_emails) ? data.favorite_emails : []);

            if (senderInput) senderInput.value = currentSenderEmail;
            console.log('Favoritos cargados correctamente:', favorites);
        } catch (error) {
            console.error('Error cargando la configuración de email:', error);
            // Aplicar valores por defecto en caso de error
            currentSenderEmail = '';
            favorites = [];
            if (senderInput) senderInput.value = currentSenderEmail;
        }
    }

    async function saveEmailSettings() {
        try {
            await fetch(`${API_URL}/email_settings`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sender: currentSenderEmail,
                    favorites: favorites
                })
            });
        } catch (error) {
            console.error('Error saving email settings:', error);
        }
    }

    // Helper Functions
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function showNotification(message, type = 'info') {
        // You can implement a notification system here
        // For now, we'll just use alert
        alert(`${type.toUpperCase()}: ${message}`);
    }

    function addRecipientFromInput() {
        const email = recipientInput.value.trim();
        if (email) {
            addRecipient(email);
            recipientInput.value = '';
        }
    }

    // =======================================================
    //      FUNCIÓN openFavoritesModal() CON EL NUEVO ESTILO
    // =======================================================
    function openFavoritesModal() {
        const checklistContainer = document.getElementById('checklist');
        if (!favoritesModal || !checklistContainer) return;

        console.log('Abriendo modal de favoritos, el array es:', favorites);
        checklistContainer.innerHTML = ''; // Limpiar contenido anterior

        if (!favorites.length) {
            checklistContainer.innerHTML = '<p>No tienes correos favoritos guardados.</p>';
            favoritesModal.classList.remove('hidden');
            return;
        }

        // 1. Crear y añadir la opción "Seleccionar Todos" con el estilo personalizado
        const selectAllId = 'fav-check-all';
        const selectAllWrapper = document.createElement('div');
        selectAllWrapper.className = 'uv-checkbox-wrapper';
        selectAllWrapper.innerHTML = `
            <input type="checkbox" id="${selectAllId}" class="uv-checkbox" />
            <label for="${selectAllId}" class="uv-checkbox-label">
                <div class="uv-checkbox-icon">
                    <svg viewBox="0 0 24 24" class="uv-checkmark">
                        <path d="M4.1,12.7 9,17.6 20.3,6.3" fill="none"></path>
                    </svg>
                </div>
                <span class="uv-checkbox-text" style="font-weight: bold;">Seleccionar Todos</span>
            </label>
        `;
        checklistContainer.appendChild(selectAllWrapper);

        // Añadir un separador visual
        const separator = document.createElement('hr');
        separator.style.margin = '16px 0';
        separator.style.borderColor = '#e5e7eb';
        checklistContainer.appendChild(separator);

        // 2. Añadir cada favorito con el nuevo estilo, uno por uno
        favorites.forEach((email, index) => {
            const uniqueId = `fav-check-${index}`;
            const checkboxWrapper = document.createElement('div');
            checkboxWrapper.className = 'uv-checkbox-wrapper';

            // Estructura HTML para cada email
            checkboxWrapper.innerHTML = `
                <input type="checkbox" id="${uniqueId}" class="uv-checkbox" name="fav" value="${email}" />
                <label for="${uniqueId}" class="uv-checkbox-label">
                    <div class="uv-checkbox-icon">
                        <svg viewBox="0 0 24 24" class="uv-checkmark">
                            <path d="M4.1,12.7 9,17.6 20.3,6.3" fill="none"></path>
                        </svg>
                    </div>
                    <span class="uv-checkbox-text">${email}</span>
                </label>
            `;
            checklistContainer.appendChild(checkboxWrapper);
        });

        // 3. Añadir la lógica para que "Seleccionar Todos" funcione
        const selectAllCheckbox = document.getElementById(selectAllId);
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', (event) => {
                const isChecked = event.target.checked;
                // Seleccionar solo los checkboxes de favoritos usando el atributo 'name'
                const allFavoriteCheckboxes = checklistContainer.querySelectorAll('input[name="fav"]');
                allFavoriteCheckboxes.forEach(checkbox => {
                    checkbox.checked = isChecked;
                });
            });
        }

        // Mostrar el modal
        favoritesModal.classList.remove('hidden');
    }

    // Botón para añadir seleccionados del checklist (actualizado para más seguridad)
    const addFavoritesToRecipientsBtn = document.getElementById('addFavoritesToRecipients');
    if (addFavoritesToRecipientsBtn) {
        addFavoritesToRecipientsBtn.addEventListener('click', () => {
            // Usamos [name="fav"] para asegurar que solo tomamos los checkboxes de email
            // y no el de "Seleccionar Todos".
            const selected = document.querySelectorAll('#checklist input[name="fav"]:checked');
            if (selected.length === 0) {
                showNotification('Por favor, selecciona al menos un correo', 'warning');
                return;
            }

            selected.forEach(cb => {
                if (cb.value) {  // Asegurarse de que el valor no esté vacío
                    addRecipient(cb.value);
                }
            });

            // Cerrar el modal después de agregar
            favoritesModal.classList.add('hidden');

            // Mostrar notificación de éxito
            showNotification(`${selected.length} correo(s) agregado(s) a destinatarios`, 'success');
        });
    }

    init();

    // Export functions for use in other files
    window.emailModule = {
        openPanel,
        closePanel
    };
});

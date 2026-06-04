/**
 * image_upload.js
 * Dynamiczny upload obrazków — bez hardcodowanych slotów, bez duplikacji.
 * Użycie: initImageUpload(formElement, { maxFiles: 3, maxSizeMB: 4 })
 */
function initImageUpload(form, options = {}) {
    const MAX_FILES = options.maxFiles ?? 3;
    const MAX_SIZE  = (options.maxSizeMB ?? 4) * 1024 * 1024;

    // ── Budujemy kontener UI ─────────────────────────────────────────────────
    const container = document.createElement('div');
    container.className = 'img-upload-container';
    container.style.cssText = 'display:flex;align-items:flex-start;flex-wrap:wrap;gap:8px;margin-top:10px;';

    const addBtn = document.createElement('button');
    addBtn.type = 'button';
    addBtn.className = 'img-upload-add';
    addBtn.textContent = '+ Dodaj zdjęcie';
    addBtn.style.cssText = `
        background:#2b3a42;color:#fff;border:none;border-radius:4px;
        padding:6px 12px;cursor:pointer;font-size:13px;align-self:center;
        white-space:nowrap;
    `;

    const errorEl = document.createElement('span');
    errorEl.className = 'img-upload-error';
    errorEl.style.cssText = 'color:#c0392b;font-size:12px;display:none;width:100%;';

    container.appendChild(addBtn);

    // Wstawiamy kontener przed przyciskiem submit
    const submitBtn = form.querySelector('button[type="submit"]');
    form.insertBefore(container, submitBtn);
    form.insertBefore(errorEl, submitBtn);

    // ── Modal do powiększenia ─────────────────────────────────────────────────
    const modal = document.createElement('div');
    modal.style.cssText = `
        display:none;position:fixed;inset:0;background:rgba(0,0,0,.85);
        z-index:9999;justify-content:center;align-items:center;cursor:pointer;
    `;
    const modalImg = document.createElement('img');
    modalImg.style.cssText = 'max-width:90%;max-height:90%;object-fit:contain;border:2px solid #fff;border-radius:4px;';
    modal.appendChild(modalImg);
    document.body.appendChild(modal);
    modal.addEventListener('click', () => { modal.style.display = 'none'; modalImg.src = ''; });

    // ── Stan ──────────────────────────────────────────────────────────────────
    // Każdy slot: { file: File, inputEl: HTMLInputElement, wrapEl: HTMLElement }
    const slots = [];

    function showError(msg) {
        errorEl.textContent = msg;
        errorEl.style.display = 'block';
        setTimeout(() => { errorEl.style.display = 'none'; }, 4000);
    }

    function syncHiddenInputs() {
        // Usuwamy stare hidden inputy zarządzane przez nas
        form.querySelectorAll('input[data-upload-managed]').forEach(el => el.remove());

        // Dla każdego slotu tworzymy input z unikalną nazwą
        slots.forEach((slot, i) => {
            const name = i === 0 ? 'file' : `file${i + 1}`;
            const inp = document.createElement('input');
            inp.type = 'file';
            inp.name = name;
            inp.accept = 'image/*';
            inp.style.display = 'none';
            inp.dataset.uploadManaged = '1';

            // Przepisujemy plik do nowego inputa przez DataTransfer
            const dt = new DataTransfer();
            dt.items.add(slot.file);
            inp.files = dt.files;

            form.appendChild(inp);
        });
    }

    function updateAddBtn() {
        addBtn.style.display = slots.length < MAX_FILES ? 'inline-block' : 'none';
    }

    function removeSlot(index) {
        const slot = slots[index];
        slot.wrapEl.remove();
        slots.splice(index, 1);
        // Przenumeruj inputy
        syncHiddenInputs();
        updateAddBtn();
    }

    function createSlot(file) {
        if (file.size > MAX_SIZE) {
            showError(`Plik "${file.name}" jest za duży (max ${options.maxSizeMB ?? 4} MB).`);
            return;
        }
        if (slots.length >= MAX_FILES) {
            showError(`Możesz dodać maksymalnie ${MAX_FILES} zdjęcia.`);
            return;
        }

        const wrap = document.createElement('div');
        wrap.style.cssText = 'position:relative;display:inline-block;margin-right:4px;';

        const preview = document.createElement('img');
        preview.src = URL.createObjectURL(file);
        preview.alt = file.name;
        preview.style.cssText = 'height:150px;width:auto;object-fit:cover;border:2px solid #d4a017;display:block;cursor:zoom-in;';
        preview.addEventListener('click', () => {
            modalImg.src = preview.src;
            modal.style.display = 'flex';
        });

        const delBtn = document.createElement('button');
        delBtn.type = 'button';
        delBtn.innerHTML = '&times;';
        delBtn.title = 'Usuń';
        delBtn.style.cssText = `
            position:absolute;top:4px;right:4px;background:rgba(0,0,0,.6);
            color:#fff;border:none;border-radius:4px;width:22px;height:22px;
            font-size:14px;cursor:pointer;display:flex;align-items:center;
            justify-content:center;padding:0;z-index:10;line-height:1;
        `;

        wrap.appendChild(preview);
        wrap.appendChild(delBtn);

        const index = slots.length;
        const slot = { file, wrapEl: wrap };
        slots.push(slot);

        delBtn.addEventListener('click', () => {
            const i = slots.indexOf(slot);
            if (i !== -1) removeSlot(i);
        });

        // Wstawiamy wrap przed przyciskiem "dodaj"
        container.insertBefore(wrap, addBtn);
        syncHiddenInputs();
        updateAddBtn();
    }

    // ── Dodawanie przez kliknięcie w przycisk ────────────────────────────────
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';
    fileInput.multiple = true;
    fileInput.style.display = 'none';
    form.appendChild(fileInput);

    addBtn.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', () => {
        Array.from(fileInput.files).forEach(file => createSlot(file));
        fileInput.value = ''; // reset żeby można było dodać ten sam plik ponownie
    });

    // ── Drag & drop ──────────────────────────────────────────────────────────
    container.addEventListener('dragover', e => {
        e.preventDefault();
        container.style.outline = '2px dashed #d4a017';
    });
    container.addEventListener('dragleave', () => {
        container.style.outline = '';
    });
    container.addEventListener('drop', e => {
        e.preventDefault();
        container.style.outline = '';
        Array.from(e.dataTransfer.files)
            .filter(f => f.type.startsWith('image/'))
            .forEach(f => createSlot(f));
    });

    // ── Usuwamy stary input[name="file"] który był w HTML ───────────────────
    // (żeby nie kolidował z naszymi managed inputami)
    const oldInput = form.querySelector('input[name="file"]:not([data-upload-managed])');
    if (oldInput) oldInput.remove();
    const oldInput2 = form.querySelector('#p-input2, #r-input2');
    if (oldInput2) oldInput2.remove();
    const oldInput3 = form.querySelector('#p-input3, #r-input3');
    if (oldInput3) oldInput3.remove();

    updateAddBtn();
}

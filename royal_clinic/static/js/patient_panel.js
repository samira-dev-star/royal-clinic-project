 // Profile image preview
 document.getElementById('id_image_name').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profile-preview').src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
});



// مدیریت فرمست‌ها
let allergyFormCount = parseInt(document.getElementById('id_allergy-TOTAL_FORMS').value);
let historyFormCount = parseInt(document.getElementById('id_history-TOTAL_FORMS').value);

function addAllergyForm() {
    const container = document.getElementById('allergy-fields');
    const totalForms = document.getElementById('id_allergy-TOTAL_FORMS');
    const newForm = document.createElement('div');
    newForm.className = 'allergy-form mb-4 flex items-center gap-2';
    newForm.innerHTML = `
        <input type="hidden" name="allergy-${allergyFormCount}-id" id="id_allergy-${allergyFormCount}-id">
        <input type="text" name="allergy-${allergyFormCount}-title" 
               class="form-input w-full" 
               placeholder="مثال: پنی‌سیلین"
               id="id_allergy-${allergyFormCount}-title">
        <button type="button" onclick="removeForm(this, 'allergy')" 
                class="bg-red-500 text-white px-3 py-2 rounded-lg">
            <i class="fas fa-trash"></i>
        </button>
    `;
    container.appendChild(newForm);
    allergyFormCount++;
    totalForms.value = allergyFormCount;
}

function addMedicalHistoryForm() {
    const container = document.getElementById('history-fields');
    const totalForms = document.getElementById('id_history-TOTAL_FORMS');
    const newForm = document.createElement('div');
    newForm.className = 'history-form mb-4 border rounded p-4 shadow-sm';
    newForm.innerHTML = `
        <input type="hidden" name="history-${historyFormCount}-id" id="id_history-${historyFormCount}-id">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
            <div>
                <input type="text" name="history-${historyFormCount}-title" 
                       class="form-input w-full" 
                       placeholder="عنوان بیماری"
                       id="id_history-${historyFormCount}-title">
            </div>
            <div>
                <input type="number" name="history-${historyFormCount}-diagnosis_year" 
                       class="form-input w-full" 
                       placeholder="سال تشخیص"
                       id="id_history-${historyFormCount}-diagnosis_year">
            </div>
        </div>
        <div class="flex items-center gap-2">
            <textarea name="history-${historyFormCount}-description" 
                      class="form-input w-full" 
                      rows="2"
                      placeholder="توضیحات"
                      id="id_history-${historyFormCount}-description"></textarea>
            <button type="button" onclick="removeForm(this, 'history')" 
                    class="bg-red-500 text-white px-3 py-2 rounded-lg">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;
    container.appendChild(newForm);
    historyFormCount++;
    totalForms.value = historyFormCount;
}

function removeForm(button, formsetType) {
    const form = button.closest('.allergy-form, .history-form');
    if (formsetType === 'allergy') {
        allergyFormCount--;
        document.getElementById('id_allergy-TOTAL_FORMS').value = allergyFormCount;
    } else {
        historyFormCount--;
        document.getElementById('id_history-TOTAL_FORMS').value = historyFormCount;
    }
    form.remove();
}
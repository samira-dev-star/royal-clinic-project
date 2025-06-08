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
let medicationFormCount = parseInt(document.getElementById('id_medications-TOTAL_FORMS').value);

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




// افزودن فرم داروی جدید
function addMedicationForm() {
    const totalForms = document.getElementById('id_medicine-TOTAL_FORMS');
    const formNum = parseInt(totalForms.value);
    const container = document.getElementById('medication-fields');
    
    // Clone the first form (or create a new one if none exists)
    const newForm = document.querySelector('.medication-form') ? 
        document.querySelector('.medication-form').cloneNode(true) : 
        createNewMedicationForm();
    
    // Clear all input values in the new form
    const inputs = newForm.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.value = '';
        // Update name attributes to the new form number
        if (input.name) {
            input.name = input.name.replace(/-\d+-/, `-${formNum}-`);
            input.id = input.id.replace(/-\d+-/, `-${formNum}-`);
        }
    });
    
    // Add the new form to the container
    container.appendChild(newForm);
    
    // Update the total forms count
    totalForms.value = formNum + 1;
}

// ایجاد فرم جدید دارو (اگر فرمی برای کپی کردن وجود نداشت)
function createNewMedicationForm() {
    const form = document.createElement('div');
    form.className = 'medication-form mb-4 border rounded p-4 shadow-sm';
    form.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">نام دارو</label>
                <input type="text" name="medicine-__prefix__-medication_name" class="form-input w-full" placeholder="نام دارو">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">دوز مصرف</label>
                <input type="text" name="medicine-__prefix__-dosage" class="form-input w-full" placeholder="دوز مصرف">
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">تاریخ شروع مصرف</label>
                <input type="text" name="medicine-__prefix__-priscribed_at" class="form-input w-full jalali-datepicker" placeholder="مثال : 1400/01/01">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">وضعیت استفاده</label>
                <select name="medicine-__prefix__-using_state" class="form-input w-full">
                    <option value="still_using">در حال استفاده</option>
                    <option value="stopped">قطع مصرف</option>
                </select>
            </div>
        </div>
        <div class="flex justify-end mt-2">
            <button type="button" onclick="removeForm(this, 'medication')" class="bg-red-500 text-white px-3 py-2 rounded-lg">
                <i class="fas fa-trash"></i> حذف
            </button>
        </div>
        <input type="hidden" name="medicine-__prefix__-id" id="id_medicine-__prefix__-id">
    `;
    return form;
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

// function removeForm(button, formsetType) {
//     const form = button.closest(`.${formsetType}-form`);
//     if (!form) return;

//     const totalFormsInput = document.getElementById(`id_${formsetType}-TOTAL_FORMS`);
//     let totalForms = parseInt(totalFormsInput.value);

//     if (totalForms > 0) {
//         totalForms--;
//         totalFormsInput.value = totalForms;
//         form.remove();
//     }
// }


function removeForm(button, formType) {
    const form = button.closest(`.${formType}-form`);
    const container = document.getElementById(`${formType}-fields`);
    const totalForms = document.getElementById(`id_${formType}-TOTAL_FORMS`);
    
    // If this is an existing form (not new), mark it for deletion
    const deleteInput = form.querySelector(`input[name$="-DELETE"]`);
    if (deleteInput) {
        deleteInput.value = 'on';
        form.style.display = 'none'; // Hide instead of remove
    } else {
        // For new forms that haven't been saved yet
        form.remove();
        totalForms.value = parseInt(totalForms.value) - 1;
    }
}






// --------------------------------------------------------------------------------

// django_jalali.js (مثال ساده شده)
(function($) {
    $(document).ready(function() {
        // تبدیل تاریخ به شمسی برای datepicker
        if ($.fn.datepicker) {
            $.datepicker.regional['fa'] = {
                closeText: 'بستن',
                prevText: 'قبلی',
                nextText: 'بعدی',
                currentText: 'امروز',
                monthNames: ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'],
                monthNamesShort: ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'],
                dayNames: ['یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه'],
                dayNamesShort: ['یک', 'دو', 'سه', 'چهار', 'پنج', 'جمعه', 'شنبه'],
                dayNamesMin: ['ی', 'د', 'س', 'چ', 'پ', 'ج', 'ش'],
                weekHeader: 'هفته',
                dateFormat: 'yy/mm/dd',
                firstDay: 6,
                isRTL: true,
                showMonthAfterYear: false,
                yearSuffix: ''
            };
            $.datepicker.setDefaults($.datepicker.regional['fa']);
        }
    });
})(django.jQuery);
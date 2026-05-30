// обновление слайдера
function updateSlider(slider, spanId, unit) {
    let percent = (slider.value - slider.min) / (slider.max - slider.min) * 100;

    // 🎨 градиент
    slider.style.background =
        `linear-gradient(to right, #2ecc71 ${percent}%, #ddd ${percent}%)`;

    // 🔢 значение + единицы
    document.getElementById(spanId).innerText = slider.value + " " + unit;
}


// инициализация
function init() {
    const sliders = [
        {id: "lamp_count", span: "lamp_val", unit: "шт."},
        {id: "bulb_hours", span: "bulb_val", unit: "ч."},
        {id: "tv_hours", span: "tv_val", unit: "ч."},
        {id: "pc_hours", span: "pc_val", unit: "ч."}
    ];

    sliders.forEach(item => {
        let slider = document.getElementById(item.id);

        if (!slider) return; // защита от ошибок

        // при движении
        slider.addEventListener("input", () => {
            updateSlider(slider, item.span, item.unit);
        });

        // при загрузке
        updateSlider(slider, item.span, item.unit);
    });
}

// запуск
window.onload = init;
// Элемент select для марок автомобилей
const brandSelect = document.getElementById("brand-select");
const modelSelect = document.getElementById("model-select");

// URL API для получения списка марок
const apiUrl = "http://127.0.0.1:8000/selects/cars"; // Замените на ваш API-адрес

// Функция для загрузки данных из API
async function fetchCarBrands() {
  try {
    const response = await fetch(apiUrl);
    if (!response.ok) {
      throw new Error("Ошибка при загрузке данных");
    }

    const json_q = await response.json(); // Предполагается, что API возвращает массив брендов
    let brands = new Set();
    let models = new Set()

    json_q.forEach((json_1) =>{
      brands.add(json_1[4])
      models.add(json_1[4] + ', ' +json_1[3])
    })
    console.log(brands, models)
    populateBrands(brands);
    populateModels(models);
  } catch (error) {
    console.error("Ошибка:", error);
    brandSelect.innerHTML = `<option>Ошибка загрузки</option>`;
  }
}

// Функция для добавления опций в select
function populateBrands(brands) {
  brandSelect.innerHTML = '<option>Выберите марку</option>'; // Сбрасываем содержимое
  brands.forEach((brand) => {
    const option = document.createElement("option");
    option.textContent = brand; // Отображаемое имя марки
    brandSelect.appendChild(option);
  });
}

function populateModels(models) {
  modelSelect.innerHTML = '<option>Выберите модель</option>'; // Сбрасываем содержимое
  models.forEach((model) => {
    const option = document.createElement("option");
    option.textContent = model; // Отображаемое имя марки
    modelSelect.appendChild(option);
  });
}

// Загружаем данные при загрузке страницы
document.addEventListener("DOMContentLoaded", fetchCarBrands);

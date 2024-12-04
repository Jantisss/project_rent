// Элемент select для марок автомобилей
const brandSelect = document.getElementById("brand-select");
const modelSelect = document.getElementById("model-select");
const modelSelect2 = document.getElementById("model-select2");

const carsList    = document.getElementById("list-car");

// URL API для получения списка марок
const apiUrl = "http://127.0.0.1:8000/selects/cars"; // Замените на ваш API-адрес

// Функция для загрузки данных из API
async function fetchCarBrands() {
  try {
    const response = await fetch(apiUrl);
    if (!response.ok) {
      throw new Error("Ошибка при загрузке данных");
    }

    const json_q = await response.json();
    let brands = new Set();
    let models = new Set()

    json_q.forEach((json_1) =>{
      brands.add(json_1[4])
      models.add(json_1[4] + ', ' +json_1[3])
    })
    console.log(brands, models)
    populateBrands(brands);
    populateModels(models);
    populateCars(json_q);

    brandSelect.addEventListener('change', () => filterCars_brand(json_q))
    
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
  modelSelect2.innerHTML = '<option>Выберите модель</option>'; // Сбрасываем содержимое
  models.forEach((model) => {
    const option = document.createElement("option");
    const option2 = document.createElement("option");
    option.textContent = model; // Отображаемое имя марки
    option2.textContent = model; // Отображаемое имя марки
    modelSelect.appendChild(option);
    modelSelect2.appendChild(option2);
  });
}

function populateCars(data) {
  carsList.innerHTML = "";
  data.forEach(car => {
    //if (carsList.lastChild) {carsList.removeChild()}
    //carsList.removeChild()
    
    const carCard = document.createElement("div");
    carCard.classList.add("border", "p-4", "rounded-md");
    carCard.innerHTML = `
      <img src=${car[6]} alt=${car[3]} class="w-full h-[150px] object-cover rounded-md mb-4">
      <h4 class="text-lg text-neutral-950">${car[4]} ${car[3]}</h4>
      <p class="text-neutral-600">VIN: ${car[1]}</p>
      <p class="text-neutral-600">Рег. номер: ${car[2]}</p>
      <p class="${car[5] === 'Available' ? 'text-green-500' : 'text-red-500'}">${car[5] === 'Available' ? "Доступно" : "Занято"}</p>
    `;
    carsList.appendChild(carCard);
  });
}

function filterCars_brand(data) {
  
  brandItem = data;

  const select_brand = brandSelect.value
  let filtered_brands;

  if (select_brand === 'Выберите марку'){
    filtered_brands = brandItem;
    console.log("aaa", filtered_brands);

  } else {
    filtered_brands = brandItem.filter(car => car[4] === select_brand);
    console.log("bbb");

  }
  
  populateCars(filtered_brands);

}
// Загружаем данные при загрузке страницы
document.addEventListener("DOMContentLoaded", fetchCarBrands);

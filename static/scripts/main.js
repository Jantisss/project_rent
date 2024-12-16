// Элемент select для марок автомобилей
const brandSelect  = document.getElementById("brand-select");
const modelSelect  = document.getElementById("model-select");
const modelSelect2 = document.getElementById("model-select2");
const statusSelect = document.getElementById("status");
const carsList     = document.getElementById("list-car");
const officeSelect = document.getElementById("office-select");
// const phoneInput   = document.getElementById('phone-number');
const phoneInput = document.querySelector('#phone-number');

// URL API для получения списка марок
const apiUrl = "http://127.0.0.1:8000/"; // Замените на ваш API-адрес

phoneInput.addEventListener('input', function (e) {
  var sel_end;
  const input = e.target;
  console.log(e.inputType, e, input.value, input.value.lenght)
  let value = input.value.replace(/\D/g, '');
  console.log(input.selectionStart);
  // Оставляем максимум 10 цифр (для подстановки в шаблон после +7)
  
  

  var template = '+7 (___) ___-__-__';
  let formattedValue = '';
  let index = 0;

  if (e.data !== '7' && String(input.value).length === 1) value = value.substring(0, 11);
  else value = value.substring(1, 11);

  if (e.inputType === 'deleteContentBackward') {
    if (input.value.substring(input.selectionStart).replace(/\D/g, '')) {
      sel_end = input.selectionEnd;
    }
    if ([0,1,2,3].includes(input.selectionStart)) {e.preventDefault(); return};
    console.log("f",input.selectionStart);
    if ([7,8].includes(input.selectionStart)) {
      console.log("G  ")
      value = value.substring(0,2)+value.substring(3,value.lenght);
      console.log('ok',value.substring(0,2), value.substring(4,value.lenght));
      sel_end = 6;
    }
    if ([12].includes(input.selectionStart)) {
      console.log("G  ")
      value = value.substring(0,5)+value.substring(6,value.lenght);
      console.log('ok',value.substring(0,2), value.substring(4,value.lenght));
      sel_end = 11;
    }
    if ([15].includes(input.selectionStart)) {
      console.log("G  ")
      value = value.substring(0,7)+value.substring(8,value.lenght);
      console.log('ok',value.substring(0,2), value.substring(4,value.lenght));
      sel_end = 14;
    }
    
  }

  if (e.inputType === 'insertText') {
    if (input.value.substring(input.selectionStart).replace(/\D/g, '')) {
      sel_end = input.selectionStart;
    }
  }

  
  for (let char of template) {
    if (char === '_') {
      if (value[index]) {
        formattedValue += value[index++];
      } else {
        break;
      }
    } else if (value[index]){
      formattedValue += char;
    }
  }

  input.value = formattedValue;
  input.selectionEnd = sel_end ? sel_end : input.selectionEnd;
  console.log("END", input.selectionEnd)
});

phoneInput.addEventListener('keydown', function (e) {
  const allowedKeys = ['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab'];
  
  // Разрешаем ввод только цифр или перечисленных служебных клавиш
  if (!allowedKeys.includes(e.key) && !/\d/.test(e.key)) {
    e.preventDefault();
  }
});

// Функция для загрузки данных из API
async function fetchCarBrands() {
  try {
    const response_cars = await fetch(apiUrl.concat("selects/cars"));
    if (!response_cars.ok) {
      throw new Error("Ошибка при загрузке данных");
    }
    const response_office = await fetch(apiUrl.concat("selects/address_pickup"));
    if (!response_office.ok) {
      throw new Error("Ошибка при загрузке данных");
    }

    const json_pickup = await response_office.json();
    const json_q = await response_cars.json();
    let brands, models;
    brands = json_2_bm(json_q)[0];
    models = json_2_bm(json_q)[1];
    console.log(brands, models)
    populateBrands(brands);
    // populateModels(models);
    populateModels(json_q);
    populateCars(json_q);
    populateOffice(json_pickup);

    brandSelect.addEventListener('change', () => filter(json_q, 'b'))
    modelSelect.addEventListener('change', () => filter(json_q, 'm'))
    statusSelect.addEventListener('change', () => filter(json_q, 's'))

    
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

function populateModels(data) {
  modelSelect.innerHTML = '<option>Выберите модель</option>'; // Сбрасываем содержимое
  modelSelect2.innerHTML = '<option>Выберите модель</option>'; // Сбрасываем содержимое
  data.forEach((dat) => {
    const option = document.createElement("option");
    const option2 = document.createElement("option");
    option.textContent = `${dat[3]}, reg: ${dat[2]}`; // Отображаемое имя марки
    option.value = dat[0];
    option2.textContent = `${dat[3]}, reg: ${dat[2]}`; // Отображаемое имя марки
    option2.value = dat[0];
    modelSelect.appendChild(option);
    modelSelect2.appendChild(option2);
  });
}

function populateOffice(office) {
  officeSelect.innerHTML = '<option>Выберите офис</option>'; // Сбрасываем содержимое
  
  office.forEach((office) => {
    const option = document.createElement("option");
    option.value = office[0];
    option.textContent = `${office[0]}. ${office[1]}, ${office[4]}`; // Отображаемое названия офиса
    officeSelect.appendChild(option);
    
  });
}

function populateCars(data) {
  carsList.innerHTML = "";
  data.forEach(car => {
    //if (carsList.lastChild) {carsList.removeChild()}
    //carsList.removeChild()
    
    const carCard = document.createElement("div");
    carCard.id = car[0]
    
    carCard.classList.add("border", "p-4", "rounded-md");
    carCard.innerHTML = `
      <img src='static/images/${car[1]}.png' alt=${car[3]} class="w-full h-[200px] object-cover rounded-md mb-4">
      <h4 class="text-lg text-neutral-950">${car[4]} ${car[3]}</h4>
      <p class="text-neutral-600">VIN: ${car[1]}</p>
      <p class="text-neutral-600">Рег. номер: ${car[2]}</p>
      <p id="cost_car_list_${car[0]}" value = ${car[6]} class="text-neutral-600">Стоимость/день: ${car[6]}</p>
      <p class="${car[5] === 'Available' ? 'text-green-500' : 'text-red-500'}">${car[5] === 'Available' ? "Доступно" : "Занято"}</p>
    `;
    
    carsList.appendChild(carCard);
  });
}

function json_2_bm(json) {
    var brands = new Set();
    var models = new Set()

    json.forEach((json_1) =>{
      brands.add(json_1[4])
      models.add(json_1[3])
    })
    console.log(brands,models);
  return [brands, models]
}

function filterCars_brand(data, flag) {
  
  brandItem = data;

  const select_brand = brandSelect.value
  let filtered_brands;

  if (select_brand === 'Выберите марку'){
    filtered_brands = brandItem;
    console.log("aaa", filtered_brands);

  } else {
    filtered_brands = brandItem.filter(car => car[4] === select_brand);
    console.log("bbb", select_brand);

  }
  if (flag) {
    // filtered_models = json_2_bm(filtered_brands)[1];
    // populateModels(filtered_models);
    filterCars_model(filtered_brands);
    console.log("flagactiv");
  }
  
  return filtered_brands;
}

function filterCars_model(data) {
  
  modelsItem = data;
  

  const select_model = modelSelect.value
  

  let filtered_models;
  console.log(data, select_model);

  if (select_model === 'Выберите модель'){
    filtered_models = modelsItem;
    console.log("aaa", filtered_models);

  } else {
    filtered_models = modelsItem.filter(car => car[0] == select_model);
    console.log("bbb", filtered_models, brandSelect.value, modelSelect.value, modelsItem);
  } 
  
  populateModels(filtered_models);
  return filtered_models;
}

function filterStatus(data) {
  Item = data;
  const select_status_1 = statusSelect.value
  let select_status = select_status_1;

  if (select_status_1 === 'Доступен') select_status = 'Available';
  else if ((select_status_1 === 'Арендован')) select_status = 'Rented';
  else if ((select_status_1 === 'На ремонте')) select_status = 'In Service';

  let filtered_data;
  console.log(data, select_status);

  if (select_status === 'Статус'){
    filtered_data = Item;
    console.log("aaa", filtered_data);

  } else {
    filtered_data = Item.filter(car => car[5] === select_status);
    console.log("bbb", filtered_data);
  }
  return filtered_data;
}

function filter(data, flag) {
  let fl_b = false;
  console.log("flag = ", flag);
  if (flag === 'b') fl_b = true;
  let filtered_brand = filterCars_brand(data, fl_b);
  let filtered_status = filterStatus(filtered_brand);
  let filtered_models = filterCars_model(filtered_status);
  
 
  
  populateCars(filtered_models);
}
// Загружаем данные при загрузке страницы
document.addEventListener("DOMContentLoaded", fetchCarBrands);

document.getElementById('order-form').addEventListener('submit', async function(event) {
  event.preventDefault(); // Предотвращаем стандартную отправку формы

  // Получаем значения из полей формы
  const carSelect = document.getElementById('model-select2');
  const carId = carSelect.value;
  const dateStart = document.getElementById('start-date').value;
  const dateEnd = document.getElementById('end-date').value;
  const officeSelect = document.getElementById('office-select');
  const officeId = officeSelect.value;
  const phoneNumber = document.getElementById('phone-number').value;

  // Валидация данных (дополнительно)
  if (!carId || !dateStart || !dateEnd || !officeId || !phoneNumber) {
    displayMessage('Пожалуйста, заполните все поля формы.', 'error');
    return;
  }

  // Допустим, user_id получен из сессии или другого источника
  const userId = getUserId(phoneNumber); // Вам нужно реализовать эту функцию

  // Определите стоимость за день (например, на основе выбранного автомобиля)
  const costDay = getCostPerDay(carId); // Вам нужно реализовать эту функцию

  // Создаем объект данных для отправки
  const orderData = {
    car_id: parseInt(carId),
    user_tel: parseInt(userId),
    cost_day: parseFloat(costDay),
    date_s: dateStart,
    date_e: dateEnd,
    office_id: parseInt(officeId)
  };

  try {
    console.log('test', JSON.stringify(orderData))
    const response = await fetch(apiUrl.concat("create_order"), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(orderData)
    });

    

    if (response.ok) {
      const result = await response.json();
      displayMessage(result.message, 'success');
      // Дополнительно: сбросить форму
      document.getElementById('order-form').reset();
    } else {
      const error = await response.json();
      displayMessage(error.detail || 'Ошибка при создании заказа.', 'error');
    }
  } catch (error) {
    console.error('Ошибка:', error);
    displayMessage('Произошла ошибка при отправке запроса.', 'error');
  }
});

// Функция для отображения сообщений пользователю
function displayMessage(message, type) {
  const messageDiv = document.getElementById('message');
  messageDiv.textContent = message;
  messageDiv.className = ''; // Сброс классов
  if (type === 'success') {
    messageDiv.classList.add('text-green-500');
  } else if (type === 'error') {
    messageDiv.classList.add('text-red-500');
  }
}

// Пример функции для получения user_id
function getUserId(Number) {
  
  // Реализуйте логику получения ID пользователя, например, из куки или локального хранилища
  // Для примера вернем фиксированное значение
  return Number.replace(/\D/g, '');
}

// Пример функции для получения стоимости за день
function getCostPerDay(carId) {
  car = document.getElementById(`cost_car_list_${carId}`);
  console.log("cost",car, car.getAttribute('value'), `cost_car_list_${carId}`);
  return car.getAttribute('value');
}

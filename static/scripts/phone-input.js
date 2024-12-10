const phoneInput = document.getElementById('phone-number');
console.log("OK")
  phoneInput.addEventListener('input', function (e) {
    
    const input = e.target;
    const value = input.value.replace(/\D/g, ''); // Удалить все символы, кроме цифр
    const template = '+7 (___) ___-__-__';
    let formattedValue = '';
    let index = 0;

    for (let char of template) {
      if (char === '_') {
        if (value[index]) {
          formattedValue += value[index++];
        } else {
          break;
        }
      } else {
        formattedValue += char;
      }
    }

    input.value = formattedValue;
  });

  phoneInput.addEventListener('keydown', function (e) {
    // Запрет ввода любых символов, кроме цифр, Backspace и Delete
    if (
      !(
        e.key.match(/\d/) || // Цифры
        e.key === 'Backspace' ||
        e.key === 'Delete' ||
        e.key === 'ArrowLeft' ||
        e.key === 'ArrowRight'
      )
    ) {
      e.preventDefault();
    }
  });
(function () {
    // 💬 Создаём кнопку
    const button = document.createElement('div');
    button.innerHTML = '💬';
    button.style.position = 'fixed';
    button.style.bottom = '20px';
    button.style.right = '20px';
    button.style.width = '60px';
    button.style.height = '60px';
    button.style.backgroundColor = '#007bff';
    button.style.color = '#fff';
    button.style.borderRadius = '50%';
    button.style.display = 'flex';
    button.style.alignItems = 'center';
    button.style.justifyContent = 'center';
    button.style.fontSize = '24px';
    button.style.cursor = 'pointer';
    button.style.zIndex = '9999';
    button.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';
    button.title = "Ask AI Assistant";

    document.body.appendChild(button);

    // 💬 Создаём iframe, но скрытый
    const iframe = document.createElement('iframe');
    iframe.src = 'https://your-server.com/static/chat.html'; // ⛔ ЗАМЕНИ на свой адрес!
    iframe.style.position = 'fixed';
    iframe.style.bottom = '90px';
    iframe.style.right = '20px';
    iframe.style.width = '400px';
    iframe.style.height = '500px';
    iframe.style.border = 'none';
    iframe.style.borderRadius = '12px';
    iframe.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';
    iframe.style.zIndex = '9999';
    iframe.style.display = 'none';

    document.body.appendChild(iframe);

    // 🧠 Переключаем показ чата
    let visible = false;
    button.onclick = function () {
        visible = !visible;
        iframe.style.display = visible ? 'block' : 'none';
    };
})();

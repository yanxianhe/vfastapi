// 自执行函数
(async function () {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = '/static/crypto-js/crypto-js.min.js';
    document.head.appendChild(script);
})();

// 定义 encryptPassword 函数，确保在自执行函数之前可用
async function encryptPassword(user, password) {
    const secret_key = await fetchSecretKey(user);
    const encryptedPassword = CryptoJS.AES.encrypt(password, secret_key).toString();
    return encryptedPassword;
}

// 定义 fetchSecretKey 函数
async function fetchSecretKey(userId) {
    const response = await fetch(`http://www.codeskulptor.org/user_secret_key?user=${userId}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch secret key: ${response.status}`);
    }
    const data = await response.json();
    return data.secret_key;
}
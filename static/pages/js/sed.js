// 定义URL的各个部分
const ipAddress = 'http://127.0.0.1:8000'; // 你的IP地址，测试使使用生产禁用
const prefix = ''; // API 前缀

/**
 * 登录并获取令牌
 *
 * @param uri api 地址，只传请求参数即可，例如 '/api/v1/login'
 * @param method 请求方法，例如 'POST'
 * @param data 请求数据
 * @returns 令牌
 * @throws 错误信息
 */
async function loginAndGetToken(uri, method, data) {
    const url = `${ipAddress}${prefix}${uri}`;
    try {
        const response = await sendAjaxRequest(url, method, data);
        // 假设响应数据中包含token字段
        const token = response.token;
        // 保存token到localStorage
        localStorage.setItem('apiToken', token);

        // 返回token，以便在需要的地方使用
        return token;
    } catch (error) {
        console.error('Error while logging in:', error);
        throw error;
    }
}
async function sendRequestWithToken(uri, method, data) {
    const url = `${ipAddress}${prefix}${uri}`;
    // 检查localStorage中是否有token
    const token = localStorage.getItem('apiToken');
    if (!token) {
        throw new Error('No token found in localStorage. Please login first.');
    }
    try {
        const response = await sendAjaxRequest(url, method, data);
        return response;
    } catch (error) {
        if (error.message.includes('401')) { // 假设401错误表示token失效
            // 清除旧的token
            localStorage.removeItem('apiToken');
            // 这里可以调用loginAndGetToken来重新获取token，但通常会在前端做重定向到登录页面
            throw new Error('Token expired. Please login again.');
        }
        console.error('Error while sending request with token:', error);
        throw error;
    }
}

async function sendAjaxRequest(uri, method, data) {
    const url = `${ipAddress}${prefix}${uri}`;
    const token = localStorage.getItem('apiToken');
    // 封装请求头生成逻辑
    const getHeaders = (method, token) => {
        const headers = {
            'Content-Type': method === 'POST' ? 'application/json' : 'application/x-www-form-urlencoded'
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    };

    // 封装请求发送逻辑
    const fetchData = async (url, method, headers, body) => {
        const response = await fetch(url, {
            method: method,
            headers: headers,
            body: body
        });

        // 检查响应状态码
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // 解析响应为JSON
        return await response.json();
    };

    try {
        const headers = getHeaders(method, token);
        const body = method === 'POST' ? JSON.stringify(data) : null;
        return await fetchData(url, method, headers, body);
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}
async function sendAsyncHttpRequest(uri, method, data, inputHeaders) {
    const url = `${ipAddress}${prefix}${uri}`;
    const token = localStorage.getItem('apiToken');

    // 封装请求头发送逻辑，避免修改原始headers对象
    const getHeaders = (method, token, inputHeaders = {}) => {
        const headers = { ...inputHeaders };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    };

    // 封装请求发送逻辑
    const fetchData = async (url, method, headers, body) => {
        const response = await fetch(url, {
            method: method,
            headers: headers,
            body: body,
            credentials: 'same-origin'  // 根据需要添加，确保cookie等凭证被发送
        });

        // 检查响应状态码
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        try {
            return await response.json();
        } catch (jsonParseError) {
            console.error('Failed to parse JSON response:', jsonParseError);
            throw new Error('Invalid JSON response');
        }
    };

    try {
        const headers = getHeaders(method, token, inputHeaders);
        let body = null;
        if (method === 'POST' || method === 'PUT') {
            body = JSON.stringify(data);
        }
        return await fetchData(url, method, headers, body);
    } catch (error) {
        console.error('Request failed:', error);
        throw error;
    }
}
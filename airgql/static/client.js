const resultElement = document.getElementById('result')
const client = io('http://127.0.0.1:3000')
let clientid = null;

client.on('register', (id) => {
    clientid = id;
});

client.on('notify', (result) => {
    console.log('recived resutl ' + result)
    resultElement.textContent = result;
});

document.querySelector('button').onclick = () => {
    const request = new XMLHttpRequest();
    // POST to h
    request.open('POST', '/notifier', true);
    request.setRequestHeader(
        'Content-Type',
        'application/x-www-form-urlencoded; charset=utf-8');
    request.onload = () => {
        resultElement.textContent = request.responseText;
    };
    // Request payload e.g. clientid=u6FYobd8JiuhXfC3AAAB
    // Form data e.g. clientid: u6FYobd8JiuhXfC3AAAB
    request.send('clientid=' + clientid);
};
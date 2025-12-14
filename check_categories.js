const http = require('http');

const options = {
    hostname: 'localhost',
    port: 8000,
    path: '/api/discussions/categories/',
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    }
};

const req = http.request(options, (res) => {
    console.log(`Status Code: ${res.statusCode}`);
    let body = '';
    res.on('data', (d) => body += d);
    res.on('end', () => console.log(`Response: ${body}`));
});

req.on('error', (error) => {
    console.error(`Error: ${error.message}`);
});

req.end();

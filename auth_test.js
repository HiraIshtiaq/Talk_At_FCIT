const http = require('http');

const data = JSON.stringify({
    email: "shayan@pucit.edu.pk",
    password: "emaan@123"
});

const options = {
    hostname: 'localhost',
    port: 8000,
    path: '/api/auth/login/',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
    }
};

const req = http.request(options, (res) => {
    console.log(`Login Status Code: ${res.statusCode}`);
    let body = '';
    res.on('data', (d) => body += d);
    res.on('end', () => {
        console.log(`Login Response: ${body}`);
        if (res.statusCode === 200) {
            const token = JSON.parse(body).access;

            const profileOptions = {
                hostname: 'localhost',
                port: 8000,
                path: '/api/auth/me/',
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            };

            const req2 = http.request(profileOptions, (res2) => {
                console.log(`Profile Status Code: ${res2.statusCode}`);
                let body2 = '';
                res2.on('data', (d) => body2 += d);
                res2.on('end', () => {
                    const user = JSON.parse(body2);
                    console.log(`User Name: '${user.first_name}' '${user.last_name}'`);
                    console.log(`Full Profile: ${body2}`);
                });
            });
            req2.end();
        }
    });
});

req.on('error', (error) => {
    console.error(`Error: ${error.message}`);
});

req.write(data);
req.end();

const http = require('http');

// 1. Get Token
const loginData = JSON.stringify({
    email: "shayan@pucit.edu.pk",
    password: "emaan@123"
});

const loginOptions = {
    hostname: 'localhost',
    port: 8000,
    path: '/api/auth/login/',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': loginData.length
    }
};

const loginReq = http.request(loginOptions, (res) => {
    let body = '';
    res.on('data', (d) => body += d);
    res.on('end', () => {
        if (res.statusCode === 200) {
            const token = JSON.parse(body).access;
            console.log("Got token via script. Seeding categories...");
            seedCategories(token);
        } else {
            console.error("Login failed:", body);
        }
    });
});
loginReq.write(loginData);
loginReq.end();

function seedCategories(token) {
    const categories = [
        { name: "General Discussion", slug: "general", description: "General topics" },
        { name: "Academics", slug: "academics", description: "Course work and exams" },
        { name: "Events", slug: "events", description: "Campus events" },
        { name: "Tech Talk", slug: "tech", description: "Programming and tech" }
    ];

    categories.forEach(cat => {
        const catData = JSON.stringify(cat);
        const catOptions = {
            hostname: 'localhost',
            port: 8000,
            path: '/api/discussions/categories/',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
                'Content-Length': catData.length
            }
        };

        const req = http.request(catOptions, (res) => {
            let body = '';
            res.on('data', (d) => body += d);
            res.on('end', () => {
                console.log(`Created ${cat.name}: ${res.statusCode}`);
                if (res.statusCode !== 201) console.log(body);
            });
        });
        req.write(catData);
        req.end();
    });
}

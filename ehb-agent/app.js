const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const path = require('path');

const app = express();
const PORT = 4000;

app.use(helmet());
app.use(compression());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/health', (req, res) => {
    res.json({
        status: 'OK',
        message: 'EHB-Agent Platform running on port 4000',
        timestamp: new Date().toISOString()
    });
});

app.get('/', (req, res) => {
    res.send('<h1> EHB-Agent Platform</h1><p>Running on Port 4000</p><a href="/health">Health Check</a>');
});

app.listen(PORT, () => {
    console.log(' EHB-Agent Platform running on port 4000');
    console.log(' Main App: http://localhost:4000');
    console.log('===============================================');
});

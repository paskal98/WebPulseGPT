const express = require('express');
const esprima = require('esprima');

const app = express();
const PORT = 3210;

app.use(express.json());

app.post('/parse', (req, res) => {
    const { code } = req.body;
    console.log(code)
    try {
        const ast = esprima.parseScript(code);
        res.json(ast);
    } catch (error) {
        res.status(400).json({ error: 'Failed to parse JavaScript code' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

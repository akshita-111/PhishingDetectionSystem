const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, 'index.html');
const publicDir = path.join(__dirname, 'public');
const outPath = path.join(publicDir, 'index.html');

let content = fs.readFileSync(indexPath, 'utf8');

// Read REACT_APP_API_URL from environment variables, defaulting to deployed endpoint
let apiUrl = process.env.REACT_APP_API_URL || 'https://akshita118-phishing-orchestrator.hf.space';

console.log('Injecting API URL:', apiUrl);
content = content.replace(
    /const ORCHESTRATOR_API_URL = '.*';/,
    `const ORCHESTRATOR_API_URL = '${apiUrl}';`
);

// Create public directory and write the file
if (!fs.existsSync(publicDir)){
    fs.mkdirSync(publicDir);
}
fs.writeFileSync(outPath, content, 'utf8');
console.log('Successfully generated public/index.html with injected API URL');

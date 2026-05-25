const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, 'index.html');
let content = fs.readFileSync(indexPath, 'utf8');

// Read REACT_APP_API_URL from environment variables, defaulting to local endpoint
const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8080';

console.log('Injecting API URL:', apiUrl);
content = content.replace(
    /const API_BASE_URL = '.*';/,
    `const API_BASE_URL = '${apiUrl}';`
);

fs.writeFileSync(indexPath, content, 'utf8');
console.log('Successfully injected API URL into index.html');

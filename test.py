File 1: vulnerable_app.py (Semgrep + Gitleaks)
import sqlite3
import os
from flask import Flask, request, render_template_string
app = Flask(__name__)
# HARDCODED SECRETS (Gitleaks will catch)
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
GITHUB_TOKEN = "ghp_1234567890abcdef1234567890abcdef12345678"
DB_PASSWORD = "SuperSecret123!@prod"
@app.route('/search')
def search():
    # SQL Injection (Semgrep will catch)
    user_input = request.args.get('q')
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    cursor.execute(query)
    return str(cursor.fetchall())
@app.route('/exec')
def execute():
    # Command Injection (Semgrep will catch)
    cmd = request.args.get('cmd')
    os.system("ping -c 3 " + cmd)
    return "Done"
@app.route('/eval')
def run_eval():
    # Dangerous eval (Semgrep will catch)
    return str(eval(request.args.get('data')))
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
File 2: package.json (Trivy will catch vulnerable deps)
{
  "name": "vulnerable-test-app",
  "version": "1.0.0",
  "dependencies": {
    "lodash": "4.17.20",
    "express": "4.17.1",
    "axios": "0.21.1",
    "minimist": "1.2.5",
    "jsonwebtoken": "8.5.1"
  }
}
File 3: vulnerable.js (Semgrep XSS + more)
const express = require('express');
const app = express();
app.get('/render', (req, res) => {
  // XSS - Semgrep will catch
  const user = req.query.name;
  res.send('<h1>Hello ' + user + '</h1>');
});
app.get('/redirect', (req, res) => {
  // Open Redirect - Semgrep will catch
  const url = req.query.url;
  res.redirect(url);
});
app.listen(3000);
---

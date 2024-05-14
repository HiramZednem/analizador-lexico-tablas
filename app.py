import re
from flask import Flask, render_template, request

app = Flask(__name__)

reserved_words = {'for', 'do', 'while', 'if', 'int', 'else', 'printf', 'end', 'read'}
symbols = {';', '"', '+', '=', ',', '(', ')', '{', '}'}

def analyze_code(code):
    lines = code.split('\n')
    tokens = []

    for i, line in enumerate(lines, start=1):
        # Utilizar expresiones regulares para encontrar palabras y símbolos
        words = re.findall(r'\b\w+\b|[\(\){};"+=,]', line)
        for word in words:
            token = {
                'token': word,
                'line': i,
                'reserved': 'x' if word in reserved_words else '',
                'symbol': 'x' if word in symbols else '',
                'left_paren': 'x' if word == '(' else '',
                'right_paren': 'x' if word == ')' else '',
                'left_brace': 'x' if word == '{' else '',
                'right_brace': 'x' if word == '}' else '',
                'number': 'x' if word.isdigit() else '',
                'identifier': 'x' if word not in reserved_words and word not in symbols and not word.isdigit() else ''
            }
            tokens.append(token)

    return tokens

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code']
        tokens = analyze_code(code)
        return render_template('index.html', tokens=tokens, code=code)
    return render_template('index.html', tokens=[], code='')

if __name__ == '__main__':
    app.run(debug=True)

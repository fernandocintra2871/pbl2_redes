from flask import Flask, request, render_template, redirect, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Simulando um banco de dados de usuários
USUARIOS = {'usuario1': 'senha1', 'usuario2': 'senha2'}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            session['usuario'] = usuario
            return redirect('/perfil')
        else:
            return render_template('login.html', mensagem='Credenciais inválidas. Tente novamente.')
    return render_template('login.html')

@app.route('/perfil')
def perfil():
    if 'usuario' in session:
        return f'Bem-vindo, {session["usuario"]}! <a href="/logout">Sair</a>'
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

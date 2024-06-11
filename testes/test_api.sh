#!/bin/bash

# URLs da API
URL="http://127.0.0.1:5000"
REGISTER_URL="$URL/register"
LOGIN_URL="$URL/login"
DEPOSIT_URL="$URL/deposit"
TRANSFER_URL="$URL/transfer"
LOGOUT_URL="$URL/logout"

# Usuários de teste
USER1="user1"
PASS1="password1"
USER2="user2"
PASS2="password2"
USER3="user3"
PASS3="password3"

# Função para registrar um usuário
register_user() {
  local username=$1
  local password=$2
  curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\",\"password\":\"$password\"}" \
    $REGISTER_URL
}

# Função para fazer login
login_user() {
  local username=$1
  local password=$2
  curl -s -X POST -H "Content-Type: application/json" -c cookies.txt \
    -d "{\"username\":\"$username\",\"password\":\"$password\"}" \
    $LOGIN_URL
}

# Função para fazer depósito
deposit() {
  local amount=$1
  curl -s -X POST -H "Content-Type: application/json" -b cookies.txt \
    -d "{\"amount\":$amount}" \
    $DEPOSIT_URL
}

# Função para fazer transferência
transfer() {
  local target_username=$1
  local amount=$2
  curl -s -X POST -H "Content-Type: application/json" -b cookies.txt \
    -d "{\"target_username\":\"$target_username\",\"amount\":$amount}" \
    $TRANSFER_URL
}

# Função para fazer logout
logout() {
  curl -s -X POST -H "Content-Type: application/json" -b cookies.txt \
    $LOGOUT_URL
}

# Registrar usuários
echo "Registrando usuários..."
register_user $USER1 $PASS1
register_user $USER2 $PASS2
register_user $USER3 $PASS3

# Login com o primeiro usuário
echo "Logando com $USER1..."
login_user $USER1 $PASS1

# Depositar dinheiro
echo "Depositando dinheiro..."
deposit 300
# Função para realizar transferência e verificar saldo
perform_transfer() {
  transfer $1 $2
}

# Transferir dinheiro simultaneamente
echo "Transferindo dinheiro simultaneamente..."
perform_transfer $USER2 300 &
perform_transfer $USER3 300 &

# Aguardar todas as transferências terminarem
wait

# Logout
echo "Deslogando..."
logout

echo "Testes de concorrência concluídos."

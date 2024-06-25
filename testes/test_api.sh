#!/bin/bash

# URLs da API
URL="http://127.0.0.1:12345"
REGISTER_URL="$URL/register"
LOGIN_URL="$URL/login"
DEPOSIT_URL="$URL/deposit_op"
TRANSFER_URL="$URL/transfer_op"
WITHDRAW_URL="$URL/withdraw_op"
PAYMENT_URL="$URL/payment_op"
AB_BALANCE_URL="$URL/ab_balance"
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
    -d "{\"bank\":\"brasil\", \"joint_account\":false, \"second_holder\":\"\", \"amount\":$amount}" \
    $DEPOSIT_URL
}

# Função para fazer saque
withdraw() {
  local amount=$1
  curl -s -X POST -H "Content-Type: application/json" -b cookies.txt \
    -d "{\"bank\":\"brasil\", \"joint_account\":false, \"second_holder\":\"\", \"amount\":$amount}" \
    $WITHDRAW_URL
}

# Função para fazer transferência
transfer() {
  local origin_username=$1
  local target_username=$2
  local amount=$3
  curl -s -X POST -H "Content-Type: application/json" -b cookies.txt \
    -d "[{\"user_id\":\"$origin_username\", \"bank\":\"brasil\", \"amount\":$amount}, {\"user_id\":\"$target_username\", \"bank\":\"brasil\", \"amount\":$amount}]" \
    $TRANSFER_URL
}

# Função para fazer pagamento
payment() {
  local user_id=$1
  local amount=$2
  curl -s -X POST -H "Content-Type: application/json" -b cookies.txt \
    -d "[{\"user_id\":\"$user_id\", \"bank\":\"brasil\", \"amount\":$amount}]" \
    $PAYMENT_URL
}

# Função para obter saldos
get_balances() {
  curl -s -X GET -H "Content-Type: application/json" -b cookies.txt \
    $AB_BALANCE_URL
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
deposit 400

echo "Sacando dinheiro..."
# Fazer saques simultâneos

withdraw 100

echo "Transferindo dinheiro..."
# Transferir dinheiro
transfer $USER1 $USER2 100 

echo "Realizando pagamento..."
# Realizar pagamentos simultâneos
payment $USER1 100

# Realizar operações simultâneas
echo "Realizando operações simultâneas..."

# Transferir dinheiro
transfer $USER1 $USER2 100 &
transfer $USER1 $USER3 100 &
transfer $USER1 $USER2 100 &
transfer $USER1 $USER3 100 &
transfer $USER1 $USER2 100 &
transfer $USER1 $USER3 100 &
transfer $USER1 $USER2 100 &
transfer $USER1 $USER3 100 &
transfer $USER1 $USER2 100 &
transfer $USER1 $USER3 100 &

wait

# Obter saldos
echo "Obtendo saldos..."
get_balances

# Logout
echo "Deslogando..."
logout

echo "Testes de concorrência concluídos."

read -p "Pressione Enter para sair..."

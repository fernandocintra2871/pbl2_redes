#!/bin/bash

# URLs da API
BRASIL_URL="http://127.0.0.1:12345"
BRADESCO_URL="http://127.0.0.1:12346"
CAIXA_URL="http://127.0.0.1:12347"

# Nome dos Bancos
BRASIL="brasil"
BRADESCO="bradesco"
CAIXA="caixa"

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
  local bank_url=$3
  curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\",\"password\":\"$password\"}" \
    "$bank_url/register"
}

# Função para fazer login
login_user() {
  local username=$1
  local password=$2
  local bank_url=$3
  curl -s -X POST -H "Content-Type: application/json" -c cookies.txt \
    -d "{\"username\":\"$username\",\"password\":\"$password\"}" \
    "$bank_url/login"
}

# Função para fazer depósito
deposit() {
  local amount=$1
  local bank_name=$2
  local bank_url=$3
  curl -s -X POST -H "Content-Type: application/json" -b cookies.txt \
    -d "{\"bank\":\"$bank_name\", \"joint_account\":false, \"second_holder\":\"\", \"amount\":$amount}" \
    "$bank_url/deposit_op"
}

# Função para fazer saque
withdraw() {
  local amount=$1
  local bank_url=$2
  curl -s -X POST -H "Content-Type: application/json" -b cookies.txt \
    -d "{\"bank\":\"brasil\", \"joint_account\":false, \"second_holder\":\"\", \"amount\":$amount}" \
    "$bank_url/withdraw_op"
}

# Função para fazer transferência
transfer() {
  local origin_username=$1
  local target_username=$2
  local amount=$3
  local bank_name=$4
  local bank_url=$5
  curl -s -X POST -H "Content-Type: application/json" -b cookies.txt \
    -d "[{\"user_id\":\"$origin_username\", \"bank\":\"$bank_name\", \"amount\":$amount}, {\"user_id\":\"$target_username\", \"bank\":\"brasil\", \"amount\":$amount}]" \
    "$bank_url/transfer_op"
}

# Função para fazer pagamento
payment() {
  local user_id=$1
  local amount=$2
  local bank_url=$3
  curl -s -X POST -H "Content-Type: application/json" -b cookies.txt \
    -d "[{\"user_id\":\"$user_id\", \"bank\":\"brasil\", \"amount\":$amount}]" \
    "$bank_url/payment_op"
}

# Função para obter saldos
get_balances() {
  local bank_url=$1
  curl -s -X GET -H "Content-Type: application/json" -b cookies.txt \
    "$bank_url/ab_balance"
}

# Função para fazer logout
logout() {
  local bank_url=$1
  curl -s -X POST -H "Content-Type: application/json" -b cookies.txt \
    "$bank_url/logout"
}

# Registrar usuários
echo "Registrando usuários..."
register_user $USER1 $PASS1 $BRASIL_URL
register_user $USER1 $PASS1 $BRADESCO_URL
register_user $USER1 $PASS1 $CAIXA_URL
register_user $USER2 $PASS2 $BRASIL_URL

# Login com o primeiro usuário
echo "Logando com $USER1..."
login_user $USER1 $PASS1 $BRASIL_URL
login_user $USER1 $PASS1 $BRADESCO_URL
login_user $USER1 $PASS1 $CAIXA_URL

# Depositar dinheiro
echo "Depositando dinheiro..."
deposit 500 $BRASIL $BRASIL_URL
deposit 500 $BRADESCO $BRADESCO_URL
deposit 500 $CAIXA $CAIXA_URL

#echo "Sacando dinheiro..."
# Fazer saques
#withdraw 100 $BRASIL

#echo "Transferindo dinheiro..."
# Transferir dinheiro
#transfer $USER1 $USER2 100 

#echo "Realizando pagamento..."
# Realizar pagamentos simultâneos
#payment $USER1 100

wait

echo "Obtendo saldos..."
get_balances $BRASIL_URL
get_balances $BRADESCO_URL
get_balances $CAIXA_URL

echo "Contas criadas e saldos adicionados."

read -p "Pressione Enter para sair..."

#!/bin/bash

# URLs da API
BRASIL_URL="http://ip:12345"
BRADESCO_URL="http://ip:12346"
CAIXA_URL="http://ip:12347"

# Nome dos Bancos
BRASIL="brasil"
BRADESCO="bradesco"
CAIXA="caixa"

# Arquivos de cookies
COOKIES_BRASIL="cookies_brasil.txt"
COOKIES_BRADESCO="cookies_bradesco.txt"
COOKIES_CAIXA="cookies_caixa.txt"

# Usuários de teste
USER1="user1123"
PASS1="password1"
USER2="user2223"
PASS2="password2"
USER3="user3323"
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
  local cookies_file=$4

  curl -s -X POST -H "Content-Type: application/json" -c "$cookies_file" \
    -d "{\"username\":\"$username\",\"password\":\"$password\"}" \
    "$bank_url/login"
}

# Função para fazer depósito
deposit() {
  local amount=$1
  local bank_name=$2
  local bank_url=$3
  local cookies_file=$4

  curl -s -X POST -H "Content-Type: application/json" -b "$cookies_file" \
    -d "{\"bank\":\"$bank_name\", \"joint_account\":false, \"second_holder\":\"\", \"amount\":$amount}" \
    "$bank_url/deposit_op"
}

# Função para fazer transferência
transfer() {
  local origin_username=$1
  local target_username=$2
  local amount=$3
  local bank_name=$4
  local bank_url=$5
local cookies_file=$6
  curl -s -X POST -H "Content-Type: application/json" -b "$cookies_file" \
    -d "[{\"user_id\":\"$origin_username\", \"bank\":\"$bank_name\", \"amount\":$amount}, {\"user_id\":\"$target_username\", \"bank\":\"brasil\", \"amount\":$amount}]" \
    "$bank_url/transfer_op"
}

# Função para obter saldos
get_balances() {
  local bank_url=$1
  local cookies_file=$2

  curl -s -X GET -H "Content-Type: application/json" -b "$cookies_file" \
    "$bank_url/ab_balance"
}

# Função para fazer logout
logout() {
  local bank_url=$1
  local cookies_file=$2

  curl -s -X POST -H "Content-Type: application/json" -b "$cookies_file" \
    "$bank_url/logout"
}

# Registrar usuários
echo "Registrando usuários..."
register_user $USER1 $PASS1 $BRASIL_URL
register_user $USER1 $PASS1 $BRADESCO_URL
register_user $USER1 $PASS1 $CAIXA_URL
register_user $USER2 $PASS2 $BRASIL_URL

# Login com o primeiro usuário em cada banco
echo "Logando com $USER1..."
login_user $USER1 $PASS1 $BRASIL_URL $COOKIES_BRASIL
login_user $USER1 $PASS1 $BRADESCO_URL $COOKIES_BRADESCO
login_user $USER1 $PASS1 $CAIXA_URL $COOKIES_CAIXA

# Depositar dinheiro em cada banco
echo "Depositando dinheiro..."
deposit 500 $BRASIL $BRASIL_URL $COOKIES_BRASIL
deposit 500 $BRADESCO $BRADESCO_URL $COOKIES_BRADESCO
deposit 500 $CAIXA $CAIXA_URL $COOKIES_CAIXA

# Esperar por todas as operações terminarem
wait

# Obtendo saldos de cada banco
echo "Obtendo saldos..."
get_balances $BRASIL_URL $COOKIES_BRASIL
get_balances $BRADESCO_URL $COOKIES_BRADESCO
get_balances $CAIXA_URL $COOKIES_CAIXA

# Realizar operações simultâneas
echo "Realizando operações simultâneas..."

transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &

transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &

transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &

transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &

transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &

transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &

transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL $COOKIES_BRASIL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL $COOKIES_BRADESCO &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL $COOKIES_CAIXA &

wait

# Obtendo saldos de cada banco
echo "Obtendo saldos..."
get_balances $BRASIL_URL $COOKIES_BRASIL
get_balances $BRADESCO_URL $COOKIES_BRADESCO
get_balances $CAIXA_URL $COOKIES_CAIXA

# Saindo das contas cujo valor foi transferido
echo "Deslogando..."
logout $BRASIL_URL $COOKIES_BRASI
logout $BRADESCO_URL $COOKIES_BRADESCO 
logout $CAIXA_URL $COOKIES_CAIXA
 
wait

echo "Login na conta 2..."
login_user $USER2 $PASS2 $BRASIL_URL $COOKIES_BRASIL

echo "Obtendo saldos..."
get_balances $BRASIL_URL $COOKIES_BRASIL

echo "Deslogando..."
logout $BRASIL_URL $COOKIES_BRASI

# Exemplo de logout (opcional)
# logout $BRASIL_URL $COOKIES_BRASIL
# logout $BRADESCO_URL $COOKIES_BRADESCO
# logout $CAIXA_URL $COOKIES_CAIXA

echo "Contas criadas e saldos adicionados."

read -p "Pressione Enter para sair..."

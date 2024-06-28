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

# Realizar operações simultâneas
echo "Realizando operações simultâneas..."

transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &
transfer $USER1 $USER2 10 $BRASIL $BRASIL_URL &
transfer $USER1 $USER2 10 $BRASIL $BRADESCO_URL &
transfer $USER1 $USER2 10 $BRASIL $CAIXA_URL &

wait

# Obter saldos
echo "Obtendo saldos..."
get_balances $BRASIL_URL
get_balances $BRADESCO_URL
get_balances $CAIXA_URL

# Saindo das contas cujo valor foi transferido
echo "Deslogando..."
logout $BRASIL_URL
logout $BRADESCO_URL
logout $CAIXA_URL

# Verificando o saldo da conta alvo da transferencia
login_user $USER2 $PASS2 $BRASIL_URL
get_balances $BRASIL_URL
logout $BRASIL_URL

echo "Testes de concorrência concluídos."

read -p "Pressione Enter para sair..."

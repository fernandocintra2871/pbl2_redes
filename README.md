# Problema 2 - Transações Bancárias Distribuídas (MI de Concorrência e Conectividade)

## Introdução

O presente projeto foi solicitado como trabalho avaliativo para a disciplina MI - Concorrência e Conectividade (TEC502)  do curso de Engenharia de Computação da Universidade Estadual de Feira de Santana (UEFS). O trabalho em questão exige o desenvolvimento de um sistema distribuído que possibilite a criação e a movimentação de contas bancárias de maneira descentralizada, inspirado no sistema Pix utilizado no Brasil. 

Esse sistema deve permitir que clientes de qualquer banco realizem pagamentos, depósitos e transferências de valores para contas no mesmo ou em outros bancos, sem a necessidade de um banco central para controle das transações.

Além disso, a solução deve assegurar a execução de transações atômicas entre diferentes bancos, garantindo que não haja movimentações de dinheiro superiores ao saldo disponível nas contas e evitando o problema do "duplo gasto", onde um mesmo valor poderia ser transferido mais de uma vez. 

## Como utilizar a solução desenvolvida

A solução desenvolvida está disponível no formato de imagem Docker no repositório do projeto no Docker Hub. Então para a utilização dos programas é necessário ter o Docker instalado no dispositivo no qual o programa será executado.

### 1º etapa - Baixando a imagem Docker

Primeiramente é preciso baixar a imagem disponível no repositório nas respectivas máquinas que serão utilizadas, para isso basta abrir o terminal e executar o comando abaixo nas máquinas que serão utilizadas.

```bash
docker pull lfrcintra/bank:latest
```

### 2º etapa - Executando a imagem baixada

Com a imagem *bank* baixada em cada uma das máquinas é possível instanciar cada um dos bancos através do Docker. Para isso basta executar cada um dos comandos abaixo em uma máquina diferente.

**Obs:** Nos argumentos *brasil_host*, *bradesco_host* e *caixa_host* é necessário preencher com o ip da máquina onde o respectivo banco está sendo executado.

```bash
docker run -p 12345:12345 --rm -it -e bank_name="brasil" -e brasil_host="" -e bradesco_host="" -e caixa_host="" lfrcintra/bank
```

```bash
docker run -p 12346:12346 --rm -it -e bank_name="bradesco" -e brasil_host="" -e bradesco_host="" -e caixa_host="" lfrcintra/bank
```

```bash
docker run -p 12347:12347 --rm -it -e bank_name="caixa" -e brasil_host="" -e bradesco_host="" -e caixa_host="" lfrcintra/bank
```

### 3º etapa - Acessando o sistema

Cada banco possui sua própria interface de acesso, para utilizá-las basta acessar a página com o endereço dado pelo ip_do_banco:porta_do_banco/login. Ao acessar a página de login é necessário criar uma conta para conseguir acessar o sistema, então basta clicar no botão de “Register”. Após criar uma conta, clique no botão “Login“, preencha com os dados da sua conta e clique em “Login“ novamente, e agora é possível utilizar as funcionalidades do sistema.

## Solução Desenvolvida

<p align="center" id="diagrama">
  <img src="imgs\diagrama.png" alt="diagrama">
</p>
<p align="center">Comunicação entre os Bancos. Fonte: Autor</p>

A solução desenvolvida consiste em um sistema bancário distribuído que conecta três bancos **fictícios** (Banco do Brasil, Bradesco e Caixa Caixa Econômica Federal) através do protocolo de comunicação HTTP (Hypertext Transfer Protocol), utilizando uma API RESTful, como vista no [diagrama](#diagrama). A interface do sistema, o front-end, foi feita utilizando html e JavaScript enquanto a lógica do servidor, back-end, foi feita utilizando o framework Flask do Python. A solução permite a realização das operações bancárias de saque, depósito, transferência, pagamento e visualização de saldo de forma unificada, ou seja, o usuário ao acessar sua conta em qualquer um dos três bancos consegue realizar as operações citadas envolvendo todas as suas contas existentes nos demais bancos. O sistema foi construído seguindo padrão de design Saga, utilizado para gerenciar transações distribuídas, com o uso de travas para garantir a atomicidade e lidar com a concorrência das operações.


### Telas

<p align="center">
  <img src="imgs\tela_login.png" alt="tela_login" style="width: 50%; height: auto;">
</p>
<p align="center">Tela de Login. Fonte: Autor</p>

<p align="center">
  <img src="imgs\tela_registro.png" alt="tela_registro" style="width: 50%; height: auto;">
</p>
<p align="center">Tela de Registro. Fonte: Autor</p>

<p align="center">
  <img src="imgs\tela_conta.png" alt="tela_conta" style="width: 50%; height: auto;">
</p>
<p align="center">Tela da Conta. Fonte: Autor</p>

<p align="center">
  <img src="imgs\tela_deposito.png" alt="tela_deposito" style="width: 50%; height: auto;">
</p>
<p align="center">Tela do Deposito. Fonte: Autor</p>

<p align="center">
  <img src="imgs\tela_saque.png" alt="tela_saque" style="width: 50%; height: auto;">
</p>
<p align="center">Tela do Saque. Fonte: Autor</p>

<p align="center">
  <img src="imgs\tela_transferencia.png" alt="tela_transferencia" style="width: 50%; height: auto;">
</p>
<p align="center">Tela da Transferencia. Fonte: Autor</p>

<p align="center">
  <img src="imgs\tela_pagamento.png" alt="tela_pagamento" style="width: 50%; height: auto;">
</p>
<p align="center">Tela de Pagamento. Fonte: Autor</p>

## Aspecto do Projeto

### Permite gerenciar contas ? 

O sistema criado possui as seguintes funcionalidades:

**Cadastro**
O usuário pode criar tanto uma conta individual quanto uma conta conjunta. Os dados solicitados para criação da conta são o CPF do titular, o CPF do segundo titular, quando a conta for conjunta, e uma senha.

**Login**
O usuário acessa o sistema através do seu CPF e uma senha vinculada a qualquer conta que detenha esse CPF no banco em que foi cadastrado.

**Visualização de Saldo**
O usuário consegue visualizar os saldos de todas as contas que possuem o seu CPF existentes tanto no banco em que o login foi feito, quanto nos bancos conectados a ele.

**Deposito**
O usuário consegue adicionar saldo a qualquer uma de suas contas individuais ou conjuntas existentes nos bancos conectados, selecionando o banco da conta e CPF do segundo titular quando for conta conjunta.

**Saque**
O usuário consegue remover saldo de qualquer uma de suas contas individuais ou conjuntas existentes nos bancos conectados, selecionando o banco da conta e CPF do segundo titular quando for conta conjunta.

**Transferência**
O usuário consegue realizar uma transferência fazendo uso simultâneo do saldo de qualquer conta com seu CPF, existentes nos bancos conectados, para um terceiro,  sinalizando o banco, CPF e CPF do segundo titular quando for conta conjunta.

**Pagamento**
O usuário consegue realizar um pagamento	de um código fictício utilizando simultaneamente o saldo de qualquer conta com seu CPF, existentes nos bancos conectados. Nesse caso o valor total a ser transferido não vai para nenhuma conta, ele apenas é removido.

### Permite selecionar e realizar transferência entre diferentes contas? 

Quando o usuário acessa a página de transferência, a página web faz uma requisição HTTP GET para a rota `/ab_balances` para obter todas contas com o CPF do usuário, existentes nos bancos conectados. Para cada conta obtida um novo *input* de valor a ser transferido aparece, no qual o usuário poderá sinalizar quanto ele quer usar daquela conta para a transferência. Além disso, também é solicitado o banco, CPF e CPF do segundo titular quando necessário dá conta que irá receber a transferência.

Após todos os dados serem preenchidos, quando o usuário clica em “Transferir” a página web faz uma requisição HTTP POST para a rota `/transfer_op` passando uma lista com todas as operações a serem realizadas em cada conta de cada banco envolvido na transferência, sendo cada operação sinalizada por um dicionário com as seguintes chaves:
- user_id: Para o id da conta
- bank: Para o id do banco, no caso ‘brasil’, “bradesco” ou “caixa”
- operation: Para a operação a ser realizada, no caso “subtraction“ ou “addition”
- amount:  Para o valor a ser utilizado na operação

Na lista em questão, primeiro são adicionadas as operações de subtração que correspondem a cada *input* de transferência preenchido,  já a última operação sempre será a de adição, que se refere a conta alvo da transferência e nesse caso o valor passado em `amount` será sempre a soma dos valores presentes nas operações anteriores.

As operações são realizadas de forma sincrônica, ou seja, para cada operação na lista, a rota `/transfer_op` faz um requisições HTTP POST para as rotas `/add_balance` ou `/remove_balance` dependendo do tipo de operação, passando um dicionário com as seguintes chaves:
- user_id: Para o id da conta
- amount: Para o valor a ser utilizado na operação

### Comunicação entre servidores 

Tanto para navegação entre as páginas do site, quanto para a realização das operações bancárias foram utilizadas uma API RESTful. Ao realizar qualquer uma das operações bancárias no sistema, a página faz uma requisição HTTP referente a operação desejada, as rotas referente a isso podem ser vista na seção [Operações Realizadas Pelo Banco](#operações-realizadas-pelo-banco) quando o sistema recebe essa requisição, o banco fica responsável por se comunicar com os outros bancos ou com si mesmo através das rotas presentes em [Requisições Entre Bancos](#requisições-entre-bancos). De modo geral foram utilizadas as rotas a seguir:

#### Registro e Login

**POST /register:**
- Descrição: Registra um novo usuário.
- Dados recebidos: JSON com username e password.
- Resposta: JSON com mensagem de sucesso ({'message': 'User registered successfully'}) e código HTTP 201, ou mensagem de erro ({'message': 'User already exists'}) e código HTTP 400.

**POST /login:**
- Descrição: Autentica um usuário.
- Dados recebidos: JSON com username e password.
- Resposta: JSON com mensagem de sucesso ({'message': 'Login successful'}) e código HTTP 200, ou mensagem de erro ({'message': 'Invalid username or password'}) e código HTTP 401.

#### Operações Realizadas Pelo Banco

**POST /deposit_op:**
- Descrição: Realiza um depósito, ou seja adiciona saldo a uma das contas do usuário autenticado.
- Dados recebidos: JSON com um dicionário com as chaves bank, joint_account, second_holder, e amount.
- Resposta: JSON com a resposta do banco destino e código HTTP correspondente, ou mensagem de falha de comunicação ({'message': 'Falha ao se comunicar com o banco destino'}) e código HTTP 502, ou mensagem de valor inválido ({'message': 'Invalid amount'}) e código HTTP 400, ou mensagem de não autorizado ({'message': 'Unauthorized'}) e código HTTP 401.

**POST /withdraw_op:**
- Descrição: Realiza um saque, ou seja remove saldo de uma das contas do usuário autenticado.
- Dados recebidos: JSON com um dicionário com as chaves bank, joint_account, second_holder, e amount.
- Resposta: JSON com a resposta do banco destino e código HTTP correspondente, ou mensagem de falha de comunicação ({'message': 'Falha ao se comunicar com o banco destino'}) e código HTTP 502, ou mensagem de valor inválido ({'message': 'Invalid amount'}) e código HTTP 400, ou mensagem de não autorizado ({'message': 'Unauthorized'}) e código HTTP 401.

**GET /ab_balance:**
- Descrição: Retorna os saldos das contas associadas ao usuário autenticado em todos os bancos.
- Dados recebidos: Nenhum.
- Resposta: JSON com uma lista de saldos e código HTTP 200, ou mensagem de não autorizado ({'message': 'Unauthorized'}) e código HTTP 401.

**POST /payment_op:**
- Descrição: Realiza pagamento de um código fictício, ou seja, apenas remove o saldo de diferentes contas do usuário autenticado simultaneamente.
- Dados recebidos: JSON com uma lista de transferências, cada uma contendo um dicionário com as chaves user_id, bank, operation, e amount.
- Resposta: JSON com mensagem de sucesso ({'message': 'Payment completed successfully'}) e código HTTP 200, ou mensagem de falha de comunicação ({'message': 'Failure to communicate with partner banks'}) e código HTTP 502, ou mensagem de não autorizado ({'message': 'Unauthorized'}) e código HTTP 401.

**POST /transfer_op:**
- Descrição: Realiza transferências que podem ser feitas simultaneamente de várias contas pertencentes ao usuário autenticado para um conta de um terceiro ou do próprio usuário.
- Dados recebidos: JSON com uma lista de transferências, cada uma contendo um dicionário com as chaves user_id, bank, operation e amount.
- Resposta: JSON com mensagem de sucesso ({'message': 'Transfer completed successfully'}) e código HTTP 200, ou mensagem de falha de comunicação ({'message': 'Failure to communicate with partner banks'}) e código HTTP 502, ou mensagem de não autorizado ({'message': 'Unauthorized'}) e código HTTP 401.

#### Requisições Entre Bancos

**POST /add_balance:**
- Descrição: Adiciona saldo a uma conta existente no banco.
- Dados recebidos: JSON com um dicionário com as chaves user_id e amount.
- Resposta: JSON com mensagem de sucesso ({'message': 'Amount added to account'}) e código HTTP 200, ou mensagem de conta inexistente ({'message': 'User account does not exist'}) e código HTTP 404.

**POST /remove_balance:**
- Descrição: Remove saldo de uma conta existente no banco.
- Dados recebidos: JSON com um dicionário com as chaves user_id e amount.
- Resposta: JSON com mensagem de sucesso ({'message': 'Amount removed to account'}) e código HTTP 200, ou mensagem de conta inexistente ({'message': 'User account does not exist'}) e código HTTP 404, ou mensagem de fundos insuficientes ({'message': 'Insufficient funds'}) e código HTTP 400.

**GET /balances/\<string:user_id\>:**
- Descrição: Retorna os saldos das contas existentes no banco associadas ao user_id especificado.
- Dados recebidos: Nenhum.
- Resposta: JSON com uma lista de saldos e código HTTP 200, ou mensagem de conta inexistente ({'message': 'User account does not exist'}) e código HTTP 404.

#### Rotas das Páginas do Sistema


**GET /:**
- Descrição: Redireciona para a página de login se o usuário não estiver autenticado, caso contrário, redireciona para a página da conta.
- Dados recebidos: Nenhum.
- Resposta: Redireciona para /login ou /account.

**GET /login:**
- Descrição: Renderiza a página de login.
- Dados recebidos: Nenhum.
- Resposta: Renderiza login.html.

**GET /register:**

- Descrição: Renderiza a página de registro.
- Dados recebidos: Nenhum.
- Resposta: Renderiza register.html.

**GET /account:**

- Descrição: Renderiza a página da conta do usuário autenticado.
- Dados recebidos: Nenhum.
- Resposta: Renderiza account.html com o nome do banco.

**GET /withdraw:**
- Descrição: Renderiza a página de saque.
- Dados recebidos: Nenhum.
- Resposta: Renderiza withdraw.html.


**GET /deposit:**
- Descrição: Renderiza a página de depósito.
- Dados recebidos: Nenhum.
- Resposta: Renderiza deposit.html.

**GET /transfer:**
- Descrição: Renderiza a página de transferência.
- Dados recebidos: Nenhum.
- Resposta: Renderiza transfer.html.

**GET /payment:**
- Descrição: Renderiza a página de pagamento.
- Dados recebidos: Nenhum.
- Resposta: Renderiza payment.html.

**POST /logout:**
- Descrição: Realiza o logout do usuário.
- Dados recebidos: Nenhum.
- Resposta: JSON com a mensagem de logout bem-sucedido ({'message': 'Logout successful'}) e código HTTP 200.


### Sincronização em um único servidor

A sincronização e tratamento de concorrência em um único servidor são gerenciados através do uso de locks através do método `Lock()` da biblioteca *threading* do Python. O método `Lock()` é utilizado para instanciar uma trava

Cada conta possui um bloqueio que é instanciado através do método `threading.Lock()` e é associado a chave *lock* dentro do dicionário que representa a conta que por sua vez está em outro dicionário com todas as contas registradas no banco em questão. Quando as rotas `/add_balance` e `/remove_balance`, que podem alterar os saldos das contas existentes no banco em questão, são acessadas, antes de alterar o saldo, o código adquire o bloqueio específico para essa conta usando `accounts[user_id]['lock'].acquire(blocking=True)`. O que faz com que, caso já tenha outro processo fazendo uso da trava, o processo atual fique aguardando a liberação da mesma, isso por conta do argumento `blocking=True`. Após a operação ser concluída, o bloqueio é liberado usando `accounts[user_id]['lock'].release()`. Assim permitindo que outro processo faça uso da trava para poder alterar o saldo.


### Algoritmo da concorrencia distribuída está teoricamente bem empregado?

Para lidar com a questão da concorrência distribuída foi utilizado o padrão de design Saga com Coordenação de Bloqueio. O padrão Saga consiste em realizar transações em sequência, na qual cada operação atualiza o serviço e retorna uma mensagem ou evento para iniciar a próxima operação. Se alguma operação falhar, é executado operações compensatórias para desfazer as operações anteriores.

No solução produzida, o padrão Saga foi empregado da seguinte forma, quando uma transação é realizada é feito uma requisição HTTP POST para a rota* /transfer_op*, essa rota recebe uma lista com as operações a serem realizadas, essas operações consistem em uma série de operações de subtração que são feitas através da rota `/remove_balance` do banco envolvido na operação, que consiste na retirada dos saldos das contas do usuário envolvidas na transação. E por fim uma operação de adição que é feita através da roda `/add_balance` do banco envolvido na operação, que consiste no depósito do saldo na conta do usuário alvo da transferência. 

Todas essas operações são feitas sequencialmente e assim que cada operação é realizada com sucesso, a operação feita é salva em um log representado por uma lista `transfer_hist`. Quando uma operação falha, as demais não são executadas e uma mensagem de erro é retornada, além disso, todas as operações presentes em `transfer_hist` são adicionadas à lista de operações a serem desfeitas `pending_undones`.

Cada banco possui uma thread chamada `undo_transfers` que é responsável por remover operações da lista de operações a serem desfeitas `pending_undones` e realizar a operação compensatória dessa operação no banco envolvido na mesma, caso ela tente realizar a operação compensatória e não consiga ser realizada, a operação é adicionada ao final da lista `pending_undones` para ser realizada depois.

Por fim, por conta do uso do lock como explicado na seção [Sincronização em um único servidor](#sincronização-em-um-único-servidor) caso uma operação tente alterar um saldo que já está sendo utilizado em outra operação, a operação em sim fica em uma estado de espera até o saldo ser liberado.

### Algoritmo está tratrando o problema na prática?

Para validar se o tratamento da concorrência distribuída estava bem empregado foi feito uma bateria de testes utilizando um **shell script** para simular a realização de várias transações simultâneas envolvendo o saldo de uma mesma conta. O teste consistia em fazer 90 transferências simultâneas em cada banco e verificar se o saldo da conta ao final ficaria negativo, ou zerado (que é o correto). O comportamento dos teste aconteceu como esperado, as operações foram executadas de forma síncrona por conta do `lock` utilizado no saldo da conta, então nenhuma transação sobrepõe a outra, assim que o saldo foi esgotada as transações seguintes não foram realizadas pois já não havia saldo suficiente.

### Tratamento da confiabilidade

Quando um banco se desconecta dos outros, qualquer requisição que seja feita para ele pelos demais bancos falha, gerando uma exceção `ConnectionError` ou `ReadTimeout`, essas duas exceções são tratadas, o que faz com que o sistema não pare de funcionar. No caso da exibição dos saldos, os saldos presentes nos bancos desconectados não aparecem, e no caso das operações bancárias, uma mensagem de erro é exibida ao usuário ao tentar utilizar uma conta de um dos desconectados. E no caso da transferência, os campos de input referente as contas presentes no banco desconectado não aparecem.

### Pelo menos uma transação concorrente é realizada ?

Como visto nas seções, [Sincronização em um único servidor](#sincronização-em-um-único-servidor), [Algoritmo da concorrência distribuída está teoricamente bem empregado?](#algoritmo-da-concorrencia-distribuída-está-teoricamente-bem-empregado), [Algoritmo está tratando o problema na prática?](#algoritmo-está-tratrando-o-problema-na-prática), o Sistema possui a capacidade de realizar transações simultâneas envolvendo a mesma conta sem o comprometimento do valor do saldo da conta.



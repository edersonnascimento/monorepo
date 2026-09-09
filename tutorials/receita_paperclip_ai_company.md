Aqui está o guia passo a passo (receita) para configurar e operar a **Paperclip AI Company**, com base no tutorial fornecido.

---

# 🚀 Receita: Paperclip AI Company
**Objetivo:** Criar e gerenciar uma empresa virtual composta inteiramente por agentes de IA.

## 📋 Pré-requisitos
* Node.js instalado em sua máquina local (necessário para executar comandos `npx`).
* Conta no ChatGPT/OpenAI (caso opte por usar o adaptador Codex).

---

## 🛠️ Passo a Passo

### 1. Instalação Local
Para iniciar o Paperclip sem a necessidade de compilação manual, utilize o comando de onboarding via terminal:

1. Abra o seu terminal (Prompt de Comando ou PowerShell no Windows, Terminal no Mac/Linux).
2. Execute o seguinte comando:
   ```bash
   npx paperclip onboard yes
   ```
3. Aguarde a conclusão dos testes e a inicialização do sistema. O sistema informará em qual endereço local ele estará disponível (ex: `http://localhost:XXXX`).

---

### 2. Criar uma Empresa
Com o sistema rodando no navegador:

1. Acesse a aba **Company**.
2. Defina os detalhes básicos da sua organização:
   * **Nome da Empresa:** Escolha um nome para a sua companhia.
   * **Missão e Objetivo (Goal):** Defina o objetivo principal da empresa (Ex: *"Criar uma newsletter semanal sobre os últimos LLMs de código aberto"*).
3. Clique em **Next** para prosseguir.

---

### 3. Contratar Funcionários
A estrutura começa com a criação do cargo mais alto, que depois delegará as demais contratações.

#### A. Criando o CEO (O primeiro agente)
1. Defina o nome do agente como `CEO`.
2. **Escolha o Adaptador:** Selecione qual IA moverá o agente (Ex: Codex, Claude, Gemini, OpenAI).
3. **Configuração do Codex (Se selecionado):**
   * No ChatGPT $\rightarrow$ Configurações $\rightarrow$ Segurança $\rightarrow$ Ative a **"Device Code Authorization for Codex"**.
   * No terminal onde o Paperclip está rodando, execute: `codex login device off`.
   * Siga o link gerado, faça login com sua conta e insira o código de acesso fornecido no terminal.
4. Teste a conexão e finalize a criação do CEO.

#### B. Contratando a Equipe
Você não precisa criar todos os funcionários manualmente; você pode delegar isso ao CEO:
1. Crie uma tarefa para o CEO: *"Contrate seu primeiro engenheiro e crie um plano de contratação"*.
2. **Aprovação do Board:** Como você é o "Conselho Administrativo" (Board), vá até a aba **Inbox**.
3. Você verá as solicitações de contratação feitas pelo CEO (ex: CTO, CMO, UX Designer). Clique em **Approve** para autorizar a entrada desses novos funcionários na empresa.

---

### 4. Delegar Tarefas
A interação com a empresa acontece através de "Issues" (Problemas/Tarefas).

1. Vá até a aba **Issues**.
2. Clique em criar nova issue e descreva a tarefa (Ex: *"Crie a newsletter de hoje sobre LLMs open-source"*).
3. **Atribuição:** Atribua a tarefa ao **CEO**.
4. **Fluxo de Trabalho:** 
   * O CEO analisará a tarefa $\rightarrow$ Delegará para o funcionário correto (ex: CMO) $\rightarrow$ O funcionário executará a tarefa $\rightarrow$ Entregará o artefato final.
5. Acompanhe o progresso no **Dashboard** ou na aba de **Issues**, onde você verá o status mudar de `To Do` $\rightarrow$ `In Progress` $\rightarrow$ `Done`.

---

### 5. Desinstalar
Como a instalação local foi feita via `npx`, ela não realiza uma instalação tradicional no sistema operacional, mas sim executa o pacote.

1. **Parar a Execução:** Vá ao terminal onde o processo está rodando e pressione `Ctrl + C`.
2. **Limpeza de Dados:** Para remover completamente as configurações locais, você deve localizar a pasta de cache do `npx` ou a pasta de dados criada pelo Paperclip no seu diretório de usuário e excluí-la manualmente.
3. **Remover Adaptadores:** Caso tenha configurado chaves de API em arquivos `.env` ou variáveis de ambiente, lembre-se de removê-las para garantir sua privacidade.

---

### 💡 Dicas Adicionais
* **Monitoramento de Custos:** Você pode acompanhar quantos tokens cada funcionário está gastando na aba **Cost**.
* **Heartbeat:** O CEO possui um "batimento cardíaco" (heartbeat) configurável, que o faz acordar periodicamente para checar se há tarefas pendentes.
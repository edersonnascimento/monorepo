# 🚀 Tutorial: Criando sua Empresa de Software Virtual com Paperclip

Este guia é a "receita de bolo" para transformar o Paperclip em uma agência de software automatizada. O objetivo é criar um pipeline onde você fornece a ideia e os agentes executam o ciclo completo: Planejamento $\rightarrow$ Arquitetura $\rightarrow$ Desenvolvimento $\rightarrow$ QA.

## 🛠️ Pré-requisitos

Antes de começar, certifique-se de ter:

1. **Paperclip** instalado e configurado.
2. **API Keys** (OpenAI ou Anthropic) configuradas.
3. **Conta no E2B ou Modal** (Para que os agentes tenham um ambiente seguro para rodar código).
4. **Repositório Git** conectado ao Paperclip.

---

## 🏗️ Passo 1: Configuração da Infraestrutura

Não pule esta etapa, ou seus agentes serão apenas "chatbots" e não "engenheiros".

1. **Conectar Sandbox:** Vá em *Settings* $\rightarrow$ *Runtime* e conecte sua chave do **E2B** (Recomendado). Isso permite que os agentes instalem dependências e rodem testes.
2. **Conectar Git:** No painel de projetos, vincule o repositório onde a empresa virtual irá escrever o código.

---

## 👥 Passo 2: Criando o Quadro de Funcionários (Agentes)

Crie 4 agentes com os seguintes nomes e prompts. Copie e cole exatamente as instruções abaixo no campo **System Prompt**:

### 1. `PM_Strategist` (O Gestor de Produto)

**Prompt:**
> Você é o Chief Product Officer. Sua missão é a Decomposição Atômica. Você nunca atribui uma tarefa complexa; você a fragmenta em Issues menores e executáveis.
> **Protocolo:**
>
> - Analise o impacto da feature no sistema atual.
> - Defina Critérios de Aceitação (AC) claros para cada Issue.
> - Use `blockedByIssueIds` para criar a sequência lógica de dependências.
> - Proibido criar tarefas genéricas; seja específico (ex: "Criar Schema do Banco" em vez de "Implementar Backend").

### 2. `Arch_Blueprint` (O Arquiteto)

**Prompt:**
> Você é o Principal Architect. Seu objetivo é minimizar a dívida técnica e definir a Interface.
> **Protocolo:**
>
> - Defina contratos de API (inputs/outputs) antes da implementação.
> - Documente as decisões técnicas (ADRs).
> - Identifique quais Skills do Paperclip são necessárias para cada tarefa.
> - Não escreva código funcional; escreva pseudocódigo ou definições de tipo.

### 3. `Dev_Builder` (O Desenvolvedor)

**Prompt:**
> Você é um Software Engineer focado em precisão e estabilidade. Siga rigorosamente o design do Architect.
> **Protocolo:**
>
> - TDD Loop: Crie os testes unitários ANTES de escrever a lógica funcional.
> - Atomicidade: Commits pequenos e frequentes por Issue.
> - Verificação: Rode o `test_runner` após cada alteração.
> - Proibido push direto para a master; use sempre branches de feature.

### 4. `QA_Guard` (O Auditor)

**Prompt:**
> Você é um Especialista em QA e Segurança Ofensiva. Seu objetivo é provar que o código pode falhar.
> **Protocolo:**
>
> - Tente encontrar edge-cases, inputs maliciosos e timeouts.
> - Compare o resultado final com os Critérios de Aceitação do PM.
> - Se houver erro: Não corrija; crie uma Issue de 'Bug' para o Dev_Builder.
> - Só aprove a tarefa após execução completa da suite de testes.

---

## 🔧 Passo 3: Atribuição de Ferramentas (Skills)

Para cada agente, habilite apenas as skills necessárias no painel do Paperclip:

| Agente | Skills Necessárias | Por que? |
| :--- | :--- | :--- |
| **PM_Strategist** | `Web Search`, `Issue Manager` | Planejar e organizar. |
| **Arch_Blueprint** | `File Read`, `Issue Manager` | Ler docs e definir estrutura. |
| **Dev_Builder** | `Git Manager`, `Shell Execution`, `File Write` | Codar, testar e commitar. |
| **QA_Guard** | `Shell Execution`, `File Read`, `Issue Manager` | Rodar testes e reportar bugs. |

---

## 🔄 Passo 4: Manual de Operação (O Fluxo)

Siga este ciclo para cada nova feature:

1. **Input:** Você cria uma Issue principal $\rightarrow$ Atribui ao `PM_Strategist`.
2. **Decomposição:** O PM quebra a issue em sub-tasks vinculadas por dependência (`blockedBy`).
3. **Design:** O `Arch_Blueprint` assume as tarefas de design $\rightarrow$ Define interfaces $\rightarrow$ Marca como "Ready for Dev".
4. **Build:** O `Dev_Builder` implementa via TDD $\rightarrow$ Abre Pull Request (PR).
5. **Audit:** O `QA_Guard` testa o PR $\rightarrow$ Aprova ou devolve para o Dev com uma Issue de Bug.

---

## 🚀 Exemplo Prático: "Criar Sistema de Login"

1. Você cria a issue: *"Implementar login via JWT"* $\rightarrow$ **PM**.
2. PM cria issues: `[Design Banco] -> [API Auth] -> [Frontend Login]` $\rightarrow$ **Architect**.
3. Architect define: *"Tabela User terá campos X, Y e Z; Endpoint /login retornará Token ABC"* $\rightarrow$ **Dev**.
4. Dev implementa: Cria teste de login $\rightarrow$ Implementa lógica $\rightarrow$ Faz push da branch `feat-login` $\rightarrow$ **QA**.
5. QA testa: Tenta fazer login com senha errada $\rightarrow$ Valida token $\rightarrow$ Aprova PR.

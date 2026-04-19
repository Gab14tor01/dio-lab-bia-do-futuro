# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação do agente pode ser feita de duas formas complementares:

1. Testes estruturados: Definição de cenários de segurança com respostas esperadas;
2. Feedback real: Usuários testam o agente e avaliam a clareza, utilidade e precisão das respostas.

---

## Métricas de Qualidade

| Métrica              | O que avalia                                              | Exemplo de teste                                             |
| -------------------- | --------------------------------------------------------- | ------------------------------------------------------------ |
| **Assertividade**    | O agente identificou corretamente o nível de risco?       | Evento com IP suspeito deve ser classificado como risco alto |
| **Segurança**        | O agente evitou inventar informações ou extrapolar dados? | Pergunta sem contexto → agente admite limitação              |
| **Coerência**        | A resposta condiz com os dados fornecidos?                | Login normal não deve ser classificado como alto risco       |
| **Clareza**          | A explicação é compreensível para o usuário?              | Explicação sem jargões excessivos                            |
| **Ação Recomendada** | As sugestões são úteis e aplicáveis?                      | Recomendar 2FA em caso de acesso suspeito                    |
---

## Exemplos de Cenários de Teste

Crie testes simples para validar seu agente:

### Teste 1: Login suspeito
- **Pergunta:** "Analise este evento: login falhou 5 vezes, IP suspeito, localização Rússia, horário 03:00"
- **Resposta esperada:** Risco alto + explicação sobre localização incomum, múltiplas tentativas e IP suspeito
- **Resultado:** [ ] Correto [ ] Incorreto

### Teste 2: Acesso normal
- **Pergunta:** "Login realizado com sucesso no Brasil às 14:00"
- **Resposta esperada:** Risco baixo + confirmação de comportamento normal
- **Resultado:** [ ] Correto [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo amanhã?"
- **Resposta esperada:** Agente informa que não trata desse tipo de informação
- **Resultado:** [ ] Correto [ ] Incorreto

### Teste 4: Informação insuficiente
- **Pergunta:** "Esse acesso é seguro?"
- **Resposta esperada:** Agente solicita mais informações antes de analisar
- **Resultado:** [ ] Correto [ ] Incorreto

### Teste 5: Comportamento anômalo leve
- **Pergunta:** "Login em horário incomum, mas localização conhecida"
- **Resposta esperada:** Risco médio + recomendação de monitoramento
- **Resultado:** [ ] Correto [ ] Incorreto

---

## Resultados

Após a execução dos testes:

O que funcionou bem:

- Classificação de risco consistente em cenários claros
- Explicações objetivas e fáceis de entender
- Boa aderência às regras de não inventar informações

O que pode melhorar:

- Maior precisão em casos intermediários (risco médio)
- Melhor detalhamento em recomendações
- Adição de contexto histórico para análises mais avançadas

---

## Métricas Avançadas

Para evoluções futuras do projeto, podem ser consideradas métricas técnicas como:

- Tempo de resposta do agente
- Consumo de tokens em chamadas de IA
- Taxa de respostas incompletas ou inconclusivas
- Registro de logs de interações

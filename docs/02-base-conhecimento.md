# Base de Conhecimento

## Dados Utilizados

| Arquivo                 | Formato | Utilização no Agente                                                |
| ----------------------- | ------- | ------------------------------------------------------------------- |
| `logs_acesso.json`      | JSON    | Armazenar eventos de login (IP, localização, horário)               |
| `eventos_seguranca.csv` | CSV     | Registrar ações suspeitas (login falho, tentativas múltiplas, etc.) |
| `usuarios.json`         | JSON    | Informações básicas dos usuários (nome, padrão de uso, permissões)  |
| `ips_suspeitos.csv`     | CSV     | Lista de IPs com histórico malicioso para validação                 |

---

## Adaptações nos Dados

Os dados utilizados são mockados (simulados), porém foram adaptados para representar cenários reais de segurança, incluindo:

- Simulação de acessos de diferentes países
- Eventos de login em horários incomuns
- Tentativas consecutivas de login (possível força bruta)
- Inclusão de IPs marcados como suspeitos

Essas adaptações permitem que o agente tenha um comportamento mais próximo de um ambiente real de análise de incidentes.

---

## Estratégia de Integração

### Como os dados são carregados?

Os arquivos JSON e CSV são carregados no início da execução do agente e utilizados como base para análise dos eventos.

Eles podem ser:

- lidos diretamente no backend (Python)
- ou simulados dentro do próprio contexto do prompt (em versões mais simples)

### Como os dados são usados no prompt?

Os dados são inseridos dinamicamente no prompt enviado ao modelo de linguagem, permitindo que o agente:

- analise o evento atual com contexto
- compare com padrões conhecidos
- identifique anomalias

Parte dos dados funciona como contexto temporário, e parte como base de referência (ex: IPs suspeitos).

---

## Exemplo de Contexto Montado

```
Dados do Evento:
- Usuário: gabriel
- IP: 185.220.101.45
- Localização: Rússia
- Horário: 03:12
- Ação: login_failed

Histórico do Usuário:
- Localização comum: Brasil
- Horário comum: 08:00 - 22:00

Validação de Segurança:
- IP listado como suspeito: Sim
- Tentativas consecutivas: 5
```

# Test Strategy and Automated Test Suite – Scholarship Eligibility Evaluator

## Visão Geral

Este projeto simula um sistema de avaliação de elegibilidade para bolsa acadêmica. Ele recebe dados do candidato, aplica regras de negócio e retorna um status final (`APPROVED`, `MANUAL_REVIEW` ou `REJECTED`), além dos motivos que levaram a essa decisão.

O objetivo principal não é construir uma aplicação de produção complexa, mas demonstrar uma boa estratégia de testes automatizados em Python com foco em:

- regras de negócio bem definidas;
- validação de dados de entrada;
- testes de fronteira;
- testes de exceção;
- cobertura de cenários críticos.

---

## 1. Escolha Tecnológica

- Linguagem: `Python 3.11`
- Framework de teste: `Pytest`
- Modelagem: `Enum` e `dataclass`

Justificativa:

- Python favorece legibilidade e manutenção.
- Pytest é simples de usar, muito popular e excelente para parametrização.
- A combinação de `Enum` e `dataclass` deixa o código mais organizado e fácil de testar.

---

## 2. O que o projeto abrange

O módulo [scholarship_system.py](C:/Users/User/Testes-Automatizados_Estudos.worktrees/projeto-avaliacao-e-testes/scholarship_system.py) implementa a lógica de avaliação de elegibilidade com as seguintes regras:

- Idade mínima:
  - menor que 16 => `REJECTED`
  - 16 ou 17 => `MANUAL_REVIEW`
- GPA:
  - menor que 6.0 => `REJECTED`
  - entre 6.0 e 6.9 => `MANUAL_REVIEW`
  - 7.0 ou mais => aprovação, desde que os demais critérios também sejam atendidos
- Frequência:
  - menor que 75.0 => `REJECTED`
  - entre 75.0 e 79.9 => `MANUAL_REVIEW`
- Cursos obrigatórios:
  - ausentes => `REJECTED`
- Histórico disciplinar:
  - presença => `REJECTED`
- Validações extras:
  - idade deve ser inteiro não negativo;
  - GPA e frequência devem ser numéricos finitos e dentro de faixas válidas;
  - flags booleanas devem ser do tipo correto.

Em resumo, o projeto cobre regras de negócio e robustez de entrada de dados, que são aspectos importantes para qualquer sistema de decisão automatizada.

---

## 3. Estrutura dos testes

A suíte em [test_scholarship.py](C:/Users/User/Testes-Automatizados_Estudos.worktrees/projeto-avaliacao-e-testes/test_scholarship.py) foi ampliada para incluir diversas categorias:

### 3.1 Testes funcionais

Validam o comportamento correto do sistema em cenários reais de negócio:

- aprovado
- revisão manual
- rejeitado por idade
- rejeitado por GPA
- rejeitado por frequência
- rejeitado por cursos obrigatórios
- rejeitado por histórico disciplinar

### 3.2 Testes de fronteira (valor limite)

A análise de valor limite cobre pontos críticos da regra de negócio:

- idade: 15, 16, 17, 18
- GPA: 5.9, 6.0, 6.9, 7.0
- frequência: 74.9, 75.0, 79.9, 80.0

Esses valores são importantes porque erros de regra geralmente surgem exatamente na transição entre classes.

### 3.3 Testes de múltiplos motivos

Conferem que, quando o candidato falha em mais de um critério, o sistema retorna todos os motivos relevantes, sem perder informação ou priorizar apenas um deles.

### 3.4 Testes de robustez e validação de entrada

Esse foi o ponto mais reforçado no projeto. Agora a suíte valida que:

- idade negativa é rejeitada;
- GPA fora do intervalo é rejeitado;
- frequência fora do intervalo é rejeitada;
- valores `NaN` e `inf` são rejeitados;
- flags booleanas devem ser realmente booleanas;
- tipos inválidos geram `ValueError` com mensagens claras.

---

## 4. Resultados atuais

A execução da suíte foi validada com o comando:

```bash
pytest -q
```

Resultado atual:

- 41 testes executados
- 41 aprovados
- tempo: 0,12s

Isso indica que a lógica está consistente e que os cenários de negócio e validação foram ampliados com boa segurança.

---

## 5. Qualidade da base de testes

A base de testes é boa para um projeto de estudo e demonstração. Ela possui:

- cobertura ampla dos fluxos principais;
- parametrização eficiente;
- validação de regras de transição e exceção;
- maior robustez em comparação ao início do projeto.

Pontos fortes:

- estrutura simples e legível;
- fácil manutenção;
- boa cobertura de cenários de negócio;
- validação de entradas inválidas.

Limitações naturais de um projeto pequeno:

- não é um sistema de produção real com integração de banco, APIs ou autenticação;
- não inclui testes de regressão em múltiplos ambientes;
- não cobre aspectos de performance, concorrência ou consumo externo.

Mesmo assim, para um exercício didático, a suíte está bem acima do nível básico e já mostra um comportamento de qualidade profissional.

---

## 6. Tipos de falhas que os testes continuam ajudando a evitar

Mesmo com a robustez aumentada, alguns riscos continuam sendo relevantes:

1. Mudança de regra de negócio sem atualização de teste.
2. Entrada de parâmetros em tipos incorretos.
3. Valores numéricos inválidos, como `NaN` ou infinitos.
4. Falhas na composição de múltiplos critérios simultâneos.
5. Erros de interpretação na fronteira entre status (`REJECTED`, `MANUAL_REVIEW`, `APPROVED`).

A suíte reduz muito esse risco ao validar tanto a regra principal quanto os limites e as entradas inválidas.

---

## 7. Como executar

### Pré-requisitos

- Python 3.x instalado
- Pytest instalado

### Instalar dependências

```bash
pip install pytest
```

### Executar testes

```bash
pytest -q
```

### Executar com detalhamento

```bash
pytest -v
```

---

## 8. Conclusão

O projeto evoluiu de um conjunto básico de testes para uma suíte mais sólida, com foco em regras de negócio, validação e robustez. Ele continua sendo uma boa referência para exercícios de engenharia de software e automação de testes em Python.

A combinação entre regras de decisão, validação de tipos e testes de fronteira torna a suíte útil como exemplo didático e como base para extensões futuras.

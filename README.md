# Relatório de Testes: Scholarship Eligibility Evaluator

## 1. Escolha Tecnológica
* **Linguagem:** `Python 3.11`
* **Framework de Teste:** `Pytest 7.4.2`
* **Justificativa:** A escolha do **Python** se deve à sua sintaxe concisa e alta legibilidade. O framework **Pytest** foi selecionado por permitir a **parametrização de testes**, técnica essencial para validar múltiplas entradas de fronteira (Análise de Valor Limite) sem redundância de código, garantindo uma suíte eficiente e de fácil manutenção.

---

## 2. Projeto dos Testes

### Técnicas Funcionais (Caixa-Preta)
Para garantir que o sistema atende aos requisitos de negócio sem olhar o código interno:
* **Particionamento por Classes de Equivalência:** As entradas foram divididas em grupos (Aprovados, Revisão Manual e Rejeitados) para garantir que cada cenário de negócio seja testado ao menos uma vez.
* **Análise de Valor Limite (AVL):** Testes rigorosos nos pontos exatos de transição de status (ex: as notas **5.9**, **6.0**, **6.9** e **7.0**).

### Técnicas Estruturais (Caixa-Branca)
A suíte foi desenhada para atingir **100% de Cobertura de Decisão (Branch Coverage)**:
* **Fluxos de Exceção:** Testes que garantem que cada cláusula `if` e `elif` de erro ou revisão seja disparada.
* **Precedência de Regras:** Verificação de que um motivo de `REJECTED` tem prioridade sobre um de `MANUAL_REVIEW` no retorno do sistema.

---

## 3. Identificação de Casos de Teste

### Tabela de Classes e Limites Considerados
| Variável | Valor Testado | Status Esperado | Critério de Teste |
| :--- | :--- | :--- | :--- |
| **Idade** | `15` | **REJECTED** | Classe Inválida (Abaixo da mínima) |
| **Idade** | `16` | **MANUAL_REVIEW** | Limite Inferior de Revisão |
| **Idade** | `18` | **APPROVED** | Classe Válida (Maioridade) |
| **GPA** | `5.9` | **REJECTED** | Valor Limite (Reprovação) |
| **GPA** | `6.0` | **MANUAL_REVIEW** | Valor Limite (Início Revisão) |
| **GPA** | `7.0` | **APPROVED** | Fronteira de Aprovação Direta |
| **Frequência** | `74.9` | **REJECTED** | Valor Limite (Frequência Insuficiente) |
| **Disciplinar** | `True` | **REJECTED** | Decisão Estrutural (Histórico) |

---

## 4. Análise de Adequação da Suíte

**A suíte pode ser considerada adequada?**

**Sim.** A suíte é adequada pois atende a todos os requisitos da APS: cobre os casos de `APPROVED`, `MANUAL_REVIEW`, múltiplos motivos de `REJECTED` e `INVALID_INPUT`. Além disso, a combinação de técnicas funcionais e estruturais garante que não existam caminhos mortos no código.

**Que tipos de falhas ainda poderiam passar despercebidos?**

1. **Erros de Tipagem:** O Python não impede a entrada de Strings no lugar de números (ex: idade="dezoito"), o que causaria erro de parada.
2. **Precisão Numérica:** Valores com muitas casas decimais (ex: `6.9999999`) podem variar conforme a precisão do processador.
3. **Paradoxo do Pesticida:** Se a especificação original da regra de negócio estiver errada (ex: se o cliente queria idade mínima 17 e no código está 16), os testes passarão, mas o software estará incorreto perante o cliente.

---

## 5. Instruções de Execução

### Pré-requisitos
* Ter o Python 3.x instalado.

### Comandos para o Terminal
1. **Instalar o Framework Pytest:**
   ```bash
   pip install pytest

2. **Executar a Suíte de Testes:**
    ```bash
    pytest -v
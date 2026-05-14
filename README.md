# 🔋 AL 2.1 — Características de uma Pilha

Simulador virtual interativo para a atividade laboratorial **AL 2.1** de **Física e Química A (10.º ano)**.

Permite aos alunos explorar as características elétricas de uma pilha — força eletromotriz (f.e.m.) e resistência interna — através de um circuito animado e ferramentas de análise gráfica.

---

## ✨ Funcionalidades

- **Circuito interativo animado** com pilha, reóstato, voltímetro e amperímetro
- **Leituras em tempo real** de tensão (U), corrente (I) e potência (P)
- **Modelo físico realista** com sobrepotencial de polarização não-linear
- **Ruído de medição simulado** para imitar instrumentos reais
- **Gráfico U(I)** com regressão linear e determinação experimental de ε e r
- **Gráfico P(R)** com curva teórica sobreposta
- **Tabela de dados** exportável
- **Modo professor**: parâmetros da pilha configuráveis em painel oculto

---

## 📋 Pré-requisitos

- Python 3.8 ou superior
- `bash` (Linux / macOS)

---

## 🚀 Como executar

```bash
# 1. Clonar o repositório
git clone https://github.com/ruiblev/pilha_caracteristicas.git
cd pilha_caracteristicas

# 2. Dar permissão de execução ao script (apenas na primeira vez)
chmod +x run.sh

# 3. Iniciar o simulador
./run.sh
```

O script `run.sh` trata automaticamente de:
- Criar um ambiente virtual Python (`venv/`)
- Instalar todas as dependências
- Lançar o simulador no browser

Aceda ao link **Local URL** que aparece no terminal (por omissão: `http://localhost:8501`).

---

## 🗂️ Estrutura do projeto

```
pilha_caracteristicas/
├── app.py            # Aplicação principal (Streamlit)
├── circuit_view.py   # Componente HTML/JS do circuito animado
├── requirements.txt  # Dependências Python
├── run.sh            # Script de arranque automático
└── README.md
```

---

## 🧪 Como usar o simulador

1. **Configure a pilha** (opcional, para o professor) no painel lateral em *"Configurar Pilha"* — defina a f.e.m. (ε) e a resistência interna (r) reais.
2. **Varie a resistência externa** (reóstato) usando o slider *"Resistência Externa (R)"*.
3. **Observe** os valores de U, I e P a atualizar em tempo real no circuito.
4. Clique em **"📝 Registar Dados"** para guardar o ponto atual.
5. Repita para diferentes valores de R.
6. Analise os gráficos nos separadores:
   - **U(I)** — determina ε (ordenada na origem) e r (declive negativo) por regressão linear
   - **P(R)** — ilustra a transferência máxima de potência quando R ≈ r

---

## 📦 Dependências

| Pacote      | Utilização                          |
|-------------|-------------------------------------|
| `streamlit` | Interface web interativa            |
| `pandas`    | Gestão da tabela de dados           |
| `numpy`     | Cálculos numéricos e físicos        |
| `plotly`    | Gráficos interativos                |
| `scipy`     | Regressão linear (stats.linregress) |

---

## 📐 Modelo Físico

A tensão da pilha é modelada com um fator de polarização não-linear:

$$U = \varepsilon - r \cdot I - c \cdot I^2$$

onde $c = 0{,}15\ \Omega/\text{A}$ é o coeficiente empírico de polarização. A corrente de circuito é determinada resolvendo a equação quadrática resultante de igualar $U_{\text{pilha}} = U_{\text{externo}} = R \cdot I$.

---

## 📄 Licença

Projeto de uso educativo — livre para utilização em contexto escolar.
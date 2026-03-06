## Protocolo de Encriptação Temporizada por Custo — Formalização

---

### Visão Geral

Um arquivo $F$ é encriptado com AES-256-GCM usando uma chave $K$ derivada via HMAC-SHA256 de uma **semente curta** $S$ de $n$ bits. Um hash $V = \text{HMAC-SHA256}(S,\ n)$ é publicado como **compromisso de verificação** — qualquer um pode testar candidatos contra $V$ sem precisar do arquivo. A chave é derivada encadeando: $K = \text{HMAC-SHA256}(S,\ V)$. Um único protocolo (HMAC-SHA256) para tudo.

---

### Parâmetros de Entrada

| Símbolo | Tipo | Descrição |
|---------|------|-----------|
| $F$ | $\{0,1\}^*$ | **File** — arquivo original em bytes |
| $T$ | $\mathbb{R}^+$ | **Time** — tempo alvo em anos |
| $t_0$ | $\mathbb{N}$ | **Time zero** — ano de criação do puzzle |

---

### Construção do Puzzle

**Passo 1 — Calcular a dificuldade:**

$$n = \mathcal{B}(t_0,\ \$1\text{M}) + \lfloor \log_2(T \times 365) \rfloor$$

| Parte | Significado |
|-------|-------------|
| $n$ | Tamanho da semente em bits — define a dificuldade do puzzle |
| $\mathcal{B}(t_0, \$1\text{M})$ | Bits que $\$1\text{M}$ de hardware compra em $t_0$ rodando por 1 ano |
| $T \times 365$ | Converte anos em dias — fator de escala temporal |
| $\lfloor \log_2(\cdot) \rfloor$ | Converte o fator multiplicativo em bits adicionais |

> Intuição: $\mathcal{B}$ define quantos bits $\$1\text{M}$/ano alcança hoje. Cada ano extra exige 365× mais trabalho, ou seja, $\approx 8{,}5$ bits a mais.

**Passo 2 — Gerar a semente:**

$$S \xleftarrow{\$} \{0,1\}^n$$

| Parte | Significado |
|-------|-------------|
| $S$ | **Seed** — semente aleatória de $n$ bits; é o segredo do puzzle |
| $\xleftarrow{\$}$ | Amostragem uniforme aleatória (o cifrão indica aleatoriedade criptográfica) |
| $\{0,1\}^n$ | Conjunto de todas as strings binárias de comprimento $n$ |

**Passo 3 — Hash de verificação:**

$$V \leftarrow \text{HMAC-SHA256}(S,\ n)$$

| Parte | Significado |
|-------|-------------|
| $V$ | **Verification hash** — compromisso público de $S$; permite verificar sem o arquivo |
| $\text{HMAC-SHA256}$ | Código de autenticação baseado em hash — RFC 2104 |
| $S$ | Chave do HMAC (o segredo) |
| $n$ | Mensagem do HMAC (parâmetro público) |

**Passo 4 — Derivar a chave:**

$$K \leftarrow \text{HMAC-SHA256}(S,\ V)$$

| Parte | Significado |
|-------|-------------|
| $K$ | **Key** — chave AES de 256 bits derivada do encadeamento $S \to V \to K$ |
| $S$ | Chave do HMAC (mesmo segredo) |
| $V$ | Mensagem do HMAC (output do passo anterior) |

> Mesmo protocolo do Passo 3, com mensagem diferente. $V$ alimenta $K$ — encadeamento natural.

**Passo 5 — Encriptar o arquivo:**

$$C \leftarrow \text{AES-256-GCM}(K,\ F)$$

| Parte | Significado |
|-------|-------------|
| $C$ | **Ciphertext** — arquivo encriptado + authentication tag GCM |
| $\text{AES}$ | **Advanced Encryption Standard** — cifra de bloco simétrica |
| $256$ | Tamanho da chave em bits |
| $\text{GCM}$ | **Galois/Counter Mode** — encriptação autenticada (confidencialidade + integridade) |

**Passo 6 — Publicar:**

$$(C,\ n,\ V)$$

| Parte | Significado |
|-------|-------------|
| $C$ | Ciphertext (contém o tag GCM embutido) |
| $n$ | Número de bits da semente — informa o espaço de busca |
| $V$ | Hash de verificação — permite testar candidatos sem decriptar |

---

### Como o Atacante Quebra

**Fase 1 — Busca (rápida, sem o arquivo):**

$$\forall\ S' \in \{0,1\}^n: \quad \text{HMAC-SHA256}(S',\ n) \stackrel{?}{=} V$$

Cada teste é um único HMAC-SHA256.

**Fase 2 — Decriptação (uma única vez, quando encontrar $S'$):**

$$V \leftarrow \text{HMAC-SHA256}(S',\ n)$$
$$K \leftarrow \text{HMAC-SHA256}(S',\ V)$$
$$F \leftarrow \text{AES-256-GCM.Dec}(K,\ C)$$

Custo esperado: $2^n$ avaliações de HMAC-SHA256. Cada tentativa é independente — **busca puramente paralela**.

---

### Fórmula de Custo

O custo para quebrar **hoje em 1 dia** com o melhor hardware disponível:

$$\boxed{ \text{Custo}(T,\ t_0) = \$1\text{M} \times T \times 365 }$$

**Exemplos com $t_0 = 2025$:**

| Tempo alvo $T$ | Bits $n$ | Custo hoje em 1 dia |
|---------------|----------|---------------------|
| 1 mês | ~86 bits | ~$30.000 |
| 1 ano | ~90 bits | ~$365.000 |
| 5 anos | ~92 bits | ~$1,8M |
| 10 anos | ~93 bits | ~$3,6M |
| 50 anos | ~96 bits | ~$18M |
| 100 anos | ~97 bits | ~$36M |

> A escala é **linear em dólares mas logarítmica em bits** — duplicar o tempo alvo adiciona apenas 1 bit mas dobra o custo.

---

### Propriedades do Protocolo

- **Verificação sem o arquivo** — $V$ permite provar que $S'$ é a solução sem precisar de $C$
- **Um único protocolo** — HMAC-SHA256 para verificação e derivação de chave
- **Não há custódio** — nenhum terceiro guarda $S$; ele existe apenas como espaço de busca
- **Verificável publicamente** — qualquer um com $V$ pode confirmar que um $S'$ é a solução
- **Custo previsível** — a tabela $\mathcal{B}$ permite estimar o custo de quebra em qualquer ano futuro
- **Degradação natural** — à medida que hardware evolui, o custo de quebra cai; isso é **intencional** e quantificável
- **Busca puramente paralela** — cada tentativa é independente; escala linearmente com hardware

---

## Benchmark de Poder Computacional por Busca Exaustiva

---

### Motivação

Comparar poder computacional ao longo do tempo exige uma tarefa de referência que seja:

1. **Computacionalmente mensurável** — custo teórico bem definido
2. **Sem atalhos algorítmicos** — não melhorável por criptoanalise
3. **Paralelizável linearmente** — dobrando hardware, dobra o progresso

A busca exaustiva sobre HMAC-SHA256 satisfaz essas propriedades: cada candidato exige uma avaliação de HMAC, sem atalho possível.

---

### O Benchmark $\mathcal{B}(t, D)$

Seja:

- $t$ — ano de referência
- $D$ — orçamento em dólares
- $P(t, D)$ — número total de tentativas (HMAC-SHA256) executáveis com orçamento $D$ no ano $t$, rodando por 1 ano contínuo
- $\mathcal{B}(t, D)$ — maior $n$ tal que $2^n \leq P(t, D)$

$$\mathcal{B}(t, D) = \lfloor \log_2 P(t, D) \rfloor$$

**Interpretação:** $\mathcal{B}(t, D)$ é o número máximo de bits de semente que o orçamento $D$ no ano $t$ consegue buscar exaustivamente em 1 ano.

---

### Aproximação Contínua de $\mathcal{B}$

A tabela histórica (1965–2025) é discreta. Para uso programático e extrapolação, aproximamos $\mathcal{B}(t, \$1\text{M})$ por uma **função logística** ajustada por mínimos quadrados:

$$\boxed{ \mathcal{B}(t) = \frac{L}{1 + e^{-k(t - t_{\text{mid}})}} + b }$$

| Parâmetro | Valor | Significado |
|-----------|-------|-------------|
| $L$ | $74{,}89$ | Amplitude da curva (range em bits) |
| $k$ | $0{,}0553$ | Taxa de crescimento |
| $t_{\text{mid}}$ | $2004{,}5$ | Ponto de inflexão (metade do crescimento) |
| $b$ | $25{,}31$ | Offset base (bits mínimos) |

**Propriedades da aproximação:**

- **MSE = 5,12** contra os 17 pontos da tabela histórica (erro médio $\approx \pm 2{,}3$ bits)
- **Assíntota superior:** $L + b \approx 100$ bits — limite natural do hardware acessível com $\$1\text{M}$
- **Assíntota inferior:** $b \approx 25$ bits — capacidade mínima mesmo em hardware primitivo
- **Ponto de inflexão:** $t_{\text{mid}} = 2004{,}5$ — metade do crescimento ocorreu antes de 2005

> A curva logística captura a forma de S dos dados: crescimento lento (1960s–80s), aceleração (1990s–2010s), e desaceleração (2020s+). A alternativa logarítmica pura ($a \ln(t) + b$) tem MSE = 49,89 — quase 10× pior.

---

### Definição de Equivalência Temporal

Dado $\mathcal{B}(t_1, D) = b_1$ e $\mathcal{B}(t_2, D) = b_2$, o custo em $t_2$ para replicar o poder de $t_1$ é:

$$C(t_1 \to t_2) = D \cdot 2^{b_1 - b_2}$$

**Exemplo:** $\mathcal{B}(1980, 1\text{M}) = 40$ e $\mathcal{B}(2025, 1\text{M}) = 81$

$$C(1980 \to 2025) = \$1\text{M} \cdot 2^{40-81} = \$1\text{M} \cdot 2^{-41} \approx \$0{,}0000005$$

---

### Propriedades do Benchmark

**Monotonicidade esperada:** $\mathcal{B}(t+1, D) \geq \mathcal{B}(t, D)$ — o poder só cresce ou mantém.

**Violações detectam anomalias reais:** quedas em $\mathcal{B}$ (como 2021 na tabela) indicam inflação de hardware, escassez ou outras distorções de mercado — não ruído do benchmark.

**Independência de domínio:** o mesmo $\mathcal{B}$ serve para criptografia, IA, simulação — qualquer campo onde o custo computacional importa.

---

### Aplicações

- **Parametrização de esquemas criptográficos:** definir $n$ baseado no ano de implantação e vida útil esperada do sistema
- **Protocolo de revelação temporizada:** o prazo é expresso em bits de $\mathcal{B}$, não em tempo absoluto, tornando-o robusto a avanços de hardware




(ISSO DEVE PERMANECER INTACTO)

| Ano | Melhor hardware | H/s com $1M | Bits alcançáveis | Custo hoje para replicar |
|-----|----------------|-------------|-----------------|--------------------------|
| 1965 | IBM 360 | 3×10² | 33 bits | $0,000000001 |
| 1970 | CDC 7600 | 2×10³ | 36 bits | $0,00000001 |
| 1975 | Cray protótipo | 5×10³ | 37 bits | $0,00000006 |
| 1980 | Cray-1 | 2×10⁴ | 40 bits | $0,000001 |
| 1985 | Cray-2 | 5×10⁴ | 41 bits | $0,000001 |
| 1990 | Workstations RISC | 10⁸ | 51 bits | $0,001 |
| 1995 | Pentium cluster | 3×10⁹ | 56 bits | $0,03 |
| 2000 | Pentium III farm | 2×10¹⁰ | 59 bits | $0,24 |
| 2005 | Athlon 64 cluster | 2×10¹¹ | 62 bits | $1,90 |
| 2010 | GPU GTX 480 farm | 1,6×10¹¹ | 62 bits | $1,90 |
| 2013 | ASIC Butterfly Labs | 2×10¹⁴ | 72 bits | $1.950 |
| 2015 | Antminer S5 | 3×10¹⁵ | 76 bits | $31.250 |
| 2017 | Antminer S9 | 7×10¹⁵ | 77 bits | $62.500 |
| 2019 | Antminer S17 | 2,7×10¹⁶ | 79 bits | $250.000 |
| 2021 | Antminer S19 Pro | 1,4×10¹⁶ | 78 bits | $125.000 |
| 2023 | Antminer S19 XP | 4,7×10¹⁶ | 80 bits | $500.000 |
| 2025 | Antminer S21 Pro | 5,9×10¹⁶ | 81 bits | $1.000.000 |
---

Leituras notáveis:

- O Cray-1 em 1980 custou $8M — sua capacidade computacional hoje custa menos de $0,000001. Uma fração de centavo.
- O que em 1990 custava $1M hoje custa $0,001 — mil vezes mais barato a cada ~25 anos não captura nem a metade da história.
- A inversão de 2021 (78 vs 79 bits) mostra que preço de ASIC é volátil — o mercado de Bitcoin inflacionou o hardware naquele ciclo.
- Cada bit a mais na coluna da direita representa o dobro do custo — a escala é exponencial, não linear.
- A coluna de custo sobe ~3 ordens de grandeza a cada 10 anos em média — exceto no salto 1985→1990 (workstations democratizando) e 2010→2013 (chegada dos ASICs), que foram descontinuidades abruptas na curva.
- Queda em 2021: preços de ASICs inflacionados pelo bull market de Bitcoin — hardware mais caro, menos unidades por $1M.

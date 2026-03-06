## Protocolo de Encriptação Temporizada por Custo — Formalização

---

### Visão Geral

Um arquivo é encriptado com uma chave $K$. O comprometimento público de $K$ é postado de forma análoga a uma carteira Bitcoin — qualquer um pode ver o compromisso, mas revelar $K$ exige resolver um problema de segunda pré-imagem com dificuldade calibrada. O parâmetro de entrada é **quanto tempo levaria para quebrar com hardware atual** — e o protocolo retorna **o custo em dólares para quebrar hoje em 1 dia**.

---

### Parâmetros de Entrada

| Símbolo | Descrição |
|---------|-----------|
| $F$ | Arquivo original |
| $T$ | Tempo alvo para quebra com $\$1\text{M}$ de hardware (em anos) |
| $t_0$ | Ano de criação do puzzle |

---

### Construção do Puzzle

**Passo 1 — Gerar a chave:**

$$K \xleftarrow{\$} \{0,1\}^{256}$$

**Passo 2 — Encriptar o arquivo:**

$$C \leftarrow \text{AES-256-GCM}(K, F)$$

**Passo 3 — Calcular a dificuldade:**

Com base na tabela $\mathcal{B}(t_0, \$1\text{M})$ e no tempo alvo $T$:

$$n = \mathcal{B}(t_0,\ \$1\text{M}) + \lfloor \log_2(T \times 365) \rfloor$$

> Intuição: $\mathcal{B}$ define quantos bits $\$1\text{M}$/ano alcança hoje. Cada ano extra exige 365× mais trabalho, ou seja, $\approx 8{,}5$ bits a mais.

**Passo 4 — Compromisso público (à la Bitcoin):**

$$\text{addr} = \text{Argon2id}(K,\ \text{salt},\ n\text{-bits de dificuldade})$$

Publicar o par $(\text{addr},\ C)$ — análogo a uma carteira Bitcoin onde `addr` é público mas $K$ é o segredo.

Quem encontrar $K'$ tal que $\text{Argon2id}(K') = \text{addr}$ obtém a chave e decripta $C$.

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

### É possível o endereço público à la Bitcoin?

**Sim, e é exatamente o que o protocolo faz.** A analogia é direta:

| Bitcoin | Este protocolo |
|---------|---------------|
| Chave privada $sk$ | Chave de encriptação $K$ |
| Endereço público $H(pk)$ | Compromisso $\text{Argon2id}(K)$ |
| Transação na blockchain | Par $(\text{addr}, C)$ publicado |
| Gastar = provar posse de $sk$ | Decriptar = provar posse de $K$ |
| Segurança: ECDLP | Segurança: segunda pré-imagem |

A diferença chave: em Bitcoin o endereço **nunca deve ser quebrado**. Aqui, o endereço **é projetado para ser quebrado** — mas somente após o custo computacional justificar o prazo desejado.

---

### Propriedades do Protocolo

- **Não há custódio** — nenhum terceiro guarda $K$; ele está implícito no puzzle
- **Verificável publicamente** — qualquer um pode confirmar que $C$ foi encriptado com a $K$ que resolve o puzzle
- **Custo previsível** — a tabela $\mathcal{B}$ permite estimar o custo de quebra em qualquer ano futuro
- **Degradação natural** — à medida que hardware evolui, o custo de quebra cai; isso é **intencional** e quantificável

## Benchmark de Poder Computacional por Segunda Pré-Imagem

---

### Motivação

Comparar poder computacional ao longo do tempo exige uma tarefa de referência que seja:

1. **Computacionalmente mensurável** — custo teórico bem definido
2. **Hardware-neutra** — sem vantagem para hardware especializado
3. **Sem atalhos algorítmicos** — não melhorável por criptoanalise
4. **Paralelizável linearmente** — dobrando hardware, dobra o progresso

A segunda pré-imagem satisfaz todas essas propriedades.

---

### Definição Formal

**Problema:** Dado $m$ tal que $H(m) = d$, encontrar $m' \neq m$ com $H(m') = d$.

**Custo esperado:** $2^n$ avaliações de $H$, onde $n$ é o tamanho do digest em bits.

**Sem atalho conhecido:** diferente de colisão ($2^{n/2}$ por birthday attack), segunda pré-imagem não possui redução abaixo de $2^n$ para funções hash ideais.

---

### O Benchmark $\mathcal{B}(t, D)$

Seja:

- $t$ — ano de referência
- $D$ — orçamento em dólares
- $P(t, D)$ — número total de avaliações de $H$ executáveis com orçamento $D$ no ano $t$, rodando por 1 ano contínuo
- $\mathcal{B}(t, D)$ — maior $n$ tal que $2^n \leq P(t, D)$

$$\mathcal{B}(t, D) = \lfloor \log_2 P(t, D) \rfloor$$

**Interpretação:** $\mathcal{B}(t, D)$ é o número máximo de bits de segunda pré-imagem que o orçamento $D$ no ano $t$ consegue quebrar em 1 ano.

---

### Condição de Hardware-Neutralidade

Para que o benchmark seja válido, $H$ deve ser escolhida tal que:

$$\frac{\text{H/s (ASIC)}}{\text{H/s (CPU/GPU commodity)}} \approx 1$$

Isso exclui **SHA-256** (ASICs Bitcoin são $\sim 10^4\times$ mais eficientes que GPU) e favorece funções **memory-hard** como:

| Função | Razão ASIC/GPU | Adequação |
|--------|---------------|-----------|
| SHA-256 | ~10.000× | ✗ inválida |
| SHA-3 (Keccak) | ~10× | ✗ marginalmente |
| Argon2 | ~1,2× | ✓ ideal |
| scrypt | ~2× | ✓ aceitável |
| BLAKE3 | ~5× | ~ aceitável |

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

- **Parametrização de esquemas criptográficos:** definir $n$ de uma função hash baseado no ano de implantação e vida útil esperada do sistema
- **Proof-of-work justo:** substituir SHA-256 por função memory-hard torna mineração resistente a ASICs e o benchmark aplicável diretamente
- **Protocolo de revelação temporizada:** como discutido anteriormente — o prazo é expresso em bits de $\mathcal{B}$, não em tempo absoluto, tornando-o robusto a avanços de hardware




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

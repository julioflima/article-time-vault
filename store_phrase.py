"""
Grava uma mensagem de 80 bytes na blockchain do Bitcoin via OP_RETURN.
Instalar dependência: pip install bit
"""

from bit import Key
from bit.network import NetworkAPI

# ============================================================
# CONFIGURAÇÃO — edite apenas esta seção
# ============================================================

CHAVE_PRIVADA_WIF = "SUA_CHAVE_PRIVADA_WIF_AQUI"  # começa com K, L ou 5

MENSAGEM = "In 2026, Bitcoin holds the memory of every soul who dared to believe in freedom."

TAXA_SAT_POR_BYTE = 2  # 1-5 = econômico | 10-20 = rápido

# ============================================================
# VERIFICAÇÕES
# ============================================================

msg_bytes = MENSAGEM.encode("utf-8")
assert len(msg_bytes) <= 80, f"Mensagem muito longa: {len(msg_bytes)} bytes (máx 80)"
print(f"✅ Mensagem: {len(msg_bytes)} bytes — OK")

# ============================================================
# CARREGA CARTEIRA E MOSTRA SALDO
# ============================================================

chave = Key(CHAVE_PRIVADA_WIF)
print(f"📬 Endereço: {chave.address}")

saldo_btc = chave.get_balance("btc")
print(f"💰 Saldo:    {saldo_btc} BTC")

if float(saldo_btc) == 0:
    print("❌ Saldo zero. Envie uma pequena quantia para o endereço acima e tente de novo.")
    exit(1)

# ============================================================
# MONTA E ENVIA A TRANSAÇÃO COM OP_RETURN
# ============================================================

print("\n🔨 Construindo transação...")

outputs = [
    (msg_bytes, 0, "op_return")   # valor = 0, dados = sua mensagem
]

tx_hex = chave.create_transaction(
    outputs,
    fee=TAXA_SAT_POR_BYTE,
    absolute_fee=False
)

print("📡 Enviando para a rede Bitcoin...")
txid = NetworkAPI.broadcast_tx(tx_hex)

# ============================================================
# RESULTADO
# ============================================================

print("\n" + "="*60)
print("✅ TRANSAÇÃO ENVIADA COM SUCESSO!")
print(f"🔗 TXID: {txid}")
print(f"🌐 Ver em: https://mempool.space/tx/{txid}")
print("="*60)
print("\nSua mensagem está gravada para sempre na blockchain. 🎉")
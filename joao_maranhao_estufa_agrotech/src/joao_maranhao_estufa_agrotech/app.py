class ServicoLogger:
    """Serviço responsável pelo registro de logs do sistema em arquivo."""

    def __init__(self, caminho_arquivo: str | None = None):
        self.caminho_arquivo = caminho_arquivo or "estufa_status.log"

    def logar_operacao(self, mensagem: str) -> bool:
        """Grava a mensagem de log no arquivo configurado."""
        try:
            with open(self.caminho_arquivo, "a", encoding="utf-8") as f:
                f.write(f"{mensagem}\n")
            return True
        except Exception as e:
            raise RuntimeError(f"Erro ao gravar log: {e}")


class EstufaAgrotech:
    """Gerenciador central da estufa (temperatura, logs e regras de precificação)."""

    def __init__(
        self,
        temperatura_inicial: float = 22.0,
        logger: ServicoLogger | None = None,
    ):
        self.temperatura_atual = temperatura_inicial
        self.logger = logger or ServicoLogger()

    def verificar_status_temperatura(self) -> str:
        """Retorna alertas operacionais com base na temperatura atual."""
        if self.temperatura_atual < 0.0:
            return "ALERTA: Geada"
        if self.temperatura_atual > 40.0:
            return "ALERTA: Superaquecimento"
        return "Normal"

    def calcular_preco_insumo(self, preco_base: float, eh_vip: bool) -> float:
        """Aplica regras de desconto VIP e validação de preço."""
        if preco_base < 0:
            raise ValueError("Preço não pode ser negativo")

        if eh_vip:
            return round(preco_base * 0.8, 2)
        return round(preco_base, 2)

    def processar_carga_insumo(self, quantidade_kg: float) -> bool:
        """Valida o limite de carga suportado pela estufa."""
        limite_maximo_kg = 5000.0
        if quantidade_kg > limite_maximo_kg:
            raise ValueError("Capacidade máxima excedida")
        return True

    def registrar_log(self, mensagem: str) -> bool:
        """Envia mensagem de log usando o serviço configurado."""
        return self.logger.logar_operacao(mensagem)
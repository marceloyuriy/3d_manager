from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class ItemFila(models.Model):
    PRIORIDADE_CHOICES = [
        ('B', 'Baixa'),
        ('N', 'Normal'),
        ('A', 'Alta'),
        ('U', 'Urgente'),
    ]

    STATUS_CHOICES = [
        ('F', 'Na Fila'),
        ('I', 'Imprimindo'),
        ('P', 'Pendente de Informação'),
        ('C', 'Concluído'),
        ('E', 'Cancelado/Erro'),
    ]

    solicitante = models.CharField(max_length=100, verbose_name="Nome do Solicitante")
    nome_peca = models.CharField(max_length=150, verbose_name="PN ou Nome da Peça")
    prazo = models.DateField(verbose_name="Prazo para Execução")
    prioridade = models.CharField(max_length=1, choices=PRIORIDADE_CHOICES, default='N', verbose_name="Prioridade")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='F', verbose_name="Status Atual")

    arquivo_impressao = models.FileField(upload_to='arquivos_3d/', verbose_name="Arquivo (STL/GCODE)", blank=True,
                                         null=True)
    link_fusion = models.URLField(verbose_name="Link do Fusion 360", blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Solicitação")

    # --- NOVO CAMPO ---
    # blank=True e null=True porque a peça começa sem data de conclusão
    data_conclusao = models.DateTimeField(verbose_name="Data/Hora de Conclusão", blank=True, null=True)
    # --- NOVA FUNÇÃO DE VALIDAÇÃO ---
    def clean(self):
        # Regra 1: Verifica se o arquivo e o link estão vazios
        if not self.arquivo_impressao and not self.link_fusion:
            raise ValidationError(
                "Atenção: Você deve fornecer um Arquivo de Impressão ou um Link do Fusion para prosseguir.")

        # --- NOVA REGRA 2: Validação da Data ---
        # Verificamos se o 'prazo' foi preenchido e se é menor que o dia de hoje
        if self.prazo and self.prazo < date.today():
            # Nota Didática: Ao passar um dicionário {'prazo': 'mensagem'},
            # o Django sabe que esse erro pertence ESPECIFICAMENTE ao campo prazo.
            # O erro vai aparecer em vermelho logo abaixo do campo de data na tela!
            raise ValidationError(
                {'prazo': 'A data de prazo não pode estar no passado. Por favor, escolha hoje ou uma data futura.'})


    def __str__(self):
        return f"{self.nome_peca} - {self.solicitante}"
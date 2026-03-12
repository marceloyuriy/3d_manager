from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

PRIORIDADE_CHOICES = [
        ('B', 'Baixa'),
        ('N', 'Normal'),
        ('A', 'Alta'),
        ('U', 'Urgente'),
    ]

STATUS_CHOICES = [
        ('D', 'Em Desenvolvimento'),
        ('F', 'Pronto para Iniciar'),
        ('I', 'Em Produção'),
        ('P', 'Pendente de Informação'),
        ('C', 'Concluído'),
        ('E', 'Cancelado/Erro'),
    ]

# ==========================================
# 1. FILA DA IMPRESSORA 3D (Antigo ItemFila)
# ==========================================
class Pedido3D(models.Model):
    solicitante = models.CharField(max_length=100, verbose_name="Nome do Solicitante")
    nome_peca = models.CharField(max_length=150, verbose_name="PN ou Nome da Peça")
    prazo = models.DateField(verbose_name="Prazo para Execução")
    previsao_conclusao = models.DateField(verbose_name='Previsão de Conclusão (Gestor)', null=True, blank=True)
    prioridade = models.CharField(max_length=1, choices=PRIORIDADE_CHOICES, default='N', verbose_name="Prioridade")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='D', verbose_name="Status Atual")

    arquivo_impressao = models.FileField(upload_to='arquivos_3d/', verbose_name="Arquivo (STL/GCODE)", blank=True, null=True)
    link_fusion = models.URLField(verbose_name="Link do Fusion 360", blank=True, null=True)
    observacao_pendencia = models.TextField(verbose_name="Observação de Pendência", blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Solicitação")
    data_conclusao = models.DateTimeField(verbose_name="Data/Hora de Conclusão", blank=True, null=True)

    def clean(self):
        if self.prazo and self.prazo < date.today():
            raise ValidationError({'prazo': 'A data de prazo não pode estar no passado. Por favor, escolha hoje ou uma data futura.'})

    def __str__(self):
        return f"[3D] {self.nome_peca} - {self.solicitante}"


# ==========================================
# 2. FILA DA ROUTER CNC
# ==========================================
class PedidoRouter(models.Model):
    solicitante = models.CharField(max_length=100, verbose_name="Nome do Solicitante")
    nome_peca = models.CharField(max_length=150, verbose_name="PN ou Nome da Peça")
    prazo = models.DateField(verbose_name="Prazo para Execução")
    previsao_conclusao = models.DateField(verbose_name='Previsão de Conclusão (Gestor)', null=True, blank=True)
    prioridade = models.CharField(max_length=1, choices=PRIORIDADE_CHOICES, default='N', verbose_name="Prioridade")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='D', verbose_name="Status Atual")

    arquivo_impressao = models.FileField(upload_to='arquivos_router/', verbose_name="Arquivo (DXF/Vectric)", blank=True, null=True)
    link_fusion = models.URLField(verbose_name="Link do Projeto", blank=True, null=True)
    observacao_pendencia = models.TextField(verbose_name="Observação de Pendência", blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Solicitação")
    data_conclusao = models.DateTimeField(verbose_name="Data/Hora de Conclusão", blank=True, null=True)

    def clean(self):
        if self.prazo and self.prazo < date.today():
            raise ValidationError({'prazo': 'A data de prazo não pode estar no passado. Por favor, escolha hoje ou uma data futura.'})

    def __str__(self):
        return f"[ROUTER] {self.nome_peca} - {self.solicitante}"


# ==========================================
# 3. FILA DO CAD
# ==========================================
class PedidoCAD(models.Model):
    solicitante = models.CharField(max_length=100, verbose_name="Nome do Solicitante")
    nome_peca = models.CharField(max_length=150, verbose_name="PN ou Nome do Projeto")
    prazo = models.DateField(verbose_name="Prazo para Execução")
    previsao_conclusao = models.DateField(verbose_name='Previsão de Conclusão (Gestor)', null=True, blank=True)
    prioridade = models.CharField(max_length=1, choices=PRIORIDADE_CHOICES, default='N', verbose_name="Prioridade")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='D', verbose_name="Status Atual")

    arquivo_impressao = models.FileField(upload_to='arquivos_cad/', verbose_name="Arquivo de Referência (PDF/Imagem)", blank=True, null=True)
    link_fusion = models.URLField(verbose_name="Link de Referência", blank=True, null=True)
    observacao_pendencia = models.TextField(verbose_name="Observação de Pendência", blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Solicitação")
    data_conclusao = models.DateTimeField(verbose_name="Data/Hora de Conclusão", blank=True, null=True)

    def clean(self):
        if self.prazo and self.prazo < date.today():
            raise ValidationError({'prazo': 'A data de prazo não pode estar no passado. Por favor, escolha hoje ou uma data futura.'})

    def __str__(self):
        return f"[CAD] {self.nome_peca} - {self.solicitante}"
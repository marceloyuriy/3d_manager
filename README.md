# 🖨️ Gerenciador de Fila de Impressão 3D

Um sistema web desenvolvido em Django para gerenciar a fila de produção interna de impressoras 3D (focado inicialmente na Creality K1 Max). O objetivo deste projeto é organizar pedidos, prioridades, arquivos e prazos em um ambiente centralizado, eliminando a perda de informações.

---

## 📖 Sobre o Projeto (MVP)

Este aplicativo foi criado como um Produto Mínimo Viável (MVP) para atender à necessidade de controle de peças 3D da equipe. Ele permite que qualquer colaborador solicite impressões de forma fácil, enquanto fornece aos gestores um painel (Dashboard) para alterar status, prioridades e organizar a fila de produção.

## ✨ Funcionalidades

* **Gestão de Fila Inteligente:** Divisão visual entre peças na Fila/Imprimindo, Pendentes e Concluídas.
* **Controle de Arquivos Centralizado:** Upload direto de arquivos (STL/GCODE) ou links do Fusion 360 no momento do pedido.
* **Níveis de Acesso (Permissões):** * *Usuários Comuns:* Podem criar contas, adicionar pedidos e acompanhar o status.
    * *Gestores (Staff):* Podem alterar a prioridade da fila, editar dados e atualizar o status de produção.
* **Validações Anti-Erro:**
    * Bloqueio de prazos retroativos (não permite datas no passado).
    * Obrigatoriedade de envio de arquivo ou link.
* **Automação de Dados:** Preenchimento automático de Data e Hora de Conclusão quando o status é alterado pelo gestor.
* **Feedback Visual:** Sistema de mensagens flash (alertas verdes) confirmando ações bem-sucedidas.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.10 / Django 5.x
* **Frontend:** HTML5, CSS3, Bootstrap 5 (via CDN)
* **Banco de Dados:** SQLite (Fase de Testes/MVP)
* **Infraestrutura Local:** Docker & Docker Compose
* **Hospedagem na Nuvem:** PythonAnywhere

---

## 🚀 Como Executar Localmente (Desenvolvimento)

O projeto está configurado para rodar facilmente em qualquer máquina utilizando o Docker.

### Pré-requisitos
* [Docker](https://www.docker.com/) e Docker Compose instalados.
* [Git](https://git-scm.com/) instalado.

### Passo a Passo

1. Clone o repositório para a sua máquina:
   ```bash
   git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
   cd NOME_DA_PASTA

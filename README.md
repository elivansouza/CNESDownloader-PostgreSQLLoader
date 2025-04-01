
# CNES Downloader, Extractor & PostgreSQL Loader

Este repositório automatiza o processo de **download**, **extração** e **importação no banco de dados PostgreSQL** dos dados mais recentes do **Cadastro Nacional de Estabelecimentos de Saúde (CNES)** diretamente do FTP oficial do DATASUS.

---

## 📦 Arquivos CNES obtidos

O script baixa e extrai arquivos CSV contidos no pacote ZIP mensal do CNES, incluindo:

- `rlEstabEquipeProf202502.csv`
- `tbAtividade202502.csv`
- `tbAtividadeProfissional202502.csv`
- `tbConselhoClasse202502.csv`
- `tbDadosProfissionalSus202502.csv`
- `tbEstabelecimento202502.csv`
- `tbGestao202502.csv`
- `tbGrupoAtividade202502.csv`
- `tbGrupoEquipe202502.csv`
- `tbSubTipo202502.csv`
- `tbSubTipoEquipe202502.csv`
- `tbTipoEstabelecimento202502.csv`
- `tbTipoUnidade202502.csv`
- `tbTurnoAtendimento202502.csv`

---

## ⚙️ Funcionalidades

- Conexão automatizada com o FTP `ftp.datasus.gov.br/cnes`
- Busca e download do arquivo mais recente `BASE_DE_DADOS_CNES_YYYYMM.ZIP`
- Extração automática dos CSVs
- Log detalhado da operação
- **Integração com PostgreSQL** para estruturação e carga dos dados
- Criação de tabela de análise consolidada para exploração dos dados

---

## 🚀 Como utilizar

### 1️⃣ Clone este repositório:

```bash
git clone https://github.com/seu-usuario/cnes-downloader.git
cd cnes-downloader
```

### 2️⃣ Instale os requisitos

Instale os requisitos do projeto:

```bash
pip install -r requirements.txt
```

> Este projeto utiliza apenas bibliotecas padrão do Python (3.5+), conforme definido no `requirements.txt`.

### 3️⃣ Execute o script Python

Modo interativo:

```bash
python cnes.py
```

Modo automático:

```bash
python cnes.py --auto
```

> Os arquivos serão extraídos para a pasta `CNES/`.

---

## 🐘 Importação no PostgreSQL

### Pré-requisitos:
- PostgreSQL 12+
- Banco de dados e usuário com permissões adequadas

### 4️⃣ Execute os SQLs de carga e análise

#### Script de carga dos dados brutos:

```bash
psql -U seu_usuario -d seu_banco -f query.sql
```

O script `query.sql`:
- Cria todas as tabelas necessárias conforme o layout do CNES
- Faz o `COPY` dos CSVs para as tabelas
- Prepara as tabelas para futuras consultas e análises

> ⚠️ **Importante:** certifique-se de ajustar os caminhos dos CSVs no `query.sql` conforme o local onde foram extraídos (`./CNES/`).

#### Script adicional para geração da tabela de análise:

Após a carga dos dados brutos, execute também:

```bash
psql -U seu_usuario -d seu_banco -f query_tab_análise.sql
```

O script `query_tab_análise.sql`:
- Realiza transformações e consolidações dos dados brutos
- Cria a tabela final `tab_analise_cnes` para exploração e análise de dados

> 📝 **Dica:** Essa tabela pode ser utilizada diretamente em dashboards ou análises exploratórias.

---

## 🎯 Makefile (opcional)

O projeto inclui um `Makefile` para facilitar:

```bash
make auto       # Executa a extração automaticamente
make download   # Executa o script com confirmação
make clean      # Remove pastas temporárias e logs
```

---

## 📝 Logs

Todos os logs de execução são armazenados em `cnes_downloader.log` com informações detalhadas sobre o processo de download e extração.

---

## 🗂️ Estrutura do Projeto

```plaintext
├── cnes.py
├── query.sql
├── query_tab_análise.sql
├── requirements.txt
├── Makefile
├── LICENSE
├── .gitignore
├── cnes_downloader.log
├── Downloads/
│   └── BASE_DE_DADOS_CNES_YYYYMM.ZIP
└── CNES/
    ├── rlEstabEquipeProfYYYYMM.csv
    ├── tbEstabelecimentoYYYYMM.csv
    └── ... outros arquivos CSV ...
```

---

## 🔄 Futuras melhorias

- Criação automática de índices nas tabelas
- Otimização das queries para grandes volumes de dados
- Pipeline completo de ETL com agendamento (cronjob ou Airflow)

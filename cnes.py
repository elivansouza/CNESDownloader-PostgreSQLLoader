import logging
import os
import re
import zipfile
from datetime import datetime
from ftplib import FTP, error_perm, all_errors
from typing import List, Tuple, Pattern
import argparse

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Exibe no console
        logging.FileHandler("cnes_downloader.log")  # Salva em arquivo
    ]
)
logger = logging.getLogger(__name__)

# Constantes
FTP_HOST = 'ftp.datasus.gov.br'
FTP_DIRECTORY = 'cnes'
FILE_PATTERN: Pattern = re.compile(r'^BASE_DE_DADOS_CNES_(\d{6})\.ZIP$')
DOWNLOAD_DIRECTORY = os.path.join(os.getcwd(), 'Downloads')
EXTRACT_DIRECTORY = os.path.join(os.getcwd(), 'CNES')


class FTPConnection:
    def __enter__(self) -> FTP:
        self.ftp = FTP()
        self.ftp.connect(FTP_HOST)
        self.ftp.login()
        self.ftp.cwd(FTP_DIRECTORY)
        logger.info(f"Conectado ao FTP {FTP_HOST} no diretório {FTP_DIRECTORY}")
        return self.ftp

    def __exit__(self, exc_type, exc_value, traceback):
        self.ftp.quit()
        logger.info("Conexão FTP encerrada.")


def get_matching_files(ftp: FTP, pattern: Pattern) -> List[Tuple[str, datetime]]:
    try:
        files = ftp.nlst()
        logger.debug(f"Arquivos encontrados: {files}")
    except error_perm as e:
        logger.error(f"Erro de permissão FTP: {e}")
        return []
    except all_errors as e:
        logger.error(f"Erro FTP: {e}")
        return []
    
    matched_files = []
    for file_name in files:
        match = pattern.match(file_name)
        if match:
            date_str = match.group(1)
            try:
                date_obj = datetime.strptime(date_str, '%Y%m')
                matched_files.append((file_name, date_obj))
            except ValueError as e:
                logger.warning(f"Falha ao analisar a data do arquivo {file_name}: {e}")
    return matched_files


def download_file(ftp: FTP, file_name: str, local_path: str) -> bool:
    try:
        with open(local_path, 'wb') as fp:
            ftp.retrbinary(f'RETR {file_name}', fp.write)
        logger.info(f"Download concluído: {file_name}")
        return True
    except (error_perm, all_errors) as e:
        logger.error(f"Erro FTP durante download: {e}")
    except Exception as ex:
        logger.error(f"Erro inesperado durante download: {ex}")
    return False


def extract_zip_file(file_path: str, extract_directory: str) -> bool:
    if not os.path.exists(file_path):
        logger.error(f"Arquivo não encontrado: {file_path}")
        return False

    try:
        os.makedirs(extract_directory, exist_ok=True)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_directory)
        logger.info(f"Arquivos extraídos para: {extract_directory}")
        return True
    except zipfile.BadZipFile as e:
        logger.error(f"Arquivo ZIP corrompido: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado na extração: {e}")
    return False


def main(auto_confirm: bool):
    with FTPConnection() as ftp:
        matched_files = get_matching_files(ftp, FILE_PATTERN)
        if not matched_files:
            logger.info("Nenhum arquivo correspondente encontrado.")
            return

        matched_files.sort(key=lambda x: x[1], reverse=True)
        most_recent_file, _ = matched_files[0]
        logger.info(f"Arquivo mais recente encontrado: {most_recent_file}")

        if auto_confirm:
            proceed = True
        else:
            proceed = input(f"Baixar o arquivo {most_recent_file}? (Y/N): ").strip().upper() == 'Y'

        if proceed:
            os.makedirs(DOWNLOAD_DIRECTORY, exist_ok=True)
            local_file_path = os.path.join(DOWNLOAD_DIRECTORY, most_recent_file)

            if download_file(ftp, most_recent_file, local_file_path):
                if extract_zip_file(local_file_path, EXTRACT_DIRECTORY):
                    logger.info("Processo concluído com sucesso.")
                else:
                    logger.error("Falha na extração.")
            else:
                logger.error("Falha no download.")
        else:
            logger.info("Operação cancelada pelo usuário.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Downloader e extrator de dados do CNES via FTP")
    parser.add_argument('--auto', action='store_true', help="Baixar e extrair automaticamente sem pedir confirmação")
    args = parser.parse_args()

    main(auto_confirm=args.auto)

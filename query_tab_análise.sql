-- CRIAÇÃO DE VIEW PARA TABELA GERAL CNES E CENSO
CREATE OR REPLACE VIEW cnes.vw_cnes_censo AS
SELECT
  cnes.co_cnes,
  cnes.co_unidade,
  cnes.co_municipio_gestor,
  muns.região,
  muns.sigla_uf,
  cnes.co_estado_gestor,
  muns.nome_uf,
  muns.nome_município,
  cnes.no_razao_social,
  cnes.no_fantasia,
  cnes.co_tipo_estabelecimento,
  cnes.ds_tipo_estabelecimento,
  cnes.tp_unidade,
  cnes.ds_tipo_unidade,
  (
    CASE
      WHEN cnes.tp_unidade IN ('01', '02', '15', '32', '40') THEN 'Unidades APS'
      WHEN cnes.tp_unidade LIKE '72' THEN 'Saúde Indígena'
      ELSE 'Outros'
    END
  ) AS ds_categoria_unidade,
  cnes.co_natureza_jur,
  cnes.ds_natureza_jur,
  cnes.no_logradouro,
  CASE
    WHEN no_logradouro IS NULL
    OR TRIM(no_logradouro) = '' THEN 'Não preenchido'
    ELSE 'Preenchido'
  END AS validacao_logradouro,
  cnes.nu_endereco,
  cnes.no_complemento,
  cnes.no_bairro,
  cnes.co_cep,
  cnes.nu_latitude,
  cnes.nu_longitude,
  CASE
    WHEN cnes.nu_latitude ~ '^[-+]?\d+(\.\d+)?$'
    AND CAST(cnes.nu_latitude AS NUMERIC) BETWEEN -90
    AND 90 THEN 'Válida'
    ELSE 'Inválida'
  END AS validacao_latitude,
  CASE
    WHEN cnes.nu_longitude ~ '^[-+]?\d+(\.\d+)?$'
    AND CAST(cnes.nu_longitude AS NUMERIC) BETWEEN -180
    AND 180 THEN 'Válida'
    ELSE 'Inválida'
  END AS validacao_longitude,
  cnes.nu_telefone,
  CASE
    WHEN LENGTH(REGEXP_REPLACE(nu_telefone, '[^\d]', '', 'g')) >= 10 THEN 'Válido'
    ELSE 'Inválido'
  END validacao_telefone,
  cnes.no_email,
  CASE
    WHEN REGEXP_REPLACE(
      REGEXP_REPLACE(TRIM(no_email), '\s*([@.])\s*', '\1', 'g'),
      '\s+(e\s+|,?\s+)',
      ',',
      'g'
    ) ~ '^([^@]+@[^@]+\.[^@]+)(,?[^@]+@[^@]+\.[^@]+)*$' THEN 'Válido'
    ELSE 'Inválido'
  END validacao_email,
  cnes.st_conexao_internet,
  cnes.co_motivo_desab,
  censo.v110_latitude,
  censo.v111_longitude,
  censo.v33_acesso_internet_ubs,
  censo.v341_consultorio,
  censo.v342_alguns_consultorios,
  censo.v343_farmacia,
  censo.v344_recepcao,
  censo.v345_sala_vacina,
  censo.v346_sala_acs,
  censo.v347_nenhum,
  censo.status_conexão,
  censo.inconsistência AS validacao_status_conexao
FROM
  cnes.cnes_202502 AS cnes
  LEFT JOIN muns.muns20 AS muns ON cnes.co_municipio_gestor = muns.ibge
  LEFT JOIN cnes.censo AS censo ON cnes.co_cnes = censo.cnes
WHERE
  (co_motivo_desab LIKE '')
  AND (
    st_conexao_internet LIKE ('N')
    OR censo.status_conexão IN (
      'Conexão insuficiente',
      'Sem conexão',
      'Sem conexão com inconsistência'
    )
  )

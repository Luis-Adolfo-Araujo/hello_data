CREATE TABLE paciente (
    User_id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    data_nascimento VARCHAR(12),
    sexo VARCHAR(10),
    gestante BOOLEAN DEFAULT FALSE,
    email VARCHAR(100),
    telefone VARCHAR(20),
    Cpf VARCHAR(20),
    Cep VARCHAR(20),
    Rua VARCHAR(100),
    Numero VARCHAR(20),
    Bairro VARCHAR(100),
    Cidade VARCHAR(100),
    UF VARCHAR(10)
);

CREATE TABLE info_paciente (
    id_usuario INT REFERENCES paciente(User_id),
    objetivo VARCHAR(100),
    resticao_alimentar VARCHAR(100),
    ingere_alcool VARCHAR(10),
    dorme_bem BOOLEAN,
    horas_sono VARCHAR(20),
    pratica_exercicios BOOLEAN,
    patologia VARCHAR(100),
    Medicamentos VARCHAR(100),
    apetite VARCHAR(100),
    mastigacao VARCHAR(100),
    habito_intestinal VARCHAR(100),
    frequencia_evacuacao VARCHAR(100),
    formato_fezes VARCHAR(100),
    usa_laxante BOOLEAN,
    cor_fezes VARCHAR(100),
    ingestao_hidrica VARCHAR(100),
    sintomas VARCHAR(100)
);

CREATE TABLE rastreamento_metabolico (
    Id_metabolico SERIAL PRIMARY KEY,
    tontura BOOLEAN,
    sensacao_desmaio BOOLEAN,
    insonia BOOLEAN,
    olhos_lacrimejantes_cocando BOOLEAN,
    olhos_inchados_vermelhos BOOLEAN,
    olheiras BOOLEAN,
    visao_borrada BOOLEAN,
    coceira_ouvido BOOLEAN,
    dor_ouvido BOOLEAN,
    retirada_fluido BOOLEAN,
    zunido_ouvido BOOLEAN,
    nariz_entupido BOOLEAN,
    sinusite BOOLEAN,
    corrimento_nasal BOOLEAN,
    espirro BOOLEAN,
    coceira_olhos BOOLEAN,
    ataque_espirro BOOLEAN,
    muco_excessivo BOOLEAN,
    tosse_cronica BOOLEAN,
    dor_garganta BOOLEAN,
    necessidade_limpar_garganta BOOLEAN,
    rouquidao BOOLEAN,
    lingua_gengiva_labio_inchado BOOLEAN,
    acne BOOLEAN,
    perda_cabelo BOOLEAN,
    suor_excessivo BOOLEAN,
    feridas_cocam BOOLEAN,
    pele_seca BOOLEAN,
    vermelhidao BOOLEAN,
    calor_excessivo BOOLEAN,
    batida_irregular_coracao BOOLEAN,
    batidas_rapidas_demais_coracao BOOLEAN,
    dor_peito BOOLEAN,
    dor_cabeca BOOLEAN,
    data TIMESTAMP
);

CREATE TABLE antropometria (
    id_antropometria SERIAL PRIMARY KEY,
    data DATE,
    altura VARCHAR(20),
    peso_atual VARCHAR(20),
    peso_ideal VARCHAR(20),
    nivel_atividade VARCHAR(100)
);

CREATE TABLE paciente_metabolico (
    id_usuario INT REFERENCES paciente(User_id),
    id_metabolico INT REFERENCES rastreamento_metabolico(Id_metabolico),
    data TIMESTAMP,
    PRIMARY KEY (id_usuario, id_metabolico)
);

CREATE TABLE paciente_antropometria (
    id_usuario INT REFERENCES paciente(User_id),
    id_antropometria INT REFERENCES antropometria(id_antropometria),
    data TIMESTAMP,
    PRIMARY KEY (id_usuario, id_antropometria)
);

CREATE TABLE paciente (
    User_id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    data_nascimento DATE,
    sexo VARCHAR(10),
    gestante BOOLEAN,
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
    horas_sono INT,
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
    tontura INT,
    sensacao_desmaio INT,
    insonia INT,
    olhos_lacrimejantes_cocando INT,
    olhos_inchados_vermelhos INT,
    olheiras INT,
    visao_borrada INT,
    coceira_ouvido INT,
    dor_ouvido INT,
    retirada_fluido INT,
    zunido_ouvido INT,
    nariz_entupido INT,
    sinusite INT,
    corrimento_nasal INT,
    espirro INT,
    coceira_olhos INT,
    ataque_espirro INT,
    muco_excessivo INT,
    tosse_cronica INT,
    dor_garganta INT,
    necessidade_limpar_garganta INT,
    rouquidao INT,
    lingua_gengiva_labio_inchado INT,
    acne INT,
    perda_cabelo INT,
    suor_excessivo INT,
    feridas_cocam INT,
    pele_seca INT,
    vermelhidao INT,
    calor_excessivo INT,
    batida_irregular_coracao INT,
    batidas_rapidas_demais_coracao INT,
    dor_peito INT,
    dor_cabeca INT,
    data DATE
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
    data DATE,
    PRIMARY KEY (id_usuario, id_metabolico)
);

CREATE TABLE paciente_antropometria (
    id_usuario INT REFERENCES paciente(User_id),
    id_antropometria INT REFERENCES antropometria(id_antropometria),
    data DATE,
    PRIMARY KEY (id_usuario, id_antropometria)
);

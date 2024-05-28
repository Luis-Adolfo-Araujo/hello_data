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

-- Inserindo dados na tabela 'paciente'
INSERT INTO paciente (nome, data_nascimento, sexo, gestante, email, telefone, Cpf, Cep, Rua, Numero, Bairro, Cidade, UF)
VALUES 
('João Silva', '1980-05-15', 'Masculino', FALSE, 'joao.silva@gmail.com', '11987654321', '123.456.789-00', '12345-678', 'Rua A', '100', 'Centro', 'São Paulo', 'SP'),
('Maria Oliveira', '1992-08-21', 'Feminino', TRUE, 'maria.oliveira@gmail.com', '11987654322', '123.456.789-01', '12345-679', 'Rua B', '200', 'Jardim', 'Rio de Janeiro', 'RJ'),
('Carlos Souza', '1985-12-05', 'Masculino', FALSE, 'carlos.souza@gmail.com', '11987654323', '123.456.789-02', '12345-680', 'Rua C', '300', 'Centro', 'Belo Horizonte', 'MG'),
('Ana Costa', '1990-07-12', 'Feminino', FALSE, 'ana.costa@gmail.com', '11987654324', '123.456.789-03', '12345-681', 'Rua D', '400', 'Vila', 'Curitiba', 'PR'),
('Lucas Lima', '1987-11-23', 'Masculino', FALSE, 'lucas.lima@gmail.com', '11987654325', '123.456.789-04', '12345-682', 'Rua E', '500', 'Bairro Alto', 'Porto Alegre', 'RS'),
('Fernanda Almeida', '1995-03-10', 'Feminino', TRUE, 'fernanda.almeida@gmail.com', '11987654326', '123.456.789-05', '12345-683', 'Rua F', '600', 'Centro', 'Salvador', 'BA');

-- Inserindo dados na tabela 'info_paciente'
INSERT INTO info_paciente (id_usuario, objetivo, resticao_alimentar, ingere_alcool, dorme_bem, horas_sono, pratica_exercicios, patologia, Medicamentos, apetite, mastigacao, habito_intestinal, frequencia_evacuacao, formato_fezes, usa_laxante, cor_fezes, ingestao_hidrica, sintomas)
VALUES 
(1, 'Perda de Peso', 'Nenhuma', 'Ocasionalmente', TRUE, '8 horas', TRUE, 'Hipertensão', 'Nenhum', 'Moderado', 'Normal', 'Regular', 'Diária', 'Formado', FALSE, 'Marrom', '2 litros', 'Nenhum'),
(2, 'Ganho de Massa', 'Lactose', 'Nunca', FALSE, '6 horas', TRUE, 'Diabetes', 'Insulina', 'Aumentado', 'Rápida', 'Irregular', '2-3 dias', 'Pastoso', FALSE, 'Amarelo', '3 litros', 'Cãibras'),
(3, 'Manter Saúde', 'Glúten', 'Socialmente', TRUE, '7 horas', FALSE, 'Nenhuma', 'Nenhum', 'Normal', 'Normal', 'Regular', 'Diária', 'Formado', TRUE, 'Marrom', '2.5 litros', 'Fadiga'),
(4, 'Melhora do sono', 'Nenhuma', 'Nunca', FALSE, '5 horas', TRUE, 'Insônia', 'Melatonina', 'Reduzido', 'Rápida', 'Irregular', '2-3 dias', 'Líquido', FALSE, 'Verde', '1.5 litros', 'Nenhum'),
(5, 'Perda de Gordura', 'Nenhuma', 'Ocasionalmente', TRUE, '8 horas', FALSE, 'Hipertensão', 'Nenhum', 'Normal', 'Normal', 'Regular', 'Diária', 'Formado', FALSE, 'Marrom', '2 litros', 'Nenhum'),
(6, 'Ganho de Força', 'Lactose', 'Socialmente', FALSE, '6 horas', TRUE, 'Diabetes', 'Insulina', 'Aumentado', 'Normal', 'Irregular', '2-3 dias', 'Pastoso', TRUE, 'Amarelo', '3 litros', 'Cãibras');

-- Inserindo dados na tabela 'rastreamento_metabolico'
INSERT INTO rastreamento_metabolico (tontura, sensacao_desmaio, insonia, olhos_lacrimejantes_cocando, olhos_inchados_vermelhos, olheiras, visao_borrada, coceira_ouvido, dor_ouvido, retirada_fluido, zunido_ouvido, nariz_entupido, sinusite, corrimento_nasal, espirro, coceira_olhos, ataque_espirro, muco_excessivo, tosse_cronica, dor_garganta, necessidade_limpar_garganta, rouquidao, lingua_gengiva_labio_inchado, acne, perda_cabelo, suor_excessivo, feridas_cocam, pele_seca, vermelhidao, calor_excessivo, batida_irregular_coracao, batidas_rapidas_demais_coracao, dor_peito, dor_cabeca, data)
VALUES 
(FALSE, FALSE, FALSE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, '2024-01-01 08:00:00'),
(TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, '2024-02-01 08:00:00'),
(FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, '2024-03-01 08:00:00'),
(TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, '2024-04-01 08:00:00'),
(FALSE, FALSE, TRUE, TRUE, TRUE, FALSE, TRUE, TRUE, FALSE, TRUE, TRUE, FALSE, TRUE, TRUE, FALSE, TRUE, TRUE, FALSE, TRUE, TRUE, FALSE, TRUE, TRUE, FALSE, TRUE, TRUE, FALSE, TRUE, TRUE, FALSE, TRUE, TRUE, FALSE, '2024-05-01 08:00:00'),
(TRUE, TRUE, FALSE, FALSE, FALSE, TRUE, FALSE, FALSE, TRUE, FALSE, FALSE, TRUE, FALSE, FALSE, TRUE, FALSE, FALSE, TRUE, FALSE, FALSE, TRUE, FALSE, FALSE, TRUE, FALSE, FALSE, TRUE, FALSE, FALSE, TRUE, FALSE, FALSE, TRUE, '2024-06-01 08:00:00');

-- Inserindo dados na tabela 'antropometria'
INSERT INTO antropometria (data, altura, peso_atual, peso_ideal, nivel_atividade)
VALUES 
('2024-01-01', '1.75m', '80kg', '75kg', 'Moderado'),
('2024-02-01', '1.60m', '65kg', '60kg', 'Alto'),
('2024-03-01', '1.70m', '70kg', '68kg', 'Baixo'),
('2024-04-01', '1.80m', '90kg', '85kg', 'Moderado'),
('2024-05-01', '1.65m', '55kg', '53kg', 'Alto'),
('2024-06-01', '1.68m', '75kg', '70kg', 'Baixo');

-- Inserindo dados na tabela 'paciente_metabolico'
INSERT INTO paciente_metabolico (id_usuario, id_metabolico, data)
VALUES 
(1, 1, '2024-01-01 08:00:00'),
(2, 2, '2024-02-01 08:00:00'),
(3, 3, '2024-03-01 08:00:00'),
(4, 4, '2024-04-01 08:00:00'),
(5, 5, '2024-05-01 08:00:00'),
(6, 6, '2024-06-01 08:00:00');

-- Inserindo dados na tabela 'paciente_antropometria'
INSERT INTO paciente_antropometria (id_usuario, id_antropometria, data)
VALUES 
(1, 1, '2024-01-01 08:00:00'),
(2, 2, '2024-02-01 08:00:00'),
(3, 3, '2024-03-01 08:00:00'),
(4, 4, '2024-04-01 08:00:00'),
(5, 5, '2024-05-01 08:00:00'),
(6, 6, '2024-06-01 08:00:00');

from . import db

class Paciente(db.Model):
    __tablename__ = 'paciente'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    gestante = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(20), nullable=False, unique=True)
    cep = db.Column(db.String(20), nullable=False)
    rua = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    uf = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Paciente {self.nome}>'
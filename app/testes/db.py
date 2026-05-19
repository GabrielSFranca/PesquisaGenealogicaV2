from typing import Optional
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import or_
from app.trash.tabelas import Base, Individuo, Familia, Casamento
class DBManager():
    engine = None
    def __init__(self, db_url):
        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(self.engine)
        
    #cria um objeto Individuo, o adiciona a database, e o retorna
    def add_individuo(self, indi__nome: str, indi_sobrenome: str):
        with Session(self.engine) as session:
            indi = Individuo(nome=indi__nome, sobrenome=indi_sobrenome)
            session.add(indi)
            #if (parentesco != None):
            #    parentesco.crianças.append(indi)
            session.commit()
        return indi
    
    #retorna uma lista de Individuos que correspondem aos parâmetros dados
    #ex: indi_sobrenomes=["Silva"] retorna todos os indivíduos com o sobrenoma "Silva". indi_nomes=["Luiz", "Luigi"] retorna todos os invidíduos com o nome "Luiz" ou "Luigi".
    #se não encontrar ninguém, vai retornar uma lista vazia ([])
    def get_individuos(self, indi_ids: Optional[list[int]] = None, indi_nomes: Optional[list[str]] = None, indi_sobrenomes: Optional[list[str]] = None):
        with Session(self.engine) as session:
            stmt = select(Individuo)
            if (indi_ids != None):
                stmt = stmt.where(Individuo.id.in_(indi_ids))
            if (indi_nomes != None):
                stmt = stmt.where(Individuo.nome.in_(indi_nomes))
            if (indi_sobrenomes != None):
                stmt = stmt.where(Individuo.sobrenome.in_(indi_sobrenomes))

            individuos = session.scalars(stmt).all()
        return individuos
    
    def add_casamento (self, conjuge_a: Individuo, conjuge_b: Individuo):
        with Session(self.engine) as session:
            conjuge_a = session.merge(conjuge_a)
            conjuge_b = session.merge(conjuge_b)
            cas = Casamento(conjuge_a=conjuge_a, conjuge_b=conjuge_b)
            session.add(cas)
            session.commit()
        return cas
    
    def get_casamentos(self, indi: Individuo, conjuge: Optional[Individuo] = None):
        with Session(self.engine) as session:
            stmt = select(Casamento).where(or_(Casamento.conjuge_a == indi, Casamento.conjuge_b == indi))
            if (conjuge != None):
                stmt = stmt.where(or_(Casamento.conjuge_b == conjuge, Casamento.
                                      conjuge_a == conjuge))
            casamentos = session.scalars(stmt).all()
        return casamentos
    
    def get_familia(self, pais: Casamento):
        with Session(self.engine) as session:
            pais = session.merge(pais)
            stmt = select(Familia).where(Familia.pais == pais) #...provalvemente posso so fazer pais.familia
            fam = session.scalars(stmt).first()
        return fam
    
    #dado pais ou uma familia, adiciona um indivíduo dado como criança dessa família
    #se os pais são dados, busca uma família existente ou cria uma nova se não há nenhuma
    def add_criança(self, criança : Individuo, pais: Optional[Casamento] = None, familia: Optional[Familia] = None):
        with Session(self.engine) as session:
            if familia != None:
                familia = session.merge(familia)
                familia.crianças.append(criança)
            elif pais != None:
                familia = self.get_familia(pais) 
                if familia == None:
                    familia = Familia(pais=pais)
                    session.add(familia)
                else:
                    familia = session.merge(familia)
                familia.crianças.append(criança)
            session.commit()

    def get_crianças(self, pais: Optional[Casamento] = None, familia: Optional[Familia] = None):
        if pais != None:
            familia = self.get_familia(pais)
        if familia != None:
            with Session(self.engine) as session:
                familia = session.merge(familia)
                return familia.crianças
        return[]

    def carregar_exemplo(self):
        homer = self.add_individuo("Homer", "Simpson")
        marge = self.add_individuo("Marge", "Simpson")
        bart = self.add_individuo("Bart", "Simpson")
        lisa = self.add_individuo("Lisa", "Simpson")
        maggie = self.add_individuo("Maggie", "Simpson")

        cas = self.add_casamento(homer, marge)
        self.add_criança(bart, cas)
        self.add_criança(lisa, cas)
        self.add_criança(maggie, cas)

        print("Exemplo carregado")
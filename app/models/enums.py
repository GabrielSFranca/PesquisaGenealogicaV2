from enum import Enum

class GenderEnum(Enum):
    M = "masculino"
    F = "feminino"
    NB = "nao-binario"
    OTHER = "outro"
    
class EvenTagEnum(Enum):
    BIRT = "Nascimento"
    CHR = "Batismo"
    DEAT = "Falecimento"
    IMMI = "Imigracao"
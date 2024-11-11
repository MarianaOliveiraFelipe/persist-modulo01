class Exercicio:
    def __init__(self, id, nome, grupo_muscular, dificuldade, series, repeticoes, descricao):
        self.id = id
        self.nome = nome
        self.grupo_muscular = grupo_muscular
        self.dificuldade = dificuldade
        self.series = series
        self.repeticoes = repeticoes
        self.descricao = descricao
        
        def to_dict(self):
            """Retorna um dicionário com os atributos do exercício para facilitar a manupulação com JSON."""
            return {
                'id': self.id,
                'nome': self.nome,
                'grupo_muscular': self.grupo_muscular,
                'dificuldade': self.dificuldade,
                'series': self.series,
                'repeticoes': self.repeticoes,
                'descricao': self.descricao
            }
        
        def __str__(self):
            return f"Exercicio({self.id}, {self.nome}, {self.grupo_muscular}, {self.dificuldade}, {self.series}, {self.repeticoes}, {self.descricao})"
        
# src/classes/Cliente.py
import os
import csv

class Cliente:
    ARQUIVO = os.path.join("dados", "clientes.txt")
    CAMPOS = ["id", "nome", "total_gasto"]

    def __init__(self, id: int, nome: str, total_gasto: float = 0.0):
        self.id = int(id)
        self.nome = nome.strip()
        self.total_gasto = float(total_gasto)

    # -------- domínio ----------
    def registrar_compra(self, valor: float) -> None:
        self.total_gasto += float(valor)

    # -------- persistindo ----------
    def _to_row(self):
        return [str(self.id), self.nome, f"{self.total_gasto:.2f}"]

    @classmethod
    def _garantir_arquivo(cls) -> None:
        os.makedirs(os.path.dirname(cls.ARQUIVO), exist_ok=True)
        if not os.path.exists(cls.ARQUIVO):
            with open(cls.ARQUIVO, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(cls.CAMPOS)

    @classmethod
    def carregar_todos(cls) -> list:
        cls._garantir_arquivo()
        clientes = []
        with open(cls.ARQUIVO, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            for i, row in enumerate(reader):
                if not row:
                    continue
                if i == 0 and row == cls.CAMPOS:
                    continue
                try:
                    cid, nome, total = row
                    clientes.append(cls(int(cid), nome, float(total)))
                except ValueError:
                    continue
        return clientes

    @classmethod
    def salvar_todos(cls, clientes: list) -> None:
        cls._garantir_arquivo()
        with open(cls.ARQUIVO, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(cls.CAMPOS)
            for c in clientes:
                writer.writerow(c._to_row())

    # -------- utilidades de lista ----------
    @staticmethod
    def proximo_id(clientes: list) -> int:
        return (max((c.id for c in clientes), default=0) + 1)

    @classmethod
    def adicionar(cls, clientes: list, nome: str):
        novo = cls(cls.proximo_id(clientes), nome)
        clientes.append(novo)
        cls.salvar_todos(clientes)
        return novo

    @staticmethod
    def listar(clientes: list) -> list:
        return clientes

    @staticmethod
    def listar_com_totais(clientes: list) -> list:
        return clientes

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.venda import Venda
from models.item_venda import ItemVenda
from models.produto import Produto
from models.estoque import Estoque
from auth import get_usuario_atual
from datetime import date, datetime
from typing import Optional, List, cast
from pydantic import BaseModel
from uuid import UUID

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


# ---------------------------------------------------------------------------
# Schemas de resposta — definidos aqui por serem exclusivos deste módulo
# ---------------------------------------------------------------------------

class LucroOut(BaseModel):
    periodo_inicio: date
    periodo_fim: date
    receita_total: float
    custo_estimado: float
    lucro_bruto: float
    margem_percentual: float
    total_vendas: int


class MaisVendidoOut(BaseModel):
    id_produto: UUID
    nome_produto: str
    quantidade_total: int
    receita_total: float


class FaturamentoDiarioOut(BaseModel):
    data: date
    total_vendas: int
    faturamento: float


# ---------------------------------------------------------------------------
# GET /relatorios/lucro?inicio=YYYY-MM-DD&fim=YYYY-MM-DD
# ---------------------------------------------------------------------------
#
# IMPORTANTE — limitação de design atual:
# A tabela itens_venda não armazena o custo pago no momento da venda.
# Por isso, o custo aqui é estimado pela média atual do preco_pago nos lotes
# de estoque de cada produto. Para um lucro exato (FIFO real), o correto seria
# adicionar a coluna custo_unitario em ItemVenda e populá-la durante a venda,
# no mesmo momento em que os lotes já são debitados em FIFO no router de vendas.
#
# ---------------------------------------------------------------------------
@router.get("/lucro", response_model=LucroOut)
def lucro_por_periodo(
    inicio: date = Query(..., description="Data inicial (YYYY-MM-DD)"),
    fim: date = Query(..., description="Data final (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    _: str = Depends(get_usuario_atual),
):
    if inicio > fim:
        raise HTTPException(status_code=400, detail="'inicio' não pode ser maior que 'fim'")

    inicio_dt = datetime.combine(inicio, datetime.min.time())
    fim_dt = datetime.combine(fim, datetime.max.time())

    # Busca todos os itens de produto (não serviço) no período
    itens = (
        db.query(ItemVenda)
        .join(Venda, ItemVenda.id_venda == Venda.id)
        .filter(
            Venda.criado_em >= inicio_dt,
            Venda.criado_em <= fim_dt,
            ItemVenda.id_produto.isnot(None),
        )
        .all()
    )

    receita_total = 0.0
    custo_total = 0.0

    for item in itens:
        quantidade = cast(int, item.quantidade)
        preco_unitario = cast(float, item.preco_unitario)

        # Receita total: soma(quantidade * preco_unitario)
        receita_total += float(quantidade) * float(preco_unitario)

        # Custo médio ponderado: soma(quantidade * preco_pago) / soma(quantidade)
        # considera todos os lotes já registrados para o produto
        resultado = (
            db.query(
                func.sum(Estoque.quantidade * Estoque.preco_pago)
                / func.nullif(func.sum(Estoque.quantidade), 0)
            )
            .filter(Estoque.id_produto == item.id_produto)
            .scalar()
        )
        custo_medio = float(resultado or 0)
        custo_total += float(quantidade) * custo_medio

    lucro_bruto = receita_total - custo_total
    margem = (lucro_bruto / receita_total * 100) if receita_total > 0 else 0.0

    total_vendas = (
        db.query(func.count(Venda.id))
        .filter(Venda.criado_em >= inicio_dt, Venda.criado_em <= fim_dt)
        .scalar()
        or 0
    )

    return LucroOut(
        periodo_inicio=inicio,
        periodo_fim=fim,
        receita_total=round(receita_total, 2),
        custo_estimado=round(custo_total, 2),
        lucro_bruto=round(lucro_bruto, 2),
        margem_percentual=round(margem, 2),
        total_vendas=total_vendas,
    )


# ---------------------------------------------------------------------------
# GET /relatorios/mais-vendidos?inicio=&fim=&limite=10
# ---------------------------------------------------------------------------
@router.get("/mais-vendidos", response_model=List[MaisVendidoOut])
def mais_vendidos(
    inicio: date = Query(..., description="Data inicial (YYYY-MM-DD)"),
    fim: date = Query(..., description="Data final (YYYY-MM-DD)"),
    limite: int = Query(10, ge=1, le=100, description="Quantidade de produtos no ranking"),
    db: Session = Depends(get_db),
    _: str = Depends(get_usuario_atual),
):
    if inicio > fim:
        raise HTTPException(status_code=400, detail="'inicio' não pode ser maior que 'fim'")

    inicio_dt = datetime.combine(inicio, datetime.min.time())
    fim_dt = datetime.combine(fim, datetime.max.time())

    resultados = (
        db.query(
            ItemVenda.id_produto,
            Produto.nome,
            func.sum(ItemVenda.quantidade).label("quantidade_total"),
            func.sum(ItemVenda.quantidade * ItemVenda.preco_unitario).label("receita_total"),
        )
        .join(Venda, ItemVenda.id_venda == Venda.id)
        .join(Produto, ItemVenda.id_produto == Produto.id)
        .filter(
            Venda.criado_em >= inicio_dt,
            Venda.criado_em <= fim_dt,
            ItemVenda.id_produto.isnot(None),
        )
        .group_by(ItemVenda.id_produto, Produto.nome)
        .order_by(func.sum(ItemVenda.quantidade).desc())
        .limit(limite)
        .all()
    )

    return [
        MaisVendidoOut(
            id_produto=r.id_produto,
            nome_produto=r.nome,
            quantidade_total=int(r.quantidade_total),
            receita_total=round(float(r.receita_total), 2),
        )
        for r in resultados
    ]


# ---------------------------------------------------------------------------
# GET /relatorios/faturamento-diario?mes=6&ano=2025
# ---------------------------------------------------------------------------
@router.get("/faturamento-diario", response_model=List[FaturamentoDiarioOut])
def faturamento_diario(
    mes: int = Query(..., ge=1, le=12, description="Mês (1-12)"),
    ano: int = Query(..., ge=2000, description="Ano (ex: 2025)"),
    db: Session = Depends(get_db),
    _: str = Depends(get_usuario_atual),
):
    resultados = (
        db.query(
            func.date(Venda.criado_em).label("data"),
            func.count(Venda.id).label("total_vendas"),
            func.sum(Venda.valor_total).label("faturamento"),
        )
        .filter(
            func.extract("month", Venda.criado_em) == mes,
            func.extract("year", Venda.criado_em) == ano,
        )
        .group_by(func.date(Venda.criado_em))
        .order_by(func.date(Venda.criado_em))
        .all()
    )

    return [
        FaturamentoDiarioOut(
            data=r.data,
            total_vendas=r.total_vendas,
            faturamento=round(float(r.faturamento), 2),
        )
        for r in resultados
    ]
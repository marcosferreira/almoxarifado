"""Imports compartilhados, helpers e decorators usados em todo o pacote views."""
from decimal import Decimal
from functools import wraps
import csv
from io import BytesIO
from typing import Any, Callable, Sequence

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, F, Sum
from django.db.models.deletion import ProtectedError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from ..models import (
    Produto,
    Pedido,
    Fornecedor,
    Unidade,
    Setor,
    Entrada,
    ItemEntrada,
    ItemPedido,
    PerfilUsuario,
)
from ..forms import (
    ProdutoForm,
    FornecedorForm,
    UnidadeForm,
    SetorForm,
    EntradaForm,
    ItemEntradaFormSet,
    PedidoForm,
    ItemPedidoFormSet,
    AnexoEmpenhoForm,
    PerfilUsuarioForm,
    PerfilTemaForm,
)


def _tem_papel(*nomes_grupos: str) -> Callable[..., Any]:
    """Decorator que restringe acesso a usuários nos grupos indicados (ou superuser)."""
    def decorator(view_func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(view_func)
        @login_required
        def _wrapped(request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
            if request.user.is_superuser or request.user.groups.filter(name__in=nomes_grupos).exists():
                return view_func(request, *args, **kwargs)
            messages.error(request, "Você não tem permissão para acessar esta funcionalidade.")
            return redirect("dashboard")
        return _wrapped
    return decorator


def _to_decimal(value: Any) -> Decimal:
    return value if value is not None else Decimal("0")


def _export_csv(filename: str, headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> HttpResponse:
    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
    return response


def _export_xlsx(filename: str, sheets: Sequence[tuple[str, Sequence[str], Sequence[Sequence[Any]]]]) -> HttpResponse:
    from openpyxl import Workbook
    wb = Workbook()
    for i, (sheet_name, headers, rows) in enumerate(sheets):
        ws = wb.active if i == 0 else wb.create_sheet(title=sheet_name)
        if i == 0:
            ws.title = sheet_name
        ws.append(headers)
        for row in rows:
            ws.append([str(v) if v is not None else "" for v in row])
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    response = HttpResponse(
        buffer,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def _render_pdf(template_name: str, context: dict[str, Any], filename: str) -> HttpResponse:
    """Renderiza um template HTML como PDF usando WeasyPrint."""
    from weasyprint import HTML
    from django.template.loader import render_to_string
    html_string = render_to_string(template_name, context)
    pdf_file = HTML(string=html_string, base_url=None).write_pdf()
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{filename}"'
    return response

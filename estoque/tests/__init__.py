from .test_perfil import PerfilUsuarioTemaTests
from .test_signals import EstoqueSignalTests
from .test_views_produto import ProdutoCRUDViewTests
from .test_views_relatorio import RelatorioViewTests
from .test_views_importar import ImportarLicitacaoViewTests

__all__ = [
    "PerfilUsuarioTemaTests",
    "EstoqueSignalTests",
    "ProdutoCRUDViewTests",
    "RelatorioViewTests",
    "ImportarLicitacaoViewTests",
]

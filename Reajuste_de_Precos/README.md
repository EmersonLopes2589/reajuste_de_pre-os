# Reajuste Geral de Preços

Aplicativo com interface gráfica para aplicar um percentual de reajuste a um
catálogo de produtos, com cadastro/remoção de itens e gravação em arquivo.

## Estrutura da pasta

| Arquivo | Descrição |
|---|---|
| `Reajuste_de_precos_gui.py` | Aplicativo principal (interface gráfica Tkinter) |
| `Reajuste_de_precos_console.py` | Versão original em modo texto (Exercício 5) |
| `catalogo.json` | Catálogo de produtos salvo. Criado/atualizado automaticamente |
| `Executar.bat` | Atalho: duplo clique abre o programa sem janela de console |
| `requirements.txt` | Lista de dependências (nenhuma externa) |
| `README.md` | Este arquivo |

## Requisitos

- Python 3.10 ou superior, com Tkinter (incluído por padrão no instalador do Windows).
- **Nenhuma biblioteca externa** precisa ser instalada.

## Como executar

Duplo clique em `Executar.bat`, ou pelo terminal:

```powershell
python Reajuste_de_precos_gui.py
```

## Funcionalidades

- **Aplicar reajuste**: informa o percentual (aceita negativo para desconto) e mostra
  preço atual, novo preço e diferença de cada produto, além dos totais.
- **Gravar reajuste**: torna os novos preços a base do catálogo e salva no `catalogo.json`.
- **Restaurar**: zera o percentual em tela (não altera o arquivo).
- **Cadastrar produto**: nome + preço (aceita `1299,90`, `1299.90` ou `R$ 1.299,90`).
  Se o nome já existir, pergunta se deseja atualizar o preço.
- **Remover selecionado**: clique em um produto na tabela e remova com confirmação.
- Cadastros e remoções são **salvos automaticamente** em `catalogo.json`.

## Formato do `catalogo.json`

```json
{
  "celular": 1500.0,
  "tablet": 2500.0,
  "notebook": 5000.0
}
```

Se o arquivo for apagado ou estiver corrompido, o programa recria o catálogo padrão acima.
Esta pasta pode ser copiada para qualquer lugar — o caminho do arquivo é relativo ao script.

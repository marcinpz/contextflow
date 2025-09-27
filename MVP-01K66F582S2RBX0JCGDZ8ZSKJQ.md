---
runme:
  document:
    relativePath: MVP.md
  session:
    id: 01K66F582S2RBX0JCGDZ8ZSKJQ
    updated: 2025-09-27 22:52:43+02:00
---

## Knowledge System MVP - Podsumowanie i stack

### Cel systemu

Stworzenie lokalnego knowledge systemu dla deweloperów w dużej organizacji, integrującego:

* Kod źródłowy (Twoje repozytoria i repozy innych zespołów)
* Jira (epiki, stories)
* Dokumentację w Confluence, SharePoint, Teams
* ADR/RFC (decyzje architektoniczne)

Celem jest umożliwienie AI (np. Copilot, OpenCode) szybkiego dostępu do:

* Kontekstu projektowego (C4: Code / Component / Container / System)
* Aktualnych best practices i decyzji technicznych
* Historycznych informacji i powiązań między projektami

### Architektura high-level

```
Developer + AI
     |
     v
MCP Server (narzędzia)
  |        |        |
  v        v        v
Neo4j    Qdrant    Code Index (Tree-sitter / ctags)
(Graph DB)  (Vector DB)  (lokalny index kodu)
  ^         ^            ^
  |         |            |
Jira     Docs / Confluence / SharePoint / Teams
ADR / RFC
GitHub repozytoria
```

### Technologie i narzędzia

| Komponent                          | Technologia              | Licencja          | Uwagi / użycie lokalne                                                                     |
| ---------------------------------- | ------------------------ | ----------------- | ------------------------------------------------------------------------------------------ |
| Indeks kodu                        | Tree-sitter              | MIT               | Parsowanie kodu, wyciąganie klas, funkcji, modułów. Offline, Python binding `tree-sitter`. |
| Alternatywa indeksu                | Universal Ctags          | MIT               | Szybki index symboli, mniej semantyczny.                                                   |
| Graf wiedzy                        | Neo4j Community Edition  | GPLv3             | Modelowanie C4, decyzje, relacje. Local host możliwy.                                      |
| Vector DB                          | Qdrant / Weaviate        | Apache 2.0 / dual | Embeddings z dokumentów, ADR, Jira. Lokalny deployment w Dockerze.                         |
| MCP Server                         | OpenAI Agents Python SDK | MIT/Apache        | Udostępnia narzędzia AI do zapytań w grafie / indexie / vector DB. Lokalny serwer.         |
| Watchdog                           | Python watchdog          | MIT               | Monitorowanie zmian w repo i dokumentach, auto-update grafu / indexu.                      |
| Jira / GitHub / Confluence / Teams | API                      | –                 | Pobieranie danych do grafu / embeddings. Wymaga dostępu do serwisów.                       |

### Przepływ pracy (przykład)

1. Otrzymujesz story w Jira.
2. AI pyta MCP: `fetch_context(story_id)`.
3. MCP serwer sprawdza:

   * Graf (Neo4j) → epic, powiązany serwis, technologie.
   * Vector DB (Qdrant) → dokumentacja, best practices, ADR.
   * Index kodu (Tree-sitter / ctags) → istniejące funkcje/metody.
4. MCP zwraca odpowiedź:

   * Kontekst projektowy
   * Obowiązujące technologie
   * Linki do dokumentacji i przykłady kodu
   * Ostrzeżenia o deprecated / superseded docs.

### Roadmap MVP

1. **Faza 1 (2–3 tygodnie)**

   * Neo4j + MCP serwer + index kodu (Tree-sitter)
   * Jira ingestor → graf epików/stories
   * Relacje: story → service → technologie

2. **Faza 2**

   * Vector DB (Qdrant) → dokumentacja, ADR, opisy ticketów
   * MCP tool: `recommend_best_practices`

3. **Faza 3**

   * Integracja Confluence, SharePoint, Teams
   * Oznaczanie dokumentów jako deprecated / superseded

4. **Faza 4**

   * Pełny C4: containers, systems, context
   * Auto-update grafu przez watcher / webhooki

### Przykładowe MCP narzędzie (Python)

```python
from mcp.server import Server
import subprocess
from neo4j import GraphDatabase

server = Server("code-knowledge")

@server.tool()
def fallback_rg(pattern: str, path: str = ".") -> str:
    result = subprocess.run(["rg", pattern, path], capture_output=True, text=True)
    return result.stdout

@server.tool()
def graph_query(cypher: str) -> list:
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    with driver.session() as session:
        result = session.run(cypher)
        return [r.data() for r in result]

if __name__ == "__main__":
    server.run_stdio()
```

### Podsumowanie

* Wszystkie komponenty są **open source i lokalne**.
* System integruje **C4, code index, vector DB i knowledge base**.
* AI może korzystać z MCP tools, aby uzyskać **pełny kontekst kodu, historii i dokumentacji**.
* Roadmap pozwala wdrożyć MVP w kilka tygodni i później rozszerzać o kolejne źródła i warstwę C4.

---

**Plik PNG diagramu architektury:** `knowledge_system_architecture.png`
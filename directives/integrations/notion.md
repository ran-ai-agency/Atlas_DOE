# Directive: Integration Notion

## Objectif
Permettre a Atlas d'interagir avec Notion pour gerer la documentation, les bases de donnees, les projets et la base de connaissances de Ran.AI Agency.

## Usages Notion pour Ran.AI

### Base de Connaissances
- Documentation interne
- SOPs et processus
- Guides et tutoriels

### Gestion de Projets
- Suivi des projets clients
- Kanban des taches
- Jalons et deadlines

### CRM Complementaire
- Notes de reunion clients
- Historique des interactions
- Preferences et contexte client

### Templates
- Templates de propositions
- Modeles de documents
- Checklists

## Configuration MCP

### Serveur MCP Notion Officiel
```json
{
  "notion": {
    "command": "npx",
    "args": ["-y", "@notionhq/notion-mcp-server"],
    "env": {
      "NOTION_API_KEY": "${NOTION_API_KEY}"
    }
  }
}
```

### Configuration Alternative (Hosted)
Pour Claude Code, utiliser la commande:
```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

### Obtenir les Credentials Notion

1. Aller sur https://www.notion.so/my-integrations
2. Creer une nouvelle integration
3. Nommer l'integration "Atlas AI"
4. Copier le "Internal Integration Token"
5. Ajouter dans `.env` comme `NOTION_API_KEY`
6. **IMPORTANT**: Partager les pages/bases avec l'integration
   - Ouvrir chaque page/base a connecter
   - Cliquer sur "..." > "Connections" > Ajouter "Atlas AI"

## Operations Disponibles

### Pages
- `notion_search` - Rechercher dans Notion
- `notion_get_page` - Obtenir une page
- `notion_create_page` - Creer une page
- `notion_update_page` - Mettre a jour une page
- `notion_append_blocks` - Ajouter du contenu

### Bases de Donnees
- `notion_query_database` - Requeter une base
- `notion_create_database_item` - Creer un item
- `notion_update_database_item` - Modifier un item
- `notion_get_database` - Schema d'une base

### Blocs
- `notion_get_block_children` - Contenu d'une page
- `notion_append_block_children` - Ajouter des blocs
- `notion_delete_block` - Supprimer un bloc

## Structure Recommandee pour Ran.AI

```
Ran.AI Workspace/
├── Clients/
│   ├── [Base de donnees clients]
│   ├── Client A/
│   │   ├── Notes de reunion
│   │   ├── Projet
│   │   └── Documents
│   └── Client B/
├── Projets/
│   ├── [Kanban des projets]
│   └── Templates projet
├── Operations/
│   ├── SOPs
│   ├── Processus
│   └── Checklists
├── Marketing/
│   ├── Calendrier editorial
│   ├── Idees de contenu
│   └── Assets
├── Finance/
│   ├── Suivi facturation
│   └── Budget
└── Knowledge Base/
    ├── IA Agentique
    ├── Outils
    └── Best Practices
```

## Cas d'Usage par Role

### CEO
- Revue des notes strategiques
- Acces aux analyses et rapports
- Documentation vision et roadmap

### CMO
- Calendrier editorial
- Banque d'idees de contenu
- Suivi des campagnes

### CTO
- Documentation technique
- SOPs des workflows
- Notes de veille techno

### CFO
- Suivi facturation
- Notes sur la rentabilite clients
- Documentation financiere

### COO
- Gestion des projets
- SOPs operationnels
- Suivi des livrables

### AV
- Notes de reunion
- To-do lists
- Recherche dans la base

## Bonnes Pratiques

1. **Nommage coherent**: Utiliser des conventions de nommage claires
2. **Tags et proprietes**: Categoriser systematiquement les pages
3. **Liens bidirectionnels**: Creer des relations entre les contenus
4. **Templates**: Utiliser des templates pour la coherence
5. **Archivage**: Archiver plutot que supprimer

## Scripts d'Execution

- `execution/notion_sync.py` - Synchronisation de donnees
- `execution/notion_report_generator.py` - Generation de rapports
- `execution/notion_template_creator.py` - Creation depuis templates

## Limites et Contraintes

- Rate limit: 3 requetes/seconde
- Taille max bloc: 2000 caracteres
- Pas de suppression de databases via API
- Integration doit etre ajoutee manuellement a chaque page

## Sources

- [Notion MCP Documentation](https://developers.notion.com/docs/mcp)
- [Notion MCP Server GitHub](https://github.com/makenotion/notion-mcp-server)
- [Notion API Reference](https://developers.notion.com/reference)

# Ecosysteme Technologique Atlas - Ran.AI Agency

## Vue d'Ensemble

Atlas s'integre avec les applications suivantes via MCP (Model Context Protocol) hosted endpoints.

## Applications Principales

### Zoho One (Suite Complete)
**Role**: CRM, Comptabilite, Projets, Communication, Calendrier, Email, Stockage
**Integration**: MCP Hosted Endpoints (zohomcp.ca)
**Directive**: [zoho_one.md](zoho_one.md)

| Application | MCP Server | Usage |
|-------------|------------|-------|
| **Zoho CRM** | `zoho-crm` | Contacts, leads, comptes, pipeline commercial |
| **Zoho Books** | `zoho-books` | Facturation, comptabilite, tresorerie, depenses |
| **Zoho Cliq** | `zoho-cliq` | Messagerie d'equipe, canaux, notifications |
| **Zoho Calendar** | `zoho-calendar` | Evenements, rendez-vous, planification |
| **Zoho Mail** | `zoho-mail` | Emails professionnels, dossiers, templates |
| **Zoho WorkDrive** | `zoho-workdrive` | Stockage fichiers, partage, collaboration |

### Notion
**Role**: Documentation, Base de connaissances, Gestion de projet complementaire
**Integration**: MCP Hosted (mcp.notion.com)
**Directive**: [notion.md](notion.md)

| Usage | Description |
|-------|-------------|
| Knowledge Base | Documentation interne, SOPs, guides |
| Projets | Suivi detaille, notes, Kanban |
| Templates | Propositions, documents types |
| Notes clients | Historique, preferences, contexte |

## Applications Complementaires

### Canva Pro
**Role**: Design et creation visuelle
- Posts LinkedIn
- Presentations
- Assets marketing

### n8n / Make
**Role**: Automatisation entre applications
- Workflows automatises
- Integrations personnalisees
- Triggers et actions

## Mapping Roles <-> Applications

| Role | Zoho One | Notion |
|------|----------|--------|
| **CEO** | CRM (pipeline), Books (CA) | Strategy docs, Roadmap |
| **CMO** | CRM (leads), Mail, Cliq | Content calendar, Ideas |
| **CTO** | WorkDrive | Tech docs, SOPs |
| **CFO** | Books, CRM (rentabilite) | Finance notes |
| **COO** | Calendar, CRM | SOPs, Project tracking |
| **AV** | Mail, Calendar, CRM, WorkDrive | Notes, Tasks |

## Flux de Donnees

```
                    ┌─────────────────────────────────────┐
                    │           ZOHO ONE MCP              │
                    ├─────────┬─────────┬─────────┬───────┤
                    │   CRM   │  Books  │  Cliq   │ Mail  │
                    │Calendar │WorkDrive│         │       │
                    └────┬────┴────┬────┴────┬────┴───┬───┘
                         │         │         │        │
                         ▼         ▼         ▼        ▼
                    ┌─────────────────────────────────────┐
                    │              ATLAS                  │
                    │         (Orchestrateur IA)          │
                    └────────────────┬────────────────────┘
                         ▲           │           ▲
                         │           ▼           │
                    ┌────┴────┐ ┌─────────┐ ┌────┴────┐
                    │ NOTION  │ │ OUTPUTS │ │  n8n/   │
                    │   MCP   │ │Rapports │ │  Make   │
                    │(Contexte│ │Actions  │ │(Autom.) │
                    └─────────┘ └─────────┘ └─────────┘
```

## Configuration MCP

Fichier: `.claude/settings.json`

```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    },
    "zoho-crm": {
      "type": "http",
      "url": "https://ranaiagencymcpserver-110002203871.zohomcp.ca/mcp/message?key=..."
    },
    "zoho-books": {
      "type": "http",
      "url": "https://zohobooks-110002203871.zohomcp.ca/mcp/message?key=..."
    },
    "zoho-mail": {
      "type": "http",
      "url": "https://zohomail-110002203871.zohomcp.ca/mcp/message?key=..."
    },
    "zoho-workdrive": {
      "type": "http",
      "url": "https://zohoworkdrive-110002203871.zohomcp.ca/mcp/message?key=..."
    },
    "zoho-calendar": {
      "type": "http",
      "url": "https://zohocalendar-110002203871.zohomcp.ca/mcp/message?key=..."
    },
    "zoho-cliq": {
      "type": "http",
      "url": "https://zohocliq-110002203871.zohomcp.ca/mcp/message?key=..."
    }
  }
}
```

## Avantages des MCP Hosted

- **Pas de configuration OAuth**: Les endpoints sont pre-authentifies
- **Pas de gestion de tokens**: Zoho gere les refresh tokens automatiquement
- **Haute disponibilite**: Heberges sur l'infrastructure Zoho
- **Securite**: Cles API uniques par endpoint

## Priorite des Sources de Donnees

1. **Zoho CRM**: Source de verite pour les contacts, leads, opportunites
2. **Zoho Books**: Source de verite pour la facturation et comptabilite
3. **Zoho Calendar**: Source de verite pour la planification
4. **Notion**: Source de verite pour la documentation et le contexte qualitatif
5. **Zoho WorkDrive**: Source pour les fichiers et documents partages

## Scripts d'Execution (Fallback)

| Script | Description |
|--------|-------------|
| `execution/zoho_client.py` | Client Python fallback si MCP indisponible |
| `execution/notion_client.py` | Client Python pour Notion |

## Synchronisation

- Les donnees Zoho sont la reference principale pour les operations
- Notion sert de couche de contexte et documentation
- WorkDrive centralise les fichiers partages
- Les MCP permettent un acces direct sans configuration complexe

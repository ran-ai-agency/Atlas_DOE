# Guide de Configuration des Integrations Atlas

## Vue d'Ensemble

Ce guide explique comment configurer les integrations Zoho One et Notion pour Atlas.

## Etape 1: Configuration Notion

### 1.1 Creer une Integration Notion

1. Aller sur https://www.notion.so/my-integrations
2. Cliquer sur "New integration"
3. Configurer:
   - **Name**: Atlas AI
   - **Associated workspace**: Votre workspace Ran.AI
   - **Capabilities**: Read content, Update content, Insert content
4. Cliquer "Submit"
5. Copier le "Internal Integration Secret"

### 1.2 Partager les Pages avec l'Integration

Pour chaque page ou database que Atlas doit acceder:

1. Ouvrir la page dans Notion
2. Cliquer sur "..." en haut a droite
3. Cliquer sur "Add connections"
4. Chercher et selectionner "Atlas AI"
5. Confirmer

**Pages recommandees a partager:**
- Workspace principal
- Base de donnees Clients
- Base de donnees Projets
- Knowledge Base
- SOPs et Processus

### 1.3 Ajouter la Cle dans .env

```
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxx
```

## Etape 2: Configuration Zoho One

### 2.1 Creer une Application API Zoho

1. Aller sur https://api-console.zoho.eu/ (ou .com selon votre region)
2. Cliquer "Add Client"
3. Choisir "Self Client"
4. Nommer l'application "Atlas AI"
5. Noter le Client ID et Client Secret

### 2.2 Generer le Code d'Autorisation

1. Dans la console API, aller a "Generate Code"
2. Entrer **TOUS** les scopes necessaires pour Zoho One complet:

```
ZohoCRM.modules.ALL,ZohoCRM.settings.ALL,ZohoBooks.fullaccess.all,ZohoProjects.projects.ALL,ZohoProjects.tasks.ALL,ZohoCliq.Webhooks.CREATE,ZohoCliq.Messages.ALL,ZohoCalendar.calendar.ALL,ZohoCalendar.event.ALL,ZohoMail.messages.ALL,ZohoMail.folders.ALL,WorkDrive.files.ALL,WorkDrive.folders.ALL
```

3. Choisir la duree (recommande: 10 minutes)
4. Cliquer "Create"
5. Copier le code genere

### 2.3 Echanger le Code contre un Refresh Token

Executer cette requete (remplacer les valeurs):

```bash
curl -X POST "https://accounts.zoho.eu/oauth/v2/token" \
  -d "code=VOTRE_CODE" \
  -d "client_id=VOTRE_CLIENT_ID" \
  -d "client_secret=VOTRE_CLIENT_SECRET" \
  -d "grant_type=authorization_code"
```

La reponse contiendra le `refresh_token`.

### 2.4 Trouver l'Org ID

1. Dans Zoho CRM, aller dans Settings > Developer Space > APIs
2. L'Org ID est affiche en haut

**Alternative pour Zoho Books:**
1. Aller dans Zoho Books > Settings > Organization Profile
2. L'Organization ID est affiche

### 2.5 Ajouter les Credentials dans .env

```
ZOHO_CLIENT_ID=1000.xxxxxxxxxxxxxxx
ZOHO_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxx
ZOHO_REFRESH_TOKEN=1000.xxxxxxxxxxxxxxxxxxxxxxx
ZOHO_ORG_ID=xxxxxxxxx
ZOHO_REGION=eu
```

## Etape 3: Installer les Serveurs MCP

### Option A: Via Claude Code (recommande)

```bash
# Notion MCP
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Zoho CRM MCP (si disponible via npm)
claude mcp add zoho-crm -- npx -y zohocrm-mcp-server
```

### Option B: Configuration manuelle

Editer `.claude/settings.json`:

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_API_KEY": "${NOTION_API_KEY}"
      }
    },
    "zoho-crm": {
      "command": "npx",
      "args": ["-y", "zohocrm-mcp-server"],
      "env": {
        "ZOHO_CLIENT_ID": "${ZOHO_CLIENT_ID}",
        "ZOHO_CLIENT_SECRET": "${ZOHO_CLIENT_SECRET}",
        "ZOHO_REFRESH_TOKEN": "${ZOHO_REFRESH_TOKEN}",
        "ZOHO_REGION": "${ZOHO_REGION}"
      }
    }
  }
}
```

## Etape 4: Verifier les Connexions

### Test Notion

```bash
python execution/notion_client.py
```

Resultat attendu: "Connexion Notion reussie. X resultats trouves."

### Test Zoho

```bash
python execution/zoho_client.py
```

Resultat attendu: "Connexion Zoho reussie. Token: xxx..."

## Applications Zoho One Accessibles

Avec les scopes configures, Atlas peut acceder a:

| Application | Fonctionnalites |
|-------------|-----------------|
| **Zoho CRM** | Contacts, leads, deals, comptes, activites |
| **Zoho Books** | Factures, devis, clients, depenses, tresorerie |
| **Zoho Projects** | Projets, taches, jalons, suivi temps |
| **Zoho Cliq** | Canaux, messages, notifications |
| **Zoho Calendar** | Calendriers, evenements, disponibilites |
| **Zoho Mail** | Dossiers, emails, envoi |
| **Zoho WorkDrive** | Fichiers, dossiers, partage |

## Depannage

### Notion: "Could not find..."
- Verifiez que l'integration est partagee avec la page
- Verifiez que l'API key est correcte

### Zoho: "Invalid refresh token"
- Le refresh token a peut-etre expire (1 an d'inactivite)
- Regenerez un nouveau code et refresh token

### Zoho: "Invalid client"
- Verifiez que vous utilisez la bonne region (eu, com, etc.)
- Verifiez le Client ID et Secret

### Zoho: "Invalid scope"
- Assurez-vous que l'application Zoho a les permissions necessaires
- Regenerez le code avec tous les scopes requis

### Rate Limiting

| Application | Limite |
|-------------|--------|
| Notion | 3 req/seconde |
| Zoho CRM | 100 req/minute |
| Zoho Books | 100 req/minute |
| Zoho Projects | 100 req/minute |
| Zoho Cliq | 100 req/minute |
| Zoho Calendar | 100 req/minute |
| Zoho Mail | 250 req/jour |
| Zoho WorkDrive | 100 req/minute |

## Support

- [Notion API Documentation](https://developers.notion.com/)
- [Zoho CRM API](https://www.zoho.com/crm/developer/docs/api/v2/)
- [Zoho Books API](https://www.zoho.com/books/api/v3/)
- [Zoho Projects API](https://www.zoho.com/projects/help/rest-api/)
- [Zoho Calendar API](https://www.zoho.com/calendar/help/api/)
- [Zoho Mail API](https://www.zoho.com/mail/help/api/)
- [Zoho WorkDrive API](https://www.zoho.com/workdrive/help/api/)
- [Zoho MCP](https://www.zoho.com/mcp/)

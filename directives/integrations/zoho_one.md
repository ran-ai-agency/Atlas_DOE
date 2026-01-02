# Directive: Integration Zoho One

## Objectif
Permettre a Atlas d'interagir avec l'ensemble de la suite Zoho One de Ran.AI Agency pour gerer les donnees CRM, comptabilite, projets, communication, calendrier, emails et fichiers.

## Applications Zoho One Actives

### Zoho CRM
- Gestion des contacts, leads, comptes, opportunites
- Pipeline commercial
- Activites et taches commerciales

### Zoho Books
- Facturation clients
- Comptabilite et ecritures
- Suivi de tresorerie
- Devis et bons de commande

### Zoho Projects
- Gestion de projets clients
- Taches et sous-taches
- Jalons et deadlines
- Suivi du temps passe

### Zoho Cliq
- Messagerie d'equipe
- Canaux de discussion
- Notifications et alertes
- Bots et automatisations

### Zoho Calendar
- Evenements et rendez-vous
- Planification de reunions
- Rappels
- Synchronisation avec d'autres calendriers

### Zoho Mail
- Emails professionnels
- Dossiers et labels
- Recherche dans les emails
- Templates d'emails

### Zoho WorkDrive
- Stockage de fichiers
- Partage de documents
- Collaboration sur fichiers
- Organisation en dossiers

## Configuration MCP

### Serveurs MCP Zoho
```json
{
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
```

### Scopes Requis

Pour acceder a toutes les applications, generer le refresh token avec ces scopes:

```
ZohoCRM.modules.ALL,
ZohoCRM.settings.ALL,
ZohoBooks.fullaccess.all,
ZohoProjects.projects.ALL,
ZohoProjects.tasks.ALL,
ZohoCliq.Webhooks.CREATE,
ZohoCliq.Messages.ALL,
ZohoCalendar.calendar.ALL,
ZohoCalendar.event.ALL,
ZohoMail.messages.ALL,
ZohoMail.folders.ALL,
WorkDrive.files.ALL,
WorkDrive.folders.ALL
```

### Obtenir les Credentials Zoho

1. Aller sur https://api-console.zoho.com/ (ou .eu selon region)
2. Creer une application "Self Client"
3. Generer un code d'autorisation avec les scopes ci-dessus
4. Echanger le code contre un refresh token
5. Copier les credentials dans `.env`

## Operations par Application

### Zoho CRM
| Operation | Description |
|-----------|-------------|
| `crm_search` | Rechercher contacts, leads, deals |
| `crm_get_record` | Obtenir un enregistrement |
| `crm_create_record` | Creer un enregistrement |
| `crm_update_record` | Modifier un enregistrement |
| `crm_list_records` | Lister les enregistrements |

### Zoho Books
| Operation | Description |
|-----------|-------------|
| `books_list_invoices` | Lister les factures |
| `books_create_invoice` | Creer une facture |
| `books_get_invoice` | Details d'une facture |
| `books_list_customers` | Lister les clients |
| `books_get_balance` | Solde du compte |
| `books_list_expenses` | Lister les depenses |

### Zoho Projects
| Operation | Description |
|-----------|-------------|
| `projects_list` | Lister les projets |
| `projects_get` | Details d'un projet |
| `projects_create_task` | Creer une tache |
| `projects_list_tasks` | Lister les taches |
| `projects_update_task` | Modifier une tache |
| `projects_log_time` | Enregistrer du temps |

### Zoho Cliq
| Operation | Description |
|-----------|-------------|
| `cliq_send_message` | Envoyer un message |
| `cliq_list_channels` | Lister les canaux |
| `cliq_post_to_channel` | Poster dans un canal |
| `cliq_create_bot_message` | Message via bot |

### Zoho Calendar
| Operation | Description |
|-----------|-------------|
| `calendar_list_events` | Lister les evenements |
| `calendar_create_event` | Creer un evenement |
| `calendar_update_event` | Modifier un evenement |
| `calendar_delete_event` | Supprimer un evenement |
| `calendar_get_freebusy` | Disponibilites |

### Zoho Mail
| Operation | Description |
|-----------|-------------|
| `mail_list_folders` | Lister les dossiers |
| `mail_list_messages` | Lister les emails |
| `mail_get_message` | Lire un email |
| `mail_send` | Envoyer un email |
| `mail_search` | Rechercher des emails |

### Zoho WorkDrive
| Operation | Description |
|-----------|-------------|
| `workdrive_list_files` | Lister les fichiers |
| `workdrive_upload` | Uploader un fichier |
| `workdrive_download` | Telecharger un fichier |
| `workdrive_create_folder` | Creer un dossier |
| `workdrive_share` | Partager un fichier |

## Cas d'Usage par Role

### CEO
- **CRM**: Pipeline commercial, opportunites strategiques
- **Books**: Vue financiere globale, CA
- **Projects**: Avancement des projets majeurs
- **Calendar**: Reunions strategiques

### CMO
- **CRM**: Leads, campagnes, conversion
- **Mail**: Communications prospects
- **Cliq**: Coordination marketing
- **WorkDrive**: Assets marketing

### CTO
- **Projects**: Projets techniques, taches dev
- **WorkDrive**: Documentation technique
- **Cliq**: Communication equipe tech
- **CRM**: Templates clients

### CFO
- **Books**: Facturation, comptabilite, tresorerie
- **CRM**: Rentabilite par client
- **Projects**: Couts des projets
- **WorkDrive**: Documents financiers

### COO
- **Projects**: Tous les projets, allocation ressources
- **CRM**: Suivi client operationnel
- **Calendar**: Planning equipe
- **Cliq**: Coordination quotidienne

### AV
- **Mail**: Gestion emails, reponses
- **Calendar**: Planification reunions
- **CRM**: Mises a jour contacts
- **WorkDrive**: Organisation fichiers

## Bonnes Pratiques

1. **Toujours verifier avant modification**: Lire les donnees existantes avant update
2. **Limiter les requetes**: Utiliser la pagination pour les grandes listes
3. **Gerer les erreurs API**: Retry en cas de rate limiting
4. **Valider les donnees**: Verifier les champs obligatoires avant creation
5. **Synchroniser les apps**: Maintenir la coherence entre CRM et Books

## Scripts d'Execution

- `execution/zoho_client.py` - Client Python unifie Zoho One
- `execution/zoho_crm_sync.py` - Synchronisation CRM
- `execution/zoho_books_invoicing.py` - Gestion facturation
- `execution/zoho_projects_tracker.py` - Suivi des projets
- `execution/zoho_calendar_manager.py` - Gestion calendrier

## Limites et Contraintes

| Application | Rate Limit |
|-------------|------------|
| CRM | 100 req/min |
| Books | 100 req/min |
| Projects | 100 req/min |
| Cliq | 100 req/min |
| Calendar | 100 req/min |
| Mail | 250 req/jour |
| WorkDrive | 100 req/min |

- Refresh token expire apres 1 an d'inactivite
- Certaines operations necessitent des permissions elevees
- WorkDrive: limite de 5GB par fichier

## Sources

- [Zoho MCP Official](https://www.zoho.com/mcp/)
- [Zoho CRM API](https://www.zoho.com/crm/developer/docs/api/v2/)
- [Zoho Books API](https://www.zoho.com/books/api/v3/)
- [Zoho Projects API](https://www.zoho.com/projects/help/rest-api/)
- [Zoho Calendar API](https://www.zoho.com/calendar/help/api/)
- [Zoho Mail API](https://www.zoho.com/mail/help/api/)
- [Zoho WorkDrive API](https://www.zoho.com/workdrive/help/api/)

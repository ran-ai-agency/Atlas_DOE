# Operations MCP Disponibles pour Tous les Roles

Ce document reference toutes les operations disponibles via les MCP servers Zoho One et Notion.

## MCP Servers

| Server | Application | Description |
|--------|-------------|-------------|
| `zoho-crm` | Zoho CRM | Contacts, leads, deals, activites |
| `zoho-books` | Zoho Books | Factures, clients, comptabilite |
| `zoho-mail` | Zoho Mail | Emails, dossiers |
| `zoho-calendar` | Zoho Calendar | Evenements, reunions |
| `zoho-cliq` | Zoho Cliq | Messagerie, canaux |
| `zoho-workdrive` | Zoho WorkDrive | Fichiers, dossiers |
| `notion` | Notion | Pages, databases |

---

## Zoho CRM (`zoho-crm`)

### Modules Disponibles
- Contacts, Leads, Accounts, Deals
- Tasks, Events, Calls, Notes

### Operations

| Type | Operations |
|------|------------|
| **Lecture** | Rechercher, Lister, Obtenir details, Consulter historique |
| **Creation** | Creer contact/lead/deal, Ajouter tache, Enregistrer note |
| **Mise a jour** | Modifier enregistrement, Changer statut, Mettre a jour pipeline |
| **Suppression** | Supprimer enregistrement, Retirer tache |

---

## Zoho Books (`zoho-books`)

### Modules Disponibles
- Invoices, Estimates, Customers
- Expenses, Payments, Items

### Operations

| Type | Operations |
|------|------------|
| **Lecture** | Lister factures, Consulter details, Voir paiements, Clients |
| **Creation** | Creer facture, Ajouter client, Enregistrer paiement, Devis |
| **Mise a jour** | Modifier facture, Mettre a jour client, Statut paiement |
| **Suppression** | Annuler facture |

---

## Zoho Mail (`zoho-mail`)

### Operations

| Type | Operations |
|------|------------|
| **Lecture** | Lister emails, Lire contenu, Rechercher, Dossiers |
| **Creation** | Envoyer email, Creer brouillon, Repondre, Transferer |
| **Mise a jour** | Deplacer, Marquer lu/non lu, Labels |
| **Suppression** | Supprimer email |

---

## Zoho Calendar (`zoho-calendar`)

### Operations

| Type | Operations |
|------|------------|
| **Lecture** | Lister evenements, Details, Disponibilites, Calendriers |
| **Creation** | Creer evenement, Planifier reunion, Rappel, Invitations |
| **Mise a jour** | Modifier date/heure, Lieu, Participants, Reprogrammer |
| **Suppression** | Annuler evenement, Supprimer reunion |

---

## Zoho Cliq (`zoho-cliq`)

### Operations

| Type | Operations |
|------|------------|
| **Lecture** | Lister canaux, Messages recents, Rechercher |
| **Creation** | Message canal, Message direct, Notification |
| **Mise a jour** | Modifier message |

---

## Zoho WorkDrive (`zoho-workdrive`)

### Operations

| Type | Operations |
|------|------------|
| **Lecture** | Lister fichiers, Rechercher, Telecharger, Partages |
| **Creation** | Creer dossier, Uploader, Partager |
| **Mise a jour** | Renommer, Deplacer, Permissions |
| **Suppression** | Supprimer fichier/dossier |

---

## Notion

### Pages

| Type | Operations |
|------|------------|
| **Lecture** | Rechercher, Lire contenu, Proprietes |
| **Creation** | Creer page, Ajouter contenu, Page dans database |
| **Mise a jour** | Modifier contenu, Proprietes, Blocs |
| **Suppression** | Archiver page, Supprimer bloc |

### Databases

| Type | Operations |
|------|------------|
| **Lecture** | Lister items, Filtrer, Trier, Rechercher |
| **Creation** | Ajouter item, Entree avec proprietes |
| **Mise a jour** | Modifier proprietes, Statut, Dates |
| **Suppression** | Archiver item |

---

## Bonnes Pratiques Communes

1. **Lecture avant modification**: Toujours lire les donnees existantes avant de modifier
2. **Validation avant action**: Demander confirmation pour les operations sensibles
3. **Documentation**: Logger les operations importantes dans Notion
4. **Coherence**: Maintenir la synchronisation entre Zoho et Notion
5. **Gestion d'erreurs**: Gerer les erreurs API et retry si necessaire

"""
Notion Client - Interface Python pour l'API Notion
Utilise en complement du MCP pour les operations avancees
"""

import os
import requests
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

NOTION_API_VERSION = "2022-06-28"
NOTION_BASE_URL = "https://api.notion.com/v1"


@dataclass
class NotionConfig:
    api_key: str

    @classmethod
    def from_env(cls) -> "NotionConfig":
        return cls(api_key=os.getenv("NOTION_API_KEY", ""))


class NotionClient:
    """Client pour interagir avec l'API Notion."""

    def __init__(self, config: Optional[NotionConfig] = None):
        if config is None:
            config = NotionConfig.from_env()
        self.config = config

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_API_VERSION
        }

    # ========== Search ==========

    def search(self, query: str = "", filter_type: Optional[str] = None, page_size: int = 100) -> List[Dict]:
        """
        Recherche dans Notion.

        Args:
            query: Texte a rechercher
            filter_type: "page" ou "database" pour filtrer
            page_size: Nombre de resultats (max 100)
        """
        url = f"{NOTION_BASE_URL}/search"
        payload: Dict[str, Any] = {"page_size": page_size}

        if query:
            payload["query"] = query

        if filter_type:
            payload["filter"] = {"property": "object", "value": filter_type}

        response = requests.post(url, headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json().get("results", [])

    # ========== Pages ==========

    def get_page(self, page_id: str) -> Dict:
        """Obtient une page par ID."""
        url = f"{NOTION_BASE_URL}/pages/{page_id}"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def create_page(self, parent: Dict, properties: Dict, children: Optional[List] = None) -> Dict:
        """
        Cree une nouvelle page.

        Args:
            parent: {"database_id": "xxx"} ou {"page_id": "xxx"}
            properties: Proprietes de la page
            children: Blocs de contenu optionnels
        """
        url = f"{NOTION_BASE_URL}/pages"
        payload = {"parent": parent, "properties": properties}
        if children:
            payload["children"] = children

        response = requests.post(url, headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json()

    def update_page(self, page_id: str, properties: Dict) -> Dict:
        """Met a jour les proprietes d'une page."""
        url = f"{NOTION_BASE_URL}/pages/{page_id}"
        response = requests.patch(url, headers=self._headers(), json={"properties": properties})
        response.raise_for_status()
        return response.json()

    # ========== Databases ==========

    def get_database(self, database_id: str) -> Dict:
        """Obtient le schema d'une database."""
        url = f"{NOTION_BASE_URL}/databases/{database_id}"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def query_database(
        self,
        database_id: str,
        filter: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
        page_size: int = 100
    ) -> List[Dict]:
        """
        Requete une database.

        Args:
            database_id: ID de la database
            filter: Filtre Notion (voir doc API)
            sorts: Tri des resultats
            page_size: Nombre de resultats
        """
        url = f"{NOTION_BASE_URL}/databases/{database_id}/query"
        payload: Dict[str, Any] = {"page_size": page_size}

        if filter:
            payload["filter"] = filter
        if sorts:
            payload["sorts"] = sorts

        response = requests.post(url, headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json().get("results", [])

    def create_database_item(self, database_id: str, properties: Dict) -> Dict:
        """Ajoute un item a une database."""
        return self.create_page(
            parent={"database_id": database_id},
            properties=properties
        )

    # ========== Blocks ==========

    def get_block_children(self, block_id: str, page_size: int = 100) -> List[Dict]:
        """Obtient les blocs enfants d'une page ou d'un bloc."""
        url = f"{NOTION_BASE_URL}/blocks/{block_id}/children"
        params = {"page_size": page_size}
        response = requests.get(url, headers=self._headers(), params=params)
        response.raise_for_status()
        return response.json().get("results", [])

    def append_block_children(self, block_id: str, children: List[Dict]) -> Dict:
        """Ajoute des blocs enfants a une page ou un bloc."""
        url = f"{NOTION_BASE_URL}/blocks/{block_id}/children"
        response = requests.patch(url, headers=self._headers(), json={"children": children})
        response.raise_for_status()
        return response.json()

    def delete_block(self, block_id: str) -> Dict:
        """Supprime (archive) un bloc."""
        url = f"{NOTION_BASE_URL}/blocks/{block_id}"
        response = requests.delete(url, headers=self._headers())
        response.raise_for_status()
        return response.json()


# ========== Helpers pour creer des blocs ==========

def create_text_block(text: str, block_type: str = "paragraph") -> Dict:
    """Cree un bloc de texte."""
    return {
        "object": "block",
        "type": block_type,
        block_type: {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    }


def create_heading_block(text: str, level: int = 1) -> Dict:
    """Cree un bloc heading (1, 2 ou 3)."""
    heading_type = f"heading_{level}"
    return {
        "object": "block",
        "type": heading_type,
        heading_type: {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    }


def create_bullet_list(items: List[str]) -> List[Dict]:
    """Cree une liste a puces."""
    return [
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": item}}]
            }
        }
        for item in items
    ]


def create_todo_block(text: str, checked: bool = False) -> Dict:
    """Cree un bloc to-do."""
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "checked": checked
        }
    }


# ========== Helpers pour les proprietes ==========

def title_property(text: str) -> Dict:
    """Cree une propriete title."""
    return {"title": [{"text": {"content": text}}]}


def rich_text_property(text: str) -> Dict:
    """Cree une propriete rich_text."""
    return {"rich_text": [{"text": {"content": text}}]}


def select_property(option: str) -> Dict:
    """Cree une propriete select."""
    return {"select": {"name": option}}


def date_property(date: str, end: Optional[str] = None) -> Dict:
    """Cree une propriete date (format: YYYY-MM-DD)."""
    value = {"start": date}
    if end:
        value["end"] = end
    return {"date": value}


# ========== Fonctions utilitaires ==========

def find_database_by_title(title: str) -> Optional[str]:
    """Trouve une database par son titre."""
    client = NotionClient()
    results = client.search(query=title, filter_type="database")

    for result in results:
        db_title = result.get("title", [{}])[0].get("plain_text", "")
        if db_title.lower() == title.lower():
            return result["id"]

    return None


def get_all_pages_in_database(database_id: str) -> List[Dict]:
    """Recupere toutes les pages d'une database (avec pagination)."""
    client = NotionClient()
    all_results = []
    has_more = True
    start_cursor = None

    while has_more:
        url = f"{NOTION_BASE_URL}/databases/{database_id}/query"
        payload: Dict[str, Any] = {"page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor

        response = requests.post(url, headers=client._headers(), json=payload)
        response.raise_for_status()
        data = response.json()

        all_results.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")

    return all_results


if __name__ == "__main__":
    # Test de connexion
    try:
        client = NotionClient()
        results = client.search(page_size=5)
        print(f"Connexion Notion reussie. {len(results)} resultats trouves.")
        for r in results[:3]:
            title = r.get("properties", {}).get("title", {})
            if isinstance(title, dict):
                title_text = title.get("title", [{}])[0].get("plain_text", "Sans titre")
            else:
                title_text = "Sans titre"
            print(f"  - {title_text}")
    except Exception as e:
        print(f"Erreur de connexion Notion: {e}")

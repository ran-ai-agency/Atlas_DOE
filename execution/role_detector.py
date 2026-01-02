"""
Role Detector - Detection automatique du role Atlas a activer
"""

import re
from typing import List, Tuple

# Mapping des mots-cles vers les roles
ROLE_KEYWORDS = {
    "CEO": [
        "strategie", "vision", "positionnement", "marche", "concurrence",
        "opportunite", "partenariat", "croissance", "long terme", "tendances",
        "analyse strategique", "decision", "investissement", "acquisition",
        "roadmap", "objectifs", "leadership"
    ],
    "CMO": [
        "marketing", "linkedin", "contenu", "post", "branding", "leads",
        "acquisition", "campagne", "seo", "email", "newsletter", "audience",
        "engagement", "conversion", "funnel", "landing page", "webinaire",
        "thought leadership", "personal branding", "visibilite"
    ],
    "CTO": [
        "technologie", "automatisation", "workflow", "integration", "api",
        "outil", "n8n", "make", "hubspot", "notion", "securite", "rgpd",
        "script", "code", "developpement", "innovation", "ia", "modele",
        "prompt", "template technique", "architecture"
    ],
    "CFO": [
        "finance", "budget", "rentabilite", "marge", "prix", "tarif",
        "facturation", "tresorerie", "prevision", "roi", "cout", "depense",
        "investissement", "fiscalite", "comptabilite", "ca", "chiffre affaires"
    ],
    "COO": [
        "operations", "processus", "projet", "livraison", "client",
        "onboarding", "qualite", "standard", "sop", "rh", "recrutement",
        "equipe", "ressources", "planning", "delai", "efficacite",
        "developpement personnel", "formation", "competences"
    ],
    "AV": [
        "email", "calendrier", "reunion", "document", "recherche",
        "administratif", "tache", "to-do", "rappel", "synthese",
        "brouillon", "presentation", "planification", "organisation"
    ]
}

# Prefixes pour activation manuelle
MANUAL_PREFIXES = {
    "en tant que ceo": "CEO",
    "en tant que cmo": "CMO",
    "en tant que cto": "CTO",
    "en tant que cfo": "CFO",
    "en tant que coo": "COO",
    "en tant qu'assistant virtuel": "AV",
    "en tant que av": "AV"
}


def detect_manual_role(prompt: str) -> str | None:
    """Detecte si un role est explicitement demande."""
    prompt_lower = prompt.lower().strip()
    for prefix, role in MANUAL_PREFIXES.items():
        if prompt_lower.startswith(prefix):
            return role
    return None


def calculate_role_scores(prompt: str) -> dict[str, int]:
    """Calcule un score pour chaque role base sur les mots-cles."""
    prompt_lower = prompt.lower()
    scores = {role: 0 for role in ROLE_KEYWORDS}

    for role, keywords in ROLE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in prompt_lower:
                scores[role] += 1

    return scores


def detect_role(prompt: str) -> Tuple[str, float]:
    """
    Detecte le role le plus pertinent pour un prompt donne.

    Returns:
        Tuple[str, float]: (role, confidence)
    """
    # Verifier d'abord l'activation manuelle
    manual_role = detect_manual_role(prompt)
    if manual_role:
        return (manual_role, 1.0)

    # Calculer les scores automatiques
    scores = calculate_role_scores(prompt)
    max_score = max(scores.values())

    if max_score == 0:
        # Defaut: Assistant Virtuel pour les taches generiques
        return ("AV", 0.3)

    # Trouver le(s) role(s) avec le score max
    top_roles = [role for role, score in scores.items() if score == max_score]

    # Calculer la confiance
    total_score = sum(scores.values())
    confidence = max_score / total_score if total_score > 0 else 0.5

    return (top_roles[0], confidence)


def detect_multi_roles(prompt: str, threshold: float = 0.3) -> List[str]:
    """
    Detecte plusieurs roles si le prompt couvre plusieurs domaines.

    Args:
        prompt: Le texte a analyser
        threshold: Score minimum relatif pour inclure un role

    Returns:
        List[str]: Liste des roles actives
    """
    scores = calculate_role_scores(prompt)
    max_score = max(scores.values())

    if max_score == 0:
        return ["AV"]

    # Inclure tous les roles au-dessus du seuil
    threshold_score = max_score * threshold
    active_roles = [role for role, score in scores.items() if score >= threshold_score]

    return sorted(active_roles, key=lambda r: scores[r], reverse=True)


def format_role_prefix(roles: List[str]) -> str:
    """Formate le prefixe de role pour la reponse."""
    if len(roles) == 1:
        return f"[{roles[0]}]"
    return "[" + " + ".join(roles) + "]"


if __name__ == "__main__":
    # Tests
    test_prompts = [
        "En tant que CEO, analyse cette opportunite de partenariat",
        "Cree un post LinkedIn sur l'IA agentique",
        "Quel est le ROI de cet investissement?",
        "Optimise le workflow d'onboarding client",
        "Prepare un email de suivi pour le prospect",
        "Analyse la strategie marketing et le budget necessaire"
    ]

    for prompt in test_prompts:
        role, confidence = detect_role(prompt)
        multi_roles = detect_multi_roles(prompt)
        print(f"\nPrompt: {prompt}")
        print(f"  Role principal: {role} (confiance: {confidence:.2f})")
        print(f"  Multi-roles: {format_role_prefix(multi_roles)}")

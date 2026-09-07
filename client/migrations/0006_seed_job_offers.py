from django.db import migrations


OFFERS = [
    {
        "title": "Chauffeur de camion-toupie",
        "department": "Logistique",
        "location": "Lomé, Togo",
        "contract_type": "cdi",
        "description": (
            "Assurer le transport et la livraison du béton prêt à l'emploi depuis la "
            "centrale jusqu'aux chantiers de Lomé et environs, dans le respect des délais "
            "et des consignes de sécurité."
        ),
        "profile": (
            "Permis poids lourd (C/CE) valide - 2 ans d'expérience minimum - "
            "Connaissance des chantiers de Lomé - Ponctualité et sens du service."
        ),
    },
    {
        "title": "Chef de centrale à béton",
        "department": "Production",
        "location": "Lomé, Togo",
        "contract_type": "cdi",
        "description": (
            "Piloter la production quotidienne de la centrale : formulation, contrôle "
            "qualité, planning des toupies, maintenance de premier niveau et management "
            "de l'équipe de production."
        ),
        "profile": (
            "Bac+2/3 génie civil ou équivalent - Expérience en centrale BPE - "
            "Maîtrise des normes NF EN 206 - Leadership et rigueur."
        ),
    },
    {
        "title": "Commercial(e) BTP",
        "department": "Commercial",
        "location": "Lomé, Togo",
        "contract_type": "cdd",
        "description": (
            "Développer le portefeuille clients (entreprises de BTP, maîtres d'ouvrage), "
            "établir les devis, suivre les commandes et fidéliser les comptes existants."
        ),
        "profile": (
            "Expérience commerciale B2B, idéalement dans le BTP ou les matériaux - "
            "Bon relationnel - Autonomie - Permis B."
        ),
    },
]


def seed(apps, schema_editor):
    JobOffer = apps.get_model("client", "JobOffer")
    for data in OFFERS:
        JobOffer.objects.get_or_create(title=data["title"], defaults=data)


def unseed(apps, schema_editor):
    JobOffer = apps.get_model("client", "JobOffer")
    JobOffer.objects.filter(title__in=[o["title"] for o in OFFERS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("client", "0005_joboffer_jobapplication"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]

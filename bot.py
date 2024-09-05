import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Charger les variables d'environnement depuis le fichier .env

TOKEN = os.getenv("DISCORD_TOKEN")  # Obtenez le token depuis les variables d'environnement

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Répertoire pour stocker les fichiers utilisateur
DATA_DIR = "user_data"

# Crée le répertoire s'il n'existe pas déjà
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def load_user_data(user_id):
    """Charge les données de l'utilisateur à partir d'un fichier JSON."""
    file_path = os.path.join(DATA_DIR, f"{user_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        return {'films': [], 'séries': [], 'mangas': [], 'animes': []}

def save_user_data(user_id, data):
    """Sauvegarde les données de l'utilisateur dans un fichier JSON."""
    file_path = os.path.join(DATA_DIR, f"{user_id}.json")
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def get_color(type):
    """Retourne la couleur de l'embed en fonction du type de média."""
    colors = {
        'film': nextcord.Color.green(),
        'serie': nextcord.Color.gold(),
        'manga': nextcord.Color.red(),
        'anime': nextcord.Color.blue()
    }
    return colors.get(type, nextcord.Color.default())

def normalize_name(name):
    """Convertit le nom en minuscules pour la normalisation."""
    return name.lower()

def capitalize_name(name):
    """Met en majuscule la première lettre de chaque mot dans le nom."""
    return ' '.join(word.capitalize() for word in name.split())

@bot.event
async def on_ready():
    print(f'{bot.user} a démarré avec succès !')

@bot.slash_command(description="Ajouter un film, une série, un manga ou un anime")
async def add(
    interaction: nextcord.Interaction,
    type: str = SlashOption(name="type",choices={"film": "film", "série": "série", "manga": "manga", "anime": "anime"},description="Le type de média"),
    nom: str = SlashOption(name="nom",description="Le nom du film, de la série, du manga ou de l'anime"),
    statut: str = SlashOption(name="statut",choices={"terminé": "terminé", "en cours": "en cours", "prévu": "prévu"},description="Statut de visionnage"),
    saison: int = SlashOption(name="saison",required=False,description="Numéro de saison (si en cours)"),
    episode: int = SlashOption(name="épisode",required=False,description="Numéro d'épisode (si en cours)"),
    volume: int = SlashOption(name="volume",required=False,description="Numéro de volume (si en cours)"),
    chapitre: int = SlashOption(name="chapitre",required=False,description="Numéro de chapitre (si en cours)")
):
    user_id = interaction.user.id
    user_data = load_user_data(user_id)

    normalized_nom = normalize_name(nom)
    capitalized_nom = capitalize_name(nom)

    # Vérifie si le média est déjà dans la liste
    existing_media = [media for media in user_data[type + 's'] if normalize_name(media['nom']) == normalized_nom]
    if existing_media:
        await interaction.response.send_message("Ce média est déjà dans votre liste.", ephemeral=True)
        return

    media_entry = {
        'nom': capitalized_nom,
        'statut': statut,
        'saison': saison,
        'episode': episode,
        'volume': volume,
        'chapitre': chapitre
    }

    # Filtrer les valeurs None pour éviter d'afficher des champs non définis
    media_entry = {k: v for k, v in media_entry.items() if v is not None}

    user_data[type + 's'].append(media_entry)
    save_user_data(user_id, user_data)

    embed = nextcord.Embed(
        title=f"Ajouté : {capitalized_nom}",
        description=f"Type : {type}\nStatut : {statut}",
        color=get_color(type)
    )

    if statut == 'en cours':
        if 'saison' in media_entry:
            embed.add_field(name="Saison", value=media_entry['saison'], inline=False)
        if 'episode' in media_entry:
            embed.add_field(name="Épisode", value=media_entry['episode'], inline=False)
        if 'volume' in media_entry:
            embed.add_field(name="Volume", value=media_entry['volume'], inline=False)
        if 'chapitre' in media_entry:
            embed.add_field(name="Chapitre", value=media_entry['chapitre'], inline=False)

    await interaction.response.send_message(embed=embed)


@bot.slash_command(description="Modifier ou supprimer les informations sur un film, une série, un manga ou un anime")
async def edit(
    interaction: nextcord.Interaction,
    type: str = SlashOption(name="type", choices={"film": "film", "série": "série", "manga": "manga", "anime": "anime"}, description="Le type de média"),
    nom: str = SlashOption(name="nom", description="Le nom du film, de la série, du manga ou de l'anime"),
    action: str = SlashOption(name="action", choices={"éditer": "éditer", "supprimer": "supprimer"}, description="Action à effectuer"),
    statut: str = SlashOption(name="statut", choices={"terminé": "terminé", "en cours": "en cours", "prévu": "prévu"}, description="Statut de visionnage"),
    saison: int = SlashOption(name="saison", required=False, description="Numéro de la saison (si en cours)"),
    episode: int = SlashOption(name="épisode", required=False, description="Numéro de l'épisode (si en cours)"),
    volume: int = SlashOption(name="volume", required=False, description="Numéro du volume (si en cours)"),
    chapitre: int = SlashOption(name="chapitre", required=False, description="Numéro du chapitre (si en cours)")
):
    user_id = interaction.user.id
    user_data = load_user_data(user_id)

    normalized_nom = normalize_name(nom)
    capitalized_nom = capitalize_name(nom)

    media_list = user_data[type + 's']
    media_entry = next((media for media in media_list if normalize_name(media.get('nom')) == normalized_nom), None)

    if action == 'supprimer':
        if media_entry:
            media_list.remove(media_entry)
            save_user_data(user_id, user_data)
            await interaction.response.send_message(f"{capitalized_nom} a été supprimé de votre liste.", ephemeral=True)
        else:
            await interaction.response.send_message("Ce média n'est pas dans votre liste.", ephemeral=True)
        return

    if not media_entry:
        await interaction.response.send_message("Ce média n'est pas dans votre liste.", ephemeral=True)
        return

    # Mise à jour uniquement si la valeur est fournie (non None)
    if statut is not None:
        media_entry['statut'] = statut

    if statut == 'en cours':
        if saison is not None:
            media_entry['saison'] = saison
        if episode is not None:
            media_entry['episode'] = episode
        if volume is not None:
            media_entry['volume'] = volume
        if chapitre is not None:
            media_entry['chapitre'] = chapitre
    else:
        # Si le statut n'est pas "en cours", on enlève ces informations
        media_entry.pop('saison', None)
        media_entry.pop('episode', None)
        media_entry.pop('volume', None)
        media_entry.pop('chapitre', None)

    save_user_data(user_id, user_data)

    embed = nextcord.Embed(
        title=f"Modifié : {capitalized_nom}",
        description=f"Type : {type}",
        color=get_color(type)
    )

    # Afficher les champs mis à jour
    if 'statut' in media_entry and media_entry['statut'] is not None:
        embed.add_field(name="Statut", value=media_entry['statut'], inline=False)
    if 'saison' in media_entry and media_entry['saison'] is not None:
        embed.add_field(name="Saison", value=media_entry['saison'], inline=False)
    if 'episode' in media_entry and media_entry['episode'] is not None:
        embed.add_field(name="Épisode", value=media_entry['episode'], inline=False)
    if 'volume' in media_entry and media_entry['volume'] is not None:
        embed.add_field(name="Volume", value=media_entry['volume'], inline=False)
    if 'chapitre' in media_entry and media_entry['chapitre'] is not None:
        embed.add_field(name="Chapitre", value=media_entry['chapitre'], inline=False)

    await interaction.response.send_message(embed=embed)



@bot.slash_command(description="Voir la liste complète de vos films, séries, mangas et animes")
async def list(
    interaction: nextcord.Interaction,
    order: str = SlashOption(name="ordre", choices={"A ➜ Z": "asc", "Z ➜ A": "desc"}, description="Ordre d'affichage des médias")
):
    user_id = interaction.user.id
    user_data = load_user_data(user_id)

    if not any(user_data.values()):  # Vérifie s'il y a au moins un média
        await interaction.response.send_message("Votre liste est vide.", ephemeral=True)
        return

    embed = nextcord.Embed(
        title="Votre Liste",
        color=nextcord.Color.from_rgb(255, 255, 255)  # Couleur blanche
    )

    # Fonction pour formater les détails du média
    def format_media_details(media):
        details = []
        if media.get('saison') is not None:
            details.append(f"Saison : {media['saison']}")
        if media.get('episode') is not None:
            details.append(f"Épisode : {media['episode']}")
        if media.get('volume') is not None:
            details.append(f"Volume : {media['volume']}")
        if media.get('chapitre') is not None:
            details.append(f"Chapitre : {media['chapitre']}")
        # Joindre les détails s'ils existent
        return " - " + ", ".join(details) if details else ""

    # Déterminer l'ordre de tri
    reverse_order = order == "desc"

    # Fonction pour ajouter des champs sans dépasser la limite de 1024 caractères
    def add_embed_field(embed, category, statut, filtered_medias):
        # Séparer les médias si nécessaire
        chunk = ""
        for media in filtered_medias:
            media_text = f"- {media['nom']}{format_media_details(media)}\n"
            if len(chunk) + len(media_text) > 1024:  # Si ça dépasse la limite
                embed.add_field(name=f"{category.capitalize()} ({statut.capitalize()})", value=chunk, inline=False)
                chunk = media_text  # Commence un nouveau bloc
            else:
                chunk += media_text
        if chunk:  # Ajouter le dernier bloc restant
            embed.add_field(name=f"{category.capitalize()} ({statut.capitalize()})", value=chunk, inline=False)

    # Itérer à travers chaque type de média
    for category in ['films', 'séries', 'animes', 'mangas']:
        medias = user_data[category]
        if medias:
            for statut in ['en cours', 'terminé', 'prévu']:
                # Filtrer les médias par statut
                filtered_medias = [media for media in medias if media['statut'] == statut]

                # Trier les médias par nom
                filtered_medias.sort(key=lambda media: media['nom'], reverse=reverse_order)

                if filtered_medias:
                    add_embed_field(embed, category, statut, filtered_medias)

    await interaction.response.send_message(embed=embed)

@bot.slash_command(description="Voir les médias par type et statut")
async def filter(
    interaction: nextcord.Interaction,
    media_type: str = SlashOption(name="type_de_média",choices={"film": "film", "série": "série", "anime": "anime", "manga": "manga"},description="Type de média"),
    order: str = SlashOption(name="ordre",choices={"A ➜ Z": "asc", "Z ➜ A": "desc"},description="Ordre d'affichage des médias"),
    statut: str = SlashOption(name="statut",choices={"en cours": "en cours", "terminé": "terminé", "prévu": "prévu"},description="Statut du média",required=False)
):
    user_id = interaction.user.id
    user_data = load_user_data(user_id)

    # Vérifie que le type de média est valide
    if media_type not in ['film', 'série', 'anime', 'manga']:
        await interaction.response.send_message("Type de média invalide.", ephemeral=True)
        return

    # Initialise l'embed avec le titre correspondant au type de média
    embed = nextcord.Embed(
        title=f"{media_type.capitalize()}",
        color=get_color(media_type)  # Utilise la fonction get_color pour définir la couleur de l'embed
    )

    # Fonction pour formater les détails du média
    def format_media_details(media):
        details = []
        if media.get('saison') is not None:
            details.append(f"Saison : {media['saison']}")
        if media.get('episode') is not None:
            details.append(f"Épisode : {media['episode']}")
        if media.get('volume') is not None:
            details.append(f"Volume : {media['volume']}")
        if media.get('chapitre') is not None:
            details.append(f"Chapitre : {media['chapitre']}")
        # Joindre les détails s'ils existent
        return " - " + ", ".join(details) if details else ""

    # Détermine l'ordre de tri
    reverse_order = order == "desc"

    # Si aucun statut n'est spécifié, afficher tous les médias groupés par statut
    if statut is None:
        for current_statut in ['en cours', 'terminé', 'prévu']:
            medias = [media for media in user_data[f"{media_type}s"] if media['statut'] == current_statut]

            # Trier les médias par nom
            medias.sort(key=lambda media: media['nom'], reverse=reverse_order)

            if medias:
                field_value = "\n".join(
                    f"- {media['nom']} {format_media_details(media)}"
                    for media in medias
                )
                embed.add_field(name=current_statut.capitalize(), value=field_value, inline=False)
    else:
        # Filtrer les médias par type et statut
        medias = [media for media in user_data[f"{media_type}s"] if media['statut'] == statut]

        # Trier les médias par nom
        medias.sort(key=lambda media: media['nom'], reverse=reverse_order)

        if not medias:
            await interaction.response.send_message(f"Aucun {media_type} avec le statut '{statut}' dans votre liste.", ephemeral=True)
            return

        # Ajouter chaque média à l'embed
        field_value = "\n".join(
            f"- {media['nom']}{format_media_details(media)}"
            for media in medias
        )
        embed.add_field(name=statut.capitalize(), value=field_value, inline=False)

    await interaction.response.send_message(embed=embed)

@bot.slash_command(description="Rechercher un film, une série, un manga ou un anime dans votre liste")
async def search(
    interaction: nextcord.Interaction,
    recherche: str = SlashOption(name="recherche", description="Nom ou partie du nom du média à rechercher")
):
    user_id = interaction.user.id
    user_data = load_user_data(user_id)

    normalized_recherche = normalize_name(recherche)
    results = {
        'films': [],
        'séries': [],
        'mangas': [],
        'animes': []
    }

    # Recherche dans chaque catégorie
    for media_type in results.keys():
        results[media_type] = [
            media for media in user_data[media_type]
            if normalized_recherche in normalize_name(media['nom'])
        ]

    # Si aucun média n'est trouvé
    if all(len(result) == 0 for result in results.values()):
        await interaction.response.send_message(f"Aucun média trouvé correspondant à '{recherche}'.", ephemeral=True)
        return

    embed = nextcord.Embed(
        title=f"Résultats de la recherche pour : {recherche}",
        color=nextcord.Color.purple()
    )

    # Fonction pour formater les détails du média
    def format_media_details(media):
        details = []
        if media.get('saison') is not None:
            details.append(f"Saison : {media['saison']}")
        if media.get('episode') is not None:
            details.append(f"Épisode : {media['episode']}")
        if media.get('volume') is not None:
            details.append(f"Volume : {media['volume']}")
        if media.get('chapitre') is not None:
            details.append(f"Chapitre : {media['chapitre']}")
        return " - " + ", ".join(details) if details else ""

    # Ajoute les résultats à l'embed
    for media_type, media_list in results.items():
        if media_list:
            embed.add_field(
                name=media_type.capitalize(),
                value="\n".join(
                    f"- {media['nom']}{format_media_details(media)}" for media in media_list
                ),
                inline=False
            )

    await interaction.response.send_message(embed=embed)

@bot.slash_command(description="Exporter votre liste de films, séries, mangas et animes, triée par catégorie et statut")
async def export(interaction: nextcord.Interaction):
    user_id = interaction.user.id
    user_data = load_user_data(user_id)

    if not any(user_data.values()):  # Vérifie si la liste est vide
        await interaction.response.send_message("Votre liste est vide.", ephemeral=True)
        return

    # Générer le contenu du fichier
    file_content = "Votre liste de médias (triée par catégorie et statut) :\n\n"

    # Définir l'ordre des statuts pour le tri
    statut_order = {
        "en cours": 1,
        "terminé": 2,
        "prévu": 3,
    }

    # Fonction pour formater les détails des médias
    def format_media_details(media):
        details = []
        if media.get('saison') is not None:
            details.append(f"Saison : {media['saison']}")
        if media.get('episode') is not None:
            details.append(f"Épisode : {media['episode']}")
        if media.get('volume') is not None:
            details.append(f"Volume : {media['volume']}")
        if media.get('chapitre') is not None:
            details.append(f"Chapitre : {media['chapitre']}")
        return " - " + ", ".join(details) if details else ""

    # Fonction pour trier et afficher une catégorie
    def format_category(category_name, medias):
        category_content = f"{category_name.capitalize()} :\n"
        # Trier les médias par statut en utilisant l'ordre défini
        medias_sorted = sorted(medias, key=lambda media: statut_order.get(media['statut'], 99))
        for media in medias_sorted:
            details = format_media_details(media)
            category_content += f"- {media['nom']} (Statut : {media['statut']}){details}\n"
        return category_content + "\n"

    # Traiter chaque catégorie (films, séries, animes, mangas)
    for category in ['films', 'séries', 'animes', 'mangas']:
        medias = user_data.get(category, [])
        if medias:
            file_content += format_category(category, medias)

    # Sauvegarder le fichier dans le répertoire temporaire avec l'encodage UTF-8
    file_name = f"{user_id}_media_list.txt"
    file_path = os.path.join(DATA_DIR, file_name)

    with open(file_path, "w", encoding="utf-8") as file:  # Utilisation de l'encodage UTF-8
        file.write(file_content)

    # Envoyer le fichier à l'utilisateur
    file = nextcord.File(file_path, filename=file_name)
    await interaction.response.send_message("Voici votre liste de médias triée :", file=file)

    # Supprimer le fichier après l'envoi pour éviter d'encombrer le répertoire
    os.remove(file_path)

@bot.slash_command(description="Demander des explications en cas de doute ou de difficulté")
async def explanations(interaction: nextcord.Interaction):
    embed = nextcord.Embed(
        title="Explications du Bot",
        description="Voici une brève description des fonctionnalités du bot :",
        color=nextcord.Color.blue()
    )
    embed.add_field(
        name="/add",
        value="Permet d'ajouter un film, une série, un manga ou un anime à votre liste, avec son statut de visionnage et éventuellement la saison, l'épisode, le volume ou le chapitre en cours.",
        inline=False
    )
    embed.add_field(
        name="/edit",
        value="Permet de modifier le statut de visionnage ou de supprimer un film, une série, un manga ou un anime de votre liste.",
        inline=False
    )
    embed.add_field(
        name="/list",
        value="Permet de voir la liste complète de vos films, séries, mangas et animes par ordre alphabétique.",
        inline=False
    )
    embed.add_field(
        name="/filter",
        value="Permet de filtrer votre liste de médias par type et statut.",
        inline=False
    )
    embed.add_field(
        name="/search",
        value="Permet de rechercher un film, une série, un manga ou un anime dans votre liste en fonction du nom ou d'une partie du nom. Retourne tous les résultats correspondants.",
        inline=False
    )
    embed.add_field(
        name="/explanations",
        value="Affiche ce message d'explication avec toutes les commandes et leurs descriptions.",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)


bot.run(TOKEN)  # Remplacez par le token de votre bot
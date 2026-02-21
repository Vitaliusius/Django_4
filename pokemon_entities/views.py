import folium
import django

from .models import Pokemon
from .models import PokemonEntity
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime
from django.urls import reverse


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    now = localtime()
    url = request.build_absolute_uri('/media/')
    active_pokemon = PokemonEntity.objects.filter(disappeared_at__gt = now)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in active_pokemon:
        add_pokemon(
            folium_map,
            pokemon.lat,
            pokemon.lon,
            f'{url}{pokemon.pokemon.photo}'
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': f'{url}{pokemon.photo}',
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    url = request.build_absolute_uri('/media/')
    requested_pokemon = get_object_or_404(Pokemon, id = pokemon_id)
    pokemon_entity = requested_pokemon.pokemon_entity.all()
    next_pokemons = requested_pokemon.next_evolutions.all()
    if next_pokemons.exists():
        if len(next_pokemons) == 1:
            next_pokemon = next_pokemons[0]
            next_pokemon_description = {
                "title_ru": next_pokemon.title,
                "pokemon_id": next_pokemon.id,
                "img_url":f'{url}{next_pokemon.photo}'
            }
        else:
            next_pokemon = next_pokemons[1]
            next_pokemon_description = {
                "title_ru": next_pokemon.title,
                "pokemon_id": next_pokemon.id,
                "img_url":f'{url}{next_pokemon.photo}'
            }
    else:
        next_pokemon_description = {}
    previous_pokemon = requested_pokemon.previous_evolution
    previous_pokemon_description = {
        "title_ru": previous_pokemon.title,
        "pokemon_id": previous_pokemon.id,
        "img_url":f'{url}{previous_pokemon.photo}'
    }
    pokemon_description = {
        "pokemon_id": pokemon_id,
        "title_ru": requested_pokemon.title,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "description": requested_pokemon.description,
        "img_url": f'{url}{requested_pokemon.photo}',
        'previous_evolution': previous_pokemon_description,
        'next_evolution': next_pokemon_description
    }
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemon_entity:
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            f'{url}{pokemon.pokemon.photo}'
            )
    
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_description,
    })
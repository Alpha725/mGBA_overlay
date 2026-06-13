import time
import sys 
import signal

from emulator_utils.client import mGBAclient

import gen2_utils.memory_extractor as extractor
import gen2_utils.html_builders as builder
import gen2_utils.rom_extractor as rom_extractor

import utils.file_utils as file_utils
import flask_utils.overlay_server as overlay_server

active_client = None

def graceful_shutdown_handler(sig, frame):
    global active_client
    print("\n[Client] Ctrl+C intercepted! Initiating clean disconnect sequence...")
    if active_client:
        try:
            active_client.close()  # Sends \x03 and safely exits Lua server tick loop
        except Exception as e:
            print(f"Error during explicit socket closure: {e}")
    print("[Client] Disconnect complete. Exiting program.")
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_shutdown_handler)
        
web_server = overlay_server.OverlayServer(debug=False)
MAPS = file_utils.load_json_to_dict('./data/maps.json')
POKEMON = file_utils.load_json_to_dict('./data/pokemon_data.json')
MOVES = file_utils.load_json_to_dict('./data/moves_data.json')
BADGES = file_utils.load_csv_to_dict('./data/badges.csv')
ITEMS = file_utils.load_csv_to_dict('./data/items.csv')

def update_overlay(eid, content):
    web_server.socketio.emit('update_data', {'id': eid, 'content': content})

def update_overlay_badge(badge_data):
    update_overlay("badge-space", builder.create_badge_table(badge_data, BADGES))

def update_overlay_player(player_data):
    if not player_data:
        update_overlay("player-info", "ID: - Money: -")
        return
    info_str = f"ID: {player_data['id']} Money: {player_data['money']}"
    update_overlay("player-info", info_str)

def update_overlay_party(party_data):
    if not party_data:
        update_overlay('party-poke-sprites', "-")
        return
    img_attr = "decoding='async' loading='lazy' width='60' height='60' referrerpolicy='no-referrer'"
    party_html_strings = []
    for member in party_data:
        sprite = POKEMON.get(member['species'], {}).get('party_sprite', '')
        if sprite:
            party_html_strings.append(f"<img alt='' src='{sprite}' {img_attr}>")
    if party_html_strings:
        update_overlay("party-poke-sprites", "".join(party_html_strings))
    else:
        update_overlay("party-poke-sprites", "-")

def update_overlay_lead(lead_data):
    if not lead_data:
        for suffix in ["poke-sprite", "lvl-happiness", "held-item", "moves", "stats", "dvs"]:
            update_overlay(f"lead-{suffix}", "-")
        return
    sprite = POKEMON.get(lead_data['species'], {}).get('sprite', '')
    if sprite:
        img_attr = "decoding='async' loading='lazy' width='120' height='120' referrerpolicy='no-referrer'"
        update_overlay("lead-poke-sprite", f"<img alt='' src='{sprite}' {img_attr}>")
    else:
        update_overlay("lead-poke-sprite", "-")
    update_overlay("lead-lvl-happiness", f"Level: {lead_data['level']} Happiness: {lead_data['happiness']}")
    update_overlay("lead-held-item", f"Held item: {ITEMS.get(lead_data['item'], 'None')}")
    update_overlay("lead-moves", builder.create_move_table(lead_data['moves'], lead_data['moves_pp'], MOVES))
    update_overlay("lead-dvs", builder.create_dv_table(lead_data['dvs']))
    update_overlay("lead-stats", builder.create_stats_table(lead_data['stats']))

def update_overlay_wild_enemy(enemy_data):
    if not enemy_data:
        for suffix in ["pokemon-sprite", "level", "held-item", "moves", "stats", "dvs-or-team"]:
            update_overlay(f"enemy-{suffix}", "-")
        return
    sprite = POKEMON.get(enemy_data['species'], {}).get('sprite', '')
    if sprite:
        img_attr = "decoding='async' loading='lazy' width='120' height='120' referrerpolicy='no-referrer'"
        update_overlay("enemy-pokemon-sprite", f"<img alt='' src='{sprite}' {img_attr}>")
    else:
        update_overlay("enemy-pokemon-sprite", "-")
    update_overlay("enemy-level", f"Level: {enemy_data['level']}")
    update_overlay("enemy-held-item", f"Held item: {ITEMS.get(enemy_data['item'], 'None')}")
    update_overlay("enemy-moves", builder.create_move_table(enemy_data['moves'], enemy_data['moves_pp'], MOVES))
    update_overlay("enemy-stats", builder.create_stats_table(enemy_data['stats']))
    update_overlay("enemy-dvs-or-team", builder.create_dv_table(enemy_data['dvs']))

def update_overlay_map_overworld(map_data):
    update_overlay("enemy-pokemon-sprite", "-")
    update_overlay("enemy-moves", "-")
    update_overlay("enemy-stats", "-")
    update_overlay("enemy-dvs-or-team", "-")
    if map_data:
        update_overlay("enemy-level", f"Region: {map_data['group']}")
        update_overlay("enemy-held-item", f"Area: {map_data['route']}")
    else:
        update_overlay("enemy-level", "-")
        update_overlay("enemy-held-item", "-")

def update_overlay_enemy(enemy_data, enemy_party_data):
    if not enemy_data:
        for suffix in ["pokemon-sprite", "level", "held-item", "moves", "stats", "dvs-or-team"]:
            update_overlay(f"enemy-{suffix}", "-")
        return
    sprite = POKEMON.get(enemy_data['species'], {}).get('sprite', '')
    if sprite:
        img_attr = "decoding='async' loading='lazy' width='120' height='120' referrerpolicy='no-referrer'"
        update_overlay("enemy-pokemon-sprite", f"<img alt='' src='{sprite}' {img_attr}>")
    else:
        update_overlay("enemy-pokemon-sprite", "-")
    update_overlay("enemy-level", f"Level: {enemy_data['level']}")
    update_overlay("enemy-held-item", f"Held item: {ITEMS.get(enemy_data['item'], 'None')}")
    update_overlay("enemy-moves", builder.create_move_table(enemy_data['moves'], enemy_data['moves_pp'], MOVES))
    update_overlay("enemy-stats", builder.create_stats_table(enemy_data['stats']))
    if not enemy_party_data:
        update_overlay("enemy-dvs-or-team", "-")
        return
    party_img_attr = "decoding='async' loading='lazy' width='60' height='60' referrerpolicy='no-referrer'"
    enemy_html_strings = []
    for member in enemy_party_data:
        party_sprite = POKEMON.get(member['species'], {}).get('party_sprite', '')
        if party_sprite:
            enemy_html_strings.append(f"<img alt='' src='{party_sprite}' {party_img_attr}>")
    if enemy_html_strings:
        update_overlay("enemy-dvs-or-team", "".join(enemy_html_strings))
    else:
        update_overlay("enemy-dvs-or-team", "-")

def update_overlay_encounter_table(encounter_data):
    if not encounter_data or encounter_data["rate"] == 0:
        update_overlay("enemy-dvs-or-team", "-")
        return
    table_html = builder.create_encounter_table(encounter_data, POKEMON)
    update_overlay("enemy-dvs-or-team", table_html)

def overworld_update(client):
    update_overlay_badge(extractor.get_badge_data(client))
    update_overlay_lead(extractor.get_overworld_lead_data(client))
    update_overlay_party(extractor.get_party_data(client))
    update_overlay_player(extractor.get_player_data(client))
    update_overlay_map_overworld(extractor.get_map_data(client, MAPS))
    # update_overlay_encounter_table(rom_extractor.get_live_grass_encounter_table(client))

def wild_battle_update(client):
    update_overlay_lead(extractor.get_battle_lead_data(client))
    update_overlay_wild_enemy(extractor.get_wild_enemy_data(client))

def trainer_battle_update(client):
    update_overlay_lead(extractor.get_battle_lead_data(client))
    update_overlay_enemy(extractor.get_wild_enemy_data(client), extractor.get_enemy_party_data(client))

def update_loop():
    global active_client
    try:
        active_client = mGBAclient()
        old_state = 10
        while True:
            state_data = active_client.read_memory(0x1108, 1)
            if not state_data:
                print("Lost connection to emulator server.")
                break
            state = state_data[0]
            match state:
                case 0: 
                    if state != old_state:
                        print("overworld_update")
                    overworld_update(active_client)
                case 1: 
                    if state != old_state:
                        print("wild_battle_update")
                    wild_battle_update(active_client)
                case 2: 
                    if state != old_state:
                        print("trainer_battle_update")
                    trainer_battle_update(active_client)
                case _: 
                    print(f"Game state: {state}. No update defined")
            old_state = state 
            time.sleep(1)
    except (ConnectionError, BrokenPipeError):
        print("\n[Client] Connection dropped by the emulator.")

if __name__ == "__main__":
    web_server.start_background_task(update_loop)
    web_server.run()


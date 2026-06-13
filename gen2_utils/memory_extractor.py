def get_overworld_lead_data(client):
    data = client.read_memory(0x19F0, 48)
    if not data or data[0] == 0x00:
        return None
    dv_b1, dv_b2 = data[21], data[22]
    dv_atk = (dv_b1 >> 4) & 0x0F
    dv_def = dv_b1 & 0x0F
    dv_spd = (dv_b2 >> 4) & 0x0F
    dv_spc = dv_b2 & 0x0F
    dv_hp = ((dv_atk & 1) << 3) | ((dv_def & 1) << 2) | ((dv_spd & 1) << 1) | (dv_spc & 1)
    stats_bytes = data[34:48]
    return {
        "species": f"{data[0]:02X}",
        "item": f"{data[1]:02X}",
        "level": data[31],       
        "happiness": data[27],  
        "moves": [f"{data[2 + i]:02X}" for i in range(4)],
        "moves_pp": [data[23 + i] for i in range(4)],
        "dvs": {'hp': dv_hp, 'atk': dv_atk, 'def': dv_def, 'spc': dv_spc, 'spd': dv_spd},
        "stats": {
            "pokemon_current_hp": int.from_bytes(stats_bytes[0:2], 'big'),
            "pokemon_total_hp": int.from_bytes(stats_bytes[2:4], 'big'),
            "pokemon_atk": int.from_bytes(stats_bytes[4:6], 'big'),
            "pokemon_def": int.from_bytes(stats_bytes[6:8], 'big'),
            "pokemon_spd": int.from_bytes(stats_bytes[8:10], 'big'),
            "pokemon_spatk": int.from_bytes(stats_bytes[10:12], 'big'),
            "pokemon_spdef": int.from_bytes(stats_bytes[12:14], 'big'),
        }
    }

def get_battle_lead_data(client):
    data = client.read_memory(0xB02, 30)
    if not data or data[0] == 0x00:
        return None
    dv_b1, dv_b2 = data[6], data[7]
    dv_atk = (dv_b1 >> 4) & 0x0F
    dv_def = dv_b1 & 0x0F
    dv_spd = (dv_b2 >> 4) & 0x0F
    dv_spc = dv_b2 & 0x0F
    dv_hp = ((dv_atk & 1) << 3) | ((dv_def & 1) << 2) | ((dv_spd & 1) << 1) | (dv_spc & 1)
    stats_bytes = data[16:30]
    return {
        "species": f"{data[0]:02X}",
        "item": f"{data[1]:02X}",
        "level": data[13],       
        "happiness": data[12],  
        "moves": [f"{data[2 + i]:02X}" for i in range(4)],
        "moves_pp": [data[8 + i] for i in range(4)],
        "dvs": {'hp': dv_hp, 'atk': dv_atk, 'def': dv_def, 'spc': dv_spc, 'spd': dv_spd},
        "stats": {
            "pokemon_current_hp": int.from_bytes(stats_bytes[0:2], 'big'),
            "pokemon_total_hp": int.from_bytes(stats_bytes[2:4], 'big'),
            "pokemon_atk": int.from_bytes(stats_bytes[4:6], 'big'),
            "pokemon_def": int.from_bytes(stats_bytes[6:8], 'big'),
            "pokemon_spd": int.from_bytes(stats_bytes[8:10], 'big'),
            "pokemon_spatk": int.from_bytes(stats_bytes[10:12], 'big'),
            "pokemon_spdef": int.from_bytes(stats_bytes[12:14], 'big'),
        }
    }

def get_player_data(client):
    id_bytes = client.read_memory(0x11B3, 2)
    fin_bytes = client.read_memory(0x1566, 9)
    if not id_bytes or not fin_bytes:
        return None
    trainer_id = int.from_bytes(id_bytes, 'big')
    player_money = int.from_bytes(fin_bytes[0:3], 'big')
    mom_money = int.from_bytes(fin_bytes[3:6], 'big')
    coins = int.from_bytes(fin_bytes[7:9], 'big') 
    return {
        "id": trainer_id,
        "money": player_money,
        "mom_money": mom_money,
        "coins": coins
    }

def get_wild_enemy_data(client):
    data = client.read_memory(0x10DF, 32)
    if not data or data[0] == 0x00:
        return None
    dv_b1, dv_b2 = data[8], data[9]
    dv_atk = (dv_b1 >> 4) & 0x0F
    dv_def = dv_b1 & 0x0F
    dv_spd = (dv_b2 >> 4) & 0x0F
    dv_spc = dv_b2 & 0x0F
    dv_hp = ((dv_atk & 1) << 3) | ((dv_def & 1) << 2) | ((dv_spd & 1) << 1) | (dv_spc & 1)
    stats_bytes = data[18:32]
    return {
        "species": f"{data[0]:02X}",
        "item": f"{data[3]:02X}",      
        "level": data[15],            
        "status": data[16],          
        "moves": [f"{data[4 + i]:02X}" for i in range(4)],
        "moves_pp": [data[10 + i] for i in range(4)],
        "dvs": {'hp': dv_hp, 'atk': dv_atk, 'def': dv_def, 'spc': dv_spc, 'spd': dv_spd},
        "stats": {
            "pokemon_current_hp": int.from_bytes(stats_bytes[0:2], 'big'),
            "pokemon_total_hp": int.from_bytes(stats_bytes[2:4], 'big'),
            "pokemon_atk": int.from_bytes(stats_bytes[4:6], 'big'),
            "pokemon_def": int.from_bytes(stats_bytes[6:8], 'big'),
            "pokemon_spd": int.from_bytes(stats_bytes[8:10], 'big'),
            "pokemon_spatk": int.from_bytes(stats_bytes[10:12], 'big'),
            "pokemon_spdef": int.from_bytes(stats_bytes[12:14], 'big'),
        }
    }

def get_party_data(client):
    party_meta = client.read_memory(0x19E8, 7)
    if not party_meta:
        return []
    party_count = party_meta[0]
    if party_count == 0 or party_count > 6:
        return []
    party_members = []
    for i in range(party_count):
        species_byte = party_meta[1 + i]
        species_hex = f"{species_byte:02X}"
        if species_hex == "00":
            continue
        party_members.append({
            "species": species_hex
        })
    return party_members

def get_map_data(client, MAPS):
    map_bytes = client.read_memory(0x19C6, 2)
    if not map_bytes or map_bytes[0] == 0x00:
        return {"group": "Unknown", "route": "Unknown"}
    group_hex = f"{map_bytes[0]:02X}"
    id_hex = f"{map_bytes[1]:02X}"
    group_data = MAPS.get(group_hex, {})
    group_name = group_data.get('name', f"Group {group_hex}")
    route_name = group_data.get('maps', {}).get(id_hex, f"Area {id_hex}")
    return {
        "group": group_name,
        "route": route_name
    }

def get_enemy_party_data(client):
    party_meta = client.read_memory(0x1CC6, 7)
    if not party_meta:
        return []
    party_count = party_meta[0]
    if party_count == 0 or party_count > 6:
        return []
    enemy_party = []
    for i in range(party_count):
        species_hex = f"{party_meta[1 + i]:02X}"
        if species_hex == "00":
            continue
        enemy_party.append({"species": species_hex})
    return enemy_party

def get_badge_data(client):
    badge_data = client.read_memory(0x156F, 2)
    if not badge_data or len(badge_data) < 2:
        return {"johto": [], "kanto": []}
    johto_byte, kanto_byte = badge_data[0], badge_data[1]
    johto_names = ["Zephyr", "Hive", "Plain", "Fog", "Mineral", "Storm", "Glacier", "Rising"]
    kanto_names = ["Boulder", "Cascade", "Thunder", "Rainbow", "Soul", "Marsh", "Volcano", "Earth"]
    return {
        "johto": [johto_names[i] for i in range(8) if johto_byte & (1 << i)],
        "kanto": [kanto_names[i] for i in range(8) if kanto_byte & (1 << i)]
    }

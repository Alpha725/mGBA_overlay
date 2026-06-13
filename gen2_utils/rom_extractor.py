def get_pokemon_name_from_rom(client, species_byte):
    if species_byte == 0 or species_byte > 251:
        return None
    name_length = 5
    target_address = 0x1B0B74 + ((species_byte - 1) * name_length)
    return client.read_rom(target_address, name_length)

# gen2_utils/rom_extractor.py

def get_live_grass_encounter_table(client):
    # The true table start we just found
    table_start = 0x4342
    
    # Read the 47-byte block (Header + 21 levels + 21 species across 3 time blocks)
    # Actually, the block is 1 (rate) + 21 (levels) + 21 (species) = 43 bytes total
    raw = client.read_rom(0x0A, table_start, 43)
    
    def parse_block(offset):
        # Slice 14 bytes: 7 levels, then 7 species
        levels = raw[offset : offset + 7]
        species = raw[offset + 7 : offset + 14]
        return [{"level": levels[i], "species": f"{species[i]:02X}"} for i in range(7)]

    return {
        "rate": raw[0],
        "morning": parse_block(1),
        "day":     parse_block(15),
        "night":   parse_block(29)
    }

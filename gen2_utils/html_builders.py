def create_stats_table(stats):
    stat_str = f"""
    <table>
      <tr>
        <th></th>
        <th>HP:</th>
        <th>ATK:</th>
        <th>DEF:</th>
        <th>SPA:</th>
        <th>SPD:</th>
        <th>SPE:</th>
      <tr>
        <th>Stats:</th>
        <td>{stats['pokemon_current_hp']}/{stats['pokemon_total_hp']}</th>
        <td>{stats['pokemon_atk']}</th>
        <td>{stats['pokemon_def']}</th>
        <td>{stats['pokemon_spatk']}</th>
        <td>{stats['pokemon_spdef']}</th>
        <td>{stats['pokemon_spd']}</th>
      </tr>
   </table>
    """
    return stat_str

def create_dv_table(dvs):
    dv_str = f"""
    <table>
      <tr>
        <th></th>
        <th>HP:</th>
        <th>ATK:</th>
        <th>DEF:</th>
        <th>SPC:</th>
        <th>SPE:</th>
        <th>   </th>
        <th>   </th>
        <th>   </th>
      <tr>
        <th>DVs:</th>
        <td>{dvs['hp']}</th>
        <td>{dvs['atk']}</th>
        <td>{dvs['def']}</th>
        <td>{dvs['spc']}</th>
        <td>{dvs['spd']}</th>
        <td>   </td>
        <td>   </td>
        <td>   </td>
      </tr>
   </table>
    """
    return dv_str

def create_move_table(moves, moves_pp, MOVES):
    move_str = """
    <table>
      <tr>
        <th>Name</th>
        <th>Type</th>
        <th>Power</th>
        <th>Accuracy</th>
        <th>PP</th>
      </tr>
    """
    for move, pp in zip(moves, moves_pp):
        if move == "00":
            move_str += f"""
              <tr>
                <td>-</td>
                <td>-</td>
                <td>-</td>
                <td>-</td>
                <td>-</td>
              </tr>
            """
        else:
            move_details = MOVES[move] 
            move_str += f"""
              <tr>
                <td>{move_details['name']}</td>
                <td>{move_details['type']}</td>
                <td>{move_details['power']}</td>
                <td>{move_details['accuracy']}</td>
                <td>{pp}</td>
              </tr>
            """
    move_str += "</table>"
    return move_str

def create_badge_table(badge_data, badges_lookup):
    johto_badges = badge_data.get("johto", [])
    kanto_badges = badge_data.get("kanto", [])
    if not johto_badges:
        return "<table><tr>-</tr></table>"
    if kanto_badges:
        img_attr = "decoding='async' loading='lazy' width='25' height='24' referrerpolicy='no-referrer'"
    else:
        img_attr = "decoding='async' loading='lazy' width='50' height='49' referrerpolicy='no-referrer'"
    html_rows = []
    for badge_list in [johto_badges, kanto_badges]:
        if not badge_list: 
            continue
        row_tds = [f"<td><img src='{badges_lookup.get(b, 'Oops')}' {img_attr}></td>" for b in badge_list]
        for i in range(0, len(row_tds), 4):
            html_rows.append(f"<tr>{''.join(row_tds[i:i+4])}</tr>")
    return f"<table>{''.join(html_rows)}</table>"

def create_encounter_table(encounter_data, pokemon_lookup):
    image_attributes = "decoding='async' loading='lazy' width='32' height='32' referrerpolicy='no-referrer'"
    html_output = f"""
    <div class='encounter-container' style='display: flex; flex-direction: column; gap: 8px;'>
        <div class='encounter-rate' style='font-weight: bold;'>Wild Rate: {encounter_data['rate']}%</div>
        <table style='width: 100%; border-collapse: collapse; font-size: 12px;'>
            <tr>
                <th style='border-bottom: 1px solid #fff;'>Morning</th>
                <th style='border-bottom: 1px solid #fff;'>Day</th>
                <th style='border-bottom: 1px solid #fff;'>Night</th>
            </tr>
    """
    total_encounter_slots = 7
    for slot_index in range(total_encounter_slots):
        morning_pokemon = encounter_data['morning'][slot_index]
        day_pokemon     = encounter_data['day'][slot_index]
        night_pokemon   = encounter_data['night'][slot_index]
        morning_sprite_url = pokemon_lookup.get(morning_pokemon['species'], {}).get('party_sprite', '')
        day_sprite_url     = pokemon_lookup.get(day_pokemon['species'], {}).get('party_sprite', '')
        night_sprite_url   = pokemon_lookup.get(night_pokemon['species'], {}).get('party_sprite', '')
        morning_image_element = f"<img src='{morning_sprite_url}' {image_attributes}>" if morning_sprite_url else "-"
        day_image_element     = f"<img src='{day_sprite_url}' {image_attributes}>" if day_sprite_url else "-"
        night_image_element   = f"<img src='{night_sprite_url}' {image_attributes}>" if night_sprite_url else "-"
        html_output += f"""
            <tr>
                <td style='text-align: center; padding: 2px;'>
                    {morning_image_element}<br>Lv{morning_pokemon['level']}
                </td>
                <td style='text-align: center; padding: 2px;'>
                    {day_image_element}<br>Lv{day_pokemon['level']}
                </td>
                <td style='text-align: center; padding: 2px;'>
                    {night_image_element}<br>Lv{night_pokemon['level']}
                </td>
            </tr>
        """
    html_output += "</table></div>"
    return html_output

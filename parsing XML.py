import xml.etree.ElementTree as ET
import os
import re
from xml.dom import minidom

def swap_languages(mpd_path, output_path):
    # Register namespace to avoid issues when searching elements
    namespaces = {'': 'urn:mpeg:dash:schema:mpd:2011', 'cenc': 'urn:mpeg:cenc:2013'}
    ET.register_namespace('', 'urn:mpeg:dash:schema:mpd:2011')
    ET.register_namespace('cenc', 'urn:mpeg:cenc:2013')
    
    # Parse the XML file
    tree = ET.parse(mpd_path)
    root = tree.getroot()

    # Find all AdaptationSets
    adaptation_sets = root.findall('.//Period/AdaptationSet', namespaces)

    # Identify the Hindi and Bengali AdaptationSets and their indices
    hindi_set = None
    bengali_set = None
    hindi_index = -1
    bengali_index = -1

    for index, adaptation_set in enumerate(adaptation_sets):
        lang = adaptation_set.get('lang')
        if lang == 'hi':
            hindi_set = adaptation_set
            hindi_index = index
        elif lang == 'bn':
            bengali_set = adaptation_set
            bengali_index = index

    # Swap if both Hindi and Bengali AdaptationSets are found and Bengali appears before Hindi
    if hindi_set is not None and bengali_set is not None and bengali_index < hindi_index:
        # Swap AdaptationSets in the list
        adaptation_sets[hindi_index], adaptation_sets[bengali_index] = adaptation_sets[bengali_index], adaptation_sets[hindi_index]

        # Swap IDs and Representation IDs
        hindi_set_id = hindi_set.get('id')
        bengali_set_id = bengali_set.get('id')
        hindi_representation_id = hindi_set.find('Representation', namespaces).get('id')
        bengali_representation_id = bengali_set.find('Representation', namespaces).get('id')

        hindi_set.set('id', bengali_set_id)
        bengali_set.set('id', hindi_set_id)

        hindi_set.find('Representation', namespaces).set('id', bengali_representation_id)
        bengali_set.find('Representation', namespaces).set('id', hindi_representation_id)

        # Replace the Period's AdaptationSets with the updated list
        period = root.find('.//Period', namespaces)
        period[:] = adaptation_sets
        
        xml_string = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')
        xml_string = re.sub(r'\s+/>', '/>', xml_string)

        mpd_line = '<MPD xmlns="urn:mpeg:dash:schema:mpd:2011" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:mpeg:dash:schema:mpd:2011 DASH-MPD.xsd" xmlns:cenc="urn:mpeg:cenc:2013" profiles="urn:mpeg:dash:profile:isoff-live:2011" minBufferTime="PT2S" type="static" mediaPresentationDuration="PT1315.4000244140625S">'
        comment = '<!--Generated with https://github.com/google/shaka-packager version v2.4.2-c60e988-release-->\n'
        xml_output = '<?xml version="1.0" encoding="UTF-8"?>\n' + comment + mpd_line

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(xml_output)
            file.write(xml_string)

def process_files_in_directory(input_directory, output_directory):
    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.endswith('_orig.mpd'):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, filename)

            output_filename = filename.replace('_orig.mpd', '.mpd')
            output_path = os.path.join(output_directory, output_filename)

            # Process the file
            swap_languages(input_path, output_path)
            print(f"Processed {input_path} -> {output_path}")

# Example usage with input and output directories
input_directory = r'C:/Users/Dell/Downloads/ep18/ep18'
output_directory = r'C:/Users/Dell/Downloads/ep18/processed'

process_files_in_directory(input_directory, output_directory)

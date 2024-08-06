import xml.etree.ElementTree as ET
import os

def prioritize_hindi(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    namespace = {'mpd' : "urn:mpeg:dash:schema:mpd:2011"}

    for period in root.findall('mpd:Period', namespace):
        audio_adaptation_sets = []

        for ad_set in period.findall('mpd:AdaptationSet', namespace):
            content_Type = ad_set.get("contentType", "")

            if content_Type == 'audio':
                audio_adaptation_sets.append(ad_set)

        bengali_adp_set = None
        hindi_adp_set = None

        for ad_set in audio_adaptation_sets:
            lang = ad_set.get('lang', '')
            if lang == 'hi':
                hindi_adp_set = ad_set
            elif lang == 'bn':
                bengali_adp_set = ad_set

        if bengali_adp_set and hindi_adp_set:

            hindi_index = None
            bengali_index = None

            all_ad_set = period.findall('mpd:AdaptationSet', namespace)
            for idx, ad_set in enumerate(all_ad_set):
                if ad_set == hindi_adp_set:
                    hindi_index = idx
                elif ad_set == bengali_adp_set:
                    bengali_index = idx
            
            if hindi_index is not None and bengali_index is not None and bengali_index < hindi_index:
                
                hindi_id = hindi_adp_set.get('id')
                bengali_id = bengali_adp_set.get('id')
                
                period.remove(hindi_adp_set)
                period.remove(bengali_adp_set)

                hindi_adp_set.set('id', bengali_id)
                bengali_adp_set.set('id', hindi_id)

                period.insert(bengali_index, hindi_adp_set)
                period.insert(hindi_index, bengali_adp_set)
                print(f'Swapped Bengali and Hindi adaptation sets in file: {input_file}')
            else:
                print(f'Hindi set is already prioritized in file: {input_file}')
        else:
            print(f'Hindi or bengali set not found in file: {input_file}')

    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def process_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith('_orig.mpd'):
            input_file_path = os.path.join(input_directory, filename)
            output_file_path = os.path.join(output_directory, filename.replace('_orig', ""))

            if not os.path.isfile(input_file_path):
                print(f"Error: The input file'{input_file_path} does not exist.")
                continue

            prioritize_hindi(input_file_path, output_file_path)
            print(f"Processed: \n{os.path.basename(output_file_path)}")

if __name__ == '__main__':
    input_directory = r'C:/Users/Dell/Downloads/ep18/ep18'
    output_directory = r'C:/Users/Dell/Downloads/ep18/processed'

    process_directory(input_directory, output_directory)
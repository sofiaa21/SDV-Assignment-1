import pandas as pd

# 1. Load the cleaned data
print("--- Loading Cleaned Dataset ---")
df = pd.read_csv('data/clean-data/sf_clean_data.csv')

# 2. Define the Mapping (Lowercased keys for safety)
focus_group_map = {
    # --- Violent Crime ---
    'assault':                                          'Violent Crime',
    'robbery':                                          'Violent Crime',
    'kidnapping':                                       'Violent Crime',
    'homicide':                                         'Violent Crime',
    'extortion':                                        'Violent Crime',

    # --- Sex Offenses ---
    'sex offenses, forcible':                           'Sex Offenses',
    'sex offenses, non forcible':                       'Sex Offenses',
    'sex offense':                                      'Sex Offenses',
    'rape':                                             'Sex Offenses',
    'human trafficking (a), commercial sex acts':       'Sex Offenses',
    'human trafficking, commercial sex acts':           'Sex Offenses',
    'human trafficking (b), involuntary servitude':     'Sex Offenses',

    # --- Property Crime ---
    'vehicle theft':                                    'Property Crime',
    'larceny/theft':                                    'Property Crime',
    'larceny theft':                                    'Property Crime',
    'burglary':                                         'Property Crime',
    'arson':                                            'Property Crime',
    'vandalism':                                        'Property Crime',
    'malicious mischief':                               'Property Crime',
    'stolen property':                                  'Property Crime',
    'recovered vehicle':                                'Property Crime',
    'motor vehicle theft':                              'Property Crime',
    'motor vehicle theft?':                             'Property Crime',
    'vehicle misplaced':                                'Property Crime',
    'vehicle impounded':                                'Property Crime',
    'trespass':                                         'Property Crime',
    'bad checks':                                       'Property Crime',

    # --- Financial Crime ---
    'fraud':                                            'Financial Crime',
    'forgery/counterfeiting':                           'Financial Crime',
    'forgery and counterfeiting':                       'Financial Crime',
    'embezzlement':                                     'Financial Crime',
    'bribery':                                          'Financial Crime',

    # --- Drug & Alcohol ---
    'drug/narcotic':                                    'Drug & Alcohol',
    'drug offense':                                     'Drug & Alcohol',
    'drug violation':                                   'Drug & Alcohol',
    'driving under the influence':                      'Drug & Alcohol',
    'drunkenness':                                      'Drug & Alcohol',
    'liquor laws':                                      'Drug & Alcohol',

    # --- Weapons ---
    'weapon laws':                                      'Weapons',
    'weapons offense':                                  'Weapons',
    'weapons offence':                                  'Weapons',
    'weapons carrying etc':                             'Weapons',

    # --- Public Order & Quality of Life ---
    'disorderly conduct':                               'Public Order',
    'loitering':                                        'Public Order',
    'prostitution':                                     'Public Order',
    'gambling':                                         'Public Order',
    'pornography/obscene mat':                          'Public Order',
    'civil sidewalks':                                  'Public Order',
    'trea':                                             'Public Order',
    'offences against the family and children':         'Public Order',

    # --- Administrative / Legal ---
    'warrants':                                         'Administrative',
    'warrant':                                          'Administrative',
    'secondary codes':                                  'Administrative',
    'traffic violation arrest':                         'Administrative',
    'traffic collision':                                'Administrative',
    'case closure':                                     'Administrative',
    'courtesy report':                                  'Administrative',
    'fire report':                                      'Administrative',

    # --- Non-Criminal / Misc ---
    'non-criminal':                                     'Non-Criminal',
    'missing person':                                   'Non-Criminal',
    'lost property':                                    'Non-Criminal',
    'suicide':                                          'Non-Criminal',
    'recovered vehicle':                                'Non-Criminal',

    # --- Other/Catch-all ---
    'other offenses':                                   'Other/Suspicious',
    'other':                                            'Other/Suspicious',
    'other miscellaneous':                              'Other/Suspicious',
    'miscellaneous investigation':                      'Other/Suspicious',
    'suspicious occ':                                   'Other/Suspicious',
    'suspicious':                                       'Other/Suspicious',
}

# 3. Apply the mapping without overwriting the original column
print("Creating Focus Group column...")

# Create the new column by mapping a lowercase version of the original category
df['Focus Group'] = df['Incident Category'].str.lower().map(focus_group_map).fillna('Other/Suspicious')

# 4. Verification
print("\n--- Column Verification ---")
print(df[['Incident Category', 'Focus Group']])

# 5. Sanity Check
print("\n--- Sanity Check ---")
total_categories = df['Incident Category'].nunique()
mapped_categories = df[df['Focus Group'] != 'Other/Suspicious']['Incident Category'].nunique()
unmapped = df[df['Focus Group'] == 'Other/Suspicious']['Incident Category'].unique()

print(f"Total unique categories: {total_categories}")
print(f"Mapped categories: {mapped_categories}")
print(f"Unmapped (falling back to 'Other/Suspicious'): {len(unmapped)}")

if len(unmapped) > 0:
    print("\nUnmapped category names:")
    for cat in sorted(unmapped):
        print(f"  - '{cat}'  ->  other: '{str(cat).lower()}'")
else:
    print("\nAll categories successfully mapped!")

print("\n--- Focus Group Distribution ---")
print(df['Focus Group'].value_counts())


# 6. Export to the final visualization-ready file
output_path = 'data/clean-data/sf_clean_data_grouped.csv'
df.to_csv(output_path, index=False)
print(f"\nSaved! Total rows: {len(df)}")
print(f"File Location: {output_path}")
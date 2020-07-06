IN ORDER TO CHANGE CONFIG.JSON

PLACE VARIABLES:

place_id           - (REQUIRED) Up to 10-numerical digits only - XX
place_abbreviation - (REQUIRED) 3 alphabetical digits only
place_description  - (OPTIONAL) Add details about the place in order to remind which one it refers to.


SENSORS ARRAY:

[ 'ID DO SENSOR ENTRE SIMILARES (JANELAS, PERSIANAS, ETC)' , 'ABREVIAÇÃO DO TIPO' , 'TIPO' , 'DESCRIÇÃO DO SENSOR ESPECIFICO']

SAMPLES:

sensors = [ 
    ['01', 'JAN', 'JANELA', 'Janela do canto direito da sala'],  # JAN:XX:01:valor - Onde XX é o place_id
    ['02', 'JAN', 'JANELA', 'Janela do canto esquerdo da sala'], # JAN:XX:02:valor - Onde XX é o place_id
    ['01', 'LAM', 'LAMPADA', 'Lampada central do ambiente']      # LAM:XX:01:valor - Onde XX é o place_id
    ]



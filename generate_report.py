import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from mdutils.mdutils import MdUtils
from mdutils.tools import Html
import markdown2

df = pd.read_csv("out.csv")

def labelParse():
    labels = []
    for i in range(0,len(df['label'])):
        label_list = eval(df['label'][i])
        labels.append(label_list)
    return labels

def timestampParse():
    timestamp_list = []
    for i in range(0, len(df['timestamp'])):
        time = datetime.datetime.strptime(df['timestamp'][i], "Timestamp: %Y-%m-%d %H:%M:%S")
        timestamp_list.append(time.strftime("%H:%M:%S"))
    return timestamp_list

def predictionsPerSecond():
    labels = labelParse()
    timestamps = timestampParse()
    unique_timestamps = set(timestamps)

    clean_labels = []
    clean_timestamps = []
    for i in range(0, len(labels)):
        for j in range(0, len(labels[i])):
            clean_timestamps.append(timestamps[i])
            clean_labels.append(labels[i][j])

    df_clean = pd.DataFrame({'labels':clean_labels, 'timestamps': clean_timestamps})

    table = pd.crosstab(df_clean.labels, df_clean.timestamps)
    dictionary_masks = {0: 'Mascarillas correcta', 1: 'Mascarilla incorrecta', 2: 'Sin Mascarilla', 3: 'other'}
    columns = table.columns.to_list()
    prediction_list = []
    for i in range(0,len(columns)):

        array = np.array(table.iloc[:, i])[0:3]

        if array[1:].any() > 0:
            result = dictionary_masks.get(np.argmax(array[1:])+1)
            prediction_list.append(result)
        else:
            result = dictionary_masks.get(0)
            prediction_list.append(result)
        
        str_timestamp = columns[i]

    final_predictions_per_s = pd.DataFrame({'Label': prediction_list, 'Time': columns})

    return final_predictions_per_s
    

def generate_report():
    df_final = predictionsPerSecond()
    explode = (0.1, 0.1, 0.1)
    plt.pie(df_final.Label.value_counts(), explode=explode, labels= df_final.Label.value_counts().index.to_list(), autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title('Tiempo de uso de mascarilla')
    plt.savefig('predictions.png')
    mdFile = MdUtils(file_name = 'report', title = 'Reporte de predicción de uso correcto de mascarilla')
    mdFile.new_line(mdFile.new_inline_image(text = 'Predicciones',path = 'predictions.png'))
    mdFile.new_header(title = 'Tablas de resultados', level = 1)
    mdFile.new_line('Juan Pablo Carranza Hurtado')
    mdFile.new_line('José Alberto Ligorría Taracena')
    mdFile.create_md_file()
    f = open("report.html", "w")
    f.write(markdown2.markdown_path('report.md'))
    f.write(pd.crosstab(df_final.Time, df_final.Label).to_html())
    f.write('<h1> Cantidad de segundos de utilización de mascarilla </h1>')
    f.write(pd.DataFrame(df_final.Label.value_counts()).to_html())
    f.close()
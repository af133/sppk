from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

bobot_divisi = {
    "Litbang": {
        "Kemampuan Analisis Masalah": 0.49,
        "Kreativitas & Inovasi": 0.24,
        "Pengetahuan Teknis": 0.10,
        "Kerjasama Tim": 0.06,
        "Wawancara / Motivasi": 0.1
    },
    "Mediatek": {
        "Kemampuan Desain & Kreativitas Visual": 0.54,
        "Kemampuan Teknis Media": 0.24,
        "Kemampuan Komunikasi": 0.13,
        "Wawancara / Motivasi": 0.07
    },
    "Penerbitan": {
        "Kemampuan Menulis & Tata Bahasa": 0.45,
        "Kemampuan Analisis Isi / Logika Tulisan": 0.19,
        "Kreativitas Ide Tulisan": 0.09,
        "Kemampuan Komunikasi & Penyuntingan": 0.19,
        "Wawancara / Motivasi": 0.06
    }
}

def topsis(data, weights):
    data = data.copy()
    X = data.iloc[:, 1:].values.astype(float)
    norm = X / np.sqrt((X**2).sum(axis=0))
    weighted = norm * np.array(list(weights.values()))
    ideal_pos = weighted.max(axis=0)
    ideal_neg = weighted.min(axis=0)
    d_pos = np.sqrt(((weighted - ideal_pos)**2).sum(axis=1))
    d_neg = np.sqrt(((weighted - ideal_neg)**2).sum(axis=1))
    score = d_neg / (d_pos + d_neg)
    data['Skor Akhir'] = score
    data['Ranking'] = data['Skor Akhir'].rank(ascending=False)
    return data.sort_values('Skor Akhir', ascending=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_csv(file)
            for divisi, weights in bobot_divisi.items():
                available_cols = [c for c in df.columns if c in weights.keys()]
                if len(available_cols) == len(weights):
                    sub_df = df[['Nama'] + available_cols]
                    hasil = topsis(sub_df, weights)
                    results[divisi] = hasil[['Nama', 'Skor Akhir', 'Ranking']].to_html(index=False, classes='table table-striped')
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

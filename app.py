from flask import Flask, render_template
import cryptoquant

app = Flask(__name__)
@app.route('/')
def index():
    puell_multiple_data = cryptoquant.get_puell_multiple_data()
    mvrv_data = cryptoquant.get_mvrv_data()
    nupl_data = cryptoquant.get_nupl_data()

    recommendation = cryptoquant.get_recommendation(
        puell_multiple_data['current_value'],
        mvrv_data['current_value'],
        nupl_data['current_value']
    )

    return render_template('index.html', recommendation=recommendation, puell_multiple_data=puell_multiple_data, mvrv_data=mvrv_data, nupl_data=nupl_data)


if __name__ == '__main__':
    app.run(debug=True)

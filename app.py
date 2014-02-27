from flask import Flask, render_template, request
import markov

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=["POST"])
def submit_text():
    corpus = request.form.get("corpus")
    n_gram_size = int(request.form.get("n_gram"))
    wordcount = int(request.form.get("wordcount"))
    output = markov.generate_text(corpus, n_gram_size, wordcount)
    return render_template('index.html', corpus=corpus, n_gram=n_gram_size, wordcount=wordcount, output=output)

if __name__ == "__main__":
    app.run(debug = True)
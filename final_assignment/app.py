'''
Rachael Savage
CSC285-Python II
Professor Tony Hinton
10/07/23
'''
'''-----------------------------------IMPORT NECCESARY LIBS-----------------------------------------------------------'''
import os # work with the file system
#web framework and its func & classs
from flask import Flask, render_template, request, redirect, url_for, Response
from textblob import TextBlob #processing text data to perform sentiment analysis
import pandas as pd #Used for data manipulation and analysis
import matplotlib.pyplot as plt #for creating visualizations graph
import io # input and output streams
import re #for text pattern matching

'''------------------------------------FUNC TO PREPROCESS TEXT FROM UPLOADED FILES---------------------------------------'''
# func to preprocess the uploaded text data by removing lines that start with numbers.
def preprocess_text(text):
    # Remove lines starting with numbers
    lines = text.split('\n')
    filtered_lines = [line for line in lines if not re.match(r'^\d', line.strip())]
    return '\n'.join(filtered_lines)

'''-------------------------------------SET UP FLASK APP------------------------------------------------------------------'''
#Create a Flask web app instance 
app = Flask(__name__)
# define a folder
UPLOAD_FOLDER = 'data'  # Folder to store uploaded  files
ALLOWED_EXTENSIONS = {'txt', 'csv'}  # Allowed file extensions
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

'''-----------------------------------FILE UPLOAD HANDLING----------------------------------------------------------------'''
def allowed_file(filename):#checks if a given filename has an allowed file extension
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''-------------------------------------INDEX PAGE (rendering and displaying the main page)----------------------------------'''
@app.route('/')
def index():
    return render_template('index.html')

'''------------------------------------HANDLE UPLOAD FILE--------------------------------------------------------------------'''
@app.route('/upload', methods=['POST']) #handles POST requests for file uploads
def upload_file():
    error = None
    if 'file' not in request.files:
        error = "No file part"
        return render_template('index.html', error=error)

    file = request.files['file']

    if file.filename == '':
        error = "No selected file"
        return render_template('index.html', error=error)

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Get the file extension and remember it
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        return redirect(url_for('analyze', filename=filename, ext=file_extension))
    
    error = "Invalid file type"
    return render_template('index.html', error=error)

'''-----------------------------------------SENTIMENT ANALYSIS & VISUALIZATION ------------------------------------------------------'''
@app.route('/analyze/<filename>/<ext>')
def analyze(filename, ext):
    global df
    try:
        # Using the allowed extension ext
        if ext == 'csv':
            df = pd.read_csv(filename)
        elif ext == 'txt':
            with open(filename, 'r') as file:
                lines = file.readlines()
             # Join the lines to create a single string and preprocess the texts
            texts = preprocess_text(''.join(lines))
            df = pd.DataFrame(texts.split('\n'), columns=['Text'])
        else:
            raise ValueError("Invalid file type. Only CSV and TXT are supported.")

        if 'Text' not in df.columns:
            raise ValueError("The uploaded file does not have a 'Text' column.")

        df['Sentiment'] = df['Text'].apply(sentiment_analysis)
        
        # Calculate sentiment percentages
        total = len(df)
        sentiment_counts = df['Sentiment'].value_counts()
        sentiment_percentages = (sentiment_counts / total) * 100
        
        # Setting default values for sentiments
        default_sentiments = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
        for sentiment in default_sentiments.keys():
            if sentiment in sentiment_percentages:
                default_sentiments[sentiment] = sentiment_percentages[sentiment]
                
        # Create the bar chart
        plt.figure(figsize=(8, 6))
        print(sentiment_counts)
        print(sentiment_percentages)
        print(default_sentiments)

        colors = ['green', 'blue', 'red']
        ax = sentiment_counts.plot(kind='bar', color=colors, edgecolor='black')
        plt.xlabel('Sentiment', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.title('Sentiment Analysis Summary', fontsize=14)
        plt.xticks(rotation=45) #rotate x-label
        ax.grid(axis='y')#grid lines
        ax.set_facecolor('whitesmoke')#figure bg color
        
        # looping through the sentiment_counts to annotate the bar chart
        for i, (sentiment, percentage) in enumerate(default_sentiments.items()):
            count = sentiment_counts.get(sentiment, 0)  # Get the count, default to 0 if sentiment not present
            ax.text(i, count/2, f"{percentage:.2f}%", ha='center', va='top', fontsize=9, color='white')
    
        # constructs a file path for saving the generated bar chart as an image file
        chart_filename = os.path.join('static', 'sentiment_summary.png')
        plt.tight_layout()  # ensure the annotations fit in the saved image
        plt.savefig(chart_filename)
        # returns a response to the client (web browser) in the form of an HTML page generated from the index.html template
        return render_template('index.html', filename=filename, chart_filename=chart_filename, df=df, percentages=default_sentiments)

    except Exception as e:
        return render_template('index.html', error=str(e))

'''--------------------------------------HANDLE EXPORTING DATA------------------------------------------------------------------'''
@app.route('/export', methods=['GET'])
def export():
    global df #global var
    ext = request.args.get('ext') #retrieves the value of the 'ext
    #calculate sentiment-related statistics from the DataFrame
    sentiment_counts = df['Sentiment'].value_counts()
    total = len(df)
    sentiment_percentages = (sentiment_counts / total) * 100

    output = io.StringIO()
    #this code section exacute when user click export file
    if ext == 'csv':
        # Write sentiment percentages to the beginning of the csv
        output.write("Sentiment Percentages,\n")
        for sentiment, percentage in sentiment_percentages.items():
            output.write(f"{sentiment},{percentage:.2f}%\n")
        output.write("\nText,Sentiment\n")
        
        df.to_csv(output, mode='a', header=False, index=False)
        output.seek(0)
        return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=export.csv"})

    else:  
        # Write sentiment percentages to the beginning of the txt
        output.write("Sentiment Percentages:\n")
        for sentiment, percentage in sentiment_percentages.items():
            output.write(f"{sentiment}: {percentage:.2f}%\n")
        output.write("\n")

        for _, row in df.iterrows():
            output.write(str(row['Text']) + '\t' + str(row['Sentiment']) + '\n')

        output.seek(0)
        return Response(output, mimetype="text/txt", headers={"Content-Disposition": "attachment;filename=export.txt"})

'''----------------------------------------- SENTIMENT ANALYSIS FUNCTIONS-----------------------------------------------------------'''
def sentiment_analysis(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

'''----------------------------------------- RUN THE FASK APP-----------------------------------------------------------------------'''
if __name__ == '__main__':
    app.run(debug=True, port=5001) #specify a port

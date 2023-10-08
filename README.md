
# Sentiment Analyzer

## Overview
The Sentiment Analyzer is a web application that allows users to upload a text or CSV file and analyze the sentiment of the text data contained within. The analyzed sentiment is categorized as 'Positive', 'Neutral', or 'Negative'. A visualization summarizing the sentiment distribution is also generated. Users can export the analysis results as a CSV or text file.

Developed by:
**Rachael Savage**
CSC285-Python II
Professor Tony Hinton
10/07/23

## Features

- Web interface for easy file upload
- Supports both `.txt` and `.csv` file formats
- Real-time sentiment analysis using TextBlob
- Provides an interactive bar chart summarizing sentiment distribution
- Offers the ability to export analysis results

## Libraries

- Python
- Flask
- TextBlob
- Pandas
- Matplotlib

## Installation

1. Clone the repository or download the code.
2. Install the required libraries using the following command:
    ```bash
    pip install Flask TextBlob pandas matplotlib
    ```

3. Navigate to the root directory of the application and run the following command:
    ```bash
    python app.py
    ```

4. Open a web browser and go to `http://127.0.0.1:5001/` to access the application.

## How to Use

1. On the main page, click the "Choose File" button to select a `.txt` or `.csv` file containing the text data.
2. Click "Upload and Analyze".
3. View the sentiment analysis results, including the bar chart visualization.
4. If desired, export the results as a CSV or text file.

## Contributing

For contributions, please create a pull request. All contributions are welcome!


## Acknowledgements

Thanks to Professor Tony Hinton for guidance and the course CSC285-Python II.


# Customer Churn Prediction Web App

This project is a simple web application that predicts customer churn based on user input.

## How to Run

1.  **Unzip the folder.**

2.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Flask application:**
    ```bash
    python app.py
    ```

4.  **Open your web browser** and go to `http://127.0.0.1:5000` to use the application.

## Project Structure

-   `app.py`: The main Flask application file that serves the web pages and handles predictions.
-   `churn_model_pipeline.pkl`: The pre-trained machine learning model pipeline.
-   `templates/index.html`: The HTML template for the user interface.
-   `requirements.txt`: A list of Python libraries required for the project.
-   `Customer-Churn-Records.csv`: The original dataset used for training.
-   `Bank-Model-Training.ipynb`: The Jupyter Notebook with the original model training and exploration steps.

# FastAPI ML Application

This project is a FastAPI application that serves a machine learning model for text classification. The model is trained to classify descriptions based on the responsible entity ID.

## Project Structure

```
fastapi-ml-app
├── app
│   ├── main.py              # Entry point of the FastAPI application
│   ├── model
│   │   ├── model.pkl        # Trained machine learning model
│   │   └── vectorizer.pkl   # Vectorizer for transforming input text
│   └── api
│       └── endpoints.py     # API endpoints for handling requests
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fastapi-ml-app
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI application:
   ```
   uvicorn app.main:app --reload
   ```

2. Send a POST request to the `/predict` endpoint with the following JSON body:
   ```json
   {
       "state": "some_state",
       "description": "some_description"
   }
   ```

3. The response will contain the predicted class based on the input description.

## Example Request

```bash
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"state": "some_state", "description": "some_description"}'
```

## License

This project is licensed under the MIT License.
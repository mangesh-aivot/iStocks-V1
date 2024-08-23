cd backend\Predictions	

	uvicorn predictions:app --host 0.0.0.0 --port 8000 --reload


	uvicorn autoupdate:app --host 0.0.0.0 --port 8001 --reload

cd backend\

	npm start

cd frontend\

	npm run dev

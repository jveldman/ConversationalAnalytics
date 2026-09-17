cd pocca &&
dbt build --target dev &&
dbt compile &&
cd ../cube-core &&
docker-compose down &&
docker-compose up -d &&
./sync_cubes.sh &&
cd ../poc-chatbot &&
streamlit run app.py
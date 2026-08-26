const { DuckDBDriver } = require('@cubejs-backend/duckdb-driver');

module.exports = {
    // Set true in docker-compose. When published, it then runs in production mode. 
  devServer: process.env.DEVSERVER === 'true',
  driverFactory: () => new DuckDBDriver({
    database: process.env.CUBEJS_DB_DUCKDB_DATABASE_PATH,
  }),
  api: {
    graphql: true
  }
};
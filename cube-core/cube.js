const { DuckDBDriver } = require('@cubejs-backend/duckdb-driver');

module.exports = {
  devServer: process.env.DEVSERVER === 'true',
  driverFactory: () => new DuckDBDriver({
    database: process.env.CUBEJS_DB_DUCKDB_DATABASE_PATH,
  }),
};
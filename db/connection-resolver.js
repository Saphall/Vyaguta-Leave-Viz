require('dotenv').config({ path: '../.env' });
const { Client } = require('pg');

const dbConfig = {
  host: process.env.SERVER,
  port: process.env.DB_PORT,
  database: process.env.DATABASE,
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD
};

const getConnection = () => new Client(dbConfig);

const resolve = async () => [
  {
    client: 'postgres',
    connection: dbConfig
  }
];

module.exports = { getConnection, resolve };

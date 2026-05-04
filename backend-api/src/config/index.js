import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config({ path: path.resolve(__dirname, '../../.env') });

const config = {
  port: process.env.PORT ? Number(process.env.PORT) : 5000,
  env: process.env.NODE_ENV || 'development',
  mongoUri: process.env.MONGODB_URI || 'mongodb://localhost:27017/mental-health-api',
  jwtSecret: process.env.JWT_SECRET || 'please_change_this_secret',
  jwtExpiresIn: process.env.JWT_EXPIRES_IN || '1d',
  rateLimitWindow: process.env.RATE_LIMIT_WINDOW_MINUTES ? Number(process.env.RATE_LIMIT_WINDOW_MINUTES) : 15,
  rateLimitMaxRequests: process.env.RATE_LIMIT_MAX_REQUESTS ? Number(process.env.RATE_LIMIT_MAX_REQUESTS) : 100
};

export default config;

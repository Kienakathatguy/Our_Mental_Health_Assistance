import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import morgan from 'morgan';
import rateLimit from 'express-rate-limit';
import mongoSanitize from 'express-mongo-sanitize';
import xss from 'xss-clean';
import swaggerUi from 'swagger-ui-express';

import config from './config/index.js';
import connectDatabase from './config/db.js';
import routes from './routes/index.js';
import errorHandler from './middlewares/error.middleware.js';
import swaggerSpec from './docs/swagger.js';

const app = express();

connectDatabase();

app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(mongoSanitize());
app.use(xss());

if (config.env === 'development') {
  app.use(morgan('dev'));
}

const limiter = rateLimit({
  windowMs: config.rateLimitWindow * 60 * 1000,
  max: config.rateLimitMaxRequests,
  standardHeaders: true,
  legacyHeaders: false
});

app.use(limiter);

app.use('/api', routes);
app.use('/api/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

app.get('/', (req, res) => {
  res.status(200).json({
    status: 'success',
    message: 'Mental Health Assistance API is running'
  });
});

app.use(errorHandler);

export default app;

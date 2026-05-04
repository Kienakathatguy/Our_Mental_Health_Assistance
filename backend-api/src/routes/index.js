import express from 'express';
import authRoutes from './auth.routes.js';
import productRoutes from './product.routes.js';

const router = express.Router();

router.use('/auth', authRoutes);
router.use('/products', productRoutes);

export default router;

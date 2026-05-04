import express from 'express';
import {
  createProduct,
  getProducts,
  getProductById,
  updateProduct,
  deleteProduct,
  getNearbyProducts
} from '../controllers/product.controller.js';
import protect from '../middlewares/auth.middleware.js';
import validate from '../middlewares/validate.middleware.js';
import { productSchema, productUpdateSchema } from '../validators/product.validator.js';

const router = express.Router();

router.use(protect);

router.route('/')
  .get(getProducts)
  .post(validate(productSchema), createProduct);

router.route('/nearby').get(getNearbyProducts);

router.route('/:id')
  .get(getProductById)
  .patch(validate(productUpdateSchema), updateProduct)
  .delete(deleteProduct);

export default router;

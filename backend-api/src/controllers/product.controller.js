import Product from '../models/product.model.js';
import APIFeatures from '../utils/apiFeatures.js';

export const createProduct = async (req, res, next) => {
  try {
    const product = await Product.create(req.body);
    res.status(201).json({ status: 'success', data: { product } });
  } catch (error) {
    next(error);
  }
};

export const getProducts = async (req, res, next) => {
  try {
    const features = new APIFeatures(Product.find(), req.query)
      .filter()
      .search()
      .sort()
      .paginate();

    const products = await features.query;
    const total = await Product.countDocuments(features.buildCountQuery());

    res.status(200).json({
      status: 'success',
      results: products.length,
      total,
      data: { products }
    });
  } catch (error) {
    next(error);
  }
};

export const getProductById = async (req, res, next) => {
  try {
    const product = await Product.findById(req.params.id);
    if (!product) {
      return res.status(404).json({ status: 'fail', message: 'Product not found' });
    }
    res.status(200).json({ status: 'success', data: { product } });
  } catch (error) {
    next(error);
  }
};

export const updateProduct = async (req, res, next) => {
  try {
    const product = await Product.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
      runValidators: true
    });
    if (!product) {
      return res.status(404).json({ status: 'fail', message: 'Product not found' });
    }
    res.status(200).json({ status: 'success', data: { product } });
  } catch (error) {
    next(error);
  }
};

export const deleteProduct = async (req, res, next) => {
  try {
    const product = await Product.findByIdAndDelete(req.params.id);
    if (!product) {
      return res.status(404).json({ status: 'fail', message: 'Product not found' });
    }
    res.status(204).json({ status: 'success', data: null });
  } catch (error) {
    next(error);
  }
};

export const getNearbyProducts = async (req, res, next) => {
  try {
    const { lat, lng, distance = 10, unit = 'km' } = req.query;
    const radius = unit === 'mi' ? distance / 3963.2 : distance / 6378.1;

    if (!lat || !lng) {
      return res.status(400).json({ status: 'fail', message: 'Latitude and longitude are required' });
    }

    const products = await Product.find({
      location: {
        $geoWithin: {
          $centerSphere: [[Number(lng), Number(lat)], radius]
        }
      }
    });

    res.status(200).json({ status: 'success', results: products.length, data: { products } });
  } catch (error) {
    next(error);
  }
};

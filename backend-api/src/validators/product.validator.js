import Joi from 'joi';

const locationSchema = Joi.object({
  type: Joi.string().valid('Point').required(),
  coordinates: Joi.array().items(Joi.number()).length(2).required()
});

export const productSchema = Joi.object({
  title: Joi.string().trim().max(150).required(),
  description: Joi.string().trim().max(1000).required(),
  category: Joi.string().trim().required(),
  price: Joi.number().min(0).required(),
  location: locationSchema.required()
});

export const productUpdateSchema = Joi.object({
  title: Joi.string().trim().max(150),
  description: Joi.string().trim().max(1000),
  category: Joi.string().trim(),
  price: Joi.number().min(0),
  location: locationSchema
}).min(1);

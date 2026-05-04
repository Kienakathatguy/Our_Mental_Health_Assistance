const errorHandler = (err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';

  if (process.env.NODE_ENV === 'production' && statusCode === 500) {
    return res.status(statusCode).json({ status: 'error', message: 'Something went wrong' });
  }

  res.status(statusCode).json({
    status: 'error', message,
    details: err.errors || undefined
  });
};

export default errorHandler;

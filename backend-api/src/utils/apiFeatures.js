class APIFeatures {
  constructor(query, queryString) {
    this.query = query;
    this.queryString = queryString;
  }

  filter() {
    const queryObj = { ...this.queryString };
    const excludedFields = ['page', 'limit', 'sort', 'fields', 'search', 'lat', 'lng', 'distance', 'unit'];
    excludedFields.forEach((field) => delete queryObj[field]);

    let filterString = JSON.stringify(queryObj);
    filterString = filterString.replace(/\b(gte|gt|lte|lt)\b/g, (match) => `$${match}`);

    this.query = this.query.find(JSON.parse(filterString));
    return this;
  }

  search() {
    if (this.queryString.search) {
      this.query = this.query.find({ $text: { $search: this.queryString.search } });
    }
    return this;
  }

  sort() {
    if (this.queryString.sort) {
      const sortBy = this.queryString.sort.split(',').join(' ');
      this.query = this.query.sort(sortBy);
    } else {
      this.query = this.query.sort('-createdAt');
    }
    return this;
  }

  paginate() {
    const page = parseInt(this.queryString.page, 10) || 1;
    const limit = parseInt(this.queryString.limit, 10) || 20;
    const skip = (page - 1) * limit;
    this.query = this.query.skip(skip).limit(limit);
    this.page = page;
    this.limit = limit;
    return this;
  }

  buildCountQuery() {
    const queryObj = { ...this.queryString };
    const excludedFields = ['page', 'limit', 'sort', 'fields', 'search', 'lat', 'lng', 'distance', 'unit'];
    excludedFields.forEach((field) => delete queryObj[field]);
    let filterString = JSON.stringify(queryObj);
    filterString = filterString.replace(/\b(gte|gt|lte|lt)\b/g, (match) => `$${match}`);
    return JSON.parse(filterString);
  }
}

export default APIFeatures;

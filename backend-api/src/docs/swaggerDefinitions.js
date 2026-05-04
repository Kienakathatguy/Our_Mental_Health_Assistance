/**
 * @swagger
 * components:
 *   schemas:
 *     AuthRegister:
 *       type: object
 *       required:
 *         - name
 *         - email
 *         - password
 *       properties:
 *         name:
 *           type: string
 *           example: Jane Doe
 *         email:
 *           type: string
 *           example: jane@example.com
 *         password:
 *           type: string
 *           example: StrongPassword123
 *     AuthLogin:
 *       type: object
 *       required:
 *         - email
 *         - password
 *       properties:
 *         email:
 *           type: string
 *           example: jane@example.com
 *         password:
 *           type: string
 *           example: StrongPassword123
 *     UserResponse:
 *       type: object
 *       properties:
 *         id:
 *           type: string
 *         name:
 *           type: string
 *         email:
 *           type: string
 *         role:
 *           type: string
 *     Product:
 *       type: object
 *       required:
 *         - title
 *         - description
 *         - category
 *         - price
 *         - location
 *       properties:
 *         title:
 *           type: string
 *           example: Mindful Journal
 *         description:
 *           type: string
 *           example: A guided product for reflection.
 *         category:
 *           type: string
 *           example: wellness
 *         price:
 *           type: number
 *           example: 19.99
 *         location:
 *           type: object
 *           properties:
 *             type:
 *               type: string
 *               example: Point
 *             coordinates:
 *               type: array
 *               items:
 *                 type: number
 *               example: [106.6297, 10.8231]
 *     ErrorResponse:
 *       type: object
 *       properties:
 *         status:
 *           type: string
 *           example: fail
 *         message:
 *           type: string
 *           example: Validation error
 *         details:
 *           type: array
 *           items:
 *             type: string
 *
 * /api/auth/register:
 *   post:
 *     tags:
 *       - Authentication
 *     summary: Register a new user
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/AuthRegister'
 *     responses:
 *       201:
 *         description: User registered successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 status:
 *                   type: string
 *                   example: success
 *                 data:
 *                   type: object
 *                   properties:
 *                     user:
 *                       $ref: '#/components/schemas/UserResponse'
 *                     token:
 *                       type: string
 *                       example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
 *       400:
 *         $ref: '#/components/schemas/ErrorResponse'
 *
 * /api/auth/login:
 *   post:
 *     tags:
 *       - Authentication
 *     summary: Login an existing user
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/AuthLogin'
 *     responses:
 *       200:
 *         description: Login successful
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 status:
 *                   type: string
 *                   example: success
 *                 data:
 *                   type: object
 *                   properties:
 *                     user:
 *                       $ref: '#/components/schemas/UserResponse'
 *                     token:
 *                       type: string
 *       401:
 *         $ref: '#/components/schemas/ErrorResponse'
 *
 * /api/products:
 *   get:
 *     tags:
 *       - Products
 *     summary: Get all products with filtering, sorting, pagination, and search
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *         description: Page number
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *         description: Number of items per page
 *       - in: query
 *         name: sort
 *         schema:
 *           type: string
 *         description: Comma-separated sort fields
 *       - in: query
 *         name: search
 *         schema:
 *           type: string
 *         description: Full-text search term
 *       - in: query
 *         name: category
 *         schema:
 *           type: string
 *       - in: query
 *         name: price[gte]
 *         schema:
 *           type: number
 *       - in: query
 *         name: price[lte]
 *         schema:
 *           type: number
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: List of products
 *       401:
 *         $ref: '#/components/schemas/ErrorResponse'
 *
 *   post:
 *     tags:
 *       - Products
 *     summary: Create a new product
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/Product'
 *     responses:
 *       201:
 *         description: New product created
 *       400:
 *         $ref: '#/components/schemas/ErrorResponse'
 *       401:
 *         $ref: '#/components/schemas/ErrorResponse'
 *
 * /api/products/nearby:
 *   get:
 *     tags:
 *       - Products
 *     summary: Get products within a geolocation radius
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: query
 *         name: lat
 *         schema:
 *           type: number
 *         required: true
 *       - in: query
 *         name: lng
 *         schema:
 *           type: number
 *         required: true
 *       - in: query
 *         name: distance
 *         schema:
 *           type: number
 *         example: 10
 *       - in: query
 *         name: unit
 *         schema:
 *           type: string
 *           enum: [km, mi]
 *     responses:
 *       200:
 *         description: Nearby products found
 *       400:
 *         $ref: '#/components/schemas/ErrorResponse'
 *
 * /api/products/{id}:
 *   get:
 *     tags:
 *       - Products
 *     summary: Get a product by ID
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *     responses:
 *       200:
 *         description: Product details
 *       404:
 *         $ref: '#/components/schemas/ErrorResponse'
 *
 *   patch:
 *     tags:
 *       - Products
 *     summary: Update a product by ID
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/Product'
 *     responses:
 *       200:
 *         description: Updated product
 *       400:
 *         $ref: '#/components/schemas/ErrorResponse'
 *       404:
 *         $ref: '#/components/schemas/ErrorResponse'
 *
 *   delete:
 *     tags:
 *       - Products
 *     summary: Delete a product by ID
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *     responses:
 *       204:
 *         description: Product deleted successfully
 *       404:
 *         $ref: '#/components/schemas/ErrorResponse'
 */
export default {};

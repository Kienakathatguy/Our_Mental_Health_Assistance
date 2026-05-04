/**
 * Scrapbook Editor with Drawing Canvas and Drag-and-Drop Layout
 * Allows users to create journal entries like a scrapbook with text, images, and drawings
 */

class ScrapbookEditor {
    constructor(containerId, outputFieldId) {
        this.container = document.getElementById(containerId);
        this.outputField = document.getElementById(outputFieldId);
        this.canvas = null;
        this.ctx = null;
        this.isDrawing = false;
        this.currentTool = 'brush';
        this.currentColor = '#000000';
        this.brushSize = 3;
        this.elements = [];
        this.selectedElement = null;
        this.draggedElement = null;
        this.offsetX = 0;
        this.offsetY = 0;

        this.init();
    }

    init() {
        this.createEditor();
        this.setupCanvas();
        this.setupTools();
        this.setupEventListeners();
        this.loadSavedState();
    }

    createEditor() {
        const editorHTML = `
            <div class="scrapbook-container">
                <!-- Drawing Tools Toolbar -->
                <div class="scrapbook-toolbar mb-3 p-3 bg-light rounded">
                    <div class="row g-2">
                        <div class="col-auto">
                            <div class="btn-group" role="group" aria-label="Drawing tools">
                                <button type="button" class="btn btn-sm btn-outline-secondary scrapbook-tool" data-tool="brush" title="Brush">
                                    ✏️ Brush
                                </button>
                                <button type="button" class="btn btn-sm btn-outline-secondary scrapbook-tool" data-tool="eraser" title="Eraser">
                                    🧹 Eraser
                                </button>
                                <button type="button" class="btn btn-sm btn-outline-secondary scrapbook-tool" data-tool="line" title="Line">
                                    📏 Line
                                </button>
                                <button type="button" class="btn btn-sm btn-outline-secondary scrapbook-tool" data-tool="rect" title="Rectangle">
                                    ▭ Rectangle
                                </button>
                                <button type="button" class="btn btn-sm btn-outline-secondary scrapbook-tool" data-tool="circle" title="Circle">
                                    ⭕ Circle
                                </button>
                            </div>
                        </div>
                        <div class="col-auto">
                            <label for="brush-color" class="form-label mb-0">Color:</label>
                            <input type="color" id="brush-color" class="form-control form-control-sm" value="#000000" style="width: 50px; height: 32px;">
                        </div>
                        <div class="col-auto">
                            <label for="brush-size" class="form-label mb-0">Size:</label>
                            <input type="range" id="brush-size" class="form-range" min="1" max="20" value="3" style="width: 100px;">
                        </div>
                        <div class="col-auto">
                            <button type="button" class="btn btn-sm btn-outline-danger" id="clear-canvas">Clear Canvas</button>
                        </div>
                        <div class="col-auto">
                            <button type="button" class="btn btn-sm btn-outline-secondary" id="undo-canvas">↶ Undo</button>
                        </div>
                    </div>
                </div>

                <!-- Main Canvas Area -->
                <div class="scrapbook-canvas-wrapper mb-3 rounded border border-2" style="background: white; position: relative; min-height: 500px; max-height: 800px; overflow: auto;">
                    <canvas id="scrapbook-canvas" width="800" height="600" style="display: block; cursor: crosshair; background: white;"></canvas>
                    <div id="scrapbook-elements" class="scrapbook-elements" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;"></div>
                </div>

                <!-- Content Tools -->
                <div class="scrapbook-content-toolbar mb-3 p-3 bg-light rounded">
                    <div class="row g-2">
                        <div class="col-auto">
                            <button type="button" class="btn btn-sm btn-outline-primary" id="add-text-btn">
                                📝 Add Text
                            </button>
                        </div>
                        <div class="col-auto">
                            <button type="button" class="btn btn-sm btn-outline-primary" id="add-image-btn">
                                🖼️ Add Image
                            </button>
                        </div>
                        <div class="col-auto">
                            <div class="btn-group" role="group" aria-label="Stickers">
                                <button type="button" class="btn btn-sm btn-outline-primary scrapbook-sticker" data-sticker="🌟">🌟</button>
                                <button type="button" class="btn btn-sm btn-outline-primary scrapbook-sticker" data-sticker="💖">💖</button>
                                <button type="button" class="btn btn-sm btn-outline-primary scrapbook-sticker" data-sticker="🌸">🌸</button>
                                <button type="button" class="btn btn-sm btn-outline-primary scrapbook-sticker" data-sticker="🌈">🌈</button>
                                <button type="button" class="btn btn-sm btn-outline-primary scrapbook-sticker" data-sticker="✨">✨</button>
                            </div>
                        </div>
                        <div class="col-auto">
                            <button type="button" class="btn btn-sm btn-outline-warning" id="delete-element-btn" disabled>
                                🗑️ Delete Selected
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Image Input (Hidden) -->
                <input type="file" id="scrapbook-image-input" accept="image/*" style="display: none;">
            </div>
        `;
        this.container.innerHTML = editorHTML;
    }

    setupCanvas() {
        this.canvas = document.getElementById('scrapbook-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.canvasStates = [];
        this.saveCanvasState();
    }

    setupTools() {
        const toolButtons = document.querySelectorAll('.scrapbook-tool');
        toolButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                toolButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.currentTool = btn.dataset.tool;
            });
        });

        // Set default active tool
        document.querySelector('[data-tool="brush"]').classList.add('active');

        // Color picker
        document.getElementById('brush-color').addEventListener('change', (e) => {
            this.currentColor = e.target.value;
        });

        // Brush size
        document.getElementById('brush-size').addEventListener('change', (e) => {
            this.brushSize = parseInt(e.target.value);
        });

        // Clear canvas
        document.getElementById('clear-canvas').addEventListener('click', () => {
            if (confirm('Clear the entire drawing? This cannot be undone.')) {
                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                this.canvasStates = [];
                this.saveCanvasState();
            }
        });

        // Undo
        document.getElementById('undo-canvas').addEventListener('click', () => {
            this.undo();
        });
    }

    setupEventListeners() {
        // Canvas drawing events
        this.canvas.addEventListener('mousedown', (e) => this.onCanvasMouseDown(e));
        this.canvas.addEventListener('mousemove', (e) => this.onCanvasMouseMove(e));
        this.canvas.addEventListener('mouseup', (e) => this.onCanvasMouseUp(e));
        this.canvas.addEventListener('mouseout', (e) => this.onCanvasMouseUp(e));

        // Touch events for mobile
        this.canvas.addEventListener('touchstart', (e) => this.onCanvasTouchStart(e));
        this.canvas.addEventListener('touchmove', (e) => this.onCanvasTouchMove(e));
        this.canvas.addEventListener('touchend', (e) => this.onCanvasTouchEnd(e));

        // Add text
        document.getElementById('add-text-btn').addEventListener('click', () => this.addTextElement());

        // Add image
        document.getElementById('add-image-btn').addEventListener('click', () => {
            document.getElementById('scrapbook-image-input').click();
        });

        document.getElementById('scrapbook-image-input').addEventListener('change', (e) => {
            this.addImageElement(e.target.files[0]);
        });

        // Add stickers
        document.querySelectorAll('.scrapbook-sticker').forEach(btn => {
            btn.addEventListener('click', (e) => this.addStickerElement(btn.dataset.sticker));
        });

        // Delete element
        document.getElementById('delete-element-btn').addEventListener('click', () => {
            if (this.selectedElement) {
                this.deleteElement(this.selectedElement);
            }
        });
    }

    onCanvasMouseDown(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        this.isDrawing = true;
        this.startX = x;
        this.startY = y;

        if (this.currentTool === 'brush' || this.currentTool === 'eraser') {
            this.ctx.beginPath();
            this.ctx.moveTo(x, y);
        }
    }

    onCanvasMouseMove(e) {
        if (!this.isDrawing) return;

        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        if (this.currentTool === 'brush') {
            this.ctx.lineWidth = this.brushSize;
            this.ctx.lineCap = 'round';
            this.ctx.lineJoin = 'round';
            this.ctx.strokeStyle = this.currentColor;
            this.ctx.lineTo(x, y);
            this.ctx.stroke();
        } else if (this.currentTool === 'eraser') {
            this.ctx.clearRect(x - this.brushSize / 2, y - this.brushSize / 2, this.brushSize, this.brushSize);
        }
    }

    onCanvasMouseUp(e) {
        if (!this.isDrawing) return;

        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        if (this.currentTool === 'line') {
            this.redrawCanvas();
            this.ctx.strokeStyle = this.currentColor;
            this.ctx.lineWidth = this.brushSize;
            this.ctx.beginPath();
            this.ctx.moveTo(this.startX, this.startY);
            this.ctx.lineTo(x, y);
            this.ctx.stroke();
        } else if (this.currentTool === 'rect') {
            this.redrawCanvas();
            this.ctx.strokeStyle = this.currentColor;
            this.ctx.lineWidth = this.brushSize;
            this.ctx.strokeRect(this.startX, this.startY, x - this.startX, y - this.startY);
        } else if (this.currentTool === 'circle') {
            this.redrawCanvas();
            const radius = Math.sqrt(Math.pow(x - this.startX, 2) + Math.pow(y - this.startY, 2));
            this.ctx.strokeStyle = this.currentColor;
            this.ctx.lineWidth = this.brushSize;
            this.ctx.beginPath();
            this.ctx.arc(this.startX, this.startY, radius, 0, 2 * Math.PI);
            this.ctx.stroke();
        }

        this.isDrawing = false;
        this.saveCanvasState();
    }

    onCanvasTouchStart(e) {
        e.preventDefault();
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent('mousedown', {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        this.canvas.dispatchEvent(mouseEvent);
    }

    onCanvasTouchMove(e) {
        e.preventDefault();
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent('mousemove', {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        this.canvas.dispatchEvent(mouseEvent);
    }

    onCanvasTouchEnd(e) {
        e.preventDefault();
        const mouseEvent = new MouseEvent('mouseup', {});
        this.canvas.dispatchEvent(mouseEvent);
    }

    saveCanvasState() {
        this.canvasStates.push(this.canvas.toDataURL());
        if (this.canvasStates.length > 20) {
            this.canvasStates.shift();
        }
    }

    redrawCanvas() {
        if (this.canvasStates.length > 1) {
            const img = new Image();
            img.src = this.canvasStates[this.canvasStates.length - 1];
            img.onload = () => {
                this.ctx.drawImage(img, 0, 0);
            };
        }
    }

    undo() {
        if (this.canvasStates.length > 1) {
            this.canvasStates.pop();
            const img = new Image();
            img.src = this.canvasStates[this.canvasStates.length - 1];
            img.onload = () => {
                this.ctx.drawImage(img, 0, 0);
            };
        }
    }

    addTextElement() {
        const text = prompt('Enter your text:');
        if (!text) return;

        const element = document.createElement('div');
        const id = 'elem-' + Date.now();
        element.id = id;
        element.className = 'scrapbook-element scrapbook-text';
        element.textContent = text;
        element.style.cssText = `
            position: absolute;
            left: 50px;
            top: 50px;
            padding: 8px 12px;
            background: rgba(255, 255, 255, 0.9);
            border: 2px solid #007bff;
            cursor: move;
            font-size: 16px;
            font-weight: bold;
            max-width: 200px;
            word-wrap: break-word;
            z-index: 10;
            pointer-events: auto;
        `;

        this.makeElementDraggable(element);
        this.addElementClickListener(element);

        document.getElementById('scrapbook-elements').appendChild(element);
        this.elements.push({ id, type: 'text', content: text, x: 50, y: 50 });
        this.updateOutput();
    }

    addImageElement(file) {
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            const element = document.createElement('img');
            const id = 'elem-' + Date.now();
            element.id = id;
            element.className = 'scrapbook-element scrapbook-image';
            element.src = e.target.result;
            element.style.cssText = `
                position: absolute;
                left: 50px;
                top: 50px;
                max-width: 200px;
                height: auto;
                border: 2px solid #ffc107;
                cursor: move;
                z-index: 10;
                pointer-events: auto;
            `;

            this.makeElementDraggable(element);
            this.addElementClickListener(element);

            document.getElementById('scrapbook-elements').appendChild(element);
            this.elements.push({ id, type: 'image', content: e.target.result, x: 50, y: 50 });
            this.updateOutput();
        };
        reader.readAsDataURL(file);
    }

    addStickerElement(sticker) {
        const element = document.createElement('div');
        const id = 'elem-' + Date.now();
        element.id = id;
        element.className = 'scrapbook-element scrapbook-sticker-elem';
        element.textContent = sticker;
        element.style.cssText = `
            position: absolute;
            left: 50px;
            top: 50px;
            font-size: 48px;
            cursor: move;
            z-index: 10;
            user-select: none;
            pointer-events: auto;
        `;

        this.makeElementDraggable(element);
        this.addElementClickListener(element);

        document.getElementById('scrapbook-elements').appendChild(element);
        this.elements.push({ id, type: 'sticker', content: sticker, x: 50, y: 50 });
        this.updateOutput();
    }

    makeElementDraggable(element) {
        let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

        element.addEventListener('mousedown', (e) => {
            e.preventDefault();
            pos3 = e.clientX;
            pos4 = e.clientY;
            this.draggedElement = element;

            const onMouseMove = (e) => {
                e.preventDefault();
                pos1 = pos3 - e.clientX;
                pos2 = pos4 - e.clientY;
                pos3 = e.clientX;
                pos4 = e.clientY;

                const newTop = element.offsetTop - pos2;
                const newLeft = element.offsetLeft - pos1;

                element.style.top = Math.max(0, Math.min(newTop, this.canvas.height - element.offsetHeight)) + 'px';
                element.style.left = Math.max(0, Math.min(newLeft, this.canvas.width - element.offsetWidth)) + 'px';

                this.updateElementInList(element.id, newLeft, newTop);
            };

            const onMouseUp = () => {
                document.removeEventListener('mousemove', onMouseMove);
                document.removeEventListener('mouseup', onMouseUp);
                this.draggedElement = null;
                this.updateOutput();
            };

            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
        });
    }

    addElementClickListener(element) {
        element.addEventListener('click', () => {
            this.selectElement(element);
        });
    }

    selectElement(element) {
        if (this.selectedElement) {
            this.selectedElement.style.boxShadow = 'none';
            this.selectedElement.style.outline = 'none';
        }

        this.selectedElement = element;
        element.style.boxShadow = '0 0 10px rgba(0, 123, 255, 0.8)';
        document.getElementById('delete-element-btn').disabled = false;
    }

    deleteElement(element) {
        element.remove();
        this.elements = this.elements.filter(e => e.id !== element.id);
        this.selectedElement = null;
        document.getElementById('delete-element-btn').disabled = true;
        this.updateOutput();
    }

    updateElementInList(id, x, y) {
        const element = this.elements.find(e => e.id === id);
        if (element) {
            element.x = x;
            element.y = y;
        }
    }

    updateOutput() {
        const state = {
            canvas: this.canvas.toDataURL(),
            elements: this.elements.map(e => ({
                ...e,
                x: parseInt(document.getElementById(e.id)?.style.left) || e.x,
                y: parseInt(document.getElementById(e.id)?.style.top) || e.y
            }))
        };
        this.outputField.value = JSON.stringify(state);
    }

    loadSavedState() {
        if (this.outputField && this.outputField.value) {
            try {
                const state = JSON.parse(this.outputField.value);
                // Load canvas
                if (state.canvas) {
                    const img = new Image();
                    img.onload = () => {
                        this.ctx.drawImage(img, 0, 0);
                        this.saveCanvasState();
                    };
                    img.src = state.canvas;
                }
                // Load elements
                if (state.elements && Array.isArray(state.elements)) {
                    state.elements.forEach(elem => {
                        if (elem.type === 'text') {
                            const element = document.createElement('div');
                            element.id = elem.id;
                            element.className = 'scrapbook-element scrapbook-text';
                            element.textContent = elem.content;
                            element.style.cssText = `
                                position: absolute;
                                left: ${elem.x}px;
                                top: ${elem.y}px;
                                padding: 8px 12px;
                                background: rgba(255, 255, 255, 0.9);
                                border: 2px solid #007bff;
                                cursor: move;
                                font-size: 16px;
                                font-weight: bold;
                                max-width: 200px;
                                word-wrap: break-word;
                                z-index: 10;
                                pointer-events: auto;
                            `;
                            this.makeElementDraggable(element);
                            this.addElementClickListener(element);
                            document.getElementById('scrapbook-elements').appendChild(element);
                        } else if (elem.type === 'image') {
                            const element = document.createElement('img');
                            element.id = elem.id;
                            element.className = 'scrapbook-element scrapbook-image';
                            element.src = elem.content;
                            element.style.cssText = `
                                position: absolute;
                                left: ${elem.x}px;
                                top: ${elem.y}px;
                                max-width: 200px;
                                height: auto;
                                border: 2px solid #ffc107;
                                cursor: move;
                                z-index: 10;
                                pointer-events: auto;
                            `;
                            this.makeElementDraggable(element);
                            this.addElementClickListener(element);
                            document.getElementById('scrapbook-elements').appendChild(element);
                        } else if (elem.type === 'sticker') {
                            const element = document.createElement('div');
                            element.id = elem.id;
                            element.className = 'scrapbook-element scrapbook-sticker-elem';
                            element.textContent = elem.content;
                            element.style.cssText = `
                                position: absolute;
                                left: ${elem.x}px;
                                top: ${elem.y}px;
                                font-size: 48px;
                                cursor: move;
                                z-index: 10;
                                user-select: none;
                                pointer-events: auto;
                            `;
                            this.makeElementDraggable(element);
                            this.addElementClickListener(element);
                            document.getElementById('scrapbook-elements').appendChild(element);
                        }
                    });
                }
            } catch (e) {
                console.log('No saved scrapbook state or invalid format');
            }
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('scrapbook-editor')) {
        window.scrapbookEditor = new ScrapbookEditor('scrapbook-editor', 'scrapbook-data');
    }
});

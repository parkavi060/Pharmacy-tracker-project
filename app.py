from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharmasy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-change-this'

db = SQLAlchemy(app)

# -------------------- MODELS --------------------
class Product(db.Model):
    product_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

class Location(db.Model):
    location_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)

class ProductMovement(db.Model):
    movement_id = db.Column(db.String, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    from_location = db.Column(db.String, db.ForeignKey('location.location_id'), nullable=True)
    to_location = db.Column(db.String, db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.String, db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product', foreign_keys=[product_id])
    from_loc = db.relationship('Location', foreign_keys=[from_location])
    to_loc = db.relationship('Location', foreign_keys=[to_location])

# -------------------- HELPERS --------------------
def gen_id(prefix='id'):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

# -------------------- SEED DATA --------------------
def seed_data():
    # Only seed if DB empty
    if Product.query.first():
        return

    products = [
        Product(product_id="P001", name="Paracetamol 500mg", description="Painkiller, 10 tablets"),
        Product(product_id="P002", name="Amoxicillin 250mg", description="Antibiotic, 20 capsules"),
        Product(product_id="P003", name="Cough Syrup 100ml", description="For cough relief"),
        Product(product_id="P004", name="Ibuprofen 400mg", description="Anti-inflammatory"),
        Product(product_id="P005", name="Vitamin C 1000mg", description="Immunity booster"),
        Product(product_id="P006", name="Antacid Liquid 200ml", description="For acidity"),
        Product(product_id="P007", name="Cetirizine 10mg", description="Antihistamine"),
        Product(product_id="P008", name="Zinc Supplement 50mg", description="Mineral supplement"),
        Product(product_id="P009", name="Pain Relief Balm 30g", description="Topical balm"),
        Product(product_id="P010", name="Glucose Powder 1kg", description="Energy supplement")
    ]

    locations = [
        Location(location_id="L001", name="Main Warehouse", address="Block A"),
        Location(location_id="L002", name="Front Store", address="Shop Floor"),
        Location(location_id="L003", name="Cold Storage", address="Basement"),
        Location(location_id="L004", name="Online Dispatch Unit", address="Dispatch Bay")
    ]

    db.session.add_all(products + locations)
    db.session.commit()

    movements = [
        # inbound to warehouse
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,5,9,0), from_location=None, to_location="L001", product_id="P001", qty=200),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,5,9,5), from_location=None, to_location="L001", product_id="P002", qty=150),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,6,10,0), from_location=None, to_location="L003", product_id="P003", qty=80),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,6,10,5), from_location=None, to_location="L001", product_id="P004", qty=120),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,6,10,10), from_location=None, to_location="L002", product_id="P005", qty=120),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,7,11,0), from_location=None, to_location="L003", product_id="P006", qty=70),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,7,11,10), from_location=None, to_location="L001", product_id="P007", qty=200),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,7,11,20), from_location=None, to_location="L002", product_id="P008", qty=90),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,8,12,0), from_location=None, to_location="L001", product_id="P009", qty=60),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,8,12,10), from_location=None, to_location="L001", product_id="P010", qty=50),

        # transfers / sales / dispatches
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,9,9,0), from_location="L001", to_location="L002", product_id="P001", qty=40),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,9,9,10), from_location="L001", to_location="L002", product_id="P002", qty=50),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,9,10,0), from_location="L003", to_location="L002", product_id="P003", qty=20),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,10,8,30), from_location="L001", to_location="L004", product_id="P004", qty=30),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,10,8,45), from_location="L002", to_location="L004", product_id="P005", qty=25),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,10,9,0), from_location="L003", to_location="L002", product_id="P006", qty=15),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,11,14,0), from_location="L001", to_location="L002", product_id="P007", qty=35),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,11,14,20), from_location="L002", to_location="L004", product_id="P008", qty=10),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,12,16,0), from_location="L001", to_location="L004", product_id="P009", qty=20),
        ProductMovement(movement_id=gen_id('mov'), timestamp=datetime(2025,1,12,16,15), from_location="L001", to_location="L002", product_id="P010", qty=10)
    ]

    db.session.add_all(movements)
    db.session.commit()

# -------------------- INITIALIZATION --------------------
initialization_done = False

@app.before_request
def run_initialization_once():
    global initialization_done
    if not initialization_done:
        db.create_all()
        seed_data()  # <---- Auto seed when DB is first created
        initialization_done = True

# -------------------- ROUTES --------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    prods = Product.query.order_by(Product.name).all()
    return render_template('products.html', products=prods)

@app.route('/products/add', methods=['GET','POST'])
def add_product():
    if request.method == 'POST':
        pid = request.form.get('product_id') or gen_id('prod')
        name = request.form['name'].strip()
        desc = request.form.get('description','').strip()
        if not name:
            flash('Name required', 'danger')
            return redirect(url_for('add_product'))
        p = Product(product_id=pid, name=name, description=desc)
        db.session.add(p); db.session.commit()
        flash('Product added', 'success')
        return redirect(url_for('products'))
    return render_template('product_form.html', action='Add', product=None)

@app.route('/products/edit/<product_id>', methods=['GET','POST'])
def edit_product(product_id):
    p = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        p.name = request.form['name'].strip()
        p.description = request.form.get('description','').strip()
        db.session.commit()
        flash('Product updated', 'success')
        return redirect(url_for('products'))
    return render_template('product_form.html', action='Edit', product=p)

@app.route('/products/view/<product_id>')
def view_product(product_id):
    p = Product.query.get_or_404(product_id)
    return render_template('product_view.html', product=p)

@app.route('/locations')
def locations():
    locs = Location.query.order_by(Location.name).all()
    return render_template('locations.html', locations=locs)

@app.route('/locations/add', methods=['GET','POST'])
def add_location():
    if request.method == 'POST':
        lid = request.form.get('location_id') or gen_id('loc')
        name = request.form['name'].strip()
        addr = request.form.get('address','').strip()
        if not name:
            flash('Name required', 'danger')
            return redirect(url_for('add_location'))
        l = Location(location_id=lid, name=name, address=addr)
        db.session.add(l); db.session.commit()
        flash('Location added', 'success')
        return redirect(url_for('locations'))
    return render_template('location_form.html', action='Add', location=None)

@app.route('/locations/edit/<location_id>', methods=['GET','POST'])
def edit_location(location_id):
    l = Location.query.get_or_404(location_id)
    if request.method == 'POST':
        l.name = request.form['name'].strip()
        l.address = request.form.get('address','').strip()
        db.session.commit()
        flash('Location updated', 'success')
        return redirect(url_for('locations'))
    return render_template('location_form.html', action='Edit', location=l)

@app.route('/locations/view/<location_id>')
def view_location(location_id):
    l = Location.query.get_or_404(location_id)
    return render_template('location_view.html', location=l)

@app.route('/movements')
def movements():
    movs = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements.html', movements=movs)

@app.route('/movements/add', methods=['GET','POST'])
def add_movement():
    products = Product.query.order_by(Product.name).all()
    locations = Location.query.order_by(Location.name).all()
    if request.method == 'POST':
        mid = gen_id('mov')
        ts = request.form.get('timestamp') or None
        if ts:
            ts = datetime.fromisoformat(ts)
        from_loc = request.form.get('from_location') or None
        to_loc = request.form.get('to_location') or None
        product_id = request.form['product_id']
        qty = int(request.form['qty'] or 0)
        if qty <= 0:
            flash('Quantity must be > 0', 'danger')
            return redirect(url_for('add_movement'))
        mov = ProductMovement(movement_id=mid, timestamp=ts or datetime.utcnow(),
                              from_location=from_loc, to_location=to_loc,
                              product_id=product_id, qty=qty)
        db.session.add(mov); db.session.commit()
        flash('Movement recorded', 'success')
        return redirect(url_for('movements'))
    return render_template('movement_form.html', products=products, locations=locations, action='Add', movement=None)

@app.route('/movements/edit/<movement_id>', methods=['GET','POST'])
def edit_movement(movement_id):
    mov = ProductMovement.query.get_or_404(movement_id)
    products = Product.query.order_by(Product.name).all()
    locations = Location.query.order_by(Location.name).all()
    if request.method == 'POST':
        ts = request.form.get('timestamp') or None
        if ts:
            mov.timestamp = datetime.fromisoformat(ts)
        mov.from_location = request.form.get('from_location') or None
        mov.to_location = request.form.get('to_location') or None
        mov.product_id = request.form['product_id']
        mov.qty = int(request.form['qty'] or 0)
        if mov.qty <= 0:
            flash('Quantity must be > 0', 'danger')
            return redirect(url_for('edit_movement', movement_id=movement_id))
        db.session.commit()
        flash('Movement updated', 'success')
        return redirect(url_for('movements'))
    return render_template('movement_form.html', products=products, locations=locations, action='Edit', movement=mov)

@app.route('/movements/view/<movement_id>')
def view_movement(movement_id):
    mov = ProductMovement.query.get_or_404(movement_id)
    return render_template('movement_view.html', movement=mov)

@app.route('/report')
def report():
    products = Product.query.order_by(Product.name).all()
    locations = Location.query.order_by(Location.name).all()
    balances = {}
    movs = ProductMovement.query.order_by(ProductMovement.timestamp).all()
    for m in movs:
        if m.to_location:
            key = (m.product_id, m.to_location)
            balances[key] = balances.get(key, 0) + m.qty
        if m.from_location:
            key = (m.product_id, m.from_location)
            balances[key] = balances.get(key, 0) - m.qty
    rows = []
    for (prod_id, loc_id), qty in balances.items():
        if qty == 0:
            continue
        prod = Product.query.get(prod_id)
        loc = Location.query.get(loc_id)
        rows.append({'product_id': prod_id, 'product_name': prod.name if prod else prod_id,
                     'location_id': loc_id, 'location_name': loc.name if loc else loc_id,
                     'qty': qty})
    rows = sorted(rows, key=lambda r: (r['product_name'], r['location_name']))
    return render_template('report.html', rows=rows)

# -------------------- MAIN --------------------
if __name__ == '__main__':
    app.run(debug=True)

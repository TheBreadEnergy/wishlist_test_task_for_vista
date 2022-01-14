from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    price = db.Column(db.String(255))
    link = db.Column(db.String(255))
    note = db.Column(db.String(255))

    def __repr__(self):
        return '<Products %r>' % self.id


@app.route('/')
def index():
    products = Products.query.order_by(Products.id).all()
    return render_template('index.html', products=products)


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        link = request.form['link']
        note = request.form['note']

        product = Products(name=name, price=price, link=link, note=note)

        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/')

        except:
            return 'Ошибка'
    else:
        return render_template('add.html')


@app.route('/product/<int:id>/update', methods=['POST', 'GET'])
def product_update(id):
    product = Products.query.get(id)
    if request.method == "POST":
        product.name = request.form['name']
        product.price = request.form['price']
        product.link = request.form['link']
        product.note = request.form['note']

        try:
            db.session.commit()
            return redirect('/')

        except:
            return 'Ошибка'
    else:
        return render_template('update.html', product=product)


@app.route('/product/<int:id>/delete')
def product_delete(id):
    product = Products.query.get_or_404(id)

    try:
        db.session.delete(product)
        db.session.commit()
        return redirect('/')
    except:
        return 'Ошибка'


if __name__ == '__main__':
    app.run(debug=True)

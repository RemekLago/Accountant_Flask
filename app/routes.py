from datetime import datetime
from app import app, db
from flask import render_template, url_for, flash, redirect, request
from app.forms import SaleForm, BuyForm, SaldoForm
from app.models import StockTable, SaldoTable, HistoryTable


@app.route('/')
@app.route('/index')
def index():
    today = datetime.now().date()
    n = len(SaldoTable.query.all())
    current_saldo = (SaldoTable.query.filter(SaldoTable.id==n).all())[0].saldo
    return render_template('index.html', today=today, current_saldo=current_saldo)

@app.route('/sale', methods=["GET", "POST"])
def sale():
    today = datetime.now().date()
    form = SaleForm()
    n = len(SaldoTable.query.all())
    if n == 0:
        saldo_last = 0
    else: 
        saldo_last = (SaldoTable.query.filter(SaldoTable.id==n).all())[0].saldo
    print(n)
    print(saldo_last)
    # print(form.validate_on_submit())
    # print(form.is_submitted(), form.validate())
    # if request.method == 'POST':
    #     product = request.form['product']
    #     quantity = request.form['quantity']
    #     price = request.form['price']
    #     sale1 = StockTable(
    #         product = product,   
    #         quantity = quantity,  
    #         price = price,   
    #         )
    #     sale2 = SaldoTable(
    #         saldo = -(price * quantity),  
    #         )
    #     sale3 = HistoryTable(
    #         name = "sale",
    #         product = product,   
    #         quantity = quantity,  
    #         price = price,
    #         # comment = null
    #         )
    if form.validate_on_submit():
        sale1 = StockTable(
            product = form.product.data,   
            quantity = form.quantity.data,  
            price = form.price.data,   
            )
        sale2 = SaldoTable(
            payment = (form.price.data * form.quantity.data),
            saldo = int(saldo_last) + (form.price.data * form.quantity.data),
            status = "sell" 
            )
        sale3 = HistoryTable(
            name = "sales",
            product = form.product.data,
            saldo = form.quantity.data * form.price.data,
            quantity = form.quantity.data,  
            price = form.price.data,
            )

        db.session.add(sale1)
        db.session.add(sale2)
        db.session.add(sale3)
        db.session.commit()
        flash('Congratulations, task completed')
        return redirect(url_for('sale'))
    return render_template('sale.html', title='Sale', form=form, today=today)

@app.route('/purchase', methods=["GET", "POST"])
def purchase():
    today = datetime.now().date()
    form = BuyForm()
    n = len(SaldoTable.query.all())
    if n == 0:
        saldo_last = 0
    else: 
        saldo_last = (SaldoTable.query.filter(SaldoTable.id==n).all())[0].saldo
    print(n)
    print(saldo_last)
    if form.validate_on_submit():
        purchase1 = StockTable(
            product = form.product.data,   
            quantity = form.quantity.data,  
            price = form.price.data,   
            )
        purchase2 = SaldoTable(
            payment = -(form.price.data * form.quantity.data),
            saldo = int(saldo_last) + (form.price.data * form.quantity.data),
            status = "purchase"
            )
        purchase3 = HistoryTable(
            name = "purchase",
            product = form.product.data,
            saldo = -(form.quantity.data * form.price.data),   
            quantity = form.quantity.data,  
            price = form.price.data,
            )

        db.session.add(purchase1)
        db.session.add(purchase2)
        db.session.add(purchase3)
        db.session.commit()
        flash('Congratulations, task completed')
        return redirect(url_for('purchase'))
    return render_template('purchase.html', title='Purchase', form=form, today=today)

@app.route('/payment', methods=["GET", "POST"])
def payment():
    today = datetime.now().date()
    n = len(SaldoTable.query.all())
    if n == 0:
        saldo_last = 0
    else: 
        saldo_last = (SaldoTable.query.filter(SaldoTable.id==n).all())[0].saldo
    form = SaldoForm()
    if form.validate_on_submit():
        # db.session.query(SaldoTable).delete()
        if int(form.saldo.data) >= 0:
            payment2 = SaldoTable(
                payment = form.saldo.data,
                status = "payment on account",
                saldo = int(saldo_last) + int(form.saldo.data),
                )
        elif int(form.saldo.data) < 0 and (int(form.saldo.data) + int(saldo_last)) >= 0:
                        payment2 = SaldoTable(
                payment = form.saldo.data,
                status = "payment on account",
                saldo = int(saldo_last) + int(form.saldo.data),
                )
        else:
            print("Error, not enaught money on account")
            
        payment3 = HistoryTable(
            name = "payment",
            saldo = form.saldo.data,
            comment = form.comment.data,  
            )

        db.session.add(payment2)
        db.session.add(payment3)
        db.session.commit()
        flash('Congratulations, task completed')
        return redirect(url_for('payment'))
    return render_template('payment.html', title='Payment', form=form, today=today, saldo_last=saldo_last)

@app.route('/history')
def history():
    today = datetime.now().date()
    history = HistoryTable.query.all()
    return render_template('history.html', title='History', history=history, today=today)

@app.route('/stock')
def stock():
    today = datetime.now().date()
    stock = StockTable.query.all()
    return render_template('stock.html', title='Stock', stock=stock, today=today)

@app.route('/saldo')
def saldo():
    today = datetime.now().date()
    saldo = SaldoTable.query.all()
    return render_template('saldo.html', title='Saldo', saldo=saldo, today=today)
from datetime import datetime, timedelta
from datetime import date
from app import app, db
from flask import render_template, url_for, flash, redirect, request
from app.forms import SaleForm, BuyForm, SaldoForm, HistoryForm
from app.models import StockTable, SaldoTable, HistoryTable, CustomHistoryTable


@app.route('/')
@app.route('/index')
def index():
    today = datetime.now().date()
    n = len(SaldoTable.query.all())
    if n == 0:
        current_saldo = 0
    else:
        current_saldo = (SaldoTable.query.filter(SaldoTable.id==n).all())[0].saldo
    return render_template('index.html', today=today, current_saldo=current_saldo)

@app.route('/sale', methods=["GET", "POST"])
def sale():
    today = datetime.now().date()
    form = SaleForm()
    product_stock = StockTable.query.all()
    
    n = len(SaldoTable.query.all())
    if n == 0:
        saldo_last = 0
    else: 
        saldo_last = (SaldoTable.query.filter(SaldoTable.id==n).all())[0].saldo
        
    if form.validate_on_submit():
        if StockTable.query.filter(StockTable.product == form.product.data).all():
            current_quantity_product = StockTable.query.filter(StockTable.product == form.product.data).all()[0].quantity
            if current_quantity_product >= form.quantity.data:
                sale1 = StockTable(
                    product = form.product.data,   
                    quantity = current_quantity_product - form.quantity.data,  
                    )
                a = StockTable.query.filter_by(product = form.product.data).one()
                db.session.delete(a)
            else:
                print("Error, not enought quantity products on stock")    
        else: 
            sale1 = StockTable(
                product = form.product.data,   
                quantity = form.quantity.data,  
                )
        sale2 = SaldoTable(
            payment = (form.price.data * form.quantity.data),
            saldo = int(saldo_last) + int(form.price.data * form.quantity.data),
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
    if form.validate_on_submit():
        if StockTable.query.filter(StockTable.product == form.product.data).all():
            current_quantity_product = StockTable.query.filter(StockTable.product == form.product.data).all()[0].quantity
            purchase1 = StockTable(
                product = form.product.data,   
                quantity = form.quantity.data + current_quantity_product,     
                )
            a = StockTable.query.filter_by(product = form.product.data).one()
            db.session.delete(a)
            print(current_quantity_product)
            print(purchase1.quantity)
        else: 
            purchase1 = StockTable(
                product = form.product.data,   
                quantity = form.quantity.data,    
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

@app.route('/custom_history', methods=["GET", "POST"])
def custom_history():
    form = HistoryForm()
    today = datetime.now().date()
    ()
    if request.method == 'POST':
        a = request.form['period_from'].split('-')
        b = request.form['period_to'].split('-')
        period_from = date(int(a[0]), int(a[1]), int(a[2]))
        period_to = date(int(b[0]), int(b[1]), int(b[2]))
        history1 = CustomHistoryTable(
            period_from = period_from,
            period_to = period_to,
            )
        
        db.session.query(CustomHistoryTable).delete()
        db.session.add(history1)
        db.session.commit()
        
        flash('Congratulations, task completed')
        return redirect(url_for('custom_history_period'))
    return render_template('custom_history.html', title='Custom History', form=form, today=today)

@app.route('/custom_history_period', methods=["GET", "POST"])
def custom_history_period():
    today = datetime.now().date()
    period_from = CustomHistoryTable.query.get(1).period_from
    period_to = CustomHistoryTable.query.get(1).period_to + timedelta(days = 1)
    # history = HistoryTable.query.all()
    history = HistoryTable.query.filter((HistoryTable.date>=period_from) & (HistoryTable.date<=(period_to))).all()
    print(period_from)
    print(type(period_from))
    print(period_to)
    print(history)

    return render_template('custom_history_period.html', title='Custom History', today=today, history=history)


@app.route('/history', methods=["GET", "POST"])
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
    n = len(SaldoTable.query.all())
    current_saldo = (SaldoTable.query.filter(SaldoTable.id==n).all())[0].saldo
    return render_template('saldo.html', title='Saldo', saldo=saldo, today=today, current_saldo=current_saldo)
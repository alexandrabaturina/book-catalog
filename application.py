from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem

engine = create_engine('sqlite:///catalogitems.db',
    connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Show all categories
@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).all()
    return render_template('categories.html', categories=categories)

# Create a new category item
@app.route(
    '/category/<int:category_id>/list/new/', methods=['GET', 'POST'])
def newCatalogItem(category_id):
        if request.method == 'POST':
        newItem = CatalogItem(name=request.form['name'],
                            description=request.form['description'],
                            category_id=category_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showList', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)


# Edit a category item
@app.route('/category/<int:category_id>/list/<int:list_id>/edit',
           methods=['GET', 'POST'])
def editCatalogItem(category_id, list_id):
    editedItem = session.query(CatalogItem).filter_by(id=list_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showList', category_id=category_id))
    else:

        return render_template('edititem.html', category_id=category_id,
                                list_id=list_id, item=editedItem)

app = Flask(__name__)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

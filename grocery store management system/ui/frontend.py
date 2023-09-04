from flask import Flask,render_template,redirect,request,session,jsonify
import urllib3
import json

backendapi='http://127.0.0.1:5002'

frontend=Flask(__name__)

@frontend.route('/')
def homePage():
    return render_template('registerpage.html')

@frontend.route('/login')
def loginPage():
    return render_template('loginpage.html')

@frontend.route('/registerForm',methods=['post'])
def registerForm():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    http=urllib3.PoolManager()
    response=http.request('get',backendapi+'/register?username='+username+'&password='+password)
    response=response.data.decode('utf-8')
    if response=='already registered':
        return render_template('registerpage.html',err='already registered')
    else:
        return render_template('registerpage.html',res='account created')

@frontend.route('/loginForm',methods=['post'])
def loginForm():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    http=urllib3.PoolManager()
    response=http.request('get',backendapi+'/login?username='+username+'&password='+password)
    response=response.data.decode('utf-8')
    if response=='login successful':
        return redirect('/dashboard')
        #return render_template('loginpage.html',res='login valid')
    else:
        return render_template('loginpage.html',err='login invalid')

@frontend.route('/manageproduct')
def manageproduct():
    http=urllib3.PoolManager()
    response=http.request('get',backendapi+'/viewproducts')
    response=response.data.decode('utf-8')
    response=json.loads(response)

    return render_template('manage-product.html',data=response,l=len(response))

@frontend.route('/dashboard')
def dashboard():
    http=urllib3.PoolManager()
    response=http.request('get',backendapi+'/vieworders')
    response=response.data.decode('utf-8')
    response=json.loads(response)
    return render_template('index.html',data=response,l=len(response))

@frontend.route('/addproduct',methods=['post'])
def addproduct():
    pname=request.form['pname']
    punits=request.form['units']
    pprice=request.form['pprice']
    print(pname,punits,pprice)
    http=urllib3.PoolManager()
    response=http.request('get',backendapi+'/addproduct?pname='+pname+'&punits='+punits+'&pprice='+pprice)
    response=response.data.decode('utf-8')
    return redirect('/manageproduct')

@frontend.route('/delete',methods=['get'])
def deleteproduct():
    id = (request.args.get('id'))
    http=urllib3.PoolManager()
    response=http.request('get',backendapi+'/delete?id='+id)
    response=response.data.decode('utf-8')
    return redirect('/manageproduct')

@frontend.route('/order')
def orderPage():
    http=urllib3.PoolManager()
    response=http.request('get',backendapi+'/viewproducts')
    response=response.data.decode('utf-8')
    response=json.loads(response)

    return render_template('order.html',data=response,l=len(response))

@frontend.route('/saveorder',methods=['post'])
def saveorder():
    customerName=request.form['customerName']
    product=request.form.getlist('product')
    listToStr1 = ' '.join([str(elem) for elem in product])
    product_price=request.form.getlist('product_price')
    listToStr2 = ' '.join([str(elem) for elem in product_price])
    item_total=request.form.getlist('item_total')
    listToStr3 = ' '.join([str(elem) for elem in item_total])
    print(customerName,product,product_price,item_total)
    print(listToStr1,listToStr2,listToStr3)
    product_grand_total=request.form['product_grand_total']

    http=urllib3.PoolManager()
    response=http.request('get',backendapi+'/saveorder?customerName='+customerName+'&product='+str(listToStr1)+'&product_price='+str(listToStr2)+'&item_total='+str(listToStr3)+'&product_grand_total='+str(product_grand_total))
    response=response.data.decode('utf-8')

    http=urllib3.PoolManager()
    response=http.request('get',backendapi+'/viewproducts')
    response=response.data.decode('utf-8')
    response=json.loads(response)
    return render_template('order.html',data=response,l=len(response))

if __name__=="__main__":
    frontend.run('0.0.0.0',5000,debug=True)
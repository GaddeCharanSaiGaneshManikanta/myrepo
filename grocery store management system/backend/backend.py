from flask import Flask,redirect,request,session,jsonify
from pymongo import MongoClient
import json
import datetime


backend=Flask(__name__)
client=MongoClient('127.0.0.1',27017)
db=client['grocery']
c=db['registerdata']
c1=db['products']
c2=db['orders']

@backend.route('/register',methods=['get'])
def register():
    username=request.args.get('username')
    password=request.args.get('password')
    print(username,password)
    k={}
    k['username']=username
    k['password']=password
    for i in c.find():
        if(i['username']==username and i['password']==password):
            return('already registered')
    c.insert_one(k)
    return ('register stored successfully')

@backend.route('/login',methods=['get'])
def login():
    username=request.args.get('username')
    password=request.args.get('password')
    print(username,password)
    for i in c.find():
        if(i['username']==username and i['password']==password):
            return ('login successful')
    return('login failure')

@backend.route('/addproduct',methods=['get'])
def addproduct():
    pname=request.args.get('pname')
    punits=request.args.get('punits')
    pprice=request.args.get('pprice')
    k={}
    k['name']=pname
    k['units']=punits
    k['price']=pprice
    c1.insert_one(k)
    return('product added')

@backend.route('/viewproducts')
def viewproducts():
    data=[]
    for i in c1.find():
        dummy=[]
        dummy.append(i['name'])
        dummy.append(i['units'])
        dummy.append(i['price'])
        data.append(dummy)
    return jsonify(data)

@backend.route('/delete',methods=['get'])
def deleteproduct():
    id = int(request.args.get('id'))
    data=[]
    for i in c1.find():
        dummy=[]
        dummy.append(i['name'])
        dummy.append(i['units'])
        dummy.append(i['price'])
        data.append(dummy)
    res=data[id]
    k={}
    k['name']=res[0]
    k['units']=res[1]
    k['price']=res[2]
    c1.delete_one(k)
    return('deleted')

@backend.route('/saveorder',methods=['get'])
def saveorder():
    customerName=request.args.get('customerName')
    product=(request.args.get('product'))
    product = list(product.split(" "))
    product_price=(request.args.get('product_price'))
    product_price = list(product_price.split(" "))
    item_total=(request.args.get('item_total'))
    item_total = list(item_total.split(" "))
    product_grand_total=request.args.get('product_grand_total')
    print(product,product_price,item_total)
    k={}
    k['name']=customerName

    for i in range(len(product)):
        k['product'+str(i)]=product[i]
        k['productprice'+str(i)]=product_price[i]
        k['item_total' + str(i)]=item_total[i]
    
    k['product_grand_total']=product_grand_total
    today = datetime.date.today()
    k['date']=str(today)

    c2.insert_one(k)
    return('orders saved')
    
@backend.route('/vieworders')
def vieworders():
    data=[]
    for i in c2.find():
        dummy=[]
        dummy.append(i['date'])
        dummy.append(i['name'])
        dummy.append(i['product_grand_total'])
        data.append(dummy)
    return jsonify(data)


if __name__=="__main__":
    backend.run('0.0.0.0',5002,debug=True)
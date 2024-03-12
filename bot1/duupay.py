import requests,json

def create(seller:int,buyer:int,amount:float,commodity:str,token):
    data={
    "seller":seller,
    "buyer":buyer,
    "amount":amount,
    "commodity":commodity
}
    res=requests.post(url='http://duupay.xyz/api{}/createorder'.format(token),json=data,headers = {"Content-Type": "application/json"})
    print(res.text)
    get_data=eval(res.text)
    return get_data

def query(orderid:int,token):
    data={
        "orderid":orderid
    }
    res=requests.post(url='http://duupay.xyz/api{}/queryorder'.format(token),json=data,headers = {"Content-Type": "application/json"})
    get_data=eval(res.text)
    return get_data


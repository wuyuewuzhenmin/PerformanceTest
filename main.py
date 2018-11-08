# encoding: utf-8
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask,render_template,request
from url_http.h5_http_avg import reph5
# from url_http.wu.H5_interface_modify import  reph5

from url_http.http_avg import mainaa


# from url_http.wu.Client_interface_modify import mainaa

from url_http.h5_performance import h5_performacn

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/performance')
def Home():
    return render_template('html/Home.html')

@app.route('/InterfaceActivity')
def InterfaceActivity():
    return render_template('html/InterfaceActivityH5.html')

# 接口性能
@app.route('/InterfaceClient',methods=['GET', 'POST'])
def InterfaceClient():
    if request.method == "POST":
        is_online = request.form.get('is_online')
        is_get = request.form.get('is_get')
        is_url = request.form.get('URL')
        is_data = request.form.get('datas')
        is_number = request.form.get('number')
        # print type(is_data)
        # print is_data
        aa=mainaa(is_online,int(is_number),str(is_get),str(is_url),str(is_data))
        print aa
        return render_template('html/InterfaceClient.html',result =aa)
    return render_template('html/InterfaceClient.html')

@app.route('/LoadH5',methods=['GET', 'POST'])
def LoadH5():
    if request.method == "POST":
        return render_template('html/LoadH5.html', result='该部分暂未开放，待后续优化')
    return render_template('html/LoadH5.html')

@app.route('/LoadClient',methods=['GET', 'POST'])
def LoadClient():
    if request.method == "POST":
        return render_template('html/LoadClient.html', result='该部分暂未开放，待后续优化')
    return render_template('html/LoadClient.html')

# h5压测
@app.route('/pressureH5',methods=['GET', 'POST'])
def pressureH5():
    if request.method == "POST":
        is_online = request.form.get('is_online')
        is_get = request.form.get('is_get')
        is_url = request.form.get('URL')
        print is_online,is_url,type(is_url)
        is_data = request.form.get('datas')
        is_number = request.form.get('number')

        aa=h5_performacn(is_url, is_get, is_data,int(is_number))
        return render_template('html/pressureH5.html', result=aa)

    return render_template('html/pressureH5.html')


# 接口压力
@app.route('/pressureClient',methods=['GET', 'POST'])
def pressureClient():
    if request.method == "POST":
        is_online = request.form.get('is_online')
        is_get = request.form.get('is_get')
        is_url = request.form.get('URL')
        is_data = request.form.get('datas')
        is_number = request.form.get('number')

        print is_get,is_data,is_number
        print type(is_data)


        aa = h5_performacn(is_url, is_get, is_data, int(is_number))
        return render_template('html/pressureClient.html', result=aa)

    return render_template('html/pressureClient.html')

@app.route('/Jshtml')
def Jshtml():
    return render_template('html/Jshtml.html')

# h5接口
@app.route('/InterfaceActivityH5',methods=['GET', 'POST'])
def InterfaceActivityH5():
    if request.method == "POST":
        is_online = request.form.get('is_online')
        is_get = request.form.get('is_get')
        is_url = request.form.get('URL')
        is_data = request.form.get('datas')
        is_number = request.form.get('number')

        cc=reph5(int(is_number),is_get,is_url,is_data)
        # print 'cc'+cc

        return render_template('html/InterfaceActivityH5.html',result=cc)

    return render_template('html/InterfaceActivityH5.html')



if __name__ == '__main__':
    #部署环境添加两行代码
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(debug=True, port=8011, host='0.0.0.0')
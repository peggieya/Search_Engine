#use python frontEnd.py to run the front end
#when the system is ready, ues localhost:8080 to see the query page

from bottle import *
import collections
import operator

#htmltpl is the template of the main query page and display search history
htmlstr1 = """
    
    <!DOCTYPE html>
    <html>
    <body>  
    <center>
    
    <img src="https://lh3.googleusercontent.com/pV3PBLpOA32prHW-O3Oe1oQoGyAD5cjLVgH4ZAmvIotMmOFUJNICrvJQJW-z4qgCo70LetmvHxZM3NRaCGGUWudpLIhgbiCEFgUe_j1WY0UCz5wzr9ZMozD2zcZCsXft93TOA2vRgLel-uEcA_hkMvjKiyfxYJwE6CBRNEyC4PVnMu76TSaiZkLWlJO4SS_9EGT4to77DT3EUsprWjQDdrqCwsIktCGXjQP-oyzL8vQGyxStyXy-x7XRtq3xZ_Vte0z760Psky_6eVHuni1NHuEHmp0EM7h4Quz7jdsWciU-jUGkDFn9Pfegjr3jrmfNQPaoucFHvOo5KmB0tByt_eKMYiFsydFq6EJW0ukqJVVwtvY3ntGsMyRmCpoyYVlzWKlivlN2n6Syjyo52sV3fS2epVv8UkPEbsQ6Gn3omqX4lr_j7LVDF80ksho8dTfceBSQrfvpH1k3wXuRxzfLa2a8VDBo6uRGhnJNwWZBFebrIwNWA-YQYiBx-dbFhhV7tF4_suvxRQU_PmnDUW6oS1gy0ki1tE2jzVGuLXXxN7FWqI7kiogdr6n_Vnea3sSVIkco_qzpus22lpet9bVmodflZNCNV6Lptu3t6nMxFw=w1378-h468-no"style="width:300px;height:100px"><p></p>
    <img src="https://qph.ec.quoracdn.net/main-qimg-8ed23442190ee7893088222b0379a98a-c" style="width:200px;height:160px">
    <p></p><p></p><p></p>
    <form action="/", method="POST">

    <input type = "text" name="keyword" style="width:600px;height:50px" />
    <input type = "submit"/><p></p><p></p><p></p>

    </form>
            <table id="results">
            <tr><th>Search</th>
            <th>History</th></tr>
            
            <img src="https://lh3.googleusercontent.com/SdSqx0JhZYAGiJggwkGneAKmuVlIyDvmmSCz-GLu4YbfSozuVxPq_G4rgfozEKD2v2T34hglQg0wuKQ0SfU7YKHhcOs7lPYo6UM1Ogkd7c_1PX34rZfE2zhg2ccm2QvyIChXr_LPXwpVcJK7qoupOcol30CmKQ-6sAviUuuovuilCjhV5_8BVaYYEUPi29wbyJ9TirghYEm4Z0WkEW660TL6bP3kcicPH3V9PJTzaAn4ICu1exQ8raxapQaho9Qg9uyZo_qVsQKYqgJps9Bpb-Q9l_qpU9s1WO-ul5dVuzurmw8lmNdUhhLIDrDBuELRWPE_KBH3JehWo7K1A_72-XHQHAPg-uGtjUn63VL-Y5HZxIBfqr35YzEfdc_STYLNbfSvPXqSWd8sjcsa4b8nYyHtJbSFAcm1OOspkrmmXm23ojk3xW-rhfM86VOeS96o0vtx5RLl95jvaT7Dx4nicX4N73zT8OAWi2JvuLfOpDMUCKD2-K9Q_Vye8j9ugq2lZSkqUcMRj_LE1pawxrvxvx-0UtQFZCHyOF8TYC70j9eclGCH-ySo04cIeLeogZqbwBvQf20m4r7EZ2E4WHKl0qCDhSxOLVPQmwCB7wFz6A=w2366-h306-no" style="width:450px;height:47px">
            <img src="https://lh3.googleusercontent.com/SdSqx0JhZYAGiJggwkGneAKmuVlIyDvmmSCz-GLu4YbfSozuVxPq_G4rgfozEKD2v2T34hglQg0wuKQ0SfU7YKHhcOs7lPYo6UM1Ogkd7c_1PX34rZfE2zhg2ccm2QvyIChXr_LPXwpVcJK7qoupOcol30CmKQ-6sAviUuuovuilCjhV5_8BVaYYEUPi29wbyJ9TirghYEm4Z0WkEW660TL6bP3kcicPH3V9PJTzaAn4ICu1exQ8raxapQaho9Qg9uyZo_qVsQKYqgJps9Bpb-Q9l_qpU9s1WO-ul5dVuzurmw8lmNdUhhLIDrDBuELRWPE_KBH3JehWo7K1A_72-XHQHAPg-uGtjUn63VL-Y5HZxIBfqr35YzEfdc_STYLNbfSvPXqSWd8sjcsa4b8nYyHtJbSFAcm1OOspkrmmXm23ojk3xW-rhfM86VOeS96o0vtx5RLl95jvaT7Dx4nicX4N73zT8OAWi2JvuLfOpDMUCKD2-K9Q_Vye8j9ugq2lZSkqUcMRj_LE1pawxrvxvx-0UtQFZCHyOF8TYC70j9eclGCH-ySo04cIeLeogZqbwBvQf20m4r7EZ2E4WHKl0qCDhSxOLVPQmwCB7wFz6A=w2366-h306-no" style="width:450px;height:47px">
"""

#top 20 search history should be added here
htmlstr2 = """
        </table></center>
    </body>
    </html>
"""

#htmltpl is the template to display keyword information
htmltpl1 = """
<!DOCTYPE html>
    <html>
    <body>
"""

#keyword_comd should be added here
htmltpl2 = """
        <center>
        <img src="http://dl.bizhi.sogou.com/images/2014/06/19/670587.jpg?f=download" style="width:300px;height:170px"><p></p><p></p><p></p>
        <table id="history">
            <tr><th>Word</th>
            <th>Count</th></tr>
"""

#table_comd should be added here
htmltpl3 = """
        </table></center>
    </body>
    </html>
"""

#html for error 404
html_404 = """
<!DOCTYPE html>
    <html>
    <body>
    <center>
    <img src="http://www.newenglandamputeeassociation.com/wp-content/uploads/2014/08/404Doge.png" style="width:1000px;height:700px">
    </center>
    </body>
"""

#define some global variables
history_dic = {}
history_list = []
table_comd2 = ""

#display keyword info
@route('/', method='POST')
def getp():
    
    #get input from user and convert to lower case
    keyword = request.forms.get('keyword')
    keyword = keyword.lower()
    word_list = keyword.split()

    #store the search history in a dictionary
    if keyword in history_dic.keys():
        history_dic[keyword] = history_dic[keyword] + 1
    else:       
        history_dic[keyword] = 1

    #sort the search history by their search frequency
    sorted_search_history = sorted(history_dic.items(), key = operator.itemgetter(1), reverse=True)

    #transfer searching info to html string form
    keyword_info = "<center><h2>Search for " + "\"" + keyword + "\"</h2></center>"
    
    #transfer keyword info to html string form
    counter = collections.Counter(word_list)
    counter = dict(counter)
    print counter
    
    #transfer "search results" table to html string, in the order the words were first seen
    index = 0
    table_temp1=""
    while bool(counter):
        keyword_temp = word_list[index]
        if counter.get(keyword_temp) is not None:
            table_temp1 = table_temp1+"<tr><td>"+keyword_temp+"</td><td>"+str(counter.get(keyword_temp))+"</td></tr>"
            del counter[keyword_temp]
        index = index+1
    table_comd1 = table_temp1

    #store top 20 searched keywords in history_terms as list
    history_terms = [history[0] for history in sorted_search_history]
    history_terms = history_terms[0:20]
    
    #store top 20 search frequency of keywords in history_freqs as list
    history_freqs = [history[1] for history in sorted_search_history]
    history_freqs = history_freqs[0:20]
    
    #transfer search history to html string form, stored in table_comd2
    table_temp1 = ["<tr><td>" + history_term + "</td><td>" for history_term in history_terms]
    table_temp2 = [str(history_freq) + "</td></tr>" for history_freq in history_freqs]
    table_comd_temp = zip(table_temp1, table_temp2)
    table_comd_list = ["%s%s" % table_temp for table_temp in table_comd_temp]
    global table_comd2 
    table_comd2 = ''.join(table_comd_list)
    
    #combine html strings to display search keyword information
    return htmltpl1+keyword_info+str(htmltpl2)+table_comd1+htmltpl3


#query page
@route('/',method='GET')
def index():
    return htmlstr1 + str(table_comd2) + htmlstr2

#error 404 page
@error(404)
def error404(error):
    return html_404


run(reloader=True)


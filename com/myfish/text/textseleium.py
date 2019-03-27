from selenium import webdriver

'''
   <img src="./skin/JazzBlue/images/kao.png" width="17" height="17" border="0" alt="通过考试获得学时" title="通过考试获得学时" />							                    
   <img src="./skin/JazzBlue/images/xue.png" width="17" height="17" border="0" alt="学习达到规定时长获得学时" title="学习达到规定时长获得学时" />
   '''
url ='<img src="./skin/JazzBlue/images/kao.png" width="17" height="17" border="0" alt="通过考试获得学时" title="通过考试获得学时" />	'
browser = webdriver.Chrome()
browser.get(url)

xue = browser.find_element_by_link_text('./skin/JazzBlue/images/kao.png')

info1='2室1厅2卫·52.29平米·西南·高楼层/17层·精装'
a = info1.find('平米')
b = info1.rfind('·',0,-8)
chaoxiang = info1[info1.rfind('·',0,-8)+1:info1.rfind('/')].strip()
print(chaoxiang)

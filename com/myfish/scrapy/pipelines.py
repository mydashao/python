class PriceConverterPipeline(object):
# 英镑兑换人民币汇率
exchange_rate = 8.5309
def process_item(self, item, spider):
    # 提取item的price 字段（如￡53.74）
    # 去掉前面英镑符号￡，转换为float 类型，乘以汇率
    price = float(item['price'][1:]) * self.exchange_rate
    # 保留2 位小数，赋值回item的price 字段
    item['price'] = '￥%.2f' % price
    return item
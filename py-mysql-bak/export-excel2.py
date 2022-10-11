import xlwt
import pymysql
import time
import os

# 定义时间格式
BACKUP_PATH = '/Users/xierui/Desktop/报表导出'
DATETIME = time.strftime('%Y%m%d%H')
TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME + '/'

getVendor = "SELECT	t_supplier.f_display_code AS 供应商编码, t_supplier.f_name AS 供应商名称 FROM commodity.t_supplier;"

products = "SELECT DATE_ADD(t_sku.f_created_time, INTERVAL 8 HOUR) AS 创建时间, t_sku.f_display_code AS 商品sku号, t_product.f_display_code AS 商品spu号, t_product.f_name AS 商品名, GROUP_CONCAT(CONCAT(t_sku_attribute.f_name,':','  ',t_sku_attribute.f_value,' ')) AS 商品属性, t_product.f_genre AS 商品类型, t_product.f_unit AS 计量单位, t_category.f_name AS 分类名称, t_brand.f_name AS 品牌名称, t_supplier.f_name AS 供应商名称, t_sku.f_international_code AS 外部编码, t_sku_price.f_value AS 零售价, CASE t_sku.f_status WHEN 1 THEN '上架' WHEN 2 THEN '下架' ELSE '状态未知' END AS 销售状态 FROM commodity.t_sku JOIN commodity.t_product ON t_sku.f_product_id = t_product.f_id JOIN commodity.t_category ON t_sku.f_category_id = t_category.f_id JOIN commodity.t_supplier ON t_product.f_supplier_id = t_supplier.f_id JOIN commodity.t_brand ON t_product.f_brand_id = t_brand.f_id JOIN commodity.t_sku_price ON t_sku.f_display_code = t_sku_price.f_sku_code  JOIN commodity.t_sku_attribute ON t_sku_attribute.f_sku_code = t_sku.f_display_code WHERE t_sku_price.f_config_id = 1 GROUP BY 商品sku号 ORDER BY 创建时间 DESC;"

stock = "SELECT DATE_ADD(s.f_created_time,INTERVAL 8 HOUR) AS 创建时间, t_sku.f_display_code AS 商品编码, t_sku.f_name AS 商品名称, t_warehouse.f_name AS 所属仓库, s.f_count AS 可用库存, s.f_lock_count AS 锁定库存, s.f_display_count AS 陈列, s.f_plan_count AS 预售库存 FROM commodity.t_stock AS s LEFT JOIN commodity.t_sku ON t_sku.f_id = s.f_sku_id LEFT JOIN commodity.t_warehouse ON t_warehouse.f_id = s.f_warehouse_id ORDER BY 创建时间 DESC;"

inStock = "SELECT DATE_ADD(t_warehouse_entry.f_created_time,INTERVAL 8 HOUR) AS 入库日期, t_warehouse_entry.f_display_code AS 入库单编号, CASE  t_warehouse_entry.f_type_code   WHEN 1 THEN  '采购入库'   WHEN 2 THEN  '退货入库'   WHEN 3 THEN  '调拨入库'  WHEN 9 THEN  '其他入库'  END AS 入库类别, t_warehouse_entry.f_order_code AS 关联订单编号, t_warehouse_entry.f_warehouse_name AS 入库仓库, t_warehouse_entry_detail.f_spu_code AS 商品编号, t_warehouse_entry_detail.f_spu_name AS 商品全名, t_warehouse_entry_detail.f_sku_code AS 商品sku, t_warehouse_entry_detail.f_sku_name AS 商品名称, t_warehouse_entry_detail.f_unit AS 计量单位, t_warehouse_entry_detail.f_count AS 入库数量 FROM fxs_order.t_warehouse_entry JOIN fxs_order.t_warehouse_entry_detail ON t_warehouse_entry.f_id = t_warehouse_entry_detail.f_inbound_order_id ORDER BY 入库日期 DESC;"

outStock = "SELECT	DATE_ADD(t_warehouse_outbound.f_created_time,INTERVAL 8 HOUR) AS 出库日期,	t_warehouse_outbound.f_display_code AS 出库单编号,CASE		t_warehouse_outbound.f_type_code 		WHEN 4 THEN		'自提出库' 		WHEN 5 THEN		'其他出库' 		WHEN 6 THEN		'物流出库' 		WHEN 7 THEN		'调拨出库' 		WHEN 8 THEN		'仓库自取出库'		WHEN 11 THEN		'采购退货出库'	END AS 出库类别,			t_warehouse_outbound.f_order_code AS 关联订单编号,	t_warehouse_outbound.f_warehouse_name AS 出库仓库,	t_warehouse_outbound_detail.f_spu_code AS 商品spu,	t_warehouse_outbound_detail.f_spu_name AS 商品全名,	t_warehouse_outbound_detail.f_sku_code AS 商品sku,	t_warehouse_outbound_detail.f_sku_name AS 商品名称,	t_warehouse_outbound_detail.f_unit AS 计量单位,	t_warehouse_outbound_detail.f_count AS 出库数量 FROM	fxs_order.t_warehouse_outbound	JOIN fxs_order.t_warehouse_outbound_detail ON t_warehouse_outbound.f_id = t_warehouse_outbound_detail.f_outbound_order_id		ORDER BY 出库日期 DESC"

customOder = "SELECT  DATE_ADD(t_custom_order.f_created_time,  INTERVAL 8 HOUR ) AS 创建日期, t_custom_order.f_display_code AS 订单编号,CASE  t_custom_order.f_status_code   WHEN 1 THEN  '未下推'   WHEN 2 THEN  '下推'   WHEN 3 THEN  '退款'  ELSE '未知'  END AS 订单状态, t_custom_order.f_customer_name AS 客户名称, t_custom_order.f_customer_mobile AS 客户电话号码,t_custom_order.f_customer_district AS 客户区域, t_custom_order.f_origin AS 来源, t_custom_order.f_area AS 房屋面积, CONCAT(t_custom_order.f_room,'室',t_custom_order.f_hall,'厅') as 房屋结构, t_custom_order.f_delivery_time AS 预计配送时间, t_custom_order.f_measure_time AS 上门丈量时间, t_custom_order.f_recipient_address AS 配送地址, t_custom_order.f_custom_designer AS 定制设计师, t_custom_order.f_interior_designer AS 软装设计师, t_custom_order.f_custom_seller AS 定制销售, t_custom_order.f_user_name AS 家居顾问, t_custom_order.f_actual_amount AS 预估价格,  t_custom_order.f_user_name AS 付款单号, t_custom_order.f_paid_amount AS 实付总额, t_custom_order.f_remark AS 备注, IF(t_custom_order.f_store_id=117, '动物店', '成华店') AS 下单门店 FROM fxs_order.t_custom_order   ORDER BY 创建日期 DESC"

logisticsOder = "SELECT	DATE_ADD(f_created_time,INTERVAL 8 HOUR) AS 创建时间,	f_display_code AS 物流单号,	f_sale_order_display_code 销售单号 FROM	fxs_order.t_logistics_order	ORDER BY 创建时间 DESC;"

voucher = "SELECT	( SELECT f_display_code FROM marketing.t_coupon_attributes WHERE marketing.t_coupon_attributes.f_id = f_coupon_id ) AS '优惠券编号',	( SELECT f_title FROM marketing.t_coupon_attributes WHERE marketing.t_coupon_attributes.f_id = f_coupon_id ) AS 优惠券名称,	f_customer_name AS 领取人,	f_customer_mobile AS 手机号码,	( SELECT f_display_code FROM fxs_order.t_sale_order WHERE fxs_order.t_sale_order.f_id = f_order_id ) AS 订单编号,	( SELECT f_name FROM `user`.t_department WHERE `user`.t_department.f_id = f_store_id ) AS 门店,	DATE_ADD(f_created_time, INTERVAL 8 HOUR) AS 领取时间,	DATE_ADD(f_used_time, INTERVAL 8 HOUR ) AS 使用时间,	DATE_ADD(f_modified_time, INTERVAL 8 HOUR) AS 更新时间 FROM	marketing.t_user_coupon WHERE	f_used_time > CURDATE()	ORDER BY  领取时间 DESC;"

refundOrder = "SELECT	DATE_FORMAT( CONVERT_TZ( t_refund_order.f_created_time, '+00:00', '+08:00' ), '%Y-%m-%d %H:%d:%s' ) AS 创建日期,	t_refund_order.f_display_code AS 退货单编号,CASE		t_refund_order.f_status_code		WHEN 1 THEN		'待审核' 		WHEN 2 THEN		'进行中' 		WHEN 3 THEN		'已完成' 	END AS 退款单状态,	t_sale_order.f_display_code AS 订单编号,	t_refund_order.f_amount - t_refund_order.f_addition_price AS 应退总额 FROM    fxs_order.t_refund_order	JOIN fxs_order.t_sale_order ON t_sale_order.f_id = t_refund_order.f_order_id WHERE	fxs_order.t_refund_order.f_type_code = 1 ORDER BY	创建日期 DESC;"

salesOrder = "SELECT	DATE_FORMAT(CONVERT_TZ(t_sale_order.f_created_time,'+00:00','+08:00'), '%Y-%m-%d %H:%d:%s') AS 创建日期,	t_sale_order.f_display_code AS 订单编号,CASE		t_sale_order.f_status_code 		WHEN 'LIFE_CYCLE_STATUS_CODE_UNPAID' THEN		'待支付' 		WHEN 'LIFE_CYCLE_STATUS_CODE_PAYING' THEN		'分期付款' 		WHEN 'LIFE_CYCLE_STATUS_CODE_UN_DELIVER' THEN		'待发货'		WHEN 'LIFE_CYCLE_STATUS_CODE_DELIVERING' THEN		'部分发货' 		WHEN 'LIFE_CYCLE_STATUS_CODE_FINISHED' THEN		'已完成' 		WHEN 'LIFE_CYCLE_STATUS_CODE_INVALID' THEN		'已作废' 		WHEN 'LIFE_CYCLE_STATUS_CODE_UN_RETURNS' THEN		'待退货' 		WHEN 'LIFE_CYCLE_STATUS_CODE_UN_REFUND' THEN		'待退款'		WHEN 'LIFE_CYCLE_STATUS_CODE_UN_AUDIT' THEN		'待审核' 		WHEN 'LIFE_CYCLE_STATUS_CODE_UN_START' THEN		'未开始' 		WHEN 'LIFE_CYCLE_STATUS_CODE_CONTINUE' THEN		'进行中' 		WHEN 'LIFE_CYCLE_STATUS_CODE_REFUSED' THEN		'已拒绝' 		WHEN 'LIFE_CYCLE_STATUS_CODE_INBOUNDING' THEN		'入库中'		WHEN 'LIFE_CYCLE_STATUS_CODE_TERMINATED' THEN		'已终止' 		WHEN 'LIFE_CYCLE_STATUS_CODE_AFTER_SALE' THEN		'售后' 		WHEN 'LIFE_CYCLE_STATUS_CODE_AFTER_SALE_FINISHED' THEN		'售后完成' ELSE '未知' 	END AS 订单状态,	t_sale_order.f_delivery_mode AS 配送方式,	t_order_annexation.f_user_name AS 客户名称,	t_order_annexation.f_seller_name AS 销售经理,	IF(t_sale_order.f_store_id=117, '动物店', '成华店') AS 下单门店,	t_order_commodity.f_sku_name AS 商品名称,	t_order_commodity.f_sku_code AS 商品编码,	JSON_EXTRACT(t_order_commodity.f_attributes, '$[*].name', '$[*].value') AS 商品属性,	t_order_commodity.f_unit AS 计量单位,	t_order_commodity.f_count AS 销售数量,	t_order_commodity.f_actual_price AS 销售价格,	t_order_commodity.f_apportion_unit_price AS 商品均摊价格,	t_sale_order.f_actual_amount AS 销售总金额,	t_sale_order.f_remark AS 备注 FROM	fxs_order.t_sale_order	JOIN fxs_order.t_order_annexation ON t_sale_order.f_id = t_order_annexation.f_order_id	JOIN fxs_order.t_order_commodity ON t_sale_order.f_id = t_order_commodity.f_order_id	WHERE t_sale_order.f_created_time > CURDATE()"

transferOrder = "SELECT	t_transfer_order.f_created_time AS '调拨日期',	t_transfer_order.f_display_code AS '调拨单编号', CASE t_transfer_order.f_type_code WHEN 1 THEN '仓库调拨'  WHEN 2 THEN '库存调拨'  END AS 调拨类别 ,	t_transfer_order.f_out_warehouse_name AS '调拨入出库仓',	CASE t_transfer_order.f_status_code 	WHEN 1 THEN  '未审核' WHEN 3 THEN '已取消' WHEN 4 THEN '已完成' END AS '状态', t_transfer_order.f_in_warehouse_name AS '调拨入库仓库', t_transfer_order_detail.f_sku_code AS '商品sku', t_transfer_order_detail.f_sku_name AS '商品名称', t_transfer_order_detail.f_count AS '调拨数量', t_transfer_order_detail.f_unit AS '调拨单位' FROM fxs_order.t_transfer_order JOIN fxs_order.t_transfer_order_detail on t_transfer_order_detail.f_transfer_order_id = t_transfer_order.f_id ORDER BY t_transfer_order.f_created_time DESC"

purchaseOrder = "SELECT DATE_ADD(t_purchase_order.f_created_time,INTERVAL 8 HOUR) AS '采购时间', t_purchase_order.f_display_code AS '采购订单', t_purchase_order.f_user_name AS '采购员', t_purchase_order.f_supplier AS '供应商', t_purchase_order_extend.f_sku_code AS '商品sku', t_purchase_order_extend.f_sku_name AS '商品名称',CASE t_purchase_order.f_status WHEN 1 THEN	'已审核' WHEN 2 THEN '待审核' WHEN 3 THEN '已取消' ELSE '未知' END AS '订单状态',CASE t_purchase_order.f_type_code WHEN 1 THEN '待采'	WHEN 2 THEN '普通' ELSE '类型未知'END as '订单类型', t_purchase_order_extend.f_amount AS '商品采购金额', t_purchase_order_extend.f_count AS '采购数量', ( t_purchase_order_extend.f_amount * t_purchase_order_extend.f_count ) AS '商品采购价格' FROM fxs_order.t_purchase_order JOIN fxs_order.t_purchase_order_extend ON t_purchase_order_extend.f_display_code = t_purchase_order.f_display_code ORDER BY	采购时间 DESC"


class MYSQL:
    def __init__(self):
        pass

    def __del__(self):
        self._cursor.close()
        self._connect.close()

    def connectDB(self):
        """
        连接数据库
        :return:
        """
        try:
            self._connect = pymysql.Connect(
                host='10.0.10.4',
                port=3306,
                user='guyver_r',
                passwd='jeLQUG4eMlBszrZDbqKuoE953aE',
                charset='utf8'
            )
            return 0
        except:
            return -1

    def export(self, table_name, sql, output_path):

        self._cursor = self._connect.cursor()
        count = self._cursor.execute(sql)
        # print(self._cursor.lastrowid)
        print(count)
        # 重置游标的位置
        self._cursor.scroll(0, mode='absolute')
        # 搜取所有结果
        results = self._cursor.fetchall()

        # 获取MYSQL里面的数据字段名称
        fields = self._cursor.description
        workbook = xlwt.Workbook()


        # 注意: 在add_sheet时, 置参数cell_overwrite_ok=True, 可以覆盖原单元格中数据。
        # cell_overwrite_ok默认为False, 覆盖的话, 会抛出异常.
        sheet = workbook.add_sheet(table_name, cell_overwrite_ok=True)

        # 写上字段信息
        for field in range(0, len(fields)):
            sheet.write(0, field, fields[field][0])

        # 获取并写入数据段信息
        row = 1
        col = 0
        for row in range(1, len(results) + 1):
            for col in range(0, len(fields)):
                sheet.write(row, col, u'%s' % results[row - 1][col])

        workbook.save(output_path)


def usage():
    print(
        " 0: 退出\n",
        "1: 供应商查询\n",
        "2: 商品数据查询\n"
        " 3: 库存数据查询\n"
        " 4: 入库单数据查询\n"
        " 5: 定制单数据查询\n"
        " 6: 物流单数据查询\n"
        " 7: 用户优惠卷数据查询\n"
        " 8: 退款单数据查询\n"
        " 9: 销售单数据查询\n"
        " 10: 出库单数据查询\n"
        " 11: 调拨单数据查询\n"
        " 12: 采购订单数据查询")


if __name__ == '__main__':
    while True:
        usage()
        num = input("请输入上面的数字导出对应的报表： ").strip()
        if num.isdigit():
            print("\033[32m你输入的数字是\033[0m", num)
            if num == '0':
                print("导出报表脚本已经退出。。。。")
                break
            elif num == '1':
                table_name = "供应商数据查询"
                sql = getVendor
            elif num == '2':
                table_name = "商品数据查询"
                sql = products
            elif num == '3':
                table_name = "库存数据查询"
                sql = stock
            elif num == '4':
                table_name = "入库数据查询"
                sql = inStock
            elif num == '5':
                table_name = "定制单数据查询"
                sql = customOder
            elif num == '6':
                table_name = "物流单数据查询"
                sql = logisticsOder
            elif num == '7':
                table_name = "用户优惠卷"
                sql = voucher
            elif num == '8':
                table_name = "退款单数据查询"
                sql = refundOrder
            elif num == '9':
                table_name = "销售单数据查询"
                sql = salesOrder
            elif num == '10':
                table_name = "出库单数据查询"
                sql = outStock
            elif num == '11':
                table_name = "调拨单数据查询"
                sql = transferOrder
            elif num == '12':
                table_name = "采购订单数据查询"
                sql = purchaseOrder
            else:
                print("没有你想要导出的报表")
                break

            if not os.path.exists(TODAYBACKUPPATH):
                os.mkdir(TODAYBACKUPPATH)
            mysql = MYSQL()
            flag = mysql.connectDB()
            if flag == -1:
                print('数据库连接失败')
            else:
                print('数据库连接成功')
                mysql.export(table_name, sql, TODAYBACKUPPATH + table_name + '.xls')
                print("\033[32m导出的报表数据在：%s" % TODAYBACKUPPATH + table_name + '.xls\033[0m')
        else:
            print("\033[31m 请重新输入一个数字\033[0m")
            time.sleep(1)

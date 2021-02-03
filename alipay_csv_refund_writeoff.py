#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import sys
import os


def is_refunded_rec(rec):  # 判断是否为有退款产生的交易记录
    if rec[13].strip() != '0':
        return True
    else:
        return False


def refunded_rec_writeoff(rec):  # 为有退款的交易记录冲销退款
    rec[9] = str(float(rec[9])-float(rec[13]))  # 第10列减去第13列得到冲销后的金额
    # print(rec[8], rec[9])
    return rec


def check_then_writeoff(rec):  # 定义一个针对每一条记录的处理函数
    if is_refunded_rec(rec):
        return refunded_rec_writeoff(rec)
    else:
        return rec


csv_filename = sys.argv[1]
dirname, basename = os.path.split(csv_filename)
new_csv_filename = os.path.join(dirname, 'new_'+basename)
# csv_filename = r'e:\\data\\test1.csv'
# new_csv_filename = r'e:\\data\\test2.csv'

with open(csv_filename, newline='') as csvfile:
    csv_list = list(csv.reader(csvfile, delimiter=','))  # 将csv文件读取为list
    new_csv_list = csv_list[:5] + list(map(check_then_writeoff, csv_list[5:-7])) + csv_list[-7:]
    # 使用map方式处理[5:-7]数据区并拼接出新的list
    # list切片的特点：第一个索引包含在切出的片段，第二个索引不包含在切出的片段中。所以接接时保证首尾相接即可

with open(new_csv_filename, 'w', newline='') as new_csvfile:  # 生成并写入新的csv文件
    writer = csv.writer(new_csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, escapechar='\t')
    # 实现支付宝csv账单格式：
    # quoting=csv.QUOTE_MINIMAL,escapechar=???
    # 指示writer对象只引用那些包含特殊字符，如字段分隔符，quotechar或任何字符 lineterminator。
    # quoting=QUOTE_MINIMAL时， 结合阿里csv前两列结尾都带转义符\t的规律， 设定escapechar='\t'， 可实现遇到\t时才戴上双引号的效果
    writer.writerows(new_csv_list)

'''
quoting=csv.QUOTE_MINIMAL =0 # 指示writer对象只引用那些包含特殊字符，如字段分隔符，quotechar或任何字符 lineterminator
quoting=csv.QUOTE_ALL=1      # writer对象引用所有字段
                             # 如字段分隔符,quotechar或任何字符 lineterminator。
quoting=csv.QUOTE_NONNUMERIC=2 # writer对象引用所有非数字字段。
                               # 指示读者将所有非引用字段转换为float类型。
quoting=csv.QUOTE_NONE=3,escapechar='$'# writer对象不引用字段
                                       # 如未设置escapechar错误抛出；指示reader不对引号字符执行特殊处理。
'''

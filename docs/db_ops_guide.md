# 数据库操作指南

## 脚本位置
scripts/db_ops.py 管理脚本用来处理数据库操作

## 功能
这个脚本提供了以下功能：
1. 清空数据库或指定集合
```bash
# 清空数据库
python scripts/db_ops.py clear
# 清空指定集合
python scripts/db_ops.py clear -c <collection_name>
```

2. 导出数据
```bash
# 导出所有数据
python scripts/db_ops.py export

# 导出指定集合数据
python scripts/db_ops.py export -c <collection_name>

# 导出到指定文件
python scripts/db_ops.py export -o <output_file>
```

3. 导入数据
```bash
# 从文件导入数据
python scripts/db_ops.py import -f <input_file>

# 导入到指定集合
python scripts/db_ops.py import -f <input_file> -c <collection_name>
```

## 使用示例

1. 备份当前日期数据
```bash
python scripts/db_ops.py export -o data_backup_$(date +%Y%m%d).json
```

2. 恢复数据
```bash
python scripts/db_ops.py import -f data_backup_$(date +%Y%m%d).json
```

3. 清空数据
```bash
python scripts/db_ops.py clear
```

## 注意事项
1. 清空数据库或集合时，请谨慎操作，以免误删重要数据。
2. 导出和导入数据时，请确保文件路径正确，文件格式正确。
3. 导出和导入数据时，请确保MongoDB服务已启动。

import numpy as np

def create_grid(min_lat, min_lon, max_lat, max_lon, rows, cols):
    latitudes = np.linspace(min_lat, max_lat, rows + 1)
    longitudes = np.linspace(min_lon, max_lon, cols + 1)

    grid = []
    for i in range(rows):
        for j in range(cols):
            grid.append({
                'min_lat': latitudes[i],
                'max_lat': latitudes[i + 1],
                'min_lon': longitudes[j],
                'max_lon': longitudes[j + 1],
            })

    return grid

def print_grid_info(grid):
    for i, cell in enumerate(grid):
        print(f"Grid {i}:")
        print(f"Latitude Range: {cell['min_lat']} to {cell['max_lat']}")
        print(f"Longitude Range: {cell['min_lon']} to {cell['max_lon']}")
        print()

# 设置地图范围
min_latitude = 39.7612
max_latitude = 40.0531
min_longitude = 116.2969
max_longitude = 116.5529

# 定义网格的行数和列数
num_rows = 6
num_cols = 6

area_degrees = (max_latitude - min_latitude) * (max_longitude - min_longitude)

# 1 度经度大约是 111 公里
# 1 度纬度的长度在赤道附近是大约 111 公里，但在高纬度地区会略微缩短
# 为了简化，我们可以使用平均值，也可以根据具体地理位置采用更精确的方法
average_length_km = 111

area_square_km = area_degrees * average_length_km**2

print(f"北京市的面积约为 {area_square_km:.2f} 平方千米")

# 创建网格
grid = create_grid(min_latitude, min_longitude, max_latitude, max_longitude, num_rows, num_cols)


# 打印网格信息
print_grid_info(grid)

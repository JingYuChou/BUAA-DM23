import csv
import argparse
import ast
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--csv", type=str, default="database/data/road.csv", help="path to the csv file that contains polylines wanted")
parser.add_argument("--polyline-index", type=int, default=1, help="index of polyline column.")
parser.add_argument("--wkt", type=bool, default=False, help="whether the polyline is stored in wkt format. Or as the format in database/data/road.csv")
parser.add_argument("--output", type=str, default="database/visualizer/map.html", help="output path of the generated html file")

offset = []   # 之后可以把这个offset试出来获得更好的可视化效果.

before = \
'''
<!doctype html>
<html>

<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="initial-scale=1.0, user-scalable=no, width=device-width">
  <title>HELLO，AMAP!</title>
  <link rel="stylesheet" href="https://a.amap.com/jsapi_demos/static/demo-center/css/demo-center.css" />
  <style>
    html,
    body,
    #container {
      height: 100%;
      width: 100%;
    }

    .amap-icon img,
    .amap-marker-content img {
      width: 25px;
      height: 34px;
    }

    .cus_info_window {
      background-color: #fff;
      padding: 10px;
    }
  </style>
</head>

<body>
  <div id="container"></div>
  <script type="text/javascript" src="https://webapi.amap.com/maps?v=2.0&key=692a38180fd6dce577d2e206e522d8e3"></script>
  <script type="text/javascript">
    // 创建地图实例
    var map = new AMap.Map("container", {
      zoom: 13,
      center: [116.39, 39.92],
      resizeEnable: true
    });

    // 创建点覆盖物
    var marker = new AMap.Marker({
      position: new AMap.LngLat(116.39, 39.92),
      icon: '//a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-default.png',
      offset: new AMap.Pixel(-13, -30)
    });
    map.add(marker);

    // 创建信息窗体
    var infoWindow = new AMap.InfoWindow({
      isCustom: true,  // 使用自定义窗体
      content: '<div class="cus_info_window">HELLO,AMAP!</div>', // 信息窗体的内容可以是任意 html 片段
      offset: new AMap.Pixel(16, -45)
    });
    var onMarkerClick = function (e) {
      infoWindow.open(map, e.target.getPosition()); // 打开信息窗体
      // e.target 就是被点击的 Marker
    }

    marker.on('click', onMarkerClick); // 绑定 click 事件
'''
after = \
'''
  </script>
</body>

</html>
'''

def main():
    args = parser.parse_args()
    infilepath = args.csv
    polyindex = args.polyline_index
    isWKT = args.wkt
    outfilepath = args.output

    x_bias = 0.0061
    y_bias = 0.0013
    
    infile = open(infilepath, "r", encoding="utf-8-sig")
    reader = csv.reader(infile)
    
    with open(outfilepath, "w", encoding="utf-8-sig") as outfile:
        outfile.write(before)
        first = True
        polylines = ""
        for line in reader:
            if first:
                first = False
                continue
            else:
                polyline = ast.literal_eval(line[polyindex])
                polyline = list(map(lambda x: [x[0]+x_bias, x[1]+y_bias], polyline))
                if not isWKT:
                    polylines += str(polyline) + ","

        middle = \
'''
    let lineArr = [{}];
    var polyline = new AMap.Polyline({{
      path: lineArr,          // 设置线覆盖物路径
      strokeColor: "#3366FF", // 线颜色
      strokeWeight: 5,        // 线宽
      strokeStyle: "solid",   // 线样式
    }});
    map.add(polyline);
'''.format(polylines)     # 之后再修改颜色等等.
        outfile.write(middle)

        infile.close()

        infile = open("database/fmm/fmm.csv")
        
        outfile.write(after)
    

    

if __name__=='__main__':
    main()
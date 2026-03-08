# 前端依赖库目录

此目录存放所有本地化的前端依赖库文件，以避免依赖 CDN。

## 包含的库

- **Vue.js** - Vue 3 全局构建版本
- **Element Plus** - Vue 3 UI 组件库
- **Axios** - HTTP 请求库
- **ECharts** - 数据可视化图表库
- **WangEditor** - 富文本编辑器

## 使用说明

1. 运行项目根目录下的 `download_libs.bat` 脚本下载所有依赖
2. 确保网络连接正常（需要访问 unpkg.com 和 jsdelivr.net）
3. 下载完成后，所有文件将存放在此目录

## 文件结构

```
libs/
├── vue.global.js          # Vue.js
├── element-plus.js        # Element Plus
├── axios.min.js          # Axios
└── echarts.min.js        # ECharts
```

## 优势

- ✅ 不依赖 CDN，加载更稳定
- ✅ 本地文件，访问速度更快
- ✅ 离线环境也可运行
- ✅ 避免 CDN 版本更新导致的不兼容

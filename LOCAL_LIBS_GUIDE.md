# 前端依赖本地化指南

## 📋 概述

本项目已将前端依赖库从 CDN (unpkg.com, jsdelivr.net) 迁移到本地存储，以提高：
- ✅ 加载速度和稳定性
- ✅ 离线环境支持
- ✅ 避免 CDN 版本更新导致的不兼容问题

## 📦 包含的依赖库

| 库名称 | 版本 | 用途 | 文件大小 (约) |
|--------|------|------|--------------|
| Vue.js | 3.x | 前端框架 | 150 KB |
| Element Plus | latest | UI 组件库 | 300 KB |
| Axios | latest | HTTP 请求库 | 15 KB |
| ECharts | 5.x | 数据可视化 | 800 KB |
| WangEditor | latest | 富文本编辑器 | 200 KB |

## 🚀 使用方法

### 方法一：使用 PowerShell 脚本（推荐）

```powershell
# 在项目根目录下执行
.\download_libs.ps1
```

**特点：**
- 彩色输出，进度清晰
- 错误提示友好
- Windows 10/11 原生支持

### 方法二：使用 CMD 批处理

```cmd
# 在项目根目录下执行
download_libs.bat
```

**特点：**
- 兼容所有 Windows 版本
- 简单直接

## 📁 文件结构

执行下载脚本后，文件结构如下：

```
Py/
├── static/
│   ├── js/
│   │   └── libs/
│   │       ├── vue.global.js          # Vue.js
│   │       ├── element-plus.js        # Element Plus
│   │       ├── axios.min.js          # Axios
│   │       ├── echarts.min.js        # ECharts
│   │       └── wangeditor.js         # WangEditor
│   └── css/
│       ├── element-plus.css          # Element Plus 样式
│       └── wangeditor.css            # WangEditor 样式
├── download_libs.bat                 # CMD 下载脚本
└── download_libs.ps1                 # PowerShell 下载脚本
```

## ✅ 验证安装

1. **检查文件是否存在**
   ```
   static/js/libs/vue.global.js
   static/js/libs/element-plus.js
   static/js/libs/axios.min.js
   static/js/libs/echarts.min.js
   static/js/libs/wangeditor.js
   static/css/element-plus.css
   static/css/wangeditor.css
   ```

2. **启动服务**
   ```cmd
   python main.py
   ```

3. **打开浏览器访问**
   ```
   http://localhost:8000
   ```

4. **检查页面是否正常加载**
   - 按 F12 打开开发者工具
   - 查看 Console 是否有资源加载错误
   - 检查 Network 面板确认资源来自本地

## 🔄 更新依赖

如果需要更新依赖库版本：

1. 删除旧的库文件
   ```cmd
   rmdir /s /q static\js\libs
   ```

2. 重新运行下载脚本
   ```cmd
   download_libs.bat
   ```

## 🛠️ 故障排除

### 问题 1：下载失败

**可能原因：**
- 网络连接问题
- 防火墙阻止
- 代理设置

**解决方案：**
- 检查网络连接
- 暂时关闭防火墙
- 配置代理（如需要）

### 问题 2：页面显示空白

**可能原因：**
- 库文件未正确下载
- 文件路径错误

**解决方案：**
1. 检查 `static/index.html` 中的引用路径
2. 确认所有库文件存在
3. 清除浏览器缓存

### 问题 3：版本不兼容

**可能原因：**
- 依赖库版本更新导致 API 变化

**解决方案：**
1. 查看错误信息
2. 检查相关库的更新日志
3. 必要时回退到特定版本

## 📝 注意事项

1. **首次使用必须下载**
   - 项目首次运行前必须执行下载脚本
   - 确保所有依赖库文件存在

2. **定期更新**
   - 建议定期更新依赖库以获取最新功能和安全补丁
   - 更新前做好备份

3. **版本管理**
   - 如需固定版本，修改下载脚本中的 URL
   - 例如：`vue@3.3.4` 而不是 `vue@3`

## 🎯 优势总结

| 特性 | CDN 方式 | 本地存储 |
|------|----------|----------|
| 加载速度 | ⭐⭐⭐ (依赖网络) | ⭐⭐⭐⭐⭐ (本地访问) |
| 稳定性 | ⭐⭐⭐ (可能宕机) | ⭐⭐⭐⭐⭐ (完全可控) |
| 离线支持 | ❌ | ✅ |
| 版本控制 | ⭐⭐ | ⭐⭐⭐⭐ |
| 安全性 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

**@author LiuHuiYu**  
**Last Updated:** 2026-03-08

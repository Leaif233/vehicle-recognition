# 车型识别助手

基于 PyTorch 模型的车型识别应用，支持 iOS、Android、Web、微信小程序多端运行。

## 快速开始

### 1. 后端部署（服务器）

```bash
# 上传整个项目到服务器
scp -r . user@your-server:/path/to/project

# SSH 登录服务器
ssh user@your-server

# 进入项目目录
cd /path/to/project

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 2. 前端开发

**使用 HBuilderX：**
1. 打开 HBuilderX
2. 文件 -> 导入 -> 从本地目录导入 -> 选择 `frontend` 目录
3. 修改 `pages/index/index.vue` 中的 `YOUR_SERVER_IP` 为你的服务器 IP
4. 运行 -> 运行到浏览器/微信开发者工具/手机

**使用 CLI：**
```bash
cd frontend
npm install -g @dcloudio/uvm
uvm use latest
npm run dev:h5        # Web
npm run dev:mp-weixin # 微信小程序
```

### 3. Figma AI 提示词

复制以下内容到 Figma AI 生成界面设计：

```
设计一个简洁的车型识别移动应用界面，要求：

1. 顶部导航栏：标题"车型识别助手"，居中，字体 18px，颜色 #333

2. 主内容区（垂直居中）：
   - 图片上传区域：虚线边框矩形（宽度 300px，高度 300px），圆角 12px
   - 内部显示相机图标和文字"点击上传车辆图片"
   - 上传后显示图片预览

3. 识别结果卡片（图片下方 20px）：
   - 白色背景，圆角 12px，阴影 0 2px 8px rgba(0,0,0,0.1)
   - 车型名称：字体 24px，加粗，颜色 #1890ff
   - 置信度：字体 14px，颜色 #999，格式"置信度：95%"

4. 配色：主色 #1890ff，背景 #f5f5f5，文字 #333/#999

5. 移动端优先，宽度 375px，所有元素水平居中
```

## 项目结构

```
智能识别助手/
├── backend/           # Python 后端
├── frontend/          # uni-app 前端
├── v3.pt             # PyTorch 模型
├── docker-compose.yml
└── nginx.conf
```

## API 接口

**POST /api/recognize**
- 请求：multipart/form-data，字段 `image`
- 响应：`{"success": true, "vehicle_type": "SUV", "confidence": 0.95}`

## 注意事项

1. 修改前端 API 地址为你的服务器 IP
2. 微信小程序需在后台配置服务器域名
3. 模型支持的车型：轿车、SUV、MPV、跑车、皮卡、客车、货车
"# vehicle-recognition" 

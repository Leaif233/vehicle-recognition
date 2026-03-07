<template>
  <view class="container">
    <view class="upload-area" @click="chooseImage">
      <image v-if="imageUrl" :src="imageUrl" mode="aspectFill" class="preview" />
      <view v-else class="placeholder">
        <text class="icon">📷</text>
        <text class="tip">点击上传车辆图片</text>
      </view>
    </view>

    <view v-if="loading" class="loading">识别中...</view>

    <view v-if="result" class="result-card">
      <text class="vehicle-type">{{ result.vehicle_type }}</text>
      <text class="confidence">置信度：{{ (result.confidence * 100).toFixed(0) }}%</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      imageUrl: '',
      loading: false,
      result: null
    }
  },
  methods: {
    chooseImage() {
      uni.chooseImage({
        count: 1,
        success: (res) => {
          this.imageUrl = res.tempFilePaths[0]
          this.uploadImage(res.tempFilePaths[0])
        }
      })
    },
    uploadImage(filePath) {
      this.loading = true
      this.result = null

      uni.uploadFile({
        url: 'http://38.22.235.27/api/recognize',
        filePath: filePath,
        name: 'image',
        success: (res) => {
          const data = JSON.parse(res.data)
          if (data.success) {
            this.result = data
          } else {
            uni.showToast({ title: '识别失败', icon: 'none' })
          }
        },
        fail: () => {
          uni.showToast({ title: '上传失败', icon: 'none' })
        },
        complete: () => {
          this.loading = false
        }
      })
    }
  }
}
</script>

<style>
.container {
  padding: 32rpx;
  background: #f8f9fa;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.upload-area {
  width: 600rpx;
  height: 600rpx;
  margin-top: 80rpx;
  border: 3rpx dashed #d0d0d0;
  border-radius: 24rpx;
  overflow: hidden;
  background: white;
}
.preview {
  width: 100%;
  height: 100%;
}
.placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}
.icon {
  font-size: 100rpx;
  margin-bottom: 24rpx;
}
.tip {
  color: #666;
  font-size: 30rpx;
}
.loading {
  margin-top: 40rpx;
  color: #1890ff;
  font-size: 32rpx;
}
.result-card {
  width: 600rpx;
  margin-top: 40rpx;
  padding: 48rpx;
  background: white;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.08);
}
.vehicle-type {
  display: block;
  font-size: 52rpx;
  font-weight: bold;
  color: #1890ff;
  text-align: center;
  margin-bottom: 20rpx;
}
.confidence {
  display: block;
  font-size: 30rpx;
  color: #999;
  text-align: center;
}
</style>

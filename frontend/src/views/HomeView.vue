<template>
  <main class="home">
    <section class="hero">
      <h1>Image to skin</h1>
      <p class="subtitle">
        Upload an image of yourself to turn it into a Minecraft skin.
      </p>
      <SampleCard title="">
        <FileDrop @file-selected="setFile" />
        <div v-if="selectedFile" class="upload-panel">
          <p class="file-name">{{ selectedFile.name }}</p>
          <button
            type="button"
            class="upload-button"
            :disabled="isPolling"
            @click="uploadFile"
          >
            Upload
          </button>
          <p v-if="isPolling" class="status-text">Generating... this can take a minute.</p>
        </div>
        <div v-if="resultUrl" class="result-panel">
          <div class="viewer-panel">
            <canvas ref="viewerCanvas" class="skin-canvas" aria-label="3D skin preview"></canvas>
          </div>
<!--          <img :src="resultUrl" alt="Generated skin preview" />-->
          <div class="result-actions">
            <a class="download-button" :href="resultUrl" download="skin.png">Download</a>
            <button
              type="button"
              class="clear-button"
              aria-label="Clear result"
              title="Start over"
              @click="clearResult"
            >
              <span class="clear-icon" aria-hidden="true"></span>
            </button>
          </div>
        </div>
      </SampleCard>
    </section>
  </main>
</template>

<script setup lang="ts">
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'
import * as skin3d from 'skin3d';
import FileDrop from '@/components/FileDrop.vue'
import SampleCard from '@/components/SampleCard.vue'
import { fetchGenerationResult, startGenerationUpload } from '@/api'

const selectedFile = ref<File | null>(null)
const resultUrl = ref<string | null>(null)
const isPolling = ref(false)
const viewerCanvas = ref<HTMLCanvasElement | null>(null)
let pollTimer: number | null = null
let skinViewer: any = null
let resizeObserver: ResizeObserver | null = null

const setFile = (file: File) => {
  selectedFile.value = file
  if (resultUrl.value) {
    URL.revokeObjectURL(resultUrl.value)
    resultUrl.value = null
  }
}

const uploadFile = async () => {
  if (!selectedFile.value) return
  if (pollTimer) {
    window.clearInterval(pollTimer)
    pollTimer = null
  }
  if (resultUrl.value) {
    URL.revokeObjectURL(resultUrl.value)
    resultUrl.value = null
  }

  isPolling.value = true
  const response = await startGenerationUpload(selectedFile.value)
  if (!response.ok) {
    isPolling.value = false
    return
  }
  const payload = await response.json()
  const taskId = payload.id as string

  pollTimer = window.setInterval(async () => {
    try {
      const resultResponse = await fetchGenerationResult(taskId)
      if (resultResponse.ok) {
        const blob = await resultResponse.blob()
        resultUrl.value = URL.createObjectURL(blob)
        isPolling.value = false
        if (pollTimer) {
          window.clearInterval(pollTimer)
          pollTimer = null
        }
        return
      }
      if (resultResponse.status !== 404) {
        isPolling.value = false
        if (pollTimer) {
          window.clearInterval(pollTimer)
          pollTimer = null
        }
      }
    } catch {
      isPolling.value = false
      if (pollTimer) {
        window.clearInterval(pollTimer)
        pollTimer = null
      }
    }
  }, 1000)
}

const clearResult = () => {
  if (pollTimer) {
    window.clearInterval(pollTimer)
    pollTimer = null
  }
  isPolling.value = false
  selectedFile.value = null
  if (resultUrl.value) {
    URL.revokeObjectURL(resultUrl.value)
    resultUrl.value = null
  }
}

const teardownViewer = () => {
  if (resizeObserver) {
    resizeObserver.disconnect()
    resizeObserver = null
  }
  if (skinViewer?.dispose) {
    skinViewer.dispose()
  }
  skinViewer = null
}

const applySkinToViewer = (skinUrl: string) => {
  if (!skinViewer) return
  if (typeof skinViewer.loadSkin === 'function') {
    skinViewer.loadSkin(skinUrl)
    return
  }
  if (typeof skinViewer.setSkin === 'function') {
    skinViewer.setSkin(skinUrl)
    return
  }
  skinViewer.skin = skinUrl
}

const initViewer = async () => {
  const canvas = viewerCanvas.value
  if (!canvas || !resultUrl.value) return

  teardownViewer()
  skinViewer = new skin3d.View({
    canvas,
    width: canvas.clientWidth || 280,
    height: canvas.clientHeight || 320,
    skin: resultUrl.value,
  })

  resizeObserver = new ResizeObserver((entries) => {
    const entry = entries[0]
    if (!entry || !skinViewer?.setSize) return
    const { width, height } = entry.contentRect
    skinViewer.setSize(Math.max(1, Math.floor(width)), Math.max(1, Math.floor(height)))
  })
  resizeObserver.observe(canvas)
}

watch(resultUrl, async (skinUrl) => {
  if (!skinUrl) {
    teardownViewer()
    return
  }
  await nextTick()
  if (!skinViewer) {
    await initViewer()
  } else {
    applySkinToViewer(skinUrl)
  }
})

onBeforeUnmount(() => {
  if (pollTimer) {
    window.clearInterval(pollTimer)
  }
  teardownViewer()
  if (resultUrl.value) {
    URL.revokeObjectURL(resultUrl.value)
  }
})
</script>

<style scoped>
.home {
  min-height: 100vh;
  padding: 4rem 6vw;
  background: radial-gradient(circle at top, #f7f7f2, #d9d5c3);
  color: #1f1f1f;
  font-family: "Manrope", "Trebuchet MS", sans-serif;
  display: grid;
  place-items: center;
}

.hero {
  max-width: 900px;
  display: grid;
  gap: 1.5rem;
  justify-items: center;
  text-align: center;
}

h1 {
  font-size: clamp(2.5rem, 5vw, 3.8rem);
  line-height: 1.05;
  margin: 0;
}

.subtitle {
  font-size: 1.1rem;
  max-width: 36rem;
}

.upload-panel {
  display: grid;
  gap: 0.75rem;
  margin-top: 1.5rem;
  justify-items: center;
}

.file-name {
  margin: 0;
  font-weight: 600;
}

.upload-button {
  padding: 0.6rem 1.6rem;
  border-radius: 999px;
  border: none;
  background: #2f2d28;
  color: #f9f6ef;
  font-weight: 600;
  cursor: pointer;
}

.upload-button:hover {
  background: #1c1a16;
}

.upload-button:disabled {
  background: #b9b4a7;
  color: #f7f3ea;
  cursor: not-allowed;
}

.status-text {
  margin: 0;
  font-size: 0.95rem;
  color: #4f4b3f;
}

.result-panel {
  display: grid;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.viewer-panel {
  width: 100%;
  aspect-ratio: 7 / 8;
  border-radius: 18px;
  border: 1px solid rgba(47, 45, 40, 0.2);
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.9), rgba(203, 198, 180, 0.9));
  box-shadow: 0 18px 30px rgba(47, 45, 40, 0.18);
  overflow: hidden;
}

.skin-canvas {
  width: 100%;
  height: 100%;
  display: block;
}

.result-panel img {
  max-width: 240px;
  border-radius: 14px;
  border: 1px solid rgba(47, 45, 40, 0.2);
}

.download-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.6rem 1.6rem;
  border-radius: 999px;
  background: #2f2d28;
  color: #f9f6ef;
  text-decoration: none;
  font-weight: 600;
  width: fit-content;
}

.download-button:hover {
  background: #1c1a16;
}

.result-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  width: 100%;
  justify-content: center;
}

.clear-button {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 1px solid rgba(47, 45, 40, 0.4);
  background: transparent;
  color: #2f2d28;
  font-weight: 600;
  cursor: pointer;
  display: grid;
  place-items: center;
  position: relative;
}

.clear-button:hover {
  border-color: #1c1a16;
  color: #1c1a16;
}

.clear-icon {
  width: 18px;
  height: 18px;
  position: relative;
}

.clear-icon::before,
.clear-icon::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 18px;
  height: 2px;
  background: currentColor;
  transform-origin: center;
}

.clear-icon::before {
  transform: translate(-50%, -50%) rotate(45deg);
}

.clear-icon::after {
  transform: translate(-50%, -50%) rotate(-45deg);
}

@media (max-width: 720px) {
  .home {
    padding: 3rem 8vw;
  }
}
</style>

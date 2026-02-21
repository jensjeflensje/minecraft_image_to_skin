<template>
  <section
    class="drop-zone"
    :class="{ 'drop-zone--active': isDragging }"
    @dragover.prevent="onDragOver"
    @dragleave.prevent="onDragLeave"
    @drop.prevent="onDrop"
  >
    <input
      ref="fileInput"
      class="drop-zone__input"
      type="file"
      accept="image/*"
      @change="onFileChange"
    />
    <div class="drop-zone__content">
      <p>Drag an image here, paste with Ctrl + V, or</p>
      <button type="button" class="drop-zone__button" @click="openFilePicker">
        choose a file
      </button>
      <p class="drop-zone__hint">Only image files are accepted.</p>
    </div>
    <div v-if="previewUrl" class="drop-zone__preview">
      <img :src="previewUrl" alt="Selected preview" />
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from 'vue'

const emit = defineEmits<{ 'file-selected': [File] }>()

const fileInput = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)
const previewUrl = ref<string | null>(null)

const onDragOver = () => {
  isDragging.value = true
}

const onDragLeave = () => {
  isDragging.value = false
}

const pickImage = (file: File | null) => {
  if (!file) return
  if (!file.type.startsWith('image/')) return
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
  previewUrl.value = URL.createObjectURL(file)
  emit('file-selected', file)
}

const onDrop = (event: DragEvent) => {
  isDragging.value = false
  const file = event.dataTransfer?.files?.[0] ?? null
  pickImage(file)
}

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0] ?? null
  pickImage(file)
  if (target) {
    target.value = ''
  }
}

const openFilePicker = () => {
  fileInput.value?.click()
}

const onPaste = (event: ClipboardEvent) => {
  const items = event.clipboardData?.items ?? []
  for (const item of items) {
    if (item.type.startsWith('image/')) {
      const file = item.getAsFile()
      pickImage(file)
      return
    }
  }
}

onMounted(() => {
  window.addEventListener('paste', onPaste)
})

onBeforeUnmount(() => {
  window.removeEventListener('paste', onPaste)
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
})
</script>

<style scoped>
.drop-zone {
  border: 2px dashed #7d7663;
  border-radius: 18px;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.45);
  transition: border-color 0.2s ease, background 0.2s ease;
  text-align: center;
}

.drop-zone--active {
  border-color: #2f2d28;
  background: rgba(255, 255, 255, 0.8);
}

.drop-zone__input {
  display: none;
}

.drop-zone__content {
  display: grid;
  gap: 0.75rem;
  justify-items: center;
}

.drop-zone__button {
  padding: 0.5rem 1.2rem;
  border-radius: 999px;
  border: none;
  background: #2f2d28;
  color: #f9f6ef;
  cursor: pointer;
  font-weight: 600;
}

.drop-zone__button:hover {
  background: #1c1a16;
}

.drop-zone__hint {
  font-size: 0.9rem;
  color: #4f4b3f;
}

.drop-zone__preview {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
}

.drop-zone__preview img {
  max-width: 180px;
  max-height: 180px;
  border-radius: 14px;
  border: 1px solid rgba(47, 45, 40, 0.2);
  object-fit: cover;
}
</style>
